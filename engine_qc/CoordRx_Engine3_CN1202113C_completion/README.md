# CoordRx Engine 3 — internal QC completion add-on

This is an **add-on**, not a replacement for the already extracted `engine_qc/CoordRx_Engine3_CN1202113C` package. Extract this folder as a sibling inside `engine_qc/`. Never overwrite any existing files.

Patent: CN1202113C. The `patent_evidence/experimental_reference.json` contains visually transcribed observations from patent PDF pages 15–20 supplied in the conversation. These are source-reported observations, not independent experiments. They do **not** constitute fully mapped patent compound SMILES or prove geometry from a connectivity-only parser.

## Run

From project root in the active virtual environment:

```bash
python engine_qc/CoordRx_Engine3_CN1202113C_completion/scripts/run_completion_qc.py
```

The runner checks that the previously downloaded patent PDF exists, validates seven existing cases, runs six extra controls, runs the entire project regression suite, and **only then** writes `internal_qc_result.json` (refuses to overwrite). A passing report has narrowly scoped `INTERNAL_QC_PASS`; `patent_structure_mapping` remains `NOT_FULLY_VALIDATED` until exact patent structures are encoded and reviewed. No source code is modified. If a test fails, inspect output before making any change.

## Evidence limitations

- Formula I/II show Ru with two bipyridine donors pairs and two X ligands; III shows a terpyridine with three X groups.
- Reported cis/trans geometry and NCS linkage cannot be inferred from ordinary SMILES.
- Example 10 has a potential heading-versus-elemental-formula discrepancy; retain both without forced reconciliation.
- This package does not require or include external review.
