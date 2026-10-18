#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from rdkit import Chem

ROOT = Path(__file__).resolve().parents[1]
def run(workbench=False):
    for p in sorted((ROOT/'data').glob('*.json')):
        case=json.loads(p.read_text(encoding='utf-8'))
        mol=Chem.MolFromSmiles(case['inputs']['smiles'])
        assert mol is not None, p.name
        centers=Chem.FindMolChiralCenters(mol,includeUnassigned=True)
        exp=case['qc_expectation']
        assert len(centers)==exp['chiral_centers'],(p.name,centers)
        if exp['cip'] is not None:
            assert [x[1] for x in centers]==[exp['cip']],(p.name,centers)
        else:
            assert [x[1] for x in centers]==["?"],(p.name,centers)
        assert case['source']['expert_signoff'] is False
        if workbench:
            from patentrx.workbench import analyze_case
            output=analyze_case(case)
            assert output['engine']=='stereorx'
            assert output['scientific_review_status']=='not_expert_verified'
            assert 'stereochemistry' in output['computational_outputs']
        print('PASS',p.name,'CIP:',exp['cip'] or 'unassigned')
    print('PASS: RDKit case validation'+(' and workbench smoke test' if workbench else ''))
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--workbench',action='store_true')
    run(parser.parse_args().workbench)
