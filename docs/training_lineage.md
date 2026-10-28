# Training lineage and semantic input conflict

The checkpoint `2024-06-06 19.02.56_Model_heatmap_Unet.h5` is a full Keras HDF5 model. It was serialized with Keras 2.8.0, not the currently tested Keras 2.10.0 runtime. Serialization metadata alone does not identify the TensorFlow version or actual training environment.

The recovered `model.txt` matches its 39 layers, 31,032,837 parameters, initializers and inbound topology. It defines Adam at 1e-4, MSE and a linear output. `main.txt` loads image/target directories, uses batch size 1 and 50 epochs, divides images by 255 but leaves float32 target values on their stored scale. Saved Adam iteration count is 24,000, consistent with 50×480 batches. All 48 model-weight arrays equal those in the accompanying weights-only file; duplicate full-model files have the same hash. This strongly associates the checkpoint with the recovered TensorFlow architecture/training family, but cannot prove exact seed, paths or labels used in its training.

All 480 training targets are RGB with equal channels, sparse heatmaps; each hashes identically to its D:FIVES counterpart and has matching CRC/size evidence in the Desktop archive. All 120 archived validation heatmaps also match archive CRCs. The first-round conclusion about numerical loader shape was correct, but semantic validation was incomplete.

Actual folder contents are:

| Saved folder name | Count | Actual content | Nonzero-pixel fraction |
|---|---:|---|---|
| (1) Training_set_green_channel_preprocessed | 480 | Fundus grayscale input | 1.0 for all files |
| (2) Training_labels | 480 | Sparse bifurcation heatmaps | 0.000699–0.014245 |
| (3) Validation_set_green_channel_preprocessed | 120 | Sparse heatmaps, including empty maps | 0–0.013312 |
| (4) Validation_labels | 120 | Fundus grayscale images | 1.0 for all files |

Image inspection confirms the reversed validation semantics. On one representative pair, using declared roles gives checkpoint MSE 10962.795; a role-reversed diagnostic gives MSE 41.221. This comparison was not applied to training code or files. The original text source refers to different old directories (`6_validation_image_green_channel`, `4_validation_label`), so archived folder naming cannot prove that the actual training run used wrong roles.

The dated historical loss figure ends near training loss 18 and validation loss 67. Published PDF page 8, Fig. 9 has a different low-loss convergent curve, and the newer PyTorch loss image is also not an exact visual match. No underlying numerical loss log or exact published-figure generator was found. Do not tie the published figure to this checkpoint solely because both use 50 epochs. No new loss curve was generated from invented numbers.

A resized heatmap peak's width cannot establish source sigma 5: resizing, clipping, neighboring peaks and vessel constraints can all change its profile. Observed narrow peaks are diagnostic only. The missing label-generation source remains MISSING.

Original trainer/model sources remain in external archival storage, outside this minimized release. Author confirmation resolves project-source authorship; original executed data roles and paths remain scientifically unresolved. Main `scripts/train_unet.py` is a small external-trainer launcher; it implements no new training algorithm. Before any fit run, establish the actual input/heatmap roles, authorized architecture source and exact split manifest. No training was performed during this round.
