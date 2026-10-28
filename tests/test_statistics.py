"""Independent expectations for the newly authored diagnostic reporting."""
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from bootstrap_statistics import compute_statistics

class StatisticsTests(unittest.TestCase):
    def test_separate_estimands_against_direct_rng_calculation(self):
        rows=[{'experiment':'Example','category':'A','error':e} for e in ['0','10','inf']]
        results=compute_statistics(rows,1000,123)
        original=np.array([1.,.62,0.])
        rng=np.random.default_rng(123)
        expected=np.array([original[rng.integers(0,3,size=3)].mean() for _ in range(1000)])
        category=results[0]
        self.assertAlmostEqual(category['point_auc'],original.mean())
        self.assertAlmostEqual(category['bootstrap_mean_auc'],expected.mean())
        self.assertAlmostEqual(category['ci_lower_95'],np.percentile(expected,2.5))
        self.assertAlmostEqual(category['ci_upper_95'],np.percentile(expected,97.5))
        self.assertEqual(category['n_pairs'],3)

    def test_empty_or_invalid_iterations(self):
        self.assertEqual(compute_statistics([]),[])
        with self.assertRaises(ValueError): compute_statistics([],0)

if __name__=='__main__': unittest.main()
