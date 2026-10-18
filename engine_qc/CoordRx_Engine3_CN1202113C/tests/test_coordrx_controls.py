import json
from pathlib import Path
from patentrx.engines.coordrx.engine import inspect_complex

ROOT=Path(__file__).resolve().parents[1]

def test_generated_controls():
    for path in sorted((ROOT/'data').glob('*.json')):
        case=json.loads(path.read_text(encoding='utf-8'))
        got=inspect_complex(case['inputs']['smiles'])
        exp=case['expected']
        assert got['valid']==exp['valid'],case['case_id']
        if not exp['valid']:continue
        assert got['geometry']=='not_determined',case['case_id']
        assert len(got['metal_centers'])==exp['metal_count'],case['case_id']
        if exp['metal_element']:
            metal=got['metal_centers'][0]
            assert metal['element']==exp['metal_element']
            assert len(metal['explicit_neighbors'])==exp['first_metal_explicit_neighbor_count']

def test_disconnected_ligand_not_assumed_bonded():
    result=inspect_complex('[Ru+2].n1ccccc1-c1ccccn1')
    assert result['valid']
    assert result['metal_centers'][0]['explicit_neighbors']==[]
    assert result['geometry']=='not_determined'
