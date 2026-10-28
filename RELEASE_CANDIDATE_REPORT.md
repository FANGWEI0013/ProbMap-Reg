> Historical Round 3 report, 2026-10-19. Ownership, license and Git-status assertions below describe that date. Current author-confirmed status and release preparation supersede them in [FINAL_RELEASE_REPORT.md](FINAL_RELEASE_REPORT.md).

# ProbMap-Reg Round 3 release candidate — 2026-10-19

**READY FOR REVIEW / NOT READY FOR PUBLICATION.** Source ownership/coauthor/upstream clearance and an explicit software-license decision remain pending. This package is an executable recovered reconstruction with documented scientific gaps, not complete paper reproduction.

## 1. Included and excluded

Included: eleven unchanged reconstruction modules, six real CLI wrappers, twelve tests in three test files, minimal pinned requirements, reporting/config metadata, checkpoint/output policies and scientific/release documentation. New packaging consists of a saved-error evaluator, clearer parser/prerequisite errors, three tests and documentation/manifest updates. Detailed prior inventories are preserved privately; public evidence retains technical aggregate results and source hashes.

Excluded: FIVES/FIRE images/masks/control annotations, all weights/checkpoints, loss curves/logs, raw benchmark outputs, personal location inventories, caches/environments, original PDFs/archives, historical/archived/prior-method/downloaded-stitching/original-training source with unresolved rights. No original research files were deleted or overwritten. A separate private snapshot of the initial 53-file candidate was verified before edits. No nested Git repository was created.

Scoped external exclusions: **12 checkpoint files / 2,274,363,331 bytes**, including physical duplicate copies; **1,605 dataset/input files / 570,823,143 bytes**. These are known scoped holdings, not an exhaustive machine inventory. See docs/excluded_artifact_summary.json.

## 2. Execution supported today

With an authorized external compatible Keras HDF5 model and local FIRE inputs: single-image response/features, Proposed single-pair or A01–A03 registration/mosaics, and three-method Proposed/SIFT NN/SIFT ratio-mutual ablation. Image1 maps into image2. With saved raw errors alone: FIRE summaries, legacy percentile bootstrap, explicit point/mean/CI statistics and success-curve plotting. See docs/quickstart.md for actual flags and output paths.

Training is an external authorized-trainer launcher, not a bundled or verified training reproduction. Exact sigma 5 generation and original FPE Table 1 aggregation are not executable here. No substitute implementation was added.

## 3. Commands executed and tests

All 24 top-level command checks matched expected exit codes, including missing-checkpoint exit 2. The original nine tests passed, then all twelve tests passed. After application to the final Desktop candidate, all twelve tests passed again; its Git untracked list exactly matched the 64-file allowlist, and all manifest/mirror checksums matched. All six CLI helps and two engine helps succeeded. AST syntax validation covered 20 Python files; eleven scientific module imports and JSON configuration parsing passed. pip check found no broken requirements; isolated venv creation succeeded. The scientific modules' SHA-256 hashes remain identical to Round 2.

Executed with real local inputs: inference A01_1 (44 features), Proposed A01 visualization, Proposed A01–A03 visualization, P48, nine-row three-method ablation, saved-error evaluator, legacy bootstrap, explicit point/mean/CI wrapper and PNG success curves. External trainer help delegation succeeded without fitting. An actual missing-image call preserved failed/inf output; tests check failed denominators, geometry, CLI preflight and estimator semantics. Exact sanitized commands and return codes: docs/round3_commands.json. Detailed outcomes: docs/validation.md.

| Limited Proposed test | Mean error (pixels) | Inliers |
|---|---:|---:|
| A01 |4.657976795|22|
| A02 |11.235663643|10|
| A03 |7.823944116|17|
| P48 |1148.223381091|9|

These are limited CPU checks, not full FIRE AUC or runtime replication. SIFT outputs are in docs/round3_results.json. `success` means processing completed even for P48's large error. Failed/nonfinite errors remain in evaluation denominators.

## 4. Not tested or independently reproduced

Fresh complete requirements installation, another operating system, optional failure-comparison visualization, 50-epoch training and the full 134-pair benchmark were not executed. Exact label generation/FPE aggregation are missing; the published training-loss history is not recovered. Published 2.2 seconds/pair was not reproduced. No CUDA/drivers/system Python changes occurred. Tests used Windows 11 Home 25H2 build 26200.9711, Python 3.9.25, TensorFlow 2.10.1, Keras 2.10.0, OpenCV 4.8.1, NumPy 1.23.5, SciPy 1.10.1 and Matplotlib 3.7.5, CPU in an existing compatible environment/workspace overlay. Full fresh installation remains unverified.

## 5. Published reporting versus observed outputs

The exact local IEEE PDF is reporting authority. Published main AUC S/P/A/Overall = **0.902/0.198/0.720/0.626**. Published ablation Overall bootstrap means NN/enhanced/Proposed = **0.092/0.195/0.628**, with Proposed 95% CI **[0.567,0.687]**, 1,000 resamples. These remain metadata, not tests or output targets. README retains all category/CI values separately. No published quantities were changed or claimed independently reproduced.

The legacy bootstrap center is point AUC, not bootstrap mean. Saved-error reanalysis gives Proposed point 0.627611940 and mean 0.627471045 under the recovered order/seed; its source does not establish the publication's stated mean. No seed was searched to force agreement. Round 3 statistics used the small sample only.

## 6. Scientific audit: explained and unresolved

Established in prior recovery and reconfirmed: genuine historical 90/30 settings; HOG-library differences materially affect P48; archived validation folder contents reverse their names; full-model/weights-only arrays and topology agree with the recovered TensorFlow training family; the legacy bootstrap column is a point estimate. Round 3 confirms unchanged source, source→target direction, failed-row retention and execution of the packaged workflows. It adds no unsupported historical inference.

Still unresolved: exact sigma 5 vessel-edge generator/provider-mask lineage, split seed and executed validation paths, numeric Fig. 9 loss logs, exact published 80/20 source identity, HOG/scaling/geometry/result-set differences, original FPE aggregation and fixed-pixel versus 32-bin policy, S rounding and original publication bootstrap-mean source. No logic was adjusted to hide these gaps. docs/code_paper_audit.md records VERIFIED/PARTIAL/MISSING/CONFLICT with source files.

## 7. Privacy, licensing and approvals

No sensitive-pattern, binary/data/model, notebook or >10 MB warning was found in the positive allowlist. Scope and limitations: docs/privacy_scan.md and JSON. Automated pattern scanning is not a privacy/legal guarantee. No committed history exists to scan. Requirements name dependencies rather than vendoring them.

All eleven files in src/reconstruction require author/coauthor ownership/upstream confirmation (listed individually in docs/third_party_provenance.md). Recovery-authored wrappers/tests/docs are identified separately. Third-party/prior-method/training variants remain outside Git. No formal license exists; publication without one does not grant open-source redistribution rights.

Required human decisions: confirm source rights/coauthor consent and any required notices; select/approve the software-license scope; approve publication explicitly as an incomplete recovered reconstruction; approve the exact allowlist. A later commit, remote creation and push require separate explicit approval. Dataset/checkpoint publication is not proposed and would require separate authorization.

## 8. Git and proposed commit

Branch release-review; no commits, staged files or remotes. All proposed files are untracked; git diff --stat is empty for that reason. No commit/remote/push was performed. Future intended repository: https://github.com/FANGWEI0013/ProbMap-Reg (not created by this task).

Proposed commit contents: exactly the files listed in docs/publication_files.json, with hashes in docs/publication_manifest.json; no broad add of external folders. Suggested message: `Prepare audited recovered ProbMap-Reg research release candidate`.

## 9. Publication inventory

Inventory counts and exact byte size are written below. The machine-readable hash manifest covers every proposed file except itself (no self-referential hash); the relative-path allowlist includes the manifest. Detailed tree: docs/publication_manifest.md. Hashes are checksums, not signatures or ownership evidence.

Proposed files: **64**; Python source files: **20**; total upload content: **266,029 bytes** (excluding .git and external inputs).
