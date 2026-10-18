from rdkit import Chem
METALS={"Ru","Ir","Pt","Pd","Rh","Co","Ni","Fe","Cu","Zn","Mn","Cr","Ag","Au"}
def inspect_complex(smiles: str) -> dict:
    mol=Chem.MolFromSmiles(smiles)
    if mol is None:return {"valid":False,"error":"Invalid SMILES"}
    metals=[{"atom_index":a.GetIdx(),"element":a.GetSymbol(),"formal_charge":a.GetFormalCharge(),"explicit_neighbors":[n.GetIdx() for n in a.GetNeighbors()]} for a in mol.GetAtoms() if a.GetSymbol() in METALS]
    return {"valid":True,"metal_centers":metals,"geometry":"not_determined","warning":"SMILES connectivity alone does not establish coordination geometry, oxidation state or experimental structure"}
