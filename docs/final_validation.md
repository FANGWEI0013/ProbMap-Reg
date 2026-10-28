# Functional validation and license finalization — 2026-10-29

All **12 automated tests passed again in the actual Desktop candidate on 2026-10-29**. All twenty Python files are byte-identical to the 2026-10-28 tested source. Syntax validation covered **20 Python files**. All **six script helps**, Proposed/ablation engine helps, eleven scientific module imports, JSON configuration parsing and `pip check` succeeded. The **2026-10-28** functional run recorded fourteen successful command invocations; those dated results are retained, not claimed as new inference on 2026-10-29. [Sanitized exact argv and environment](final_validation.json) are recorded; raw local logs remain private.

## Actual minimal end-to-end execution — 2026-10-28

External authorized local inputs were available and used without copying them into the candidate. Inference on A01_1 extracted **44 points**. A01 registration completed with **4.657976795045209 pixels** mean control-point error and **22 RANSAC inliers** (44/53 source/target points). Saved-error evaluation also succeeded. Generated maps, descriptors, raw errors and summaries remain outside the public tree. This one-pair test does not establish full FIRE AUC or published runtime.

## Dependencies

Python 3.9.25; TensorFlow 2.10.1, Keras 2.10.0, NumPy 1.23.5, SciPy 1.10.1, Matplotlib 3.7.5 and cv2 4.8.1. The OpenCV provider is **opencv-contrib-python 4.8.1.78**, not the minimal **opencv-python 4.8.1.78** wheel specified in requirements. All pinned version numbers match the available provider versions, but that exact standard-wheel distribution and a fresh full installation are unverified. An initial exact-distribution lookup failed; inspecting the actual provider resolved the verification issue, without installing packages or changing code. pip check reports no broken requirements. CPU inference was used; no drivers/system Python were modified.

## Scope and integrity

All eleven scientific modules and configs/published.json retain the Round 3 baseline hashes. No training, full FIRE benchmark, bootstrap-seed search, scientific algorithm change or published-value adjustment occurred. SIFT/bootstrap/plot interfaces were help-checked here; their earlier end-to-end checks remain separately dated in Round 3 evidence. Source authorship is author-confirmed. No retained Python file showed a third-party notice or copied/adapted-source marker in the scoped check.

MIT is **APPROVED**, with **Copyright (c) 2026 Wei Fang**, by explicit author approval dated **2026-10-29**. LICENSE text is unchanged. All **68 approved files, including LICENSE**, are staged; file/index paths, raw blob bytes and SHA-256 checksums match the approved manifest. No dataset/weight publication, commit, remote creation, visibility change or push was performed. Separate authorization is still required to create the initial commit.
