"""Launch an externally supplied/authorized recovered trainer.
The original architecture/loaders remain in private rights quarantine.
This wrapper implements no training algorithm and does not correct dataset roles.
"""
import argparse
import runpy
import sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trainer-script',type=Path,required=True)
    args,forwarded=parser.parse_known_args()
    if not args.trainer_script.is_file(): parser.error('Provide an existing authorized trainer script')
    if forwarded and forwarded[0]=='--': forwarded=forwarded[1:]
    sys.argv=[str(args.trainer_script.resolve())]+forwarded
    runpy.run_path(str(args.trainer_script.resolve()),run_name='__main__')

if __name__=='__main__': main()
