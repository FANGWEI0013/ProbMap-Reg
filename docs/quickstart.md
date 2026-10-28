# Quickstart: recovered reconstruction implementation

**2026-10-28 release check:** all six CLI helps and engine helps were rechecked; inference and A01 registration passed. See [current validation](final_validation.md). Previously executed commands below retain their Round 3 date/scope.

Validated 2026-10-19 on **Windows 11 Home 25H2, build 26200.9711**, CPU, Python **3.9.25**, TensorFlow **2.10.1**, Keras **2.10.0**, OpenCV **4.8.1**, NumPy **1.23.5**, SciPy **1.10.1** and Matplotlib **3.7.5**. Commands run from the repository root. Other platforms/Python versions have not been validated.

Status meanings below: **EXECUTED SUCCESSFULLY** = same script/flags executed with real external local inputs and audit output paths; **SYNTAX/HELP VERIFIED ONLY** = interface checked but operation not performed; **NOT EXECUTABLE IN THIS CANDIDATE** = a necessary implementation or approved input is missing. Local path substitutions are recorded in the sanitized [execution log](round3_commands.json); no personal paths are published.

## 1. Select Python and prepare an environment

Choose a real 64-bit Python 3.9.25 executable; do not assume the system `python` or `py -3.9` points to it. The quoted paths below are placeholders to replace.

```powershell
$Py39 = "path\to\Python39\python.exe"
& $Py39 --version
& $Py39 -m venv .venv
$Py = ".\.venv\Scripts\python.exe"
& $Py -m pip install -r requirements.txt
```

Python version and isolated venv creation: **EXECUTED SUCCESSFULLY**, using an external probe environment; its pip was also checked. Full requirements installation: **SYNTAX/HELP VERIFIED ONLY** (`pip install --help` confirms `-r`); no complete fresh dependency installation was performed. Actual inference tests used a pre-existing compatible environment plus a workspace-only overlay. `requirements.txt` is a minimal retained-core specification, not a demonstrated clean-install lockfile. No PyTorch, archived HOG implementation or training-source dependencies are required by this public core. The tested OpenCV provider is `opencv-contrib-python==4.8.1.78` (cv2 4.8.1); requirements retain the minimal standard wheel `opencv-python==4.8.1.78`, which was not separately installed/tested. Install one variant, not both.

TensorFlow 2.10 is the last release with native-Windows GPU support according to the [official installation guide](https://www.tensorflow.org/install/pip#windows-native). The audit detected no usable TensorFlow GPU and ran CPU. It did not install CUDA/cuDNN/drivers or change system Python. The guide's current latest-version instructions must not be substituted for this pinned environment.

## 2. Supply external data and a model

```text
data/FIRE/
  Images/A01_1.jpg
  Images/A01_2.jpg
  Images/A02_1.jpg, A02_2.jpg, A03_1.jpg, A03_2.jpg, ...
  Ground Truth/control_points_A01_1_2.txt
  Ground Truth/control_points_A02_1_2.txt
  Ground Truth/control_points_A03_1_2.txt
  ...
checkpoints/2024-06-06 19.02.56_Model_heatmap_Unet.h5
```

The repository does not supply these files. Obtain FIRE/FIVES from their providers; provide an authorized, compatible Keras model yourself. [Data preparation](data_preparation.md) distinguishes provider vessel masks from bifurcation targets. Checkpoint shape must be `(None,480,480,3)` → `(None,480,480,1)`. Weights/checkpoints remain excluded.

```powershell
$FireRoot = "data/FIRE"
$Checkpoint = "checkpoints/2024-06-06 19.02.56_Model_heatmap_Unet.h5"
$Out = "results/smoke"
```

Path preflight and actual filename loading were **EXECUTED SUCCESSFULLY** against the available external FIRE copy. CLI options configure paths; do not edit scientific constants to select a local folder. `PROBMAP_FIRE_ROOT`, `PROBMAP_CHECKPOINT` and `PROBMAP_OUTPUT_DIR` are the corresponding environment overrides used by the config. `configs/*.json` are documentary metadata, not CLI input files; no `--config` flag exists.

Each proposed run rewrites its `proposed/raw_pairs.csv` and `summary.csv`. Use a distinct `$Out` per run when preserving earlier outputs. Audit command logs retain all executed runs; the last proposed CSV below contains P48.

## 3. Inspect supported options

```powershell
& $Py scripts/run_reconstruction.py --help
& $Py scripts/infer.py --help
& $Py scripts/evaluate_fire.py --help
& $Py scripts/bootstrap_statistics.py --help
& $Py scripts/plot_success_curves.py --help
```

All five commands: **EXECUTED SUCCESSFULLY**. The recovered Proposed and ablation engines' own `--help` were checked too. Proposed supports `--pair`; ablation supports `--small-test` / `--full-run` and **does not support `--pair`**. `--save-vis` is only a reserved interface option in ablation; it does not generate ablation mosaics.

## 4. Infer one image and extract descriptors

```powershell
& $Py scripts/infer.py --image "$FireRoot/Images/A01_1.jpg" --checkpoint $Checkpoint --output-dir "$Out/inference_A01"
```

**EXECUTED SUCCESSFULLY**: 44 retained features in this local test. Outputs: `probability.npy`, `probability_uint8.png`, `points_yx.csv`, `hog_descriptors.npy`. Features are at 480-scale, row/column `(y,x)`; descriptor rows correspond to point rows. These are ignored generated artifacts, not publication inputs.

## 5. Register one FIRE pair

```powershell
& $Py scripts/run_reconstruction.py proposed --checkpoint $Checkpoint --fire-root $FireRoot --output-dir $Out --pair A01 --save-vis
```

**EXECUTED SUCCESSFULLY**: A01 mean control-point error 4.657976795 pixels. Image1 is transformed into image2. Outputs: `$Out/proposed/raw_pairs.csv`, `summary.csv`, and `vis/A01/` with maps, matches, warped image and tiled mosaic. `status=success` means computation completed, not necessarily error≤25 pixels.

## 6. Small FIRE test and P48

```powershell
& $Py scripts/run_reconstruction.py proposed --checkpoint $Checkpoint --fire-root $FireRoot --output-dir $Out --small-test --save-vis
& $Py scripts/run_reconstruction.py proposed --checkpoint $Checkpoint --fire-root $FireRoot --output-dir $Out --pair P48 --no-vis
```

Both: **EXECUTED SUCCESSFULLY**. Small mode selects A01–A03; P48 returned 1148.223381091 pixels with 9 inliers. These limited tests do not establish full FIRE AUC. `--full-run` was help-verified only and was not executed. A full 134-pair experiment needs deliberate approval in this project.

## 7. Proposed/SIFT ablation

```powershell
& $Py scripts/run_reconstruction.py ablation --checkpoint $Checkpoint --fire-root $FireRoot --output-dir $Out --small-test --no-vis
```

**EXECUTED SUCCESSFULLY**: three methods × A01–A03 = 9 rows. This command includes Proposed and both SIFT baselines, so it requires the U-Net checkpoint even though SIFT itself does not. Outputs under `$Out/ablation_probmap_vs_sift/`: `raw_pairs.csv`, `summary.csv`, `ablation_table.csv`, `ablation_table_latex.txt`. The ratio/mutual baseline uses strict ratio 0.75 in both directions plus mutual checking.

## 8. Evaluate saved errors without running registration

```powershell
& $Py scripts/evaluate_fire.py --raw-csv "$Out/ablation_probmap_vs_sift/raw_pairs.csv" --output "$Out/evaluation.csv"
```

**EXECUTED SUCCESSFULLY**. This packaging wrapper calls the unchanged recovered `summarize_rows` evaluator. It groups experiment/category/ALL, retains failed/nonfinite errors in denominators and records pair counts. Required columns are `experiment,category,error,status,runtime`. It refuses to overwrite its own input. It needs no images/checkpoint once valid raw errors exist; a three-pair summary is still a three-pair summary.

## 9. Bootstrap point/mean/CI and plot curves

```powershell
& $Py scripts/run_reconstruction.py bootstrap --output-dir $Out
& $Py scripts/bootstrap_statistics.py --raw-csv "$Out/ablation_probmap_vs_sift/raw_pairs.csv" --output "$Out/bootstrap_statistics.csv"
& $Py scripts/plot_success_curves.py --raw-csv "$Out/ablation_probmap_vs_sift/raw_pairs.csv" --output "$Out/success_curves.png"
```

All: **EXECUTED SUCCESSFULLY**. Legacy bootstrap reads the previous ablation raw file and writes `auc_confidence_intervals.csv` / `ablation_table_with_ci.csv`; its `auc` center is the original-sample **point estimate**. The separate diagnostic outputs explicitly named point AUC, bootstrap mean and percentile CI, with 1,000 resamples/default seed 20260713. The small-test bootstrap is not the published full-FIRE analysis. Plotting does not run registration. See [bootstrap estimands](bootstrap_estimands.md).

## 10. Run tests

```powershell
& $Py -B -m unittest discover -s tests -v
```

**EXECUTED SUCCESSFULLY**: original 9 tests plus 3 CLI/evaluation packaging tests, 12 total. No test asserts the paper's AUC as a runtime target. On this app's restricted temporary filesystem the new tests initially encountered permission errors; rerunning with `TEMP` and `TMP` directed to a writable audit temporary folder passed. A normal local Python environment can use its standard writable temporary folder.

## Workflows intentionally not advertised as reproduced

- Exact FIVES σ=5/vessel-edge generator and full FPE Table 1: **NOT EXECUTABLE IN THIS CANDIDATE**, required source missing/quarantined. There is no `evaluate_fpe.py` in the public tree.
- `scripts/train_unet.py --help`: **EXECUTED SUCCESSFULLY**, and external trainer `--help` delegation checked; fit **not run**. Original executed data roles and training paths remain unresolved; project-source authorship is now author-confirmed. See [training lineage](training_lineage.md).
- `failure` visualization mode: source/import reviewed, **not smoke-tested in Round 3**; it needs suitable prior Category P rows for the methods it compares. Small ablation contains only A pairs. Do not substitute a full experiment merely to satisfy this optional visualization.
- Fresh full requirements install, full benchmark, published runtime, 50-epoch training: **not executed**.

## Troubleshooting

| Message / symptom | Meaning and action |
|---|---|
| `Provide an existing --checkpoint` | Supply a real model file; placeholders are not models. |
| `Provide FIRE root with Images and Ground Truth` | Point at the parent containing both exact folder names. |
| `Could not read image` / failed row with `inf` | Check the expected pair filenames and local read access; keep the failed row in evaluation. |
| `Run ablation first` | Bootstrap requires raw errors at the documented path under the same output root. |
| `unrecognized arguments: --pair` in ablation | Use its actual `--small-test` interface; no ablation single-pair flag exists. |
| `Unexpected model input/output shape` | The supplied model does not match the recovered 480×480 graph. Do not alter architecture to hide it. |
| CUDA/cuDNN warnings / zero GPUs | This audit used CPU; GPU setup is separate. No driver changes are part of this package. |
| Missing TensorFlow/OpenCV or unsupported Python wheel | Select the documented Python 3.9 environment and inspect pinned requirements; clean installation is unverified. |
| Permission error in temporary files | Use a writable temporary directory for your test process. |
| Missing label/FPE scripts | These are documented missing parts of the original study, not an installation error. |
