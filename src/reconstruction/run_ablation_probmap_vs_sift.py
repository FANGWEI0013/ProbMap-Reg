import argparse
import math
import time
from pathlib import Path

import cv2
import numpy as np

from config import (
    CNN_INPUT_SIZE,
    FIRE_GROUND_TRUTH_DIR,
    FIRE_IMAGES_DIR,
    MODEL_PATH,
    PROBABILITY_THRESHOLD,
    RANSAC_THRESHOLD_PX,
    RESULTS_ROOT,
    SMALL_TEST_PAIRS,
)
from utils_eval import (
    generate_fire_pair_ids,
    ground_truth_path,
    normalized_auc,
    read_control_points,
    registration_error,
    split_pair_id,
    write_csv,
)
from utils_features import extract_features
from utils_matching import nearest_neighbor_matches, scale_matches_to_original
from utils_model import load_unet_model, predict_pair_probability_maps, read_bgr_image
from utils_transform import affine_2x3_to_homogeneous, ransac_inliers


OUTPUT_DIR = RESULTS_ROOT / "ablation_probmap_vs_sift"

FULL_PROBMAP = "Full_ProbabilityMap"
SIFT_BASELINE = "Without_ProbabilityMap_SIFT"
SIFT_ENHANCED = "SIFT_Enhanced"
SIFT_RATIO_TEST = 0.75

EXPERIMENT_ORDER = (
    FULL_PROBMAP,
    SIFT_BASELINE,
    SIFT_ENHANCED,
)

TABLE_ORDER = (
    SIFT_BASELINE,
    SIFT_ENHANCED,
    FULL_PROBMAP,
)

METHOD_LABELS = {
    FULL_PROBMAP: "Proposed method",
    SIFT_BASELINE: "SIFT replacement baseline",
    SIFT_ENHANCED: "SIFT enhanced baseline",
}

FEATURE_LABELS = {
    FULL_PROBMAP: "U-Net probability map local maxima",
    SIFT_BASELINE: "OpenCV SIFT keypoints",
    SIFT_ENHANCED: "OpenCV SIFT keypoints",
}

DESCRIPTOR_LABELS = {
    FULL_PROBMAP: "HOG",
    SIFT_BASELINE: "SIFT",
    SIFT_ENHANCED: "SIFT + ratio/mutual",
}

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
    "mean_num_points_1",
    "mean_num_points_2",
    "mean_num_matches",
    "mean_num_inliers",
]

TABLE_FIELDNAMES = [
    "Method",
    "Feature extraction",
    "Descriptor",
    "Category S AUC",
    "Category P AUC",
    "Category A AUC",
    "Overall AUC",
    "Avg. Time (s)",
    "Failed pairs",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Ablation: probability-map features vs SIFT baseline.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--small-test", action="store_true", help="Run A01-A03 only.")
    mode.add_argument("--full-run", action="store_true", help="Run all FIRE pairs.")

    vis = parser.add_mutually_exclusive_group()
    vis.add_argument("--save-vis", action="store_true", help="Reserved for interface consistency.")
    vis.add_argument("--no-vis", action="store_true", help="Disable visual outputs.")
    return parser.parse_args()


def selected_pair_ids(args):
    if args.full_run:
        return generate_fire_pair_ids()
    return list(SMALL_TEST_PAIRS)


def base_row(experiment, pair_id, start_time, status, error, counts, message):
    category, index = split_pair_id(pair_id)
    return {
        "experiment": experiment,
        "category": category,
        "index": index,
        "pair_id": pair_id,
        "status": status,
        "error": error,
        "num_points_1": counts.get("num_points_1", 0),
        "num_points_2": counts.get("num_points_2", 0),
        "num_matches": counts.get("num_matches", 0),
        "num_inliers": counts.get("num_inliers", 0),
        "runtime": time.perf_counter() - start_time,
        "message": message,
    }


def failed_row(experiment, pair_id, start_time, message, counts=None):
    return base_row(
        experiment=experiment,
        pair_id=pair_id,
        start_time=start_time,
        status="failed",
        error=float("inf"),
        counts=counts or {},
        message=message,
    )


def finish_registration(experiment, pair_id, start_time, image_shape, matches, counts):
    if len(matches) < 2:
        return failed_row(experiment, pair_id, start_time, "not enough matches", counts)

    matrix_2x3, inliers = ransac_inliers(matches, RANSAC_THRESHOLD_PX)
    counts["num_inliers"] = len(inliers)
    similarity_matrix = affine_2x3_to_homogeneous(matrix_2x3)
    control_points = read_control_points(ground_truth_path(FIRE_GROUND_TRUTH_DIR, pair_id))
    error = registration_error(similarity_matrix, control_points)
    if not math.isfinite(error):
        return failed_row(experiment, pair_id, start_time, "registration error is not finite", counts)
    return base_row(
        experiment=experiment,
        pair_id=pair_id,
        start_time=start_time,
        status="success",
        error=float(error),
        counts=counts,
        message="ok",
    )


def process_probability_map_pair(model, pair_id):
    start = time.perf_counter()
    counts = {}
    try:
        image_1 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_1.jpg")
        image_2 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_2.jpg")
        probability_1, probability_2 = predict_pair_probability_maps(model, image_1, image_2)
        points_1, descriptors_1, _ = extract_features(probability_1, image_1, PROBABILITY_THRESHOLD)
        points_2, descriptors_2, _ = extract_features(probability_2, image_2, PROBABILITY_THRESHOLD)
        counts["num_points_1"] = len(points_1)
        counts["num_points_2"] = len(points_2)
        if len(points_1) < 2 or len(points_2) < 2:
            return failed_row(FULL_PROBMAP, pair_id, start, "not enough feature points", counts)
        if len(descriptors_1) == 0 or len(descriptors_2) == 0:
            return failed_row(FULL_PROBMAP, pair_id, start, "empty descriptors", counts)

        matches_480 = nearest_neighbor_matches(points_1, descriptors_1, points_2, descriptors_2)
        counts["num_matches"] = len(matches_480)
        matches = scale_matches_to_original(matches_480, image_1.shape, CNN_INPUT_SIZE)
        return finish_registration(FULL_PROBMAP, pair_id, start, image_1.shape, matches, counts)
    except Exception as exc:
        return failed_row(FULL_PROBMAP, pair_id, start, str(exc), counts)


def create_sift():
    if not hasattr(cv2, "SIFT_create"):
        raise RuntimeError("OpenCV SIFT is unavailable in this environment")
    return cv2.SIFT_create()


def sift_points_and_descriptors(sift, image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    if descriptors is None or not keypoints:
        return np.empty((0, 2), dtype=np.float32), np.empty((0, 128), dtype=np.float32)
    points = np.asarray([(kp.pt[1], kp.pt[0]) for kp in keypoints], dtype=np.float32)
    return points, descriptors.astype(np.float32)


def process_sift_pair(sift, pair_id):
    start = time.perf_counter()
    counts = {}
    try:
        image_1 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_1.jpg")
        image_2 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_2.jpg")
        points_1, descriptors_1 = sift_points_and_descriptors(sift, image_1)
        points_2, descriptors_2 = sift_points_and_descriptors(sift, image_2)
        counts["num_points_1"] = len(points_1)
        counts["num_points_2"] = len(points_2)
        if len(points_1) < 2 or len(points_2) < 2:
            return failed_row(SIFT_BASELINE, pair_id, start, "not enough feature points", counts)
        if len(descriptors_1) == 0 or len(descriptors_2) == 0:
            return failed_row(SIFT_BASELINE, pair_id, start, "empty descriptors", counts)

        matches = nearest_neighbor_matches(points_1, descriptors_1, points_2, descriptors_2)
        counts["num_matches"] = len(matches)
        return finish_registration(SIFT_BASELINE, pair_id, start, image_1.shape, matches, counts)
    except Exception as exc:
        return failed_row(SIFT_BASELINE, pair_id, start, str(exc), counts)


def ratio_matches(descriptors_1, descriptors_2, ratio=SIFT_RATIO_TEST):
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    knn = matcher.knnMatch(descriptors_1, descriptors_2, k=2)
    accepted = {}
    for candidates in knn:
        if len(candidates) < 2:
            continue
        first, second = candidates
        if first.distance < ratio * second.distance:
            accepted[first.queryIdx] = first.trainIdx
    return accepted


def enhanced_sift_matches(points_1, descriptors_1, points_2, descriptors_2):
    forward = ratio_matches(descriptors_1, descriptors_2)
    backward = ratio_matches(descriptors_2, descriptors_1)
    matches = []
    for idx_1, idx_2 in forward.items():
        if backward.get(idx_2) != idx_1:
            continue
        y1, x1 = points_1[idx_1]
        y2, x2 = points_2[idx_2]
        matches.append((float(y1), float(x1), float(y2), float(x2)))
    return np.asarray(matches, dtype=np.float32)


def process_sift_enhanced_pair(sift, pair_id):
    start = time.perf_counter()
    counts = {}
    try:
        image_1 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_1.jpg")
        image_2 = read_bgr_image(FIRE_IMAGES_DIR / f"{pair_id}_2.jpg")
        points_1, descriptors_1 = sift_points_and_descriptors(sift, image_1)
        points_2, descriptors_2 = sift_points_and_descriptors(sift, image_2)
        counts["num_points_1"] = len(points_1)
        counts["num_points_2"] = len(points_2)
        if len(points_1) < 2 or len(points_2) < 2:
            return failed_row(SIFT_ENHANCED, pair_id, start, "not enough feature points", counts)
        if len(descriptors_1) == 0 or len(descriptors_2) == 0:
            return failed_row(SIFT_ENHANCED, pair_id, start, "empty descriptors", counts)

        matches = enhanced_sift_matches(points_1, descriptors_1, points_2, descriptors_2)
        counts["num_matches"] = len(matches)
        return finish_registration(SIFT_ENHANCED, pair_id, start, image_1.shape, matches, counts)
    except Exception as exc:
        return failed_row(SIFT_ENHANCED, pair_id, start, str(exc), counts)


def summarize_ablation_rows(rows):
    summaries = []
    for experiment in EXPERIMENT_ORDER:
        experiment_rows = [row for row in rows if row["experiment"] == experiment]
        categories = sorted({row["category"] for row in experiment_rows})
        categories.append("ALL")
        for category in categories:
            selected = (
                experiment_rows
                if category == "ALL"
                else [row for row in experiment_rows if row["category"] == category]
            )
            if not selected:
                continue
            errors = [float(row["error"]) for row in selected]
            success_rows = [
                row for row in selected
                if row["status"] == "success" and math.isfinite(float(row["error"]))
            ]
            success_25 = sum(
                1 for row in selected
                if math.isfinite(float(row["error"])) and float(row["error"]) <= 25.0
            ) / float(len(selected))
            summaries.append(
                {
                    "experiment": experiment,
                    "category": category,
                    "num_pairs": len(selected),
                    "num_success": len(success_rows),
                    "num_failed": len(selected) - len(success_rows),
                    "success_25px": success_25,
                    "auc": normalized_auc(errors),
                    "mean_error_success_only": (
                        float(np.mean([float(row["error"]) for row in success_rows]))
                        if success_rows else float("inf")
                    ),
                    "mean_runtime": float(np.mean([float(row["runtime"]) for row in selected])),
                    "mean_num_points_1": float(np.mean([float(row["num_points_1"]) for row in selected])),
                    "mean_num_points_2": float(np.mean([float(row["num_points_2"]) for row in selected])),
                    "mean_num_matches": float(np.mean([float(row["num_matches"]) for row in selected])),
                    "mean_num_inliers": float(np.mean([float(row["num_inliers"]) for row in selected])),
                }
            )
    return summaries


def summary_lookup(summary_rows, experiment, category):
    for row in summary_rows:
        if row["experiment"] == experiment and row["category"] == category:
            return row
    return None


def format_float(value, digits=4):
    value = float(value)
    if not math.isfinite(value):
        return "inf"
    return f"{value:.{digits}f}"


def build_ablation_table(summary_rows):
    table = []
    for experiment in TABLE_ORDER:
        row_s = summary_lookup(summary_rows, experiment, "S")
        row_p = summary_lookup(summary_rows, experiment, "P")
        row_a = summary_lookup(summary_rows, experiment, "A")
        row_all = summary_lookup(summary_rows, experiment, "ALL")
        table.append(
            {
                "Method": METHOD_LABELS[experiment],
                "Feature extraction": FEATURE_LABELS[experiment],
                "Descriptor": DESCRIPTOR_LABELS[experiment],
                "Category S AUC": format_float(row_s["auc"]) if row_s else "",
                "Category P AUC": format_float(row_p["auc"]) if row_p else "",
                "Category A AUC": format_float(row_a["auc"]) if row_a else "",
                "Overall AUC": format_float(row_all["auc"]) if row_all else "",
                "Avg. Time (s)": format_float(row_all["mean_runtime"], digits=3) if row_all else "",
                "Failed pairs": int(row_all["num_failed"]) if row_all else "",
            }
        )
    return table


def write_latex_table(path, table_rows):
    lines = [
        r"\begin{tabular}{lllrrrrrr}",
        r"\hline",
        r"Method & Feature extraction & Descriptor & S AUC & P AUC & A AUC & Overall AUC & Avg. Time (s) & Failed pairs \\",
        r"\hline",
    ]
    for row in table_rows:
        lines.append(
            " & ".join(
                [
                    row["Method"],
                    row["Feature extraction"],
                    row["Descriptor"],
                    row["Category S AUC"],
                    row["Category P AUC"],
                    row["Category A AUC"],
                    row["Overall AUC"],
                    row["Avg. Time (s)"],
                    str(row["Failed pairs"]),
                ]
            )
            + r" \\"
        )
    lines.extend([r"\hline", r"\end{tabular}"])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def safe_write_csv(path, rows, fieldnames):
    try:
        write_csv(path, rows, fieldnames)
        return Path(path)
    except PermissionError:
        path = Path(path)
        fallback = path.with_name(f"{path.stem}_latest{path.suffix}")
        write_csv(fallback, rows, fieldnames)
        print(f"Warning: {path} is locked; wrote {fallback} instead.")
        return fallback


def safe_write_latex_table(path, table_rows):
    try:
        write_latex_table(path, table_rows)
        return Path(path)
    except PermissionError:
        path = Path(path)
        fallback = path.with_name(f"{path.stem}_latest{path.suffix}")
        write_latex_table(fallback, table_rows)
        print(f"Warning: {path} is locked; wrote {fallback} instead.")
        return fallback


def main():
    args = parse_args()
    pair_ids = selected_pair_ids(args)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading U-Net model: {MODEL_PATH}")
    model = load_unet_model(MODEL_PATH)
    sift = create_sift()

    rows = []
    for pair_id in pair_ids:
        print(f"Processing {pair_id} / {FULL_PROBMAP}")
        probmap_row = process_probability_map_pair(model, pair_id)
        rows.append(probmap_row)
        print(f"  {probmap_row['status']} error={probmap_row['error']} message={probmap_row['message']}")

        print(f"Processing {pair_id} / {SIFT_BASELINE}")
        sift_row = process_sift_pair(sift, pair_id)
        rows.append(sift_row)
        print(f"  {sift_row['status']} error={sift_row['error']} message={sift_row['message']}")

        print(f"Processing {pair_id} / {SIFT_ENHANCED}")
        sift_enhanced_row = process_sift_enhanced_pair(sift, pair_id)
        rows.append(sift_enhanced_row)
        print(
            f"  {sift_enhanced_row['status']} "
            f"error={sift_enhanced_row['error']} "
            f"message={sift_enhanced_row['message']}"
        )

    summary_rows = summarize_ablation_rows(rows)
    table_rows = build_ablation_table(summary_rows)

    raw_path = safe_write_csv(OUTPUT_DIR / "raw_pairs.csv", rows, RAW_FIELDNAMES)
    summary_path = safe_write_csv(OUTPUT_DIR / "summary.csv", summary_rows, SUMMARY_FIELDNAMES)
    table_path = safe_write_csv(OUTPUT_DIR / "ablation_table.csv", table_rows, TABLE_FIELDNAMES)
    latex_path = safe_write_latex_table(OUTPUT_DIR / "ablation_table_latex.txt", table_rows)

    print(f"Wrote {raw_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {table_path}")
    print(f"Wrote {latex_path}")


if __name__ == "__main__":
    main()
