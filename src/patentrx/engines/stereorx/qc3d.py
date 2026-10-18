"""Organic 3D conformer screening, not experimental structure verification."""
from rdkit import Chem
from rdkit.Chem import AllChem
import math

def audit_organic_3d(smiles: str, seed: int = 42) -> dict:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"valid": False, "status": "invalid_input", "reason": "SMILES could not be parsed"}
    if any(a.GetAtomicNum() > 20 for a in mol.GetAtoms()):
        return {"valid": True, "status": "unsupported", "reason": "Metal/heavy-element geometry requires specialized parameters; generic organic force-field QC not applied"}
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    if AllChem.EmbedMolecule(mol, params) != 0:
        return {"valid": True, "status": "unresolved", "reason": "3D embedding failed"}
    props = AllChem.MMFFGetMoleculeProperties(mol)
    if props is None:
        return {"valid": True, "status": "unsupported", "reason": "MMFF parameters unavailable"}
    before = AllChem.MMFFGetMoleculeForceField(mol, props).CalcEnergy()
    result = AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
    after = AllChem.MMFFGetMoleculeForceField(mol, props).CalcEnergy()
    conf = mol.GetConformer()
    min_nonbonded = None
    bonded = {tuple(sorted((b.GetBeginAtomIdx(),b.GetEndAtomIdx()))) for b in mol.GetBonds()}
    heavy = [a.GetIdx() for a in mol.GetAtoms() if a.GetAtomicNum()>1]
    for i, a in enumerate(heavy):
        for b in heavy[i+1:]:
            if (a,b) in bonded: continue
            d = (conf.GetAtomPosition(a)-conf.GetAtomPosition(b)).Length()
            min_nonbonded = d if min_nonbonded is None else min(min_nonbonded,d)
    return {"valid": True, "status": "computed" if result == 0 else "optimization_not_converged",
            "method": "ETKDGv3 + MMFF94", "seed": seed, "energy_before_kcal_mol": round(before,4),
            "energy_after_kcal_mol": round(after,4), "heavy_atom_min_nonbonded_angstrom": None if min_nonbonded is None else round(min_nonbonded,3),
            "converged": result == 0, "molblock_3d": Chem.MolToMolBlock(Chem.RemoveHs(mol)),
            "limitations": ["One computed conformer is not a global minimum or experimentally determined structure", "Nonbonded distance is descriptive, not a validated clash classification", "CIP and source stereochemistry require separate review"]}
