# PatentRx Intelligence X — Unified Scientific QC Workbench

One cohesive project presenting expertise in **organic patent reactions, chemical structure drawing, stereochemistry, 3D molecules, metal complexes, biopharma patents, Markush interpretation and evidence-based scientific AI QC**.

## What is included
- All five original engines (ReactionRx, StereoRx, CoordRx, BioRx, MarkushRx), preserved and integrated.
- Existing QC modules for organic conformers, metal coordinate inventories and PDB ligand proximity.
- A unified JSON case runner, downloadable JSON/Markdown scientific QC reports and an optional Streamlit dashboard.
- Six clearly labeled demonstration cases: five synthetic demonstrations and one **unverified** patent transcription.
- Automated tests and documentation for scientific review; tests do **not** establish experimental validation.

## Windows Git Bash quick start
```bash
cd /d/PatentRx_Intelligence_X_COMPLETE
PYTHONPATH=src python -m pytest tests/ -q
PYTHONPATH=src python -m patentrx.workbench_cli data/workbench_cases/01_reaction_demo.json --output reports/reaction.json --markdown reports/reaction.md
```

### Dashboard (optional dependency)
```bash
python -m pip install -e '.[dashboard]'
streamlit run app.py
```

If `streamlit` is not installed, the core engines and tests still work. Run the dashboard from the project root so Python can find the installed `patentrx` package.

## Scientific limits
- No claim of full patent PDF extraction, general Markush graph interpretation, protein affinity prediction, experimentally established metal geometry, or authenticated expert review.
- RDKit conformers are **computed models**, not patent-extracted experimental 3D structures.
- PDB contact distances are **proximity screens**, not validated hydrogen bonds or evidence of activity.
- `WO2011103442A2-R001` remains **unverified** and its product structure is deliberately not invented.

Read `docs/PROJECT_VISION.md`, `docs/SCIENTIFIC_QC_CHECKLIST.md`, and `docs/SCIENTIFIC_VALIDATION.md`.
