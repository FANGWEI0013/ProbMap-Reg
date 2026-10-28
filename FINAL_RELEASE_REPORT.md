# ProbMap-Reg finalized local release report — 2026-10-29

**READY FOR INITIAL LOCAL COMMIT.** The author explicitly approved the MIT License on **2026-10-29**, with **Copyright (c) 2026 Wei Fang**. Source authorship, including the eleven reconstruction modules, is author-confirmed. No technical/license blocker remains for this documented release scope. The commit itself requires separate authorization and has not been created.

## Candidate and supported scope

The original **64-file, 266,029-byte** Round 3 candidate matched every recorded checksum before editing. A separate pre-edit snapshot was preserved outside Git. No unexpected user modifications were found. The current candidate adds only LICENSE, this report and two final-validation documents to that Round 3 inventory. The 2026-10-28 68-file candidate was snapshotted before this license-status update. No original project, dataset or checkpoint was modified or deleted. No quarantined source was restored.

This is a **recovered working research implementation**, not complete reproduction of the original training process or all published results. Supported workflows: compatible full-model inference and features; Proposed pair registration with optional mosaics; Proposed/SIFT comparisons; saved-error FIRE evaluation; separate bootstrap statistics and plotting. External datasets and a compatible full Keras HDF5 checkpoint are required for image processing. Saved-error analysis needs only prior CSV results. Training remains an external-trainer launcher with unverified original data roles/paths.

## Final functional checks

- **12/12 automated tests passed again on 2026-10-29 in the actual Desktop candidate**. AST syntax validation covered **20 Python files**; configuration JSON parsed successfully. All twenty Python files and LICENSE retain their prior bytes.
- **2026-10-28 functional checks: 14 recorded commands passed**: tests; six CLI helps; two original engine helps; pip check; dependencies/all eleven module imports; one inference; one registration; saved-error evaluation.
- A01_1 inference: **44 features**. A01 registration: **4.657976795045209 pixels** mean control-point error, **22 inliers**, with **44/53** source/target features.
- All eleven scientific source files and `configs/published.json` have the original Round 3 hashes. No numerical algorithm, matching/HOG library, threshold, coordinate rounding, model graph, optimizer or bootstrap sampling changed.
- Tests used Python 3.9.25, TensorFlow 2.10.1, Keras 2.10.0, NumPy 1.23.5, SciPy 1.10.1, Matplotlib 3.7.5 and cv2 4.8.1 on Windows 11 Home build 26200, CPU. `pip check` reported no broken requirements.
- The actual OpenCV provider is **opencv-contrib-python 4.8.1.78**. Requirements retain the minimal **opencv-python 4.8.1.78** wheel; its exact distribution was not separately installed/tested. An initial metadata lookup failure was resolved by identifying the actual provider, without installing or changing packages. Other pinned distribution/version checks passed. Full fresh installation remains unverified.

Exact sanitized argv, versions and outcomes: [final validation](docs/final_validation.json) / [readable report](docs/final_validation.md). Minimal inputs were available and used externally; generated maps, arrays and raw errors remain private. No training, full 134-pair rerun, driver change or expensive experiment was performed.

## README status

Polished and cross-checked against actual interfaces: research overview, publication/DOI/authors, installation, external model, dataset layout, inference and registration, SIFT/evaluation/statistics commands, scientific limits and citation. Published results and limited local metrics are in separate sections. Original training/data generation is explicitly not a verified one-command workflow. Source-authorship language is current; README accurately states author-approved MIT licensing and links the unchanged LICENSE.

## Scientific limitations and reporting integrity

Published main AUC **S/P/A/Overall = 0.902/0.198/0.720/0.626** remains separate from the reported Proposed bootstrap mean **0.628**, CI **[0.567, 0.687]**, with **1,000** resamples. All published ablation category/mean/CI values remain in README and unchanged reporting metadata. No output was forced to match them. The single 2026-10-28 A01 check is not full FIRE reproduction and does not validate the published **2.2 seconds/pair** runtime.

Still unresolved: exact sigma 5/vessel-edge pseudo-label generator; complete FPE Table 1 aggregation and fixed-pixel versus 32-bin policy; original executed validation roles/paths, split seed and numerical loss logs; historical **90/30** versus reported **80/20** source lineage; HOG/scaling/geometry/result-version differences; S rounding; original publication bootstrap-mean computation. The legacy bootstrap center is point AUC; the separate diagnostic reports the actual mean. These limitations remain visible rather than being silently repaired.

## Authorship, MIT and third-party scope

Author confirmation resolves the previous project-source authorship blocker. Only a scoped contrary-evidence check was performed: retained Python files showed no third-party notices, copied/adapted-source markers or embedded download URLs. Extensive provenance recovery was not repeated. No third-party library tree is vendored. Independently licensed dependencies and excluded materials keep their own rights; the approved MIT text does not relicense them.

`LICENSE` contains unchanged standard MIT text, **Copyright (c) 2026 Wei Fang**, explicitly approved on **2026-10-29**. Approval is recorded consistently in README, current reports and manifests. LICENSE is included in the complete staged allowlist. Dataset/checkpoint publication is not proposed.

## Publication safety and Git preparation

All 68 approved publication files, including the staged LICENSE, were scanned. No credential/private-key/token, private-path/host, patient-identifier, binary/notebook, dataset/model or >10 MB finding was detected. Checkpoint graph metadata contains configuration, not learned weights. Pattern scanning is limited evidence, not an exhaustive guarantee. Windows CRLF bytes were preserved; the whitespace check explicitly recognizes CR at line endings while still checking actual trailing whitespace, final blank lines and space-before-tab errors.

Branch **release-review**; **68 files staged as additions**, **zero commits/remotes**, **zero unstaged changes** and **zero untracked files**. All approved paths, including LICENSE, are in the index; every staged blob equals the reviewed file bytes. SHA-256/size checks, positive index equality and CRLF-aware cached whitespace checks passed. No datasets, model/checkpoint binaries, credentials or private research files are staged. No commit was created, nothing was pushed and visibility was not changed.

## Exact Git commands for later publication

Explicit staging and validation have been completed. The **commit/branch/remote/push commands below were not executed**. MIT approval is complete; creating the commit requires separate authorization, as do remote/publication actions. Run from the repository root only when authorized. GitHub CLI is not required.

```powershell
# If restaging is needed, use exactly the approved publication list, including LICENSE.
$approved = (Get-Content docs/publication_files.json -Raw | ConvertFrom-Json).files
foreach ($file in $approved) {
    git -c core.autocrlf=false add -- $file
    if ($LASTEXITCODE -ne 0) { throw "Staging failed: $file" }
}
git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --cached --check
git diff --cached --stat
git status --short
git var GIT_AUTHOR_IDENT
git commit -m "Initial release of recovered ProbMap-Reg research implementation"
git branch -m main

# Only after approval and creation of the empty public GitHub repository:
git remote add origin https://github.com/FANGWEI0013/ProbMap-Reg.git
git push -u origin main
git ls-remote --heads origin main
```

If Git author identity is not configured, configure the intended author identity locally before committing; do not use invented contact details. Use normal GitHub/browser credential-manager authentication when publishing, never paste tokens/passwords into chat. The target URL is future intent, not evidence that this task created a repository. No remote/visibility operation was performed.

## Exact publication inventory

`docs/publication_files.json` is the positive approved file list; `stage_files` equals that full list, including LICENSE. `docs/publication_manifest.json` records SHA-256/size for every proposed file except its own self-hash. The manifest itself remains in the file list. Full tree: [publication manifest](docs/publication_manifest.md). Checksums are integrity evidence, not signatures.

Approved files: **68**; Python source files: **20**; total content: **294,733 bytes**. Index: **68 additions**, including LICENSE; unstaged/untracked files: **0**. Tests: **12 passed on 2026-10-29**. Remaining technical/license blockers: **none for this documented scope**; commit authorization is still required.
