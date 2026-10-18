"""Explicit-coordinate metal-distance inventory, no inferred oxidation state or geometry."""
from rdkit import Chem

def audit_metal_coordinates(molblock: str, max_distance_angstrom: float=3.0) -> dict:
    if not 0 < max_distance_angstrom <= 5: raise ValueError('Invalid distance cutoff')
    mol=Chem.MolFromMolBlock(molblock,removeHs=False,sanitize=False)
    if mol is None or not mol.GetNumConformers(): return {"status":"invalid_or_missing_coordinates"}
    metals={'RU','IR','PT','PD','RH','CO','NI','FE','CU','ZN','MN','CR','AG','AU'}
    conf=mol.GetConformer(); out=[]
    for a in mol.GetAtoms():
        if a.GetSymbol().upper() not in metals: continue
        i=a.GetIdx(); near=[]
        for b in mol.GetAtoms():
            j=b.GetIdx()
            if j==i or b.GetSymbol()=='H':continue
            d=(conf.GetAtomPosition(i)-conf.GetAtomPosition(j)).Length()
            if d<=max_distance_angstrom:near.append({"atom_index":j,"element":b.GetSymbol(),"distance_angstrom":round(d,3)})
        out.append({"metal_index":i,"element":a.GetSymbol(),"nearby_atoms":sorted(near,key=lambda x:x['distance_angstrom'])})
    return {"status":"distance_inventory_only", "metal_centers":out,"geometry":"not_determined", "oxidation_state":"not_determined", "limitations":"Proximity alone does not prove coordination or establish metal oxidation state/geometry; validate atom identities, bonding and structural provenance"}
