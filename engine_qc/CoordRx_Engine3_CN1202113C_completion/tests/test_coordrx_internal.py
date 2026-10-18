"""Checks actual CoordRx functionality; no inferred cis/trans or spectroscopy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))
from patentrx.engines.coordrx.engine import inspect_complex

def test_ruthenium_atom_detected():
    result = inspect_complex('[Ru+2]')
    assert result['valid'] and len(result['metal_centers']) == 1
    assert result['metal_centers'][0]['element'] == 'Ru'
    assert result['metal_centers'][0]['formal_charge'] == 2
    assert result['geometry'] == 'not_determined'

def test_explicit_chloride_neighbor():
    result = inspect_complex('[Cl-]->[Ru+2]')
    assert result['valid']
    assert len(result['metal_centers']) == 1
    assert len(result['metal_centers'][0]['explicit_neighbors']) == 1

def test_disconnected_ligand_is_not_coordination_bond():
    result = inspect_complex('[Ru+2].n1ccccc1')
    assert result['valid']
    assert result['metal_centers'][0]['explicit_neighbors'] == []

def test_no_metal():
    result = inspect_complex('c1ccncc1')
    assert result['valid'] and result['metal_centers'] == []

def test_invalid():
    result = inspect_complex('not_a_smiles')
    assert result['valid'] is False

def test_geometry_not_guessed():
    for smi in ('[Ru+2]', '[Cl-]->[Ru+2]', '[Ru+2].n1ccccc1'):
        assert inspect_complex(smi)['geometry'] == 'not_determined'
