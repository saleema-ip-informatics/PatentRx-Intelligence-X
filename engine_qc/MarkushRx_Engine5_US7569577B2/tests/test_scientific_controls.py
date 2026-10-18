import importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('scientific_controls',ROOT/'scripts/scientific_controls.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class ScientificControls(unittest.TestCase):
 def test_core(self): self.assertTrue(mod.core_screen('c1ccc2ncncc2c1')['has_quinazoline_core'])
 def test_benzene(self): self.assertFalse(mod.core_screen('c1ccccc1')['has_quinazoline_core'])
 def test_invalid(self): self.assertFalse(mod.core_screen('not_a_smiles')['valid'])
 def test_reference(self):
  d=json.loads((ROOT/'data/controls.json').read_text());self.assertIn('NOT_PATENT',d['provenance'])
 def test_claim_limitation(self):
  d=json.loads((ROOT/'data/controls.json').read_text());self.assertIn('does not establish',d['warning'])
