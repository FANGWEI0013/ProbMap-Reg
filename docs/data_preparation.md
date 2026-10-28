# Data preparation and local inputs

FIVES and FIRE serve different roles. Provider references were checked against primary provider/data-descriptor sources on 2026-10-19; direct page fetch may depend on network availability. No dataset was downloaded or copied into the candidate. Paper results remain referenced to the local IEEE PDF, not web tables.

## FIVES: vessel masks and reported model training

Obtain FIVES from the [authors' Figshare deposit](https://doi.org/10.6084/m9.figshare.19688169.v1); the [authors' data descriptor](https://www.nature.com/articles/s41597-022-01564-3) describes `train/Original`, `train/Ground Truth`, corresponding PNG names and the provider split. Provider vessel segmentation masks are not the bifurcation heatmaps used as model targets.

```text
data/FIVES/
  train/Original/*.png
  train/Ground Truth/*.png
  test/Original/*.png
  test/Ground Truth/*.png
```

This is provider organization, not an implemented public training loader. The paper's experiment reports 600 images split 480/120; its exact sigma 5/vessel-edge label generator, split seed and original runtime paths are not recovered. Historical loaders expect matching sorted lowercase `.png` names, replicated grayscale/RGB input at 480×480 divided by 255 and raw float32 heatmap targets without division by 255. Those historical sources remain outside this minimized release; their original executed data roles remain unresolved.

All saved validation-input files were found to contain sparse heatmaps and all saved validation-target files fundus images, opposite their folder names. Do not automatically swap paths or use provider vessel masks as a replacement target. [Training lineage](training_lineage.md) preserves the uncertainty. No verified public one-command training-data generation procedure is available.

## FIRE: registration evaluation

Obtain FIRE from [FORTH](https://projects.ics.forth.gr/cvrl/fire/), with provider terms/citation. The loader expects:

```text
data/FIRE/
  Images/
    A01_1.jpg
    A01_2.jpg
    P48_1.jpg
    P48_2.jpg
    ...
  Ground Truth/
    control_points_A01_1_2.txt
    control_points_P48_1_2.txt
    ...
```

Each control row contains four whitespace-separated coordinates:

```text
x1 y1 x2 y2
```

This schema is not a literal header to add to the files. Coordinates are original-image-scale correspondences; image1 is the source mapped into image2. The retained reader parses four numeric columns and reports an error if no valid rows exist. The available FIRE copy has integral control values; float/int reader differences therefore did not change it.

Small mode expects A01/A02/A03 files in both images and controls. Full enumeration is S71/P49/A14, 134 pairs; no full Round 3 run was performed. Provider counts of unique captures and pair-named implementation files are different: the tested copy has 268 expected image filenames and 134 control files. Equal-size 2912×2912 FIRE images are the verified use case; coordinate scaling applies image1's dimensions to both endpoints.

The current ablation command includes Proposed and both SIFT baselines and requires a checkpoint. Saved-error evaluation/bootstrap/plotting require only prior valid CSV output. Missing images/controls produce failed rows; do not drop them to improve AUC.

## Checkpoint and path configuration

Supply an authorized compatible model externally, conventionally `checkpoints/2024-06-06 19.02.56_Model_heatmap_Unet.h5`. CLI `--checkpoint`, `--fire-root` and `--output-dir` select local locations. Source config also reads `PROBMAP_CHECKPOINT`, `PROBMAP_FIRE_ROOT`, `PROBMAP_OUTPUT_DIR`. Documentary JSON does not change runtime constants.

Dataset directories, images, masks, controls, derived binaries and weights remain excluded. Keep generated outputs under ignored `results/`; public audit metadata contains only limited aggregate diagnostics, never redistributed image/label/control contents. See [Quickstart](quickstart.md).
