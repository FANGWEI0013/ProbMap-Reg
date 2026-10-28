"""Packaging checks that do not load weights or compare paper scores."""
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, name, *args):
        return subprocess.run([sys.executable, '-B', str(ROOT / 'scripts' / name), *map(str, args)],
                              capture_output=True, text=True, timeout=30)

    def test_missing_checkpoint_and_dataset_preflight(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            result = self.run_cli('run_reconstruction.py', 'proposed', '--output-dir', folder)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Provide an existing --checkpoint', result.stderr)
            # A placeholder path passes only is_file; dataset failure must precede model loading.
            checkpoint = folder / 'placeholder.h5'
            checkpoint.write_bytes(b'not-a-model')
            result = self.run_cli('run_reconstruction.py', 'proposed', '--checkpoint', checkpoint,
                                  '--fire-root', folder, '--output-dir', folder / 'outputs')
            self.assertEqual(result.returncode, 2)
            self.assertIn('Provide FIRE root with Images and Ground Truth', result.stderr)
            self.assertFalse((folder / 'outputs').exists())

    def test_help_and_missing_ablation_prerequisite(self):
        result = self.run_cli('run_reconstruction.py', '--help')
        self.assertEqual(result.returncode, 0)
        self.assertIn('no --pair option', result.stdout)
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli('run_reconstruction.py', 'bootstrap', '--output-dir', directory)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Run ablation first', result.stderr)

    def test_evaluation_keeps_failed_row_and_protects_input(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            raw = folder / 'raw.csv'
            raw.write_text('experiment,category,error,status,runtime\nExample,A,0,success,1\nExample,A,inf,failed,1\n',
                           encoding='utf-8')
            output = folder / 'summary.csv'
            result = self.run_cli('evaluate_fire.py', '--raw-csv', raw, '--output', output)
            self.assertEqual(result.returncode, 0, result.stderr)
            with output.open(encoding='utf-8') as handle:
                overall = next(row for row in csv.DictReader(handle) if row['category'] == 'ALL')
            self.assertEqual(int(overall['num_pairs']), 2)
            self.assertEqual(int(overall['num_failed']), 1)
            self.assertAlmostEqual(float(overall['auc']), 0.5)
            result = self.run_cli('evaluate_fire.py', '--raw-csv', raw, '--output', raw)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Output must differ', result.stderr)
            self.assertIn('inf,failed', raw.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
