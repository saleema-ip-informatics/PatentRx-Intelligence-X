"""Conservative chemistry-aware validation of explicit atom maps."""
from rdkit import Chem


def audit_atom_mapping(reactant_smiles: str, product_smiles: str) -> dict:
    """Inspect atom-map integrity; does not infer maps or prove a reaction mechanism."""
    result = {"valid": False, "issues": [], "mapped_atoms_reactant": 0,
              "mapped_atoms_product": 0, "unmapped_atoms_reactant": 0,
              "unmapped_atoms_product": 0}
    mols = [Chem.MolFromSmiles(s) for s in (reactant_smiles, product_smiles)]
    if any(m is None for m in mols):
        result["issues"].append("INVALID_SMILES")
        return result
    mappings = []
    for side, mol in zip(("reactant", "product"), mols):
        atoms = [a for a in mol.GetAtoms() if a.GetAtomMapNum() > 0]
        nums = [a.GetAtomMapNum() for a in atoms]
        result[f"mapped_atoms_{side}"] = len(atoms)
        result[f"unmapped_atoms_{side}"] = mol.GetNumAtoms() - len(atoms)
        if len(nums) != len(set(nums)):
            result["issues"].append(f"DUPLICATE_MAP_{side.upper()}")
        mappings.append({a.GetAtomMapNum(): a for a in atoms})
    r, prod = mappings
    if not r or not prod:
        result["issues"].append("NO_SHARED_MAPPING")
    if set(r) != set(prod):
        result["issues"].append("MAP_SETS_DIFFER")
    for n in sorted(set(r) & set(prod)):
        if r[n].GetAtomicNum() != prod[n].GetAtomicNum():
            result["issues"].append(f"ELEMENT_MISMATCH_MAP_{n}")
    result["valid"] = not result["issues"]
    return result
