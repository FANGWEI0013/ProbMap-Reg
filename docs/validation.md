# Round 3 execution validation — 2026-10-19

The original nine tests passed, followed by the expanded **12-test suite**. All 24 recorded top-level command exit codes matched expectations, including the missing-checkpoint negative test (expected exit 2). The exact sanitized argv and return codes are in [round3_commands.json](round3_commands.json); full local logs remain private. Previous results are preserved as [round2_validation.md](round2_validation.md) / [JSON](round2_validation.json).

## Environment and checks actually executed

Windows 11 Home 25H2 build 26200.9711, CPU; Python 3.9.25, TensorFlow 2.10.1, Keras 2.10.0, OpenCV 4.8.1, NumPy 1.23.5, SciPy 1.10.1, Matplotlib 3.7.5. No usable TensorFlow GPU was detected. Existing compatible environment plus workspace overlay was used. `pip check` found no broken requirements. Isolated venv creation succeeded. `pip install --help` verified the requirements interface; a full fresh dependency installation was **not performed**.

- AST syntax parsing: 20 Python files. All 11 reconstruction modules imported; their SHA-256 hashes match Round 2. Configuration JSON was parsed.
- Six retained scripts' `--help`, plus Proposed and ablation engines' help, succeeded. External trainer help delegation succeeded; no fit was called.
- Inference on A01_1: 44 feature points; response/map/coordinate/descriptor files generated.
- Proposed A01 with visualization, A01–A03 small mode with visualization, P48 without visualization, and three-method A01–A03 ablation all executed successfully.
- Saved-error evaluation, recovered bootstrap, separate point/mean/CI wrapper and success-curve PNG generation succeeded.
- Actual missing-image processing produced a failed row with infinite error. Tests verify failed-pair denominators, source→target geometry, threshold boundaries and separate bootstrap estimands. `status=success` means the algorithm completed, not a successful low-error registration.
- Three new tests cover checkpoint/dataset preflight, parser/prerequisite reporting, and evaluation failure retention/input-file protection. Initial restricted temporary-directory permissions failed; directing TEMP/TMP to a writable audit directory resolved this environmental issue.

## Limited real-input results

| Pair | Proposed mean error (pixels) | RANSAC inliers |
|---|---:|---:|
| A01 | 4.657976795 | 22 |
| A02 | 11.235663643 | 10 |
| A03 | 7.823944116 | 17 |
| P48 | 1148.223381091 | 9 |

| Pair | SIFT + NN error (pixels) | SIFT ratio/mutual error (pixels) |
|---|---:|---:|
| A01 | 68.299600861 | 134.926782549 |
| A02 | 54.077926881 | 57.350780877 |
| A03 | 21.600350266 | 20.230001993 |

These match the limited Round 2 outputs. Aggregate values are in [round3_results.json](round3_results.json). Generated images, response arrays, raw benchmark files and input data remain outside the publication allowlist. Sequential Proposed runs overwrite the same raw/summary output paths; private command logs preserve the small run, and the last raw Proposed file is P48. Use separate output roots to preserve runs.

## Not executed / not established

No 50-epoch training, full 134-pair FIRE rerun, CUDA installation, dataset/checkpoint publication, commit, remote creation or push. Optional `failure` comparison mode was source/import reviewed, not smoke-tested in Round 3. Exact label generation and FPE aggregation remain missing. Neither full published AUC nor reported bootstrap mean 0.628 nor runtime 2.2 seconds/pair was independently reproduced. Full fresh installation is unverified. Metadata in published.json is reporting information, never runtime score targets.

## Final Desktop checkout verification

After applying reviewed changes, `python -B -m unittest discover -s tests -v` passed all 12 tests again in the final Desktop candidate. The 64 Git untracked files exactly matched the positive allowlist; all publication checksums and mirror bytes matched. Branch release-review has zero commits, tracked/staged files or remotes.
