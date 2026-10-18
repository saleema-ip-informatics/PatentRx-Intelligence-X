import pytest
from patentrx.engines.reactionrx.advanced import audit_atom_mapping
from patentrx.engines.stereorx.advanced import compare_mapped_stereocenters
from patentrx.engines.markushrx.advanced import match_enumerated_structures
from patentrx.engines.coordrx.advanced import coordination_bond_inventory
from patentrx.engines.biorx.advanced import inspect_pdb_text
from patentrx.core.provenance import source_fingerprint


def test_map_valid():
    assert audit_atom_mapping('[CH3:1][OH:2]', '[CH3:1][OH:2]')['valid']


def test_map_element_mismatch():
    result = audit_atom_mapping('[CH3:1][OH:2]', '[CH3:1][NH2:2]')
    assert 'ELEMENT_MISMATCH_MAP_2' in result['issues']


def test_map_sets_differ():
    assert 'MAP_SETS_DIFFER' in audit_atom_mapping('[CH3:1]O', '[CH3:1][OH:2]')['issues']


def test_invalid_map_smiles():
    assert 'INVALID_SMILES' in audit_atom_mapping('not-smiles', 'CC')['issues']


def test_stereo_same():
    s = '[CH3:1][C@H:2](O)C(=O)O'
    assert compare_mapped_stereocenters(s, s)['cip_unchanged'] == [2]


def test_stereo_changed():
    a = '[CH3:1][C@H:2](O)C(=O)O'
    b = '[CH3:1][C@@H:2](O)C(=O)O'
    assert compare_mapped_stereocenters(a, b)['cip_changed'] == [2]


def test_stereo_invalid():
    with pytest.raises(ValueError): compare_mapped_stereocenters('bad!', 'CC')


def test_markush_enumeration_exact():
    assert match_enumerated_structures('CCO', ['OCC', 'CCC'])['matched_indices'] == [0]


def test_markush_not_match():
    assert not match_enumerated_structures('CCO', ['CCN'])['exact_enumerated_match']


def test_markush_invalid():
    with pytest.raises(ValueError): match_enumerated_structures('CCO', ['invalid'])


def test_coord_metal():
    r = coordination_bond_inventory('[Pt+2]')
    assert r['metal_centers'][0]['element'] == 'Pt'
    assert r['geometry'] == 'not_determined'


def test_coord_no_metal():
    assert coordination_bond_inventory('CCO')['metal_centers'] == []


def test_bio_present():
    line = 'HETATM    1  C1  LIG A   1      11.000  12.000  13.000  1.00 20.00           C'
    assert inspect_pdb_text(line, 'LIG')['ligand_present']


def test_bio_absent():
    assert not inspect_pdb_text('', 'LIG')['ligand_present']


def test_bio_bad_residue():
    with pytest.raises(ValueError): inspect_pdb_text('', 'TOOLONG')


def test_fingerprint(tmp_path):
    f = tmp_path / 'sample.txt'; f.write_text('abc')
    r = source_fingerprint(str(f))
    assert r['sha256'] == 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    assert not r['expert_verified']
