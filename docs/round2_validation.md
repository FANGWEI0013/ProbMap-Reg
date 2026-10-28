# Second-round actual validation

Date: 2026-10-13, Asia/Tokyo. Environment: Python 3.9.25, TensorFlow 2.10.1, Keras 2.10.0, OpenCV 4.8.1, NumPy 1.23.5, SciPy 1.10.1. CPU inference; no GPU/driver or system-Python changes. Original historical checks additionally used the existing workspace validation overlay/scikit-image. Public core imports no quarantined source.

## Current minimal candidate

- All **18 Python files** parse under Python 3.9.25.
- **Nine unit tests passed**: failure denominator/endpoints, FIRE enumeration, geometry direction, scaling, strict maxima threshold, legacy bootstrap failure retention, OpenCV HOG/border behavior, and two independent reporting-diagnostic tests.
- The retained scientific modules are byte-identical to the first-round reconstruction. Requirements now list core imports only; a fresh full installation remains unverified.
- Native Proposed P48 completed: **1148.2233810909 pixels, 9 inliers**.
- All three ablation methods completed on A01–A03 after isolation. Ablation supports --small-test / --full-run; it does not support --pair. An attempted unsupported flag was rejected before processing and the valid small-test mode was then used.

| Method | Pair | Error (pixels) | Inliers |
|---|---|---:|---:|
| Full_ProbabilityMap | A01 | 4.657976795 | 22 |
| Without_ProbabilityMap_SIFT | A01 | 68.299600861 | 22 |
| SIFT_Enhanced | A01 | 134.926782549 | 9 |
| Full_ProbabilityMap | A02 | 11.235663643 | 10 |
| Without_ProbabilityMap_SIFT | A02 | 54.077926881 | 34 |
| SIFT_Enhanced | A02 | 57.350780877 | 9 |
| Full_ProbabilityMap | A03 | 7.823944116 | 17 |
| Without_ProbabilityMap_SIFT | A03 | 21.600350266 | 32 |
| SIFT_Enhanced | A03 | 20.230001993 | 9 |

- The new bootstrap reporting diagnostic ran on the actual saved 402-row ablation file with 1,000 draws per group, exposing point/mean/CI separately. Outputs agree with the direct audit replay.
- The external trainer launcher successfully delegated --help to the real preserved trainer. No fit call ran. This does not validate archived validation roles or grant trainer rights.

## Additional targeted evidence

The checkpoint/model architecture relationship, all 48 weights between full/weights-only files, 600-label archive identity, and every saved split file's content statistics were checked. Validation directory semantics are reversed. On one representative pair, declared-role MSE is 10962.795; a role-reversed diagnostic is 41.221. No source or folder role was changed. Keras 2.8 serialization and published/historical loss-image differences are documented separately.

Two-pair controlled pipelines used A01/P48 without changing production defaults. They show major HOG/inlier sensitivity, smaller rounding effects, and matching similarity refits in these examples. All 134 local FIRE control files contain integral coordinates, so dtype differences do not change this copy. FPE bin-policy comparisons demonstrate the paper/helper conflict; no full Table 1 reconstruction was claimed.

Archive source inventories/CRCs and Python 3.9/3.10 bytecode corroborate 90/30. The missing-RAR-signature volume 2 limits exhaustive archive recovery. Published PDF page8 Fig. 9 was visually compared to local loss images; its source log remains missing.

No training, full FIRE rerun, long GPU experiment, published runtime reproduction, source-rights clearance, commit, remote creation or push occurred. First-round detailed evidence is preserved in the private snapshot; this report supersedes its insufficient validation-semantic assessment.
