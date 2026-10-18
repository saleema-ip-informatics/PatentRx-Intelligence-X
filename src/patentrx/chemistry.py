from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

def validate_molecule(smiles: str) -> dict:
    mol = Chem.MolFromSmiles(smiles) if smiles else None
    if mol is None:
        return {"valid": False, "canonical_smiles": None, "formula": None, "molecular_weight": None, "heavy_atoms": None}
    return {"valid": True, "canonical_smiles": Chem.MolToSmiles(mol), "formula": rdMolDescriptors.CalcMolFormula(mol), "molecular_weight": round(Descriptors.MolWt(mol), 4), "heavy_atoms": mol.GetNumHeavyAtoms()}
