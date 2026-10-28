import cv2
import numpy as np


def ransac_inliers(matches_yxyx, threshold_px):
    if len(matches_yxyx) < 2:
        raise ValueError("Need at least 2 matches for similarity RANSAC")

    points_1 = matches_yxyx[:, [1, 0]].astype(np.float32)
    points_2 = matches_yxyx[:, [3, 2]].astype(np.float32)
    matrix_2x3, inlier_mask = cv2.estimateAffinePartial2D(
        points_1,
        points_2,
        method=cv2.RANSAC,
        ransacReprojThreshold=threshold_px,
    )
    if matrix_2x3 is None or inlier_mask is None:
        raise ValueError("RANSAC failed to estimate a similarity transform")

    inliers = matches_yxyx[inlier_mask.ravel() == 1]
    if len(inliers) < 2:
        raise ValueError("RANSAC returned fewer than 2 inliers")
    return matrix_2x3, inliers


def affine_2x3_to_homogeneous(matrix_2x3):
    matrix = np.asarray(matrix_2x3, dtype=np.float64)
    if matrix.shape != (2, 3):
        raise ValueError(f"Expected a 2x3 affine matrix, got {matrix.shape}")
    return np.vstack([matrix, np.array([0.0, 0.0, 1.0])])


def warp_image(image_bgr, matrix_2x3, output_shape):
    height, width = output_shape[:2]
    return cv2.warpAffine(image_bgr, matrix_2x3, (width, height))
