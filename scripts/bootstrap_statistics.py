"""Audit statistics: point AUC, actual bootstrap mean and percentile CI.
Calls the recovered normalized_auc; does not alter legacy script or paper values.
Default order/seed preserve legacy resampling sequence for comparison.
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'/'reconstruction'))
import numpy as np
from analyze_bootstrap_ci import normalized_auc, grouped_errors, read_raw_pairs, EXPERIMENT_ORDER, CATEGORY_ORDER, RANDOM_SEED

def compute_statistics(rows,iterations=1000,seed=RANDOM_SEED):
    if iterations<=0: raise ValueError('iterations must be positive')
    groups=grouped_errors(rows); rng=np.random.default_rng(seed); outputs=[]
    extras=sorted({r['experiment'] for r in rows}-set(EXPERIMENT_ORDER))
    for experiment in list(EXPERIMENT_ORDER)+extras:
        for category in CATEGORY_ORDER:
            errors=np.asarray(groups.get((experiment,category),[]),dtype=np.float64)
            if not len(errors): continue
            samples=np.empty(iterations,dtype=np.float64)
            for index in range(iterations):
                samples[index]=normalized_auc(errors[rng.integers(0,len(errors),size=len(errors))])
            lower,upper=np.percentile(samples,[2.5,97.5])
            outputs.append({'experiment':experiment,'category':category,'n_pairs':len(errors),'point_auc':normalized_auc(errors),'bootstrap_mean_auc':float(samples.mean()),'ci_lower_95':float(lower),'ci_upper_95':float(upper),'iterations':iterations,'seed':seed})
    return outputs

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-csv',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--iterations',type=int,default=1000)
    parser.add_argument('--seed',type=int,default=RANDOM_SEED)
    args=parser.parse_args()
    outputs=compute_statistics(read_raw_pairs(args.raw_csv),args.iterations,args.seed)
    if not outputs: parser.error('Input contains no rows')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(outputs[0]));writer.writeheader();writer.writerows(outputs)
    print('Diagnostic estimates written; no published values or recovered experiment logic were changed.')

if __name__=='__main__': main()
