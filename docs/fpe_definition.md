# FPE bin definition and missing Table 1 pipeline

The paper describes fixed 32×32-pixel bins. The recovered helper uses:

```python
H, xedges, yedges = np.histogram2d(points[:, 0], points[:, 1], bins=[32, 32])
```

With no explicit edges or range, this creates 32 bins per axis across the coordinate extent of the points, not bins whose sides are 32 pixels. A full 480-pixel image would have about 15 fixed 32-pixel bins per axis; a 2912-pixel FIRE image about 91. Automatic point extent changes boundaries between images even with the same image geometry. The helper then computes Shannon entropy in bits from point counts.

For P48's 42 reconstructed feature points, diagnostic entropies are:

| Policy | FPE |
|---|---:|
| Historical helper: 32 bins per axis, point extent | 5.249460 |
| Fixed 32-pixel bins at 480 feature scale | 4.993392 |
| Fixed 32-pixel bins at original 2912 scale | 5.392317 |

These policies are compared to demonstrate the distinction, not selected to match Table 1. No complete ORB/SIFT/SBP-FIR/UF-FIR/proposed per-image extraction/aggregation script or underlying numerical table was recovered. Published means remain ORB 241 / 5.681, SIFT 164 / 5.960, SBP-FIR 125 / 6.424, UF-FIR 222 / 7.014, Proposed 54 / 5.579. A single-image diagnostic is not their reproduction.

The original helper and prior-method implementations are retained in external quarantine. No substituted Table 1 implementation is advertised in the public candidate.
