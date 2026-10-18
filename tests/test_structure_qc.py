from patentrx.engines.stereorx.qc3d import audit_organic_3d
from patentrx.engines.biorx.qc_structure import audit_pdb_ligand
from patentrx.engines.coordrx.qc3d import audit_metal_coordinates
from rdkit import Chem
from rdkit.Chem import AllChem

def pdbline(kind, serial, atom, res, chain, resid, x,y,z, element):
    return f'{kind:<6}{serial:5d} {atom:4s} {res:>3s} {chain}{resid:4d}    {x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{20.0:6.2f}          {element:>2s}'

def test_organic_3d_success():
    x=audit_organic_3d('CCO');assert x['valid'] and x['status']=='computed' and x['converged']
    assert 'V2000' in x['molblock_3d']
def test_organic_invalid():assert not audit_organic_3d('invalid???')['valid']
def test_organic_metal_not_forcefield():assert audit_organic_3d('[Ru]')['status']=='unsupported'
def test_pdb_contact():
    p='\n'.join([pdbline('ATOM',1,'CA','ALA','A',1,0,0,0,'C'),pdbline('HETATM',2,'C1','LIG','A',2,2,0,0,'C')])
    x=audit_pdb_ligand(p,'LIG');assert x['contact_count']==1 and x['contacts'][0]['distance_angstrom']==2.0
    assert not x['binding_confirmed']
def test_pdb_no_ligand():
    x=audit_pdb_ligand(pdbline('ATOM',1,'CA','ALA','A',1,0,0,0,'C'),'LIG');assert x['status']=='ligand_not_found'
def test_pdb_ambiguous():
    p='\n'.join([pdbline('HETATM',1,'C1','LIG','A',1,0,0,0,'C'),pdbline('HETATM',2,'C1','LIG','B',1,1,0,0,'C')])
    assert audit_pdb_ligand(p,'LIG')['status']=='ambiguous_ligand_instance'
def test_pdb_invalid_cutoff():
    import pytest
    with pytest.raises(ValueError):audit_pdb_ligand('','LIG',cutoff_angstrom=0)
def test_metal_inventory():
    m=Chem.MolFromSmiles('[Pt]');m=Chem.AddHs(m);AllChem.EmbedMolecule(m,randomSeed=7)
    x=audit_metal_coordinates(Chem.MolToMolBlock(m));assert x['metal_centers'][0]['element']=='Pt' and x['geometry']=='not_determined'
def test_metal_invalid():assert audit_metal_coordinates('bad')['status']=='invalid_or_missing_coordinates'
