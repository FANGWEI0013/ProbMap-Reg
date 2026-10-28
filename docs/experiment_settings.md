# Published statements, implemented settings and evidence boundaries

Created in Round 3 from actual retained source; this file was absent at Round 2 intake. It is not a recovered historical experiment configuration. `configs/published.json` is reporting-only; `configs/reconstruction.json` documents code behavior. Neither is loaded by the runtime. Runtime constants reside in `src/reconstruction/config.py`; CLI options select paths/mode.

| Component | Publication statement | Recovered reconstruction implementation | Historical / unresolved evidence |
|---|---|---|---|
| Input | Green, 480×480 | Bicubic model-input resize; green replicated into 3 channels; float32 /255 | Historical source/checkpoint support replication |
| Pseudo-labels |Gaussian σ=5, vessel-edge constrained|No public generator|Exact source missing; sigma 3 variants remain excluded|
| Training | 600 images, 480/120, 50 epochs, 1e-4, linear | External authorized trainer only; no fit run | Archive validation role conflict; runtime paths/Fig. 9 logs unresolved |
| Map normalization | 8-bit normalized map | cv2 min/max 0..255 then uint8 | Linear output is not a calibrated probability |
| Maxima | Threshold 80 | SciPy maximum_filter size 10; equality maxima mask; strict >80; plateau ties retained | Historical threshold 90; filter details code-derived |
| HOG | 16×16, 128 dimensions | Separate bilinear 480×480 green image; OpenCV 8 orientations, 4×4-pixel cells/blocks/stride; border points dropped | Historical scikit-image differs numerically |
| NN |Nearest neighbor|Euclidean cdist,one-way argmin; duplicate targets possible|No proposed-method ratio filtering|
| Scaling | Detect at 480 then scale | Float32 per-axis factors from image1 shape; no rounding | Historical round/int32; equal-size FIRE assumption |
| RANSAC | 20 px original scale | estimateAffinePartial2D, RANSAC residual 20 | Historical 30; not overwritten |
| Similarity |Similarity/least squares|Uses returned OpenCV refined matrix|Historical explicitly refits retained inliers|
| Direction |Source→target|Image1→image2; control columns x1,y1,x2,y2|Synthetic direction test and actual input checks passed|
| Mosaic | No blending | Alternating 364×364 tiles after warping | Saved only when requested |
| Error |FIRE control-point distance|Mean Euclidean error; unsuccessful processing records inf|Status success denotes completion|
| AUC | Main Overall 0.626 | Inclusive integer thresholds 0..25; trapezoid/25; failed rows retained | Historical 0.625947 Simpson; recent saved point 0.627612 |
| SIFT | Replacement NN and ratio/mutual 0.75 | Original-size grayscale SIFT; strict forward/backward ratio + mutual | Small ablation verified; exact publication run lineage partial |
| Bootstrap | 1,000 resamples, mean and 95% CI | Uniform pair resampling; seed 20260713; percentiles 2.5/97.5 | Legacy center is point; new diagnostic explicitly reports mean |
| FPE | Fixed 32×32 pixels; Table 1 | No public aggregation implementation | Private helper is 32 bins/axis over point extent |
| Runtime | 2.2 s/pair | CPU smoke commands only | Published timing not reproduced |

No scientific source module changed in Round 3. [Detailed audit](code_paper_audit.md) distinguishes VERIFIED/PARTIAL/MISSING/CONFLICT. [Validation](validation.md) separates new checks from published reporting.
