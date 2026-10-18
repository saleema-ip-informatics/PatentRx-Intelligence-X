# Scientific QC workflows — scope and acceptance criteria

## Organic 3D (`stereorx.qc3d.audit_organic_3d`)
Input: SMILES. Outputs ETKDGv3 conformer, MMFF optimization convergence/energy, minimum nonbonded heavy-atom separation and MOL block. A converged conformer is a **computed model**, never proof of correct patent stereochemistry or experimental geometry. Metal-containing structures are excluded. Validate source connectivity and stereochemistry separately; inspect multiple conformers for research use.

## Metal 3D (`coordrx.qc3d.audit_metal_coordinates`)
Input: externally supplied MOL block with coordinates. Reports metal-to-atom distance inventory only; does not assign donor roles, coordination number, oxidation state or polyhedron. Atom labels and structural provenance must be independently checked. Do not use generic organic force fields as validation for metal complexes.

## Protein ligand (`biorx.qc_structure.audit_pdb_ligand`)
Input: fixed-column PDB text and ligand three-letter code, optional chain and residue number. Reports protein-ligand atom distances and ligand occupancy flags. This is **not** a hydrogen-bond detector, steric-clash validator, mmCIF parser, structural-refinement audit, electron-density assessment, docking score, or biological binding validation. No internet data is included. For a real case, retrieve a licensed/appropriate PDB/mmCIF structure, validate ligand chemical component identity, experimental method, occupancy and missing atoms; compare relevant patent compound and assay evidence separately.

## Existing five engines
The baseline reaction, stereo, coordination, bio and finite-enumeration Markush tests remain included. Patent example WO2011103442A2_R001_UNVERIFIED is intentionally not converted to a confirmed structure.

## Status definitions
`computed`: algorithm produced a model, not experimental verification. `coordinates_screened`: geometric proximity assessed, not binding proven. `unsupported`: no suitable algorithm. `unresolved`: algorithm did not produce reliable result. `expert_verified` must require authenticated external review, not simply a programmatic flag.

## Scientific sign-off checklist
1. Verify source patent/PDB record and provenance.
2. Verify structure identity, formula, stereochemistry and atom correspondence.
3. Review geometry or contacts against domain-specific references and experimental metadata.
4. Record limitations and reviewer evidence before any human-verified claim.
5. Keep tests, reference data, and demo predictions separate.
