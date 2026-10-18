# PatentRx Intelligence X

**A Python/RDKit workbench that turns pharmaceutical patent content into structured, auditable scientific QC reports.**
Five engines, five real patents, one shared workflow, built by a patent-informatics professional with 16+ years of experience.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![RDKit](https://img.shields.io/badge/RDKit-cheminformatics-green)
![Tests](https://img.shields.io/badge/tests-63%2F63%20passing-brightgreen)
<!-- TODO: replace the Tests badge with a GitHub Actions badge once CI is set up:
[![CI](https://github.com/saleema-ip-informatics/PatentRx-Intelligence-X/actions/workflows/ci.yml/badge.svg)](https://github.com/saleema-ip-informatics/PatentRx-Intelligence-X/actions) -->

---

## Project Summary

PatentRx Intelligence X is a modular scientific QC platform for pharmaceutical patent analysis. Instead of processing molecules in isolation, it combines chemical reasoning, patent evidence, molecular validation and structured reporting.

It covers:

- Organic reaction and atom-mapping analysis
- Stereochemistry and chirality validation
- Metal-complex connectivity screening
- Patent-derived bioactivity normalization
- Exact molecular identity and bounded Markush analysis
- Reproducible QC reports with evidence documentation

Five real patents serve as scientific reference cases, alongside synthetic demonstration records and computational controls.

**Validation:** 63/63 pytest regression tests passed on October 18, 2026.

## The Five Engines

| Engine | Reference patent | Focus | QC result |
|---|---|---|---|
| **ReactionRx** | WO2011103442A2 | Reaction pathways, atom mapping, bond changes | Defined computational QC completed |
| **StereoRx** | US20110124909A1 | CIP R/S assignment, enantiomer differentiation | Computational QC passed |
| **CoordRx** | CN1202113C | Ruthenium complexes, metal-ligand connectivity | Internal QC passed (limited scope) |
| **BioRx** | EP3567030B1 | EGFR assay extraction, IC50 normalization | Internal QC passed (assay and evidence processing) |
| **MarkushRx** | US7569577B2 | Exact stereospecific matching, substituent controls | Internal QC passed; 5/5 structural controls |

### 1. ReactionRx: Organic Reaction Intelligence

Reaction parsing and validation, atom correspondence and reaction-center analysis, bond-change checks, a four-step patent route analysis, and provenance tracking.

**Scope:** computational reaction and structure-consistency checks. The demonstration record `WO2011103442A2-R001` is explicitly unverified. [One sentence on what the open item is, e.g. what evidence is missing before it can be marked verified.]

### 2. StereoRx: Stereochemistry Intelligence

Stereocenter detection, CIP R/S assignment, enantiomer differentiation, detection of unspecified stereochemistry, and conformer comparison.

**Case:** S-pregabalin compared against R-pregabalin and an unspecified-stereochemistry control.

### 3. CoordRx: Coordination Chemistry Intelligence

Metal atom recognition, ligand and connectivity screening, disconnected-component detection, positive and negative coordination controls, and computational 3D structural screening.

**Scope:** connectivity and structural screening only. It does not establish experimental coordination geometry, oxidation states, or full authentication of the patent structure.

### 4. BioRx: Bioactivity and Patent Evidence Intelligence

Assay table extraction, IC50 normalization, potency calculations, handling of exact, censored and missing values, compound example indexing, and a source-linked evidence inventory.

**Dataset:** 34 compounds, 5 assay endpoints, 170 assay measurement cells (EGFR wild-type, EGFR mutant and cellular assays).

**Scope:** patent-derived assay normalization and consistency. It does not reproduce biological activity or fully verify structure-to-assay mapping.

### 5. MarkushRx: Patent Structure Intelligence

Canonical SMILES processing, exact molecular identity matching, stereochemical comparison, substituent variation controls, and formula/mass consistency checks.

**Case:** Example 35, the (2S) quinazoline parent compound.

- 5/5 patent-specific structural controls passed
- S vs R stereochemistry distinguished
- Unspecified stereochemistry rejected as an exact stereospecific match
- Substituent-modified and unrelated structures rejected
- Calculated [M+H]⁺ ≈ 475.154, consistent with the patent's reported nominal m/z 475

**Scope:** exact parent-structure matching. It is not generic Markush enumeration or a legal claim-coverage determination.

## Example Output

<!-- TODO: paste a trimmed real QC report here, e.g. from reports/reaction.json -->

```json
{
  "case_id": "...",
  "engine": "...",
  "status": "...",
  "findings": [],
  "evidence": []
}
```

## Dashboard

<!-- TODO: add a Streamlit screenshot, e.g. ![Dashboard](docs/images/dashboard.png) -->

## Technology Stack

```text
Language           Python
Cheminformatics    RDKit
Chemical naming    OPSIN
Data               JSON, structured patent evidence
Molecular analysis SMILES, SMARTS, CIP stereochemistry
Reaction analysis  Atom mapping, bond changes, reaction centers
3D chemistry       RDKit conformers
Quality control    Pytest, positive/negative controls, regression tests
Interface          Streamlit (optional)
Reporting          JSON and Markdown QC reports
Version control    Git and GitHub
```

## Repository Structure

```text
PatentRx_Intelligence_X_COMPLETE/
├── README.md
├── QUICK_START.md
├── README_QC_PACKAGE.md
├── pyproject.toml
├── app.py
├── src/patentrx/
│   ├── core/
│   ├── engines/
│   │   ├── reactionrx/
│   │   ├── stereorx/
│   │   ├── coordrx/
│   │   ├── biorx/
│   │   └── markushrx/
│   ├── workbench.py
│   ├── workbench_cli.py
│   └── reporting.py
├── engine_qc/
│   ├── BioRx_Engine4_EP3567030B1/
│   ├── CoordRx_Engine3_CN1202113C/
│   ├── CoordRx_Engine3_CN1202113C_completion/
│   ├── MarkushRx_Engine5_US7569577B2/
│   └── StereoRx_Engine2_US20110124909A1/
├── qc_review/WO2011103442A2/
├── data/
│   ├── examples/
│   ├── patent_cases/
│   └── workbench_cases/
├── docs/
│   ├── INTEGRATION.md
│   ├── PROJECT_VISION.md
│   ├── QC_WORKFLOWS.md
│   ├── SCIENTIFIC_QC_CHECKLIST.md
│   └── SCIENTIFIC_VALIDATION.md
├── tests/
│   ├── test_advanced.py
│   ├── test_platform.py
│   ├── test_structure_qc.py
│   └── test_workbench.py
└── tools/opsin/
```

## Scientific Workflow

```text
        Pharmaceutical patent / molecular data
                        |
                        v
             Source evidence preparation
                        |
                        v
              Chemical structure parsing
                        |
            +-----------+-----------+
            |           |           |
            v           v           v
       ReactionRx    StereoRx    CoordRx
            |           |           |
            +-----------+-----------+
                        |
                +-------+-------+
                |               |
                v               v
              BioRx         MarkushRx
                |               |
                +-------+-------+
                        |
                        v
             RDKit scientific QC checks
                        |
                        v
           Patent evidence consistency
                        |
                        v
             JSON / Markdown QC report
```

The engines can be used independently. The diagram shows the shared workbench flow, not a requirement that every case pass through all five.

## Installation and Quick Start

**1. Clone** (access requires permission while the repository is private)

```bash
git clone https://github.com/saleema-ip-informatics/PatentRx-Intelligence-X.git
cd PatentRx-Intelligence-X
```

**2. Create a virtual environment**

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (Git Bash)
source .venv/Scripts/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

**3. Install**

```bash
python -m pip install -e .
```

**4. Run the tests**

```bash
python -m pytest -q
```

**5. Run a QC example**

```bash
python -m patentrx.workbench_cli \
  data/workbench_cases/01_reaction_demo.json \
  --output reports/reaction.json \
  --markdown reports/reaction.md
```

**6. Launch the optional dashboard**

```bash
python -m pip install -e '.[dashboard]'
streamlit run app.py
```

## Validation Results

| Metric | Result |
|---|---|
| Framework | Pytest |
| Tests executed | 63 |
| Tests passed | 63 |
| Tests failed | 0 |
| Test date | October 18, 2026 |

These results show that the tested functions behave as expected under the defined cases. They do not establish comprehensive scientific or experimental validation.

## Evidence and Traceability

Each reference case keeps its supporting records: patent PDF sources and metadata, structure representations, reaction and stereochemistry controls, assay normalization records, molecular identity checks, QC results, and documented limitations. Evidence files are organized by engine under `engine_qc/`.

## Scope and Limitations

This is a computational QC and research portfolio project. It does not claim:

- Legal interpretation of patent claims
- Full generic Markush enumeration
- Experimentally validated molecular geometry
- Experimental verification of every patent structure
- Confirmed biological activity beyond the source-reported measurements
- Independent certification or laboratory validation

RDKit conformers are computational models. All QC statuses are limited to their documented acceptance criteria.

## Applications and Future Scope

Relevant to pharmaceutical patent intelligence, reaction data curation, cheminformatics, scientific AI response evaluation, bioactivity evidence normalization and molecular data benchmarking.

Possible extensions (not implemented): additional patent-supported cases, broader chemical validation methods, and improved automated evidence reporting.

## About the Developer

Built by a pharmaceutical patent and chemical informatics professional with 16+ years of industry experience in patent analysis, structure drawing and validation, reaction extraction, Markush and scaffold analysis, RDKit/Python cheminformatics, and scientific data QC.

PatentRx Intelligence X pairs that domain expertise with reproducible scientific software, to make pharmaceutical patent data more structured, chemically interpretable and auditable.
