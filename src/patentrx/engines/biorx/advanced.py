"""Simple evidence-aware PDB text inspection; no binding affinity inference."""


def inspect_pdb_text(pdb_text: str, ligand_resname: str) -> dict:
    """Count HETATM ligand records; not a binding-site or interaction analysis."""
    if len(ligand_resname) != 3 or not ligand_resname.isalnum():
        raise ValueError("Ligand residue name must be three alphanumeric characters")
    atoms = []
    for line in pdb_text.splitlines():
        if line.startswith('HETATM') and len(line) >= 26 and line[17:20].strip() == ligand_resname:
            atoms.append(line)
    return {"ligand_resname": ligand_resname, "ligand_atom_records": len(atoms),
            "ligand_present": bool(atoms), "binding_confirmed": False,
            "limitation": "Presence of ligand coordinates does not establish affinity, biological activity or structural quality."}
