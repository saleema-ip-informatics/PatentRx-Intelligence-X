# MARKUSHRX — internal QC package

Patent: US7569577B2
Source: https://patents.google.com/patent/US7569577B2/en

This package is additive: place the folder under `engine_qc/`. It does not replace existing `src/patentrx/engines/markushrx/` files.

## Run from project root with active .venv

`python engine_qc/MarkushRx_Engine5_US7569577B2/scripts/run_internal_qc.py`

The runner validates local reference data, tests scientific utility functions, runs the entire project test suite and checks the engine import. It writes a dated-free reproducible `reports/internal_qc_result.json` if the destination does not exist. It does NOT claim patent compound structures or numerical assays have been verified until the source evidence is completed.

## Evidence policy

The PDF can be obtained from the Google Patents URL above. The included `scripts/download_patent.py` downloads the official patent PDF linked from the page when available; PDF must be inspected before exact structure/assay certification. No patent-derived SMILES or invented assay values are included.

Complete `patent_evidence/source_review.json` with checked page numbers, source images, exact structures/assays, and reviewer notes before declaring full internal patent QC. Computational controls are explicitly not patent compounds.

All QC is internal. No external approval workflow.
