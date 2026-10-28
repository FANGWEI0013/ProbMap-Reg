import csv
import math
from pathlib import Path

import cv2
import numpy as np

from config import (
    CNN_INPUT_SIZE,
    FIRE_IMAGES_DIR,
    MODEL_PATH,
    PROBABILITY_THRESHOLD,
    RANSAC_THRESHOLD_PX,
    RESULTS_ROOT,
)
from run_ablation_probmap_vs_sift import (
    FULL_PROBMAP,
    SIFT_ENHANCED,
    create_sift,
    enhanced_sift_matches,
    sift_points_and_descriptors,
)
from utils_features import extract_features
from utils_matching import nearest_neighbor_matches, scale_matches_to_original
from utils_model import load_unet_model, predict_pair_probability_maps, read_bgr_image
from utils_transform import ransac_inliers, warp_image
from utils_vis import create_tiled_mosaic, draw_matches, draw_points


RAW_PAIRS_PATH = RESULTS_ROOT / "ablation_probmap_vs_sift" / "raw_pairs.csv"
OUTPUT_DIR = RESULTS_ROOT / "ablation_probmap_vs_sift" / "failure_cases"

METHOD_DIR_NAMES = {
    FULL_PROBMAP: "proposed_method",
    SIFT_ENHANCED: "sift_enhanced_baseline",
}

METHOD_LABELS = {
    FULL_PROBMAP: "Proposed method",
    SIFT_ENHANCED: "SIFT enhanced baseline",
}


def parse_error(value):
    try:
        error = float(value)
    except (TypeError, ValueError):
        return float("inf")
    return error if math.isfinite(error) else float("inf")


def read_raw_rows(path):
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["error_float"] = parse_error(row.get("error"))
    return rows


def p_rows(rows, experiment):
    return [
        row for row in rows
        if row["experiment"] == experiment and row["category"] == "P"
    ]


def min_error_row(rows):
    finite_rows = [row for row in rows if math.isfinite(row["error_float"])]
    return min(finite_rows, key=lambda row: row["error_float"])


def max_error_row(rows):
    return max(rows, key=lambda row: row["error_float"])


def choose_cases(rows):
    proposed_rows = p_rows(rows, FULL_PROBMAP)
    sift_rows = p_rows(rows, SIFT_ENHANCED)
    sift_by_pair = {row["pair_id"]: row for row in sift_rows}

    cases = [
        {
            "case_name": "proposed_best_P",
            "pair_id": min_error_row(proposed_rows)["pair_id"],
            "methods": [FULL_PROBMAP],
        },
        {
            "case_name": "proposed_worst_P",
            "pair_id": max_error_row(proposed_rows)["pair_id"],
            "methods": [FULL_PROBMAP],
        },
        {
            "case_name": "sift_enhanced_worst_P",
            "pair_id": max_error_row(sift_rows)["pair_id"],
            "methods": [SIFT_ENHANCED],
        },
    ]

    contrast_candidates = []
    for proposed in proposed_rows:
        sift = sift_by_pair.get(proposed["pair_id"])
        if sift is None:
            continue
        if proposed["status"] != "success" or not math.isfinite(proposed["error_float"]):
            continue
        contrast_candidates.append(
            (
                sift["error_float"] - proposed["error_float"],
                proposed["pair_id"],
            )
        )
    if contrast_candidates:
        _, pair_id = max(contrast_candidates, key=lambda item: item[0])
        cases.append(
            {
                "case_name": "proposed_vs_sift_contrast_P",
                "pair_id": pair_id,
                "methods": [FULL_PROBMAP, SIFT_ENHANCED],
            }
        )
    return cases


def resize_for_points(image_bgr):
    return cv2.resize(image_bgr, (CNN_INPUT_SIZE, CNN_INPUT_SIZE), interpolation=cv2.INTER_LINEAR)


def side_by_side_points(image_1, points_1, image_2, points_2):
    left = draw_points(image_1, points_1)
    right = draw_points(image_2, points_2)
    return np.hstack([left, right])


def run_proposed_visualization(model, pair_id):
    image_1 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_1.jpg")
    image_2 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_2.jpg")
    probability_1, probability_2 = predict_pair_probability_maps(model, image_1, image_2)
    points_1, descriptors_1, _ = extract_features(probability_1, image_1, PROBABILITY_THRESHOLD)
    points_2, descriptors_2, _ = extract_features(probability_2, image_2, PROBABILITY_THRESHOLD)
    matches_480 = nearest_neighbor_matches(points_1, descriptors_1, points_2, descriptors_2)
    matches = scale_matches_to_original(matches_480, image_1.shape, CNN_INPUT_SIZE)
    matrix_2x3, inliers = ransac_inliers(matches, RANSAC_THRESHOLD_PX)
    warped = warp_image(image_1, matrix_2x3, image_2.shape)
    return {
        "image_1": image_1,
        "image_2": image_2,
        "points_image_1": resize_for_points(image_1),
        "points_image_2": resize_for_points(image_2),
        "points_1": points_1,
        "points_2": points_2,
        "matches": matches,
        "inliers": inliers,
        "warped": warped,
    }


def run_sift_enhanced_visualization(sift, pair_id):
    image_1 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_1.jpg")
    image_2 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_2.jpg")
    points_1, descriptors_1 = sift_points_and_descriptors(sift, image_1)
    points_2, descriptors_2 = sift_points_and_descriptors(sift, image_2)
    matches = enhanced_sift_matches(points_1, descriptors_1, points_2, descriptors_2)
    matrix_2x3, inliers = ransac_inliers(matches, RANSAC_THRESHOLD_PX)
    warped = warp_image(image_1, matrix_2x3, image_2.shape)
    return {
        "image_1": image_1,
        "image_2": image_2,
        "points_image_1": image_1,
        "points_image_2": image_2,
        "points_1": points_1,
        "points_2": points_2,
        "matches": matches,
        "inliers": inliers,
        "warped": warped,
    }


def write_metadata(path, metadata):
    lines = [f"{key}: {value}" for key, value in metadata.items()]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_visualization(output_dir, pair_id, method, raw_row, result):
    output_dir.mkdir(parents=True, exist_ok=True)
    feature_points = side_by_side_points(
        result["points_image_1"],
        result["points_1"],
        result["points_image_2"],
        result["points_2"],
    )
    raw_matches = draw_matches(result["image_1"], result["image_2"], result["matches"], thickness=2)
    inliers = draw_matches(result["image_1"], result["image_2"], result["inliers"], thickness=3)
    mosaic = create_tiled_mosaic(result["warped"], result["image_2"])

    cv2.imwrite(str(output_dir / "feature_points.png"), feature_points)
    cv2.imwrite(str(output_dir / "raw_matches.png"), raw_matches)
    cv2.imwrite(str(output_dir / "ransac_inliers.png"), inliers)
    cv2.imwrite(str(output_dir / "registered_mosaic.png"), mosaic)

    write_metadata(
        output_dir / "metadata.txt",
        {
            "pair_id": pair_id,
            "method": METHOD_LABELS[method],
            "experiment": method,
            "error": raw_row.get("error", ""),
            "num_points_1": raw_row.get("num_points_1", ""),
            "num_points_2": raw_row.get("num_points_2", ""),
            "num_matches": raw_row.get("num_matches", ""),
            "num_inliers": raw_row.get("num_inliers", ""),
            "status": raw_row.get("status", ""),
            "message": raw_row.get("message", ""),
        },
    )


def raw_lookup(rows):
    return {
        (row["experiment"], row["pair_id"]): row
        for row in rows
    }


def render_method(case_dir, pair_id, method, raw_row, model, sift):
    method_dir = case_dir / METHOD_DIR_NAMES[method]
    if method == FULL_PROBMAP:
        result = run_proposed_visualization(model, pair_id)
    elif method == SIFT_ENHANCED:
        result = run_sift_enhanced_visualization(sift, pair_id)
    else:
        raise ValueError(f"Unsupported method: {method}")
    save_visualization(method_dir, pair_id, method, raw_row, result)


def main():
    rows = read_raw_rows(RAW_PAIRS_PATH)
    lookup = raw_lookup(rows)
    cases = choose_cases(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    model = load_unet_model(MODEL_PATH)
    sift = create_sift()

    for case in cases:
        case_dir = OUTPUT_DIR / case["case_name"]
        case_dir.mkdir(parents=True, exist_ok=True)
        case_metadata = {
            "case_name": case["case_name"],
            "pair_id": case["pair_id"],
            "methods": ", ".join(case["methods"]),
        }
        for method in case["methods"]:
            raw_row = lookup[(method, case["pair_id"])]
            case_metadata[f"{method}_error"] = raw_row.get("error", "")
            print(f"Rendering {case['case_name']} / {case['pair_id']} / {method}")
            render_method(case_dir, case["pair_id"], method, raw_row, model, sift)
        write_metadata(case_dir / "metadata.txt", case_metadata)

    print(f"Wrote failure case visualizations to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
