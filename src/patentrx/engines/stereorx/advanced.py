"""Stereochemical assignment comparison for explicitly mapped centers."""
from rdkit import Chem


def compare_mapped_stereocenters(reactant: str, product: str) -> dict:
    """Compare CIP labels; CIP label change alone is NOT evidence of inversion."""
    def centers(smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError("Invalid SMILES")
        Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
        out = {}
        for a in mol.GetAtoms():
            if a.GetAtomMapNum() and a.HasProp('_CIPCode'):
                out[a.GetAtomMapNum()] = a.GetProp('_CIPCode')
        return out
    left, right = centers(reactant), centers(product)
    return {"common_mapped_centers": sorted(set(left) & set(right)),
            "cip_changed": sorted(n for n in left.keys() & right.keys() if left[n] != right[n]),
            "cip_unchanged": sorted(n for n in left.keys() & right.keys() if left[n] == right[n]),
            "unpaired_centers": sorted(set(left) ^ set(right)),
            "warning": "CIP changes can arise from priority changes; do not infer inversion or retention without atom correspondence and local geometry."}
