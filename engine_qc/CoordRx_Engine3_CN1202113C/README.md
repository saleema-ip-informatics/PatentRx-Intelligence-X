# CoordRx Engine 3 — CN1202113C

Internal QC and integration package for PatentRx Intelligence X. **Not yet validated against the patent drawings.**

Source: https://patents.google.com/patent/CN1202113C/en
PDF: https://patentimages.storage.googleapis.com/90/81/f0/9faeb3309f669f/CN1202113C.pdf

## Scientific boundary

The existing `inspect_complex(smiles)` detects metal atoms and explicitly represented graph neighbors. It does **not** establish coordination number from disconnected ligand fragments, Ru oxidation state, experimental geometry, cis/trans assignment, or N/S thiocyanate linkage. Do not claim those outcomes from SMILES alone. The cases in `data/` are computational controls, **not transcriptions of patent compounds**. The patent example register is intentionally unqualified pending inspection of original drawings and Chinese text.

## Installation (Git Bash, at project root with `.venv` active)

1. Extract this directory under `engine_qc/` (do not replace existing files).
2. `python engine_qc/CoordRx_Engine3_CN1202113C/scripts/download_patent.py` (requires internet; skip if you already have the original PDF).
3. `python engine_qc/CoordRx_Engine3_CN1202113C/scripts/validate_cases.py`
4. `python -m pytest -q engine_qc/CoordRx_Engine3_CN1202113C/tests`
5. `python engine_qc/CoordRx_Engine3_CN1202113C/scripts/install_cases.py .`
6. `python -m pytest -q tests`
7. Inspect original patent formulae and examples; fill `patent_evidence/qualified_examples.json` only after drawing-level checks; use `scripts/write_internal_qc.py` to record measured outcomes, not presumed passes.

## Integration

`install_cases.py` creates only missing `data/workbench_cases/09_coord_*.json` files and refuses to overwrite existing files. Workbench schema is not presumed: the integration script checks local code first and exits if `coordrx` is unsupported. Tests exercise the existing `inspect_complex` API without altering engine source.

## Package scope

This ZIP includes all **new Engine 3 QC/integration files**, not the pre-existing `src/patentrx/engines/coordrx/{engine,advanced,qc3d}.py` modules, which remain untouched in your repository. PDF downloading is handled locally because the source host could not be accessed while assembling this package.
