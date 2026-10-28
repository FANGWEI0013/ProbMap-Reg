# Approved publication manifest — 2026-10-29

Exactly the 68 relative paths in publication_files.json are approved and staged, including LICENSE. stage_files equals files. MIT is author-approved with Copyright (c) 2026 Wei Fang. Source authorship is confirmed; independently licensed materials, datasets and checkpoints are not relicensed or included.

All staged blob bytes match reviewed files. publication_manifest.json records byte sizes and SHA-256 checksums except its own self-hash; the manifest itself remains in the allowlist. All twenty Python files and published metadata retain their prior hashes. No commit, remote creation, push or visibility change has occurred; those require separate authorization.

```text
ProbMap-Reg/
├── checkpoints/
│   └── README.md
├── configs/
│   ├── checkpoint_metadata.json
│   ├── published.json
│   └── reconstruction.json
├── docs/
│   ├── bootstrap_estimands.md
│   ├── code_paper_audit.md
│   ├── data_preparation.md
│   ├── engineering_changes.md
│   ├── excluded_artifact_summary.json
│   ├── exclusion_manifest.json
│   ├── experiment_settings.md
│   ├── final_validation.json
│   ├── final_validation.md
│   ├── fpe_definition.md
│   ├── model_training_validation.json
│   ├── privacy_scan.json
│   ├── privacy_scan.md
│   ├── publication_files.json
│   ├── publication_manifest.json
│   ├── publication_manifest.md
│   ├── quickstart.md
│   ├── release_checklist.md
│   ├── reproducibility.md
│   ├── round2_bootstrap_statistics.json
│   ├── round2_pipeline_comparison.json
│   ├── round2_search_evidence.json
│   ├── round2_split_semantics.json
│   ├── round2_training_trace.json
│   ├── round2_validation.json
│   ├── round2_validation.md
│   ├── round3_commands.json
│   ├── round3_results.json
│   ├── saved_evidence_reanalysis.json
│   ├── search_scope.md
│   ├── source_provenance.json
│   ├── third_party_provenance.md
│   ├── training_lineage.md
│   ├── validation.json
│   ├── validation.md
│   └── version_comparison.md
├── results/
│   └── README.md
├── scripts/
│   ├── bootstrap_statistics.py
│   ├── evaluate_fire.py
│   ├── infer.py
│   ├── plot_success_curves.py
│   ├── run_reconstruction.py
│   └── train_unet.py
├── src/
│   └── reconstruction/
│       ├── analyze_bootstrap_ci.py
│       ├── analyze_failure_cases.py
│       ├── config.py
│       ├── run_ablation_probmap_vs_sift.py
│       ├── run_proposed.py
│       ├── utils_eval.py
│       ├── utils_features.py
│       ├── utils_matching.py
│       ├── utils_model.py
│       ├── utils_transform.py
│       └── utils_vis.py
├── tests/
│   ├── test_cli.py
│   ├── test_core.py
│   └── test_statistics.py
├── .gitignore
├── FINAL_RELEASE_REPORT.md
├── LICENSE
├── README.md
├── RELEASE_CANDIDATE_REPORT.md
├── RELEASE_SUMMARY.md
└── requirements.txt
```
