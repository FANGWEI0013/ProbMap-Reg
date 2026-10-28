"""Numerical invariants for recovered implementations; no benchmark target fitting."""
import importlib.util
import sys
import unittest
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'/'reconstruction'))
import utils_eval as ev
import utils_features as fe
import utils_matching as ma
import utils_transform as tr
import analyze_bootstrap_ci as boot

class CoreTests(unittest.TestCase):
    def test_failure_denominator_and_threshold_boundary(self):
        self.assertAlmostEqual(ev.normalized_auc([0,np.inf]),0.5)
        self.assertAlmostEqual(ev.normalized_auc([25]),0.02)
        self.assertEqual(ev.normalized_auc([np.inf]),0)
        self.assertEqual(ev.normalized_auc([]),0)

    def test_fire_enumeration(self):
        ids=ev.generate_fire_pair_ids()
        self.assertEqual(len(set(ids)),134)
        self.assertEqual([sum(p.startswith(c) for p in ids) for c in ['S','P','A']],[71,49,14])

    def test_transform_direction_and_coordinate_order(self):
        source=np.array([[0.,0.],[100.,0.],[0.,100.],[100.,100.]])
        target=source+np.array([17.,-9.])
        matches=np.column_stack([source[:,1],source[:,0],target[:,1],target[:,0]])
        matrix,inliers=tr.ransac_inliers(matches,20.)
        controls=np.column_stack([source,target])
        self.assertEqual(len(inliers),4)
        self.assertLess(ev.registration_error(tr.affine_2x3_to_homogeneous(matrix),controls),1e-6)

    def test_non_square_scaling(self):
        out=ma.scale_matches_to_original(np.array([[10.,20.,30.,40.]]),(960,1440,3),480)
        np.testing.assert_array_equal(out,[[20,60,60,120]])

    def test_local_maxima_strict_threshold(self):
        image=np.zeros((40,40),dtype=np.uint8); image[10,10]=80; image[30,30]=81
        np.testing.assert_array_equal(fe.detect_local_maxima(image,80),[[30,30]])

    def test_bootstrap_retains_failures_and_is_seeded(self):
        first=boot.bootstrap_auc_ci([0,np.inf],np.random.default_rng(123),1000)
        second=boot.bootstrap_auc_ci([0,np.inf],np.random.default_rng(123),1000)
        self.assertEqual(first,second)
        self.assertEqual(first,(0.,1.))

    def test_reconstruction_hog_dimension_and_border_filter(self):
        gray=np.arange(64*64,dtype=np.uint16).reshape(64,64).astype(np.uint8)
        points,descriptors=fe.compute_hog_descriptors(gray,np.array([[32,32],[0,0]]))
        np.testing.assert_array_equal(points,[[32,32]])
        self.assertEqual(descriptors.shape,(1,128))

if __name__=='__main__': unittest.main()
