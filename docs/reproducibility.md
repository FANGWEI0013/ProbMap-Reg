# Reproducibility status

Current license finalization and 12-test rerun: **2026-10-29**; prior functional smoke checks: **2026-10-28**. See [final validation](final_validation.md). Source authorship is author-confirmed and MIT is author-approved. The Round 3 scientific evidence below is retained. No scientific algorithms changed.

The **Recovered reconstruction implementation** is executable for checkpoint inference, Proposed registration, FIRE saved-error evaluation, SIFT baselines, bootstrap diagnostics and plotting with the documented inputs. It is not established as the exact published implementation.

The 11 retained scientific source modules remain byte-identical to Round 2. Round 3 changes are packaging: clearer wrapper help and missing-ablation preflight; a saved-error evaluation CLI calling the original evaluator; three packaging tests; documentation and release manifests. No HOG, maxima, coordinate rounding, optimizer, model graph, RANSAC, similarity, AUC or bootstrap-sampling logic changed.

Actually executed in Round 3: original 9 tests, expanded 12-test suite, all CLI helps, original engine helps, Python 3.9 venv creation/pip probe, dependency/import checks, inference, one A01 pair, A01–A03 Proposed and three-method ablation, P48, evaluation, both bootstrap routes, plotting, external trainer help and an actual missing-image failure-row check. Configuration JSON/syntax were checked. [Exact sanitized command log](round3_commands.json) and [validation](validation.md) record outcomes. A restricted temporary-directory permission issue in the first added-test attempt was resolved by using a writable audit TEMP/TMP, without changing scientific behavior.

A new empty environment was created, but its full requirements were not installed: this avoided another large TensorFlow download. Testing used the existing compatible environment/workspace overlay. Fresh complete dependency installation and other operating systems are unverified. Windows 11 Home 25H2, Python 3.9.25, TF 2.10.1, OpenCV 4.8.1, NumPy 1.23.5 and SciPy 1.10.1 were observed. Zero usable TensorFlow GPUs; all smoke inference used CPU. No drivers or system Python were modified.

The main reproduction gaps remain:

- Exact sigma 5/vessel-edge-constrained pseudo-label source and provider-mask lineage.
- Split seed and original executed training/validation paths; archived validation folder semantics are reversed.
- Published Fig. 9 numerical loss history and exact run/model association.
- Published 80/20 source version versus historical 90/30, HOG/scaling/geometry/result-set differences and S rounding.
- Complete FPE Table 1 aggregation and fixed-pixel versus 32-bin interpretation.
- Original publication bootstrap-mean source. Main Overall 0.626 and reported mean 0.628 remain separate paper statements; the latter is not independently verified.
- Any future checkpoint redistribution needs separate authorization. Project source authorship is confirmed and MIT is approved; datasets/weights and excluded materials remain outside the release.

No full 134-pair benchmark, 50-epoch training, published 2.2-second runtime, clinical-readiness or cross-device generalization claim follows from the few smoke pairs. Diagnostic sample statistics are not publication regression targets. RANSAC/random behavior was not reseeded to force a match. [Settings](experiment_settings.md), [audit](code_paper_audit.md) and [training lineage](training_lineage.md) preserve all conflicts.
