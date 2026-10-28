import csv
import math
from pathlib import Path

import numpy as np

from config import AUC_MAX_THRESHOLD_PX, FIRE_CATEGORIES, SUCCESS_THRESHOLD_PX


def generate_fire_pair_ids(categories=FIRE_CATEGORIES):
    pair_ids = []
    for category, max_index in categories.items():
        for index in range(1, max_index + 1):
            pair_ids.append(f"{category}{index:02d}")
    return pair_ids


def split_pair_id(pair_id):
    return pair_id[0], pair_id[1:]


def ground_truth_path(ground_truth_dir, pair_id):
    return Path(ground_truth_dir) / f"control_points_{pair_id}_1_2.txt"


def read_control_points(path):
    rows = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            parts = line.split()
            if len(parts) < 4:
                continue
            rows.append([float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])])
    if not rows:
        raise ValueError(f"No control points found in {path}")
    return np.asarray(rows, dtype=np.float64)


def registration_distances(similarity_matrix_3x3, control_points):
    source = np.column_stack(
        [
            control_points[:, 0],
            control_points[:, 1],
            np.ones(len(control_points), dtype=np.float64),
        ]
    )
    target = control_points[:, 2:4]
    transformed = (similarity_matrix_3x3 @ source.T).T
    transformed_xy = transformed[:, :2] / transformed[:, 2:3]
    return np.linalg.norm(transformed_xy - target, axis=1)


def registration_error(similarity_matrix_3x3, control_points):
    distances = registration_distances(similarity_matrix_3x3, control_points)
    return float(np.mean(distances))


def success_curve(errors, max_threshold=AUC_MAX_THRESHOLD_PX):
    finite_errors = np.asarray([err for err in errors if math.isfinite(err)], dtype=np.float64)
    thresholds = np.arange(0, max_threshold + 1, dtype=np.float64)
    if len(errors) == 0:
        return thresholds, np.zeros_like(thresholds)
    rates = np.asarray(
        [float(np.sum(finite_errors <= threshold)) / float(len(errors)) for threshold in thresholds],
        dtype=np.float64,
    )
    return thresholds, rates


def normalized_auc(errors, max_threshold=AUC_MAX_THRESHOLD_PX):
    thresholds, rates = success_curve(errors, max_threshold=max_threshold)
    if max_threshold <= 0:
        return 0.0
    return float(np.trapz(rates, thresholds) / float(max_threshold))


def summarize_rows(rows, experiment):
    summaries = []
    categories = sorted({row["category"] for row in rows})
    categories.append("ALL")
    for category in categories:
        selected = rows if category == "ALL" else [row for row in rows if row["category"] == category]
        if not selected:
            continue
        errors = [float(row["error"]) for row in selected]
        success_rows = [
            row for row in selected
            if row["status"] == "success" and math.isfinite(float(row["error"]))
        ]
        success_25 = sum(
            1 for row in selected
            if math.isfinite(float(row["error"])) and float(row["error"]) <= SUCCESS_THRESHOLD_PX
        ) / float(len(selected))
        runtimes = [float(row["runtime"]) for row in selected]
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
                "mean_runtime": float(np.mean(runtimes)) if runtimes else 0.0,
            }
        )
    return summaries


def write_csv(path, rows, fieldnames):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
