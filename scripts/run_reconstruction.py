"""Recovered reconstruction implementation: configurable execution wrapper."""
import argparse
import os
import runpy
import sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Forwarded options from the recovered entry points:\n'
               '  proposed: --pair A01 | --small-test | --full-run; --save-vis | --no-vis\n'
               '  ablation: --small-test | --full-run; --no-vis (no --pair option)\n'
               '  bootstrap: no forwarded options; reads prior ablation raw_pairs.csv\n'
               '  failure: no forwarded options; needs prior Category P ablation rows\n'
               'Full runs require deliberate approval. See docs/quickstart.md.',
    )
    parser.add_argument('experiment',choices=['proposed','ablation','bootstrap','failure'])
    parser.add_argument('--checkpoint',type=Path)
    parser.add_argument('--fire-root',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True)
    args, forwarded=parser.parse_known_args()
    if args.experiment in {'bootstrap','failure'}:
        raw=args.output_dir/'ablation_probmap_vs_sift'/'raw_pairs.csv'
        if not raw.is_file(): parser.error('Run ablation first: missing ablation_probmap_vs_sift/raw_pairs.csv under --output-dir')
    if args.experiment in {'proposed','ablation','failure'}:
        if args.checkpoint is None or not args.checkpoint.is_file(): parser.error('Provide an existing --checkpoint')
        if args.fire_root is None or not (args.fire_root/'Images').is_dir() or not (args.fire_root/'Ground Truth').is_dir(): parser.error('Provide FIRE root with Images and Ground Truth')
    if args.checkpoint: os.environ['PROBMAP_CHECKPOINT']=str(args.checkpoint.resolve())
    if args.fire_root: os.environ['PROBMAP_FIRE_ROOT']=str(args.fire_root.resolve())
    os.environ['PROBMAP_OUTPUT_DIR']=str(args.output_dir.resolve())
    os.environ.setdefault('MPLBACKEND','Agg')
    scripts={'proposed':'run_proposed.py','ablation':'run_ablation_probmap_vs_sift.py','bootstrap':'analyze_bootstrap_ci.py','failure':'analyze_failure_cases.py'}
    folder=Path(__file__).resolve().parents[1]/'src'/'reconstruction'
    sys.path.insert(0,str(folder)); sys.argv=[scripts[args.experiment]]+forwarded
    runpy.run_path(str(folder/scripts[args.experiment]),run_name='__main__')

if __name__=='__main__': main()
