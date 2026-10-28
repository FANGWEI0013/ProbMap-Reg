"""Inference/features wrapper around recovered reconstruction functions."""
import argparse
import csv
import sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image',type=Path,required=True)
    parser.add_argument('--checkpoint',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    if not args.image.is_file() or not args.checkpoint.is_file(): parser.error('Input image and checkpoint must exist')
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'/'reconstruction'))
    from utils_model import load_unet_model,read_bgr_image,predict_probability_map
    from utils_features import extract_features
    from config import PROBABILITY_THRESHOLD
    import numpy as np
    import cv2
    image=read_bgr_image(args.image)
    model=load_unet_model(args.checkpoint)
    probability=predict_probability_map(model,image)
    points,descriptors,heatmap=extract_features(probability,image,PROBABILITY_THRESHOLD)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    np.save(args.output_dir/'probability.npy',probability)
    np.save(args.output_dir/'hog_descriptors.npy',descriptors)
    if not cv2.imwrite(str(args.output_dir/'probability_uint8.png'),heatmap): raise OSError('Could not save heatmap')
    with (args.output_dir/'points_yx.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.writer(handle); writer.writerow(['y','x']); writer.writerows(points)
    print(f'Reconstruction extracted {len(points)} features; see code_paper_audit.md for differences.')

if __name__=='__main__': main()
