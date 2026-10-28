"""Plot recovered reconstruction success_curve values from generated raw CSV."""
import argparse
import csv
import sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-csv',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'/'reconstruction'))
    from utils_eval import success_curve
    with args.raw_csv.open(encoding='utf-8') as handle: rows=list(csv.DictReader(handle))
    fig,axes=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
    for ax,category in zip(axes.flat,['S','P','A','ALL']):
        for experiment in sorted({r['experiment'] for r in rows}):
            errors=[float(r['error']) for r in rows if r['experiment']==experiment and (category=='ALL' or r['category']==category)]
            if errors:
                thresholds,rates=success_curve(errors); ax.plot(thresholds,100*rates,label=experiment)
        ax.set(title=category,xlabel='Registration error threshold (pixels)',ylabel='Success (%)',xlim=(0,25),ylim=(0,100))
        ax.grid(alpha=.2)
        if ax.lines: ax.legend(fontsize=7)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(args.output,dpi=150)
    plt.close(fig)

if __name__=='__main__': main()
