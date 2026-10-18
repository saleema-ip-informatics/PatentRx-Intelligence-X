# Safe integration into your current D:\PatentRx-Intelligence

This ZIP is a separate working baseline. It does not contain or overwrite your existing project or the downloaded 150-page patent PDF.

1. Extract ZIP to `D:\PatentRx-Intelligence-X-MVP` (not your existing folder).
2. Activate your existing virtual environment, or make a new one.
3. `python -m pip install -e '.[dev]'` and `python -m pytest -q` in the extracted folder.
4. Compare modules and tests with your existing `D:\PatentRx-Intelligence` before merging.
5. Preserve `data/patents/pdfs/WO2011103442A2.pdf`, `source_extraction.csv`, and `R001.json` in your original workspace. They are **not** bundled here.

The original R001 is pending structure verification. The candidate regioisomer SMILES are not assigned as verified products.
