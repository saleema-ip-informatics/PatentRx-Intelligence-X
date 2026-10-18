"""Explicit, finite enumerated substituent structural matching (not full Markush claim scope)."""
from rdkit import Chem


def match_enumerated_structures(example_smiles: str, enumerated_smiles: list[str]) -> dict:
    target = Chem.MolFromSmiles(example_smiles)
    if target is None:
        raise ValueError("Invalid example SMILES")
    canon = Chem.MolToSmiles(target, isomericSmiles=True)
    matches = []
    for i, s in enumerate(enumerated_smiles):
        mol = Chem.MolFromSmiles(s)
        if mol is None:
            raise ValueError(f"Invalid enumerated SMILES at index {i}")
        if Chem.MolToSmiles(mol, isomericSmiles=True) == canon:
            matches.append(i)
    return {"exact_enumerated_match": bool(matches), "matched_indices": matches,
            "scope": "Exact enumerated structure matching only; not generic Markush claim coverage"}
