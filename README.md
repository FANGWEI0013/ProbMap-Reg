# ProbMap-Reg

Research software for extracting retinal bifurcation features from learned response maps and registering fundus image pairs.

This repository provides a **recovered working research implementation**. It supports model inference, feature extraction, image registration, SIFT baselines and evaluation. It does **not** provide a complete reproduction of the original training process or all published experimental results.

## Publication

**Automatic Extraction of Bifurcation Features from Probability Maps for Robust Fundus Image Registration**

Weiwei Du, Jesús Eduardo Ochoa-Astorga, Wei Fang, Masahiro Miyake, Keina Sado, Xiaozhong Xue. *IEEE Access*, 2026.

DOI: [10.1109/ACCESS.2026.3741071](https://doi.org/10.1109/ACCESS.2026.3741071).

## Overview

The method learns bifurcation responses from pseudo-labels derived from vessel masks, then uses the detected points for fundus registration. FIVES supplies the reported training data; FIRE supplies registration pairs and control-point annotations.

The available implementation is better verified for inference and registration than for training-data generation. It requires externally supplied datasets and a compatible model; neither is distributed here. The retained scientific source is unchanged from the audited Round 3 candidate.

## Method

Fundus image → resized green-channel model input → U-Net response → per-image normalization → local maxima → HOG descriptors → nearest-neighbor matching → RANSAC similarity transform → registration error / optional mosaic.

The recovered pipeline uses 480×480 model input, threshold 80, 16×16-pixel/128-dimensional OpenCV HOG and a 20-pixel RANSAC threshold. It maps image 1 into image 2. Model preprocessing uses bicubic resizing; HOG uses a separate bilinear green-channel resize. Historical source uses 90/30 and a different HOG implementation; these differences remain documented rather than silently reconciled. See [implemented settings](docs/experiment_settings.md) and the [paper/code audit](docs/code_paper_audit.md).

## Repository Structure

```text
configs/                  Published metadata and documented implementation settings
src/reconstruction/       Recovered scientific implementation
scripts/                  Inference, registration, evaluation and statistics CLIs
tests/                    Twelve numerical and CLI tests
docs/                     Quickstart, scientific audit and validation evidence
checkpoints/README.md     External checkpoint requirements
results/README.md         Generated-output policy
FINAL_RELEASE_REPORT.md   Current release checks and publication commands
```

## Installation

The tested environment is **Python 3.9.25**, TensorFlow 2.10.1, Keras 2.10.0, OpenCV 4.8.1, NumPy 1.23.5, SciPy 1.10.1 and Matplotlib 3.7.5 on Windows 11 Home, using CPU. Start with a compatible Python 3.9 interpreter, then run from the repository root:

```powershell
python -m venv .venv
$Py = ".\.venv\Scripts\python.exe"
& $Py -m pip install -r requirements.txt
& $Py -m pip check
```

The complete fresh installation has not been independently tested. Functional checks used an existing compatible environment whose OpenCV provider is `opencv-contrib-python==4.8.1.78`; the minimal requirements specify `opencv-python==4.8.1.78`. Both expose OpenCV 4.8.1, but the standard wheel was not separately installed/tested. Install only one OpenCV wheel variant in a new environment. No PyTorch dependency is required. See [environment details and troubleshooting](docs/quickstart.md).

## Quick Start

After supplying the external inputs described below, set local paths:

```powershell
$FireRoot = "data/FIRE"
$Checkpoint = "checkpoints/model.h5"
$Out = "results/example"

# Infer one response map, feature coordinates and HOG descriptors.
& $Py scripts/infer.py --image "$FireRoot/Images/A01_1.jpg" --checkpoint $Checkpoint --output-dir "$Out/inference"

# Register image 1 to image 2; optionally write visualizations.
& $Py scripts/run_reconstruction.py proposed --checkpoint $Checkpoint --fire-root $FireRoot --output-dir $Out --pair A01 --save-vis

# Run the tests without loading datasets or model weights.
& $Py -B -m unittest discover -s tests -v
```

Inference writes a response array, normalized map, `(y,x)` point CSV and descriptor array. Registration writes `proposed/raw_pairs.csv` and `summary.csv`, with visualizations when requested. Reusing an output root overwrites that run's summaries; use separate roots to preserve experiments. [Full Quickstart and execution status](docs/quickstart.md).

## Datasets

Obtain **FIVES** from its [authors' deposit](https://doi.org/10.6084/m9.figshare.19688169.v1) and **FIRE** from its [provider](https://projects.ics.forth.gr/cvrl/fire/), following their terms and citation requirements. FIVES vessel masks are not substitutes for bifurcation heatmap targets.

For the single-pair example, the FIRE loader expects:

```text
data/FIRE/
  Images/A01_1.jpg
  Images/A01_2.jpg
  Ground Truth/control_points_A01_1_2.txt
```

Each annotation row contains whitespace-separated `x1 y1 x2 y2` coordinates at original image scale, with no header. Small-test mode also needs A02/A03. [Data layouts and training-data limitations](docs/data_preparation.md). No images, masks or control-point files are redistributed.

## Pretrained Model

Provide an authorized **full Keras HDF5 model**, not a weights-only file, with input shape `(None,480,480,3)` and output shape `(None,480,480,1)`. The recovered model has a linear output; inference normalizes its response per image rather than treating it as a calibrated probability.

No checkpoint is bundled or offered for download. Local inference was checked with the recovered compatible checkpoint; its graph agrees with the recovered U-Net source, but the original executed training-data paths and labels are not fully established. [Checkpoint metadata and policy](checkpoints/README.md) · [Training lineage](docs/training_lineage.md).

## Evaluation

The following command runs Proposed and both SIFT baselines on A01–A03. It needs a checkpoint because all three methods are evaluated together:

```powershell
& $Py scripts/run_reconstruction.py ablation --checkpoint $Checkpoint --fire-root $FireRoot --output-dir $Out --small-test --no-vis
$Raw = "$Out/ablation_probmap_vs_sift/raw_pairs.csv"
& $Py scripts/evaluate_fire.py --raw-csv $Raw --output "$Out/evaluation.csv"
& $Py scripts/bootstrap_statistics.py --raw-csv $Raw --output "$Out/bootstrap_statistics.csv"
& $Py scripts/plot_success_curves.py --raw-csv $Raw --output "$Out/success_curves.png"
```

Saved-error evaluation, bootstrap statistics and plotting need no images/checkpoint once the raw CSV exists. Failed/nonfinite errors remain in AUC denominators. A row marked `success` means processing completed, not necessarily a low registration error. The recovered evaluator integrates success rates over inclusive integer thresholds 0–25 pixels with trapezoidal normalization.

The diagnostic bootstrap reports **point AUC**, **bootstrap mean** and **percentile 95% CI** separately, using 1,000 pair resamples and default seed 20260713. The legacy bootstrap remains available and unchanged; its center is a point estimate. See [bootstrap definitions](docs/bootstrap_estimands.md). A small-test summary must not be presented as full FIRE performance.

## Published Results

**Results reported in the published paper. These tables are reporting metadata, not independently reproduced results or runtime targets.**

| Main Proposed AUC | S | P | A | Overall FIRE |
|---|---:|---:|---:|---:|
| Published | 0.902 | 0.198 | 0.720 | **0.626** |

| Published ablation | S | P | A | Reported bootstrap mean Overall | 95% CI |
|---|---:|---:|---:|---:|---|
| SIFT + NN | 0.141 | 0.000 | 0.167 | 0.092 | [0.061, 0.125] |
| SIFT + ratio/mutual | 0.333 | 0.002 | 0.174 | 0.195 | [0.149, 0.243] |
| Proposed | 0.902 | 0.198 | 0.720 | **0.628** | [0.567, 0.687] |

The main Overall AUC **0.626** and reported bootstrap mean **0.628** are different published quantities. The original publication script establishing that mean has not been recovered. Published runtime is **2.2 seconds per pair**; this timing has not been reproduced.

### Locally verified smoke-test results

The 2026-10-28 CPU check extracted **44 features** from A01_1 and registered A01 with **4.657976795 pixels** mean control-point error and **22 RANSAC inliers**. Twelve tests, syntax/import checks, CLI helps and dependency checks passed. This single pair does not establish full FIRE AUC or published runtime. Earlier A01–A03/P48 checks remain separately dated in [Round 3 validation](docs/validation.md); [current validation](docs/final_validation.md) records this release check.

## Reproducibility Status

Inference, registration, SIFT comparison and saved-error/statistical workflows are executable with the documented external inputs. This is a recovered working implementation, **not the exact original published pipeline or a complete training/results reproduction**. The scientific source and published result metadata were not changed to obtain agreement.

## Known Limitations

- The exact sigma 5, vessel-edge-constrained pseudo-label generator and complete FPE Table 1 aggregation were not recovered.
- Original validation input/target roles, executed training paths, split seed and numerical loss-figure history remain unresolved. The external trainer launcher is not a verified one-command training workflow.
- Historical 90/30 settings, HOG/scaling/geometry details and saved result versions differ from this reconstruction. The published S rounding and bootstrap-mean source remain uncertain.
- `histogram2d(bins=[32,32])` uses 32 bins per axis; it is not fixed 32×32-pixel binning. No replacement is advertised as the original FPE experiment.
- Full fresh installation, full FIRE rerun, 50-epoch training and the published runtime have not been verified in this release check. Equal-size FIRE images are the tested geometry use case.

See [reproducibility boundaries](docs/reproducibility.md) and the [paper/code audit](docs/code_paper_audit.md).

## Citation

Please cite the corresponding paper when using this research implementation:

```bibtex
@article{Du2026ProbMapReg,
  author = {Du, Weiwei and Ochoa-Astorga, Jesús Eduardo and Fang, Wei and Miyake, Masahiro and Sado, Keina and Xue, Xiaozhong},
  title = {Automatic Extraction of Bifurcation Features from Probability Maps for Robust Fundus Image Registration},
  journal = {IEEE Access},
  year = {2026},
  doi = {10.1109/ACCESS.2026.3741071}
}
```

## Licensing and Third-Party Code

Project source authorship, including the eleven reconstruction modules, is author-confirmed. The author approved release under the **MIT License** on **2026-10-29**, with **Copyright (c) 2026 Wei Fang**. See [LICENSE](LICENSE) for the standard license text.

The MIT License does not relicense external dependencies, independently licensed third-party code, datasets, the paper or checkpoints. No third-party source is vendored in the candidate; prior-method/downloaded stitching materials remain excluded. A scoped source/notice check found no contrary authorship evidence. [Authorship and third-party scope](docs/third_party_provenance.md).
