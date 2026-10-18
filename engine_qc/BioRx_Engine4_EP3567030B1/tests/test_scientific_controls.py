import importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('scientific_controls',ROOT/'scripts/scientific_controls.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class ScientificControls(unittest.TestCase):
 def test_pic50(self): self.assertAlmostEqual(mod.pic50_from_nm(10),8)
 def test_fold(self): self.assertAlmostEqual(mod.fold_difference(10,100),10)
 def test_zero_rejected(self):
  with self.assertRaises(ValueError): mod.pic50_from_nm(0)
 def test_negative_rejected(self):
  with self.assertRaises(ValueError): mod.pic50_from_nm(-1)
 def test_nan_rejected(self):
  with self.assertRaises(ValueError): mod.pic50_from_nm(float('nan'))
 def test_assay_noncomparable(self):
  a,b=json.loads((ROOT/'data/controls.json').read_text())['measurements'][::2]
  self.assertFalse(mod.comparable(a,b))
 def test_reference(self):
  d=json.loads((ROOT/'data/controls.json').read_text());self.assertEqual(d['provenance'],'COMPUTATIONAL_CONTROLS_NOT_PATENT_RESULTS')
