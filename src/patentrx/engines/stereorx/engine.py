from rdkit import Chem
from patentrx.chemistry import validate_molecule

def inspect_stereochemistry(smiles: str) -> dict:
    info=validate_molecule(smiles)
    if not info['valid']:return {"valid":False,"error":"Invalid SMILES"}
    mol=Chem.MolFromSmiles(smiles)
    Chem.AssignStereochemistry(mol,cleanIt=True,force=True)
    centers=Chem.FindMolChiralCenters(mol,includeUnassigned=True,includeCIP=True)
    return {"valid":True,"canonical_smiles":info['canonical_smiles'],"centers":[{"atom_index":i,"label":label} for i,label in centers],"unassigned_count":sum(label=='?' for _,label in centers),"source_verified":False}
