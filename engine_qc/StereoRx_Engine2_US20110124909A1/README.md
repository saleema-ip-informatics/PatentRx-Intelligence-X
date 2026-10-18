# Engine 2 — StereoRx | US20110124909A1

**Status: preliminary, reproducible QC starter pack — NOT fully scientifically validated.**

The patent describes resolving racemic pregabalin to (S)-pregabalin and reports chiral-HPLC enantiomeric purity for isolated material. This package provides one patent-named target structure and two explicitly **generated computational controls** (R enantiomer and unspecified stereochemistry). The provided SMILES are RDKit-checked representations, **not independently authenticated patent drawing transcriptions**.

Patent: https://patents.google.com/patent/US20110124909A1/en

## Files
- `data/*.json`: three standalone workbench-compatible StereoRx cases
- `scripts/validate_cases.py`: independent RDKit CIP checks and optional workbench smoke test
- `scripts/install_cases.py`: non-overwriting copier to your existing project
- `tests/test_stereo_cases.py`: independent stereochemical assertions
- `manifest.json`: provenance and explicit limitations

## Install on Windows Git Bash (in project root)
1. Extract this ZIP somewhere outside your project.
2. Activate your existing `.venv`.
3. Run `python /path/to/extracted/scripts/validate_cases.py` (no project modification).
4. Run `python /path/to/extracted/scripts/install_cases.py /d/PatentRx_Intelligence_X_COMPLETE` to copy only new JSON cases, refusing to overwrite.
5. From your project root, run `python /path/to/extracted/scripts/validate_cases.py --workbench` to check `analyze_case` integration.

The validator only asserts expected RDKit stereochemical facts and that workbench results preserve engine identity and the `not_expert_verified` label. It does **not** assert uninspected `inspect_stereochemistry` output field names or invent an expert pass.

## Scientific QC remaining before Engine 2 closure
- Visually reconcile the patent structures/salts with the SMILES and label any representation differences.
- Inspect actual StereoRx stereochemistry and 3D functions and define output-level acceptance tests.
- Test enantiomer, unspecified, invalid-SMILES and other stereochemical controls.
- Record patent-specific findings, evidence, independent reviewer status and final report.
- Run project regression tests only after integration changes.

No ReactionRx, dashboard, or existing project files are modified by the package.
