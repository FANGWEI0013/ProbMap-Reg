# Two-pair controlled version diagnostics

The recovered source files were not edited. One checkpoint and each pair's same predicted maps were used to vary explicit diagnostic settings. These profiles are not discovered historical versions, and their numbers are not new published results. Only A01 and P48 were examined.

| Pair | Profile | Inliers | Error (pixels) |
|---|---|---:|---:|
| A01 | historical_native | 21 | 2.924529025 |
| A01 | historical_80_20_diagnostic | 21 | 2.924529025 |
| A01 | reconstruction_native | 22 | 4.657976795 |
| A01 | reconstruction_90_30_diagnostic | 22 | 4.657976795 |
| A01 | reconstruction_skimage_only_diagnostic | 21 | 3.015169651 |
| A01 | reconstruction_rounding_only_diagnostic | 22 | 4.523338056 |
| A01 | reconstruction_refit_only_diagnostic | 22 | 4.657976795 |
| P48 | historical_native | 8 | 28.613489178 |
| P48 | historical_80_20_diagnostic | 8 | 24.468413741 |
| P48 | reconstruction_native | 9 | 1148.223381091 |
| P48 | reconstruction_90_30_diagnostic | 11 | 17.471144076 |
| P48 | reconstruction_skimage_only_diagnostic | 8 | 24.507109942 |
| P48 | reconstruction_rounding_only_diagnostic | 9 | 1148.367370021 |
| P48 | reconstruction_refit_only_diagnostic | 9 | 1148.223381091 |

Historical native is scikit-image HOG, threshold 90, RANSAC 30, rounded original coordinates and least-squares refit. Reconstruction native is OpenCV HOG, threshold 80, RANSAC 20, float coordinates and the OpenCV returned transform. HOG-only, rounding-only and refit-only profiles vary those individual reconstruction components.

A01's native error difference persists after threshold/RANSAC substitution. P48 is highly sensitive to HOG and correspondence/inlier changes: HOG-only gives about 24.507 pixels rather than 1148.223. Rounding-only changes P48 by about 0.144 pixels. Refit-only agrees with native reconstruction to floating-point precision on both pairs. All local FIRE control coordinates are integers, resolving the integer/float-reader difference for this input copy.

These observations identify causes in the tested examples but do not justify selecting a new algorithm or claim a full AUC change. Historical parameters and reconstructed scientific code remain unchanged.
