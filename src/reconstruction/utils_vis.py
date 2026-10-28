import cv2
import numpy as np
from matplotlib import pyplot as plt


def heatmap_to_color(heatmap_uint8):
    rgba = plt.cm.jet(heatmap_uint8)[:, :, :3]
    rgb = (rgba * 255).astype(np.uint8)
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def draw_points(image_bgr, points_yx, color=(155, 173, 0), radius=3):
    output = image_bgr.copy()
    for y, x in points_yx:
        cv2.circle(output, (int(x), int(y)), radius, color, -1)
    return output


def draw_matches(image_1_bgr, image_2_bgr, matches_yxyx, thickness=2):
    combined = np.hstack((image_1_bgr, image_2_bgr.copy()))
    offset_x = image_1_bgr.shape[1]
    rng = np.random.default_rng(12345)
    for y1, x1, y2, x2 in matches_yxyx:
        color_values = rng.integers(0, 255, size=3)
        color = tuple(int(value) for value in color_values)
        cv2.line(
            combined,
            (int(round(x1)), int(round(y1))),
            (int(round(x2)) + offset_x, int(round(y2))),
            color,
            thickness=thickness,
        )
    return combined


def create_tiled_mosaic(image_1_bgr, image_2_bgr, tile_size=(364, 364)):
    min_height = min(image_1_bgr.shape[0], image_2_bgr.shape[0])
    min_width = min(image_1_bgr.shape[1], image_2_bgr.shape[1])
    image_1 = image_1_bgr[:min_height, :min_width]
    image_2 = image_2_bgr[:min_height, :min_width]

    tile_h, tile_w = tile_size
    rows = min_height // tile_h
    cols = min_width // tile_w
    mosaic = np.zeros((rows * tile_h, cols * tile_w, 3), dtype=np.uint8)
    for row in range(rows):
        for col in range(cols):
            y0 = row * tile_h
            y1 = y0 + tile_h
            x0 = col * tile_w
            x1 = x0 + tile_w
            source = image_1 if (row + col) % 2 == 0 else image_2
            mosaic[y0:y1, x0:x1] = source[y0:y1, x0:x1]
    return mosaic


def save_pair_visualizations(
    output_dir,
    pair_id,
    image_1_bgr,
    image_2_bgr,
    heatmap_1,
    heatmap_2,
    points_1,
    points_2,
    matches,
    inliers,
    warped_1=None,
):
    output_dir.mkdir(parents=True, exist_ok=True)
    image_1_480 = cv2.resize(image_1_bgr, (480, 480), interpolation=cv2.INTER_LINEAR)
    image_2_480 = cv2.resize(image_2_bgr, (480, 480), interpolation=cv2.INTER_LINEAR)

    cv2.imwrite(str(output_dir / f"{pair_id}_1_heatmap.png"), heatmap_1)
    cv2.imwrite(str(output_dir / f"{pair_id}_2_heatmap.png"), heatmap_2)
    cv2.imwrite(str(output_dir / f"{pair_id}_1_heatmap_color.png"), heatmap_to_color(heatmap_1))
    cv2.imwrite(str(output_dir / f"{pair_id}_2_heatmap_color.png"), heatmap_to_color(heatmap_2))
    cv2.imwrite(str(output_dir / f"{pair_id}_1_points.png"), draw_points(image_1_480, points_1))
    cv2.imwrite(str(output_dir / f"{pair_id}_2_points.png"), draw_points(image_2_480, points_2))
    cv2.imwrite(str(output_dir / f"{pair_id}_matches.png"), draw_matches(image_1_bgr, image_2_bgr, matches))
    cv2.imwrite(str(output_dir / f"{pair_id}_inliers.png"), draw_matches(image_1_bgr, image_2_bgr, inliers, thickness=3))
    if warped_1 is not None:
        cv2.imwrite(str(output_dir / f"{pair_id}_mosaic.png"), create_tiled_mosaic(warped_1, image_2_bgr))
