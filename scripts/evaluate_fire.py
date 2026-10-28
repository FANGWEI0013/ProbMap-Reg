"""Summarize generated FIRE errors using the unchanged recovered evaluator.

This reads results, not FIRE images or ground-truth files. Row counts are reported;
subset outputs must not be presented as full-benchmark reproduction.
"""
import argparse
import csv
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-csv', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not args.raw_csv.is_file():
        parser.error('Input raw CSV does not exist')
    if args.output.resolve() == args.raw_csv.resolve():
        parser.error('Output must differ from input raw CSV')
    with args.raw_csv.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        required = {'experiment', 'category', 'error', 'status', 'runtime'}
        if not required.issubset(reader.fieldnames or []):
            parser.error('Expected CSV columns: experiment, category, error, status, runtime')
        rows = list(reader)
    if not rows:
        parser.error('Input CSV has no data rows')
    try:
        for row in rows:
            float(row['error'])
            float(row['runtime'])
    except (ValueError, TypeError):
        parser.error('Error and runtime columns must contain numeric values (inf is allowed for failed errors)')
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'reconstruction'))
    from utils_eval import summarize_rows, write_csv
    summaries = []
    for experiment in sorted({row['experiment'] for row in rows}):
        selected = [row for row in rows if row['experiment'] == experiment]
        summaries.extend(summarize_rows(selected, experiment))
    write_csv(args.output, summaries, list(summaries[0]))
    print(f'Evaluated {len(rows)} input rows; failures retained in denominators. Output: {args.output}')


if __name__ == '__main__':
    main()
