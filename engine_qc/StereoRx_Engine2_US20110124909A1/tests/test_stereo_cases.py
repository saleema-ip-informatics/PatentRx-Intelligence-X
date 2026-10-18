import json
from pathlib import Path
from rdkit import Chem
DATA=Path(__file__).resolve().parents[1]/'data'
def test_all_cases_have_expected_stereochemistry():
    for path in sorted(DATA.glob('*.json')):
        case=json.loads(path.read_text())
        mol=Chem.MolFromSmiles(case['inputs']['smiles'])
        assert mol is not None
        centers=Chem.FindMolChiralCenters(mol,includeUnassigned=True)
        exp=case['qc_expectation']
        assert len(centers)==exp['chiral_centers']
        if exp['cip']:
            assert [c[1] for c in centers]==[exp['cip']]
        else:
            assert [c[1] for c in centers]==["?"]
def test_controls_are_not_claimed_as_patent_measurements():
    for path in DATA.glob('*.json'):
        case=json.loads(path.read_text())
        assert case['source']['expert_signoff'] is False
        if case['case_type']=='computational_control':
            assert case['source']['kind']=='generated_control'
