# PatentRx Intelligence X — Quick Start

## Requirements
- Python 3.10 or newer
- Internet access for initial dependency installation

## Installation

Open a terminal in the extracted project folder.

Windows:
```bash
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dashboard,dev]"
```

## Launch dashboard

```bash
.venv/Scripts/python -m streamlit run app.py
```

Open http://localhost:8501

## Run tests

```bash
.venv/Scripts/python -m pytest tests/ -q
```

## Scientific engines

1. ReactionRx — Organic reaction analysis
2. StereoRx — Stereochemical analysis
3. CoordRx — Metal coordination analysis
4. BioRx — Biopharma evidence QC
5. MarkushRx — Patent structure analysis

## Patent case study

WO2011103442A2 includes a four-step route leading
to phosphonate intermediate 11.

Patent-derived structure interpretations and local
bond-change assessments are not authenticated
experimental validation.

Full atom mapping and expert sign-off remain pending.

## Reports

The dashboard supports JSON and Markdown report downloads.

## Scientific limitations

Synthetic demonstrations are not patent-derived evidence.
Computational QC does not replace source verification,
experimental validation, or expert scientific review.
