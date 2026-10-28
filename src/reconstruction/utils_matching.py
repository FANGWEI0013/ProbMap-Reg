import numpy as np
from scipy.spatial.distance import cdist


def nearest_neighbor_matches(points_1, descriptors_1, points_2, descriptors_2):
    if len(points_1) == 0 or len(points_2) == 0:
        return np.empty((0, 4), dtype=np.float32)
    if len(descriptors_1) == 0 or len(descriptors_2) == 0:
        return np.empty((0, 4), dtype=np.float32)

    distances = cdist(descriptors_1, descriptors_2, metric="euclidean")
    nearest = np.argmin(distances, axis=1)

    matches = []
    for idx_1, idx_2 in enumerate(nearest):
        y1, x1 = points_1[idx_1]
        y2, x2 = points_2[idx_2]
        matches.append((float(y1), float(x1), float(y2), float(x2)))
    return np.asarray(matches, dtype=np.float32)


def scale_matches_to_original(matches_480, image_shape, input_size):
    if len(matches_480) == 0:
        return np.empty((0, 4), dtype=np.float32)
    height, width = image_shape[:2]
    scaled = matches_480.astype(np.float32).copy()
    scaled[:, [0, 2]] *= height / float(input_size)
    scaled[:, [1, 3]] *= width / float(input_size)
    return scaled
