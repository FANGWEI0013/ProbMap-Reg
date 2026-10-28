# Generated results

Keep outputs in ignored subdirectories here or outside the repository. No raw experiment CSV, image, feature array, control file or full benchmark log is in the publication allowlist. Public reports contain only limited aggregate validation/diagnostic values, distinct from paper tables.

Proposed writes `proposed/raw_pairs.csv`, `summary.csv`, and optional `vis/<pair>/`. Each new Proposed run overwrites those CSVs under the chosen output root; choose separate roots when preserving runs. Ablation writes `ablation_probmap_vs_sift/raw_pairs.csv`, `summary.csv`, `ablation_table.csv`, `ablation_table_latex.txt`. Legacy bootstrap adds `auc_confidence_intervals.csv` and `ablation_table_with_ci.csv`, whose center is a point estimate. Separate wrappers write explicit bootstrap statistics, saved-error evaluation CSV and success-curve PNG to their requested paths.

See `docs/quickstart.md` for real commands and `docs/validation.md` for the limited locally verified tests. A01–A03/P48 are not a full FIRE reproduction.
