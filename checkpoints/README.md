# Checkpoint policy

Weights are not included or approved for publication. Supply the compatible model externally via `--checkpoint`. The historical bifurcation model is Keras HDF5, input(None,480,480,3), output(None,480,480,1), linear activation, Adam/MSE,31,032,837 parameters. The full model is372,626,944 bytes (about 355.36MiB), with optimizer state. Three discovered copies have identical SHA256:

`0dfc680a326dc4c61f827e1838fb6e75a0547ba8275b27a17b358ca4d3da8df0`

The corresponding HDF5 weights-only file is124,222,112 bytes (about 118.47MiB). Older vessel-segmentation HDF5 files and later PyTorch files are different models. PyTorch containers were hashed and sized but deliberately not unpickled, so filenames alone do not verify architecture. Provider/model ownership, collaborator consent, training-data terms and redistribution rights require explicit approval before any checkpoint release. All binary patterns are ignored.

| Discovered basename (duplicate names retained as separate findings) | Bytes | Static format | SHA256 prefix |
|---|---:|---|---|
| 2024-06-06 19.02.56_Model_heatmap_Unet.h5 | 372626944 | HDF5 Keras full model | 0dfc680a326d… |
| 2024-06-06 19.02.56_Model_heatmap_Unet.h5 | 372626944 | HDF5 Keras full model | 0dfc680a326d… |
| 2023-10-11 13.19.22_Model_VesselSegmentation.h5 | 372613120 | HDF5 Keras full model | cabd0ec31068… |
| 2023-10-11 13.19.22_Model_VesselSegmentation_weights.h5 | 124217504 | HDF5 weights only | 60735e6d9d9a… |
| 2024-06-06 19.02.56_Model_heatmap_Unet.h5 | 372626944 | HDF5 Keras full model | 0dfc680a326d… |
| 2024-06-06 19.02.56_Model_heatmap_Unet_weights.h5 | 124222112 | HDF5 weights only | 0603f234e544… |
| unet_bifurcation_best.pth | 124263242 | PyTorch filename/container; deliberately not unpickled | c8bd3576dfa2… |
| unet_bifurcation_last.pth | 124263242 | PyTorch filename/container; deliberately not unpickled | edfdebb540d9… |
| unet_bifurcation_best.pth | 124263242 | PyTorch filename/container; deliberately not unpickled | d46423e12d30… |
| unet_bifurcation_last.pth | 124263242 | PyTorch filename/container; deliberately not unpickled | c27698150835… |
| unet_bifurcation.pth | 30798705 | PyTorch filename/container; deliberately not unpickled | ffcd49bd1028… |
| unet_bifurcation.pth | 7578090 | PyTorch filename/container; deliberately not unpickled | ec625e0b8693… |
