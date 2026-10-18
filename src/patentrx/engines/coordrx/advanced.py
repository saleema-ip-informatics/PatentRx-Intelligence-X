"""Connectivity-only coordination checks; never assert experimental geometry."""
from rdkit import Chem


def coordination_bond_inventory(smiles: str) -> dict:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")
    metal_symbols = {"Ru", "Ir", "Pt", "Pd", "Rh", "Co", "Ni", "Fe", "Cu", "Zn", "Mn", "Cr", "Ag", "Au"}
    centers = []
    for a in mol.GetAtoms():
        if a.GetSymbol() not in metal_symbols:
            continue
        bonds = [{"neighbor_atom": b.GetOtherAtomIdx(a.GetIdx()),
                  "bond_type": str(b.GetBondType())} for b in a.GetBonds()]
        centers.append({"atom_index": a.GetIdx(), "element": a.GetSymbol(),
                        "explicit_bond_count": len(bonds), "bonds": bonds})
    return {"metal_centers": centers, "geometry": "not_determined",
            "limitation": "Coordination number, oxidation state and 3D geometry require additional chemically validated structural evidence."}
