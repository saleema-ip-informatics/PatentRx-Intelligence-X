# PatentRx Intelligence X — consolidated QC research package

This standalone package preserves the five-engine v0.2 foundation and adds **organic 3D conformer screening**, **metal-coordinate distance inventory**, and **PDB protein–ligand proximity screening**. It is designed for sequential QC of three portfolio case studies, not a claim of experimental structure verification.

## Windows Git Bash quick start
Extract the folder into `D:/PatentRx-Intelligence-X-QC-Package` (or use the actual extracted path):

```bash
cd /d/PatentRx-Intelligence-X-QC-Package
PYTHONPATH=src python -m pytest tests/ -q
```

Install project dependencies if needed: `python -m pip install -e '.[dev]'`.

## Scientific modules
- `patentrx.engines.stereorx.qc3d.audit_organic_3d(smiles)`
- `patentrx.engines.coordrx.qc3d.audit_metal_coordinates(molblock)`
- `patentrx.engines.biorx.qc_structure.audit_pdb_ligand(pdb_text, ligand_resname, chain=None, resseq=None)`

Read `docs/QC_WORKFLOWS.md` before interpreting any results. Existing `README_V2.md` and `docs/SCIENTIFIC_VALIDATION.md` describe previous capabilities. No Streamlit dashboard is claimed or included in this package.
