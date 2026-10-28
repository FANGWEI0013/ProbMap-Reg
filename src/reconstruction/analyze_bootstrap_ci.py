import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from config import AUC_MAX_THRESHOLD_PX, RESULTS_ROOT


INPUT_PATH = RESULTS_ROOT / "ablation_probmap_vs_sift" / "raw_pairs.csv"
OUTPUT_DIR = RESULTS_ROOT / "ablation_probmap_vs_sift"
CI_OUTPUT_PATH = OUTPUT_DIR / "auc_confidence_intervals.csv"
TABLE_OUTPUT_PATH = OUTPUT_DIR / "ablation_table_with_ci.csv"

N_BOOTSTRAP = 1000
RANDOM_SEED = 20260713

EXPERIMENT_ORDER = (
    "Without_ProbabilityMap_SIFT",
    "SIFT_Enhanced",
    "Full_ProbabilityMap",
)

CATEGORY_ORDER = ("S", "P", "A", "ALL")

METHOD_LABELS = {
    "Without_ProbabilityMap_SIFT": "SIFT replacement baseline",
    "SIFT_Enhanced": "SIFT enhanced baseline",
    "Full_ProbabilityMap": "Proposed method",
}

CI_FIELDNAMES = [
    "experiment",
    "category",
    "n_pairs",
    "auc",
    "ci_lower_95",
    "ci_upper_95",
]

TABLE_FIELDNAMES = [
    "Method",
    "Category S AUC",
    "Category S 95% CI",
    "Category P AUC",
    "Category P 95% CI",
    "Category A AUC",
    "Category A 95% CI",
    "Overall AUC",
    "Overall 95% CI",
    "Avg. Time (s)",
]


def parse_error(value):
    try:
        error = float(value)
    except (TypeError, ValueError):
        return float("inf")
    return error if math.isfinite(error) else float("inf")


def read_raw_pairs(path):
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalized_auc(errors, max_threshold=AUC_MAX_THRESHOLD_PX):
    errors = np.asarray(errors, dtype=np.float64)
    thresholds = np.arange(0, max_threshold + 1, dtype=np.float64)
    if len(errors) == 0:
        return 0.0
    finite_errors = errors[np.isfinite(errors)]
    rates = np.asarray(
        [np.sum(finite_errors <= threshold) / float(len(errors)) for threshold in thresholds],
        dtype=np.float64,
    )
    return float(np.trapz(rates, thresholds) / float(max_threshold))


def bootstrap_auc_ci(errors, rng, n_bootstrap=N_BOOTSTRAP):
    errors = np.asarray(errors, dtype=np.float64)
    if len(errors) == 0:
        return 0.0, 0.0
    aucs = np.empty(n_bootstrap, dtype=np.float64)
    for idx in range(n_bootstrap):
        sample_indices = rng.integers(0, len(errors), size=len(errors))
        aucs[idx] = normalized_auc(errors[sample_indices])
    lower, upper = np.percentile(aucs, [2.5, 97.5])
    return float(lower), float(upper)


def grouped_errors(rows):
    groups = defaultdict(list)
    for row in rows:
        experiment = row["experiment"]
        category = row["category"]
        error = parse_error(row["error"])
        groups[(experiment, category)].append(error)
        groups[(experiment, "ALL")].append(error)
    return groups


def average_runtime_by_experiment(rows):
    runtimes = defaultdict(list)
    for row in rows:
        try:
            runtime = float(row["runtime"])
        except (TypeError, ValueError):
            continue
        runtimes[row["experiment"]].append(runtime)
    return {
        experiment: float(np.mean(values)) if values else 0.0
        for experiment, values in runtimes.items()
    }


def compute_ci_rows(rows):
    groups = grouped_errors(rows)
    rng = np.random.default_rng(RANDOM_SEED)
    ci_rows = []

    experiments = [experiment for experiment in EXPERIMENT_ORDER if any(row["experiment"] == experiment for row in rows)]
    for experiment in experiments:
        for category in CATEGORY_ORDER:
            errors = groups.get((experiment, category), [])
            if not errors:
                continue
            auc = normalized_auc(errors)
            lower, upper = bootstrap_auc_ci(errors, rng)
            ci_rows.append(
                {
                    "experiment": experiment,
                    "category": category,
                    "n_pairs": len(errors),
                    "auc": auc,
                    "ci_lower_95": lower,
                    "ci_upper_95": upper,
                }
            )
    return ci_rows


def format_float(value, digits=4):
    value = float(value)
    if not math.isfinite(value):
        return "inf"
    return f"{value:.{digits}f}"


def format_ci(row):
    if row is None:
        return ""
    return f"[{format_float(row['ci_lower_95'])}, {format_float(row['ci_upper_95'])}]"


def lookup_ci(ci_rows, experiment, category):
    for row in ci_rows:
        if row["experiment"] == experiment and row["category"] == category:
            return row
    return None


def build_table_rows(ci_rows, rows):
    avg_runtime = average_runtime_by_experiment(rows)
    table_rows = []
    for experiment in EXPERIMENT_ORDER:
        if not any(row["experiment"] == experiment for row in rows):
            continue
        row_s = lookup_ci(ci_rows, experiment, "S")
        row_p = lookup_ci(ci_rows, experiment, "P")
        row_a = lookup_ci(ci_rows, experiment, "A")
        row_all = lookup_ci(ci_rows, experiment, "ALL")
        table_rows.append(
            {
                "Method": METHOD_LABELS.get(experiment, experiment),
                "Category S AUC": format_float(row_s["auc"]) if row_s else "",
                "Category S 95% CI": format_ci(row_s),
                "Category P AUC": format_float(row_p["auc"]) if row_p else "",
                "Category P 95% CI": format_ci(row_p),
                "Category A AUC": format_float(row_a["auc"]) if row_a else "",
                "Category A 95% CI": format_ci(row_a),
                "Overall AUC": format_float(row_all["auc"]) if row_all else "",
                "Overall 95% CI": format_ci(row_all),
                "Avg. Time (s)": format_float(avg_runtime.get(experiment, 0.0), digits=3),
            }
        )
    return table_rows


def write_csv(path, rows, fieldnames):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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


def main():
    rows = read_raw_pairs(INPUT_PATH)
    ci_rows = compute_ci_rows(rows)
    table_rows = build_table_rows(ci_rows, rows)

    ci_path = safe_write_csv(CI_OUTPUT_PATH, ci_rows, CI_FIELDNAMES)
    table_path = safe_write_csv(TABLE_OUTPUT_PATH, table_rows, TABLE_FIELDNAMES)

    print(f"Read {INPUT_PATH}")
    print(f"Wrote {ci_path}")
    print(f"Wrote {table_path}")


if __name__ == "__main__":
    main()
