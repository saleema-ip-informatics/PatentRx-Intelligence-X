import json
from pathlib import Path
from rdkit import Chem

folder = Path(__file__).resolve().parent
route = json.loads((folder / "reactionrx_four_step_route.json").read_text())
records = json.loads((folder / "reactionrx_atom_mapping_candidates.json").read_text())

expected = {
    "R001": (0, 2, 0, 2),
    "R002": (0, 0, 1, 0),
    "R003": (1, 1, 0, 1),
    "R004": (1, 8, 0, 8),
}

lookup = {r["reaction"]: r for r in records}
assert set(lookup) == set(expected)

for step in route["steps"]:
    rid = step["id"]
    a = Chem.MolFromSmiles(route["structures"][step["reactant"]]["smiles"])
    b = Chem.MolFromSmiles(route["structures"][step["product"]]["smiles"])
    assert a is not None and b is not None

    for number, pairs in enumerate(lookup[rid]["candidate_mappings"], 1):
        mapping = dict(pairs)
        reverse = {y: x for x, y in pairs}

        assert len(mapping) == len(reverse) == len(pairs)
        assert all(
            0 <= x < a.GetNumAtoms()
            and 0 <= y < b.GetNumAtoms()
            and a.GetAtomWithIdx(x).GetAtomicNum()
                == b.GetAtomWithIdx(y).GetAtomicNum()
            for x, y in pairs
        )

        removed = 0
        added = 0
        changed = 0
        conserved = 0

        for bond in a.GetBonds():
            x, y = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()

            if x not in mapping or y not in mapping:
                removed += 1
                continue

            target = b.GetBondBetweenAtoms(mapping[x], mapping[y])
            if target is None:
                removed += 1
            elif target.GetBondType() != bond.GetBondType():
                changed += 1
            else:
                conserved += 1

        for bond in b.GetBonds():
            x, y = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()

            if x not in reverse or y not in reverse:
                added += 1
                continue

            source = a.GetBondBetweenAtoms(reverse[x], reverse[y])
            if source is None:
                added += 1

        unmatched_product = b.GetNumAtoms() - len(reverse)

        actual = (removed, added, changed, unmatched_product)
        assert actual == expected[rid], (
            f"{rid} candidate {number}: "
            f"expected {expected[rid]}, got {actual}"
        )

        if rid == "R003":
            assert a.GetAtomWithIdx(8).GetSymbol() == "O"
            assert b.GetAtomWithIdx(8).GetSymbol() == "Br"
        elif rid == "R004":
            assert a.GetAtomWithIdx(8).GetSymbol() == "Br"
            assert b.GetBondBetweenAtoms(mapping[7], 3) is not None
            assert b.GetAtomWithIdx(3).GetSymbol() == "P"

        print(
            f"PASS {rid} candidate {number}: "
            f"conserved={conserved}, removed={removed}, "
            f"added={added}, order_changed={changed}"
        )

print("\nPASS: All stored reaction-center mappings validated.")
print("Scope: structural connectivity, not experimental atom provenance.")
