import cv2
import numpy as np
from scipy.ndimage import maximum_filter

from config import (
    CNN_INPUT_SIZE,
    HOG_CELLS_PER_BLOCK,
HOG_DESCRIPTOR_DIM,
    HOG_ORIENTATIONS,
    HOG_PATCH_SIZE,
    HOG_PIXELS_PER_CELL,
    LOCAL_MAX_FILTER_SIZE,
)


_HOG_DESCRIPTOR = cv2.HOGDescriptor(
    _winSize=(HOG_PATCH_SIZE, HOG_PATCH_SIZE),
    _blockSize=HOG_PIXELS_PER_CELL,
    _blockStride=HOG_PIXELS_PER_CELL,
    _cellSize=HOG_PIXELS_PER_CELL,
    _nbins=HOG_ORIENTATIONS,
)


def normalize_probability_map(probability_map):
    image_float = probability_map.astype(np.float32)
    normalized = cv2.normalize(image_float, None, 0, 255, cv2.NORM_MINMAX)
    return normalized.astype(np.uint8)


def detect_local_maxima(image_uint8, threshold, size=LOCAL_MAX_FILTER_SIZE):
    max_filtered = maximum_filter(image_uint8, size=size)
    local_max = image_uint8 == max_filtered
    threshold_mask = image_uint8 > threshold
    combined = local_max & threshold_mask
    coordinates = np.argwhere(combined)
    return coordinates.astype(np.int32)


def green_channel_resized(image_bgr):
    image_resized = cv2.resize(
        src=image_bgr,
        dsize=(CNN_INPUT_SIZE, CNN_INPUT_SIZE),
        interpolation=cv2.INTER_LINEAR,
    )
    return image_resized[:, :, 1]


def valid_patch_points(points, image_shape, patch_size=HOG_PATCH_SIZE):
    half = patch_size // 2
    height, width = image_shape[:2]
    valid = []
    for y, x in points:
        if y - half >= 0 and y + half <= height and x - half >= 0 and x + half <= width:
            valid.append((int(y), int(x)))
    return np.asarray(valid, dtype=np.int32)


def compute_hog_descriptors(image_gray, feature_points):
    feature_points = valid_patch_points(feature_points, image_gray.shape)
    descriptors = []
    half = HOG_PATCH_SIZE // 2
    for y, x in feature_points:
        patch = image_gray[y - half : y + half, x - half : x + half]
        descriptor = _HOG_DESCRIPTOR.compute(patch).reshape(-1)
        descriptors.append(descriptor)
    if not descriptors:
        return feature_points, np.empty((0, HOG_DESCRIPTOR_DIM), dtype=np.float32)
    descriptors = np.asarray(descriptors, dtype=np.float32)
    if descriptors.shape[1] != HOG_DESCRIPTOR_DIM:
        raise ValueError(f"Unexpected HOG descriptor dimension: {descriptors.shape[1]}")
    return feature_points, descriptors


def extract_features(probability_map, image_bgr, threshold):
    heatmap_uint8 = normalize_probability_map(probability_map)
    points = detect_local_maxima(heatmap_uint8, threshold)
    green = green_channel_resized(image_bgr)
    points, descriptors = compute_hog_descriptors(green, points)
    return points, descriptors, heatmap_uint8
