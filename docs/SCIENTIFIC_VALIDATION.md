# Scientific validation status (v0.2)

All new checks are deterministic unit tests, **not** expert-reviewed chemistry benchmark results.

| Engine | New implemented feature | What it does NOT establish |
|---|---|---|
| ReactionRx | Map-set and mapped-element consistency checks | Correct atom mapping, mechanism, mass balance, full reaction role assignment |
| StereoRx | CIP comparison of mapped centers | Physical inversion/retention, 3D geometry, source stereochemistry |
| CoordRx | Explicit metal bond inventory | Oxidation state, coordination number, geometry, experimental accuracy |
| BioRx | Fixed-column PDB ligand HETATM presence check | Affinity, binding, contact quality, mmCIF parsing |
| MarkushRx | Exact finite SMILES enumeration comparison | Generic claim scope, R-group attachment semantics, legal infringement |
| Evidence core | SHA-256 source file fingerprints | Authentication of reviewer or source correctness |

## Patent WO2011103442A2
`data/patent_cases/WO2011103442A2_R001_UNVERIFIED.json` remains an **unverified structure** case. Do not promote a candidate regioisomer on the basis of matching formula, HRMS, or aromatic H count alone. Independent source-drawing review is still required.

## Test policy
Tests use controlled examples, including deliberate failures. A passing suite verifies software behavior for those cases only. Additional curated reference datasets and external expert review are required before any scientific accuracy claims.
