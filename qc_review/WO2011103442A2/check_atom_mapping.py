import json
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import rdFMCS

folder = Path("qc_review/WO2011103442A2")
data = json.loads(
    (folder / "reactionrx_four_step_route.json").read_text()
)

results = []

for step in data["steps"]:
    a = Chem.MolFromSmiles(
        data["structures"][step["reactant"]]["smiles"]
    )
    b = Chem.MolFromSmiles(
        data["structures"][step["product"]]["smiles"]
    )

    mcs = rdFMCS.FindMCS(
        [a, b],
        timeout=15,
        ringMatchesRingOnly=True,
        completeRingsOnly=True,
        bondCompare=rdFMCS.BondCompare.CompareAny
    )

    if mcs.canceled:
        raise RuntimeError(f"MCS timeout: {step['id']}")

    query = Chem.MolFromSmarts(mcs.smartsString)
    ma = a.GetSubstructMatches(query, uniquify=False)
    mb = b.GetSubstructMatches(query, uniquify=False)

    # Store all candidate mappings, not only the first.
    mappings = [
        list(zip(x, y))
        for x in ma
        for y in mb
    ]

    result = {
        "reaction": step["id"],
        "mcs_atoms": mcs.numAtoms,
        "candidate_mapping_count": len(mappings),
        "candidate_mappings": mappings,
        "status": "CANDIDATE_MAPPINGS_NOT_FULLY_VERIFIED"
    }
    results.append(result)

    print(
        step["id"],
        "MCS:", mcs.numAtoms,
        "candidate mappings:", len(mappings)
    )

output = folder / "reactionrx_atom_mapping_candidates.json"
output.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print("\nSaved:", output)
