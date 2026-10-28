import argparse
import math
import time

import cv2
import numpy as np

from config import (
    CNN_INPUT_SIZE,
    EXPERIMENT_NAME,
    FIRE_GROUND_TRUTH_DIR,
    FIRE_IMAGES_DIR,
    MODEL_PATH,
    PROBABILITY_THRESHOLD,
    PROPOSED_RESULTS_DIR,
    RANSAC_THRESHOLD_PX,
    SMALL_TEST_PAIRS,
    VIS_DIR,
)
from utils_eval import (
    generate_fire_pair_ids,
    ground_truth_path,
    read_control_points,
    registration_error,
    split_pair_id,
    summarize_rows,
    write_csv,
)
from utils_features import extract_features
from utils_matching import nearest_neighbor_matches, scale_matches_to_original
from utils_model import load_unet_model, predict_pair_probability_maps, read_bgr_image
from utils_transform import affine_2x3_to_homogeneous, ransac_inliers, warp_image
from utils_vis import save_pair_visualizations


RAW_FIELDNAMES = [
    "experiment",
    "category",
    "index",
    "pair_id",
    "status",
    "error",
    "num_points_1",
    "num_points_2",
    "num_matches",
    "num_inliers",
    "runtime",
    "message",
]

SUMMARY_FIELDNAMES = [
    "experiment",
    "category",
    "num_pairs",
    "num_success",
    "num_failed",
    "success_25px",
    "auc",
    "mean_error_success_only",
    "mean_runtime",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Run the proposed probability-map FIRE registration pipeline.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--small-test", action="store_true", help="Run a small smoke test on A01-A03.")
    mode.add_argument("--full-run", action="store_true", help="Run all FIRE pairs.")
    mode.add_argument("--pair", type=str, help="Run one pair, for example A03.")

    vis = parser.add_mutually_exclusive_group()
    vis.add_argument("--save-vis", action="store_true", help="Save visual outputs for successful pairs.")
    vis.add_argument("--no-vis", action="store_true", help="Disable visual outputs.")
    return parser.parse_args()


def selected_pair_ids(args):
    if args.pair:
        return [args.pair.upper()]
    if args.full_run:
        return generate_fire_pair_ids()
    return list(SMALL_TEST_PAIRS)


def failure_row(pair_id, start_time, message, counts=None):
    counts = counts or {}
    category, index = split_pair_id(pair_id)
    return {
        "experiment": EXPERIMENT_NAME,
        "category": category,
        "index": index,
        "pair_id": pair_id,
        "status": "failed",
        "error": float("inf"),
        "num_points_1": counts.get("num_points_1", 0),
        "num_points_2": counts.get("num_points_2", 0),
        "num_matches": counts.get("num_matches", 0),
        "num_inliers": counts.get("num_inliers", 0),
        "runtime": time.perf_counter() - start_time,
        "message": message,
    }


def process_pair(model, pair_id, save_vis):
    start = time.perf_counter()
    counts = {}
    category, index = split_pair_id(pair_id)
    try:
        image_1_path = FIRE_IMAGES_DIR / f"{pair_id}_1.jpg"
        image_2_path = FIRE_IMAGES_DIR / f"{pair_id}_2.jpg"
        image_1 = read_bgr_image(image_1_path)
        image_2 = read_bgr_image(image_2_path)

        probability_1, probability_2 = predict_pair_probability_maps(model, image_1, image_2)
        points_1, descriptors_1, heatmap_1 = extract_features(probability_1, image_1, PROBABILITY_THRESHOLD)
        points_2, descriptors_2, heatmap_2 = extract_features(probability_2, image_2, PROBABILITY_THRESHOLD)
        counts["num_points_1"] = len(points_1)
        counts["num_points_2"] = len(points_2)
        if len(points_1) < 2 or len(points_2) < 2:
            return failure_row(pair_id, start, "feature points不足", counts)
        if len(descriptors_1) == 0 or len(descriptors_2) == 0:
            return failure_row(pair_id, start, "descriptor为空", counts)

        matches_480 = nearest_neighbor_matches(points_1, descriptors_1, points_2, descriptors_2)
        counts["num_matches"] = len(matches_480)
        if len(matches_480) < 2:
            return failure_row(pair_id, start, "matches不足", counts)

        matches_original = scale_matches_to_original(matches_480, image_1.shape, CNN_INPUT_SIZE)
        matrix_2x3, inliers = ransac_inliers(matches_original, RANSAC_THRESHOLD_PX)
        counts["num_inliers"] = len(inliers)
        similarity_matrix = affine_2x3_to_homogeneous(matrix_2x3)
        control_points = read_control_points(ground_truth_path(FIRE_GROUND_TRUTH_DIR, pair_id))
        error = registration_error(similarity_matrix, control_points)
        if not math.isfinite(error):
            return failure_row(pair_id, start, "registration error is not finite", counts)

        warped = None
        if save_vis:
            warped = warp_image(image_1, matrix_2x3, image_2.shape)
            save_pair_visualizations(
                VIS_DIR / pair_id,
                pair_id,
                image_1,
                image_2,
                heatmap_1,
                heatmap_2,
                points_1,
                points_2,
                matches_original,
                inliers,
                warped_1=warped,
            )

        return {
            "experiment": EXPERIMENT_NAME,
            "category": category,
            "index": index,
            "pair_id": pair_id,
            "status": "success",
            "error": float(error),
            "num_points_1": counts["num_points_1"],
            "num_points_2": counts["num_points_2"],
            "num_matches": counts["num_matches"],
            "num_inliers": counts["num_inliers"],
            "runtime": time.perf_counter() - start,
            "message": "ok",
        }
    except Exception as exc:
        return failure_row(pair_id, start, str(exc), counts)


def main():
    args = parse_args()
    save_vis = bool(args.save_vis and not args.no_vis)
    PROPOSED_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading model: {MODEL_PATH}")
    model = load_unet_model(MODEL_PATH)
    rows = []
    for pair_id in selected_pair_ids(args):
        print(f"Processing {pair_id}...")
        row = process_pair(model, pair_id, save_vis=save_vis)
        rows.append(row)
        print(f"  {row['status']} error={row['error']} message={row['message']}")

    summary_rows = summarize_rows(rows, EXPERIMENT_NAME)
    write_csv(PROPOSED_RESULTS_DIR / "raw_pairs.csv", rows, RAW_FIELDNAMES)
    write_csv(PROPOSED_RESULTS_DIR / "summary.csv", summary_rows, SUMMARY_FIELDNAMES)
    print(f"Wrote {PROPOSED_RESULTS_DIR / 'raw_pairs.csv'}")
    print(f"Wrote {PROPOSED_RESULTS_DIR / 'summary.csv'}")


if __name__ == "__main__":
    main()
