# Point estimate, bootstrap mean and percentile CI

The recovered `analyze_bootstrap_ci.py` computes `auc = normalized_auc(errors)` on the original errors and returns only CI bounds from `bootstrap_auc_ci`. Its output `auc` column is definitively the point estimate; it never calculates a mean over bootstrap AUCs. The paper labels Table 4's central Overall value as a bootstrap mean. That semantic conflict remains documented; the original scientific script is unchanged.

The new `scripts/bootstrap_statistics.py` is an explicitly separate diagnostic. It calls the same recovered AUC definition and reports `point_auc`, `bootstrap_mean_auc`, `ci_lower_95`, and `ci_upper_95`. It retains uniform resampling of pairs with replacement, failed pairs as infinity, 1,000 draws by default, and the original seed/order for exact comparison. Two tests independently check estimands and failure retention.

Read-only replay of the saved 402-row ablation file gives:

| Method | Point Overall AUC | Actual bootstrap mean | 95% percentile CI |
|---|---:|---:|---|
| Without_ProbabilityMap_SIFT | 0.092089552 | 0.092068209 | [0.060585821, 0.124932836] |
| SIFT_Enhanced | 0.195373134 | 0.196086418 | [0.148652985, 0.243000000] |
| Full_ProbabilityMap | 0.627611940 | 0.627471045 | [0.567145522, 0.687470149] |

These are arithmetic reanalyses of saved errors, not a full registration rerun. Recent Proposed point AUC 0.627611940 rounds to 0.628, whereas the actual mean for this replay 0.627471045 rounds to 0.627. This demonstrates that the point column could explain the recovered table's center, but does not prove how the publication's stated mean was computed. A different genuine source run/seed may exist; none was selected or searched by seed to force a match.

The paper's main Overall **0.626** and bootstrap mean Overall **0.628** are retained separately. Published intervals [0.061,0.125], [0.149,0.243] and [0.567,0.687] also remain unchanged. No values are rewritten because a source diagnostic differs.

## Execution contract

The source default is seed **20260713**, with one NumPy `default_rng` advanced through the source experiment/category order. Resampling is uniform with replacement within each experiment/category group (ALL uses all its pair rows), with exactly n draws for n input pairs. Unparseable/nonfinite error values become infinity and remain in the sample count. The registration engines write infinity for failed pairs; the bootstrap reader uses the error column, not the status label. Missing required columns are not repaired. Bounds are NumPy's 2.5th/97.5th percentiles of the bootstrap AUCs. Each diagnostic row records `n_pairs`, `iterations`, `seed`, `point_auc`, `bootstrap_mean_auc` and CI bounds. Round 3 executed this workflow on three pairs per method, not the complete published experiment.
