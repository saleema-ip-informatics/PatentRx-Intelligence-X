"""PatentRx Intelligence X — Five-engine Streamlit dashboard."""
import json
from pathlib import Path

import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, rdMolDescriptors

from patentrx.workbench import ENGINES, analyze_case
from patentrx.reporting import render_markdown

ROOT = Path(__file__).resolve().parent
CASE_DIR = ROOT / "data" / "workbench_cases"
PATENT_DIR = ROOT / "qc_review" / "WO2011103442A2"

LABELS = {
    "reactionrx": "ReactionRx | Organic Synthesis",
    "stereorx": "StereoRx | Stereochemistry",
    "coordrx": "CoordRx | Metal Coordination",
    "biorx": "BioRx | Biopharma Evidence",
    "markushrx": "MarkushRx | Patent Structures",
}

st.set_page_config(
    page_title="PatentRx Intelligence X",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 PatentRx Intelligence X")
st.caption("Pharmaceutical Patent & Molecular Intelligence Platform")
st.warning(
    "Computational QC is not experimental validation "
    "or authenticated expert review."
)

st.sidebar.header("Scientific Engines")
selected_engine = st.sidebar.radio(
    "Choose an engine",
    ENGINES,
    format_func=lambda engine: LABELS[engine],
)

cases = []
for path in sorted(CASE_DIR.glob("*.json")):
    try:
        case = json.loads(path.read_text(encoding="utf-8"))
        if case.get("engine") == selected_engine:
            cases.append((path, case))
    except (OSError, ValueError):
        continue

tab_analysis, tab_patent, tab_overview = st.tabs([
    "Scientific Analysis",
    "Patent Case Explorer",
    "Platform Overview",
])

with tab_analysis:
    st.header(LABELS[selected_engine])

    if not cases:
        st.info("No cases available for this engine.")
    else:
        index = st.selectbox(
            "Select case",
            range(len(cases)),
            format_func=lambda i: cases[i][1].get(
                "title", cases[i][0].stem
            ),
        )

        path, case = cases[index]
        st.subheader(case.get("title", case["case_id"]))
        st.write(case.get("description", ""))
        st.caption(
            f"Case ID: {case['case_id']} | "
            f"Type: {case.get('case_type', 'unspecified')}"
        )

        smiles = case.get("inputs", {}).get("smiles")
        if smiles:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                left, right = st.columns(2)
                with left:
                    st.image(
                        Draw.MolToImage(mol, size=(500, 300)),
                        caption="RDKit-generated 2D structure",
                    )
                with right:
                    st.write(
                        "**Molecular formula:**",
                        rdMolDescriptors.CalcMolFormula(mol),
                    )
                    st.code(Chem.MolToSmiles(mol))

        try:
            result = analyze_case(case)

            st.subheader("Scientific QC Results")
            st.json(result["computational_outputs"])

            with st.expander("Evidence and limitations"):
                st.json({
                    "source": result["source"],
                    "case_type": result["case_type"],
                    "scientific_review_status":
                        result["scientific_review_status"],
                    "disclaimer": result["disclaimer"],
                })

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Download JSON Report",
                    json.dumps(result, indent=2),
                    file_name=f"{case['case_id']}.json",
                    mime="application/json",
                )
            with col2:
                st.download_button(
                    "Download Markdown Report",
                    render_markdown(result),
                    file_name=f"{case['case_id']}.md",
                    mime="text/markdown",
                )
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")

with tab_patent:
    st.header("WO2011103442A2 — Patent QC Explorer")
    st.info(
        "Patent-derived computational evidence. "
        "Structures and atom mappings remain subject "
        "to expert verification."
    )

    files = {
        "Four-Step Reaction Route":
            "reactionrx_four_step_route.json",
        "Scientific QC Report":
            "reactionrx_qc_report.json",
        "Atom-Mapping Candidates":
            "reactionrx_atom_mapping_candidates.json",
    }

    for label, filename in files.items():
        path = PATENT_DIR / filename
        with st.expander(label):
            if path.exists():
                try:
                    content = json.loads(
                        path.read_text(encoding="utf-8")
                    )
                    if filename == "reactionrx_four_step_route.json":
                        structures = content.get("structures", {})
                        for step in content.get("steps", []):
                            st.markdown(f"### {step['id']}: {step['reactant']} → {step['product']}")
                            left, right = st.columns(2)
                            for column, key in (
                                (left, step["reactant"]),
                                (right, step["product"]),
                            ):
                                with column:
                                    record = structures.get(key, {})
                                    smiles = record.get("smiles", "")
                                    mol = Chem.MolFromSmiles(smiles) if smiles else None
                                    st.write(f"**Compound {key}**")
                                    if mol:
                                        st.image(Draw.MolToImage(mol, size=(420, 250)))
                                        st.code(smiles)
                                        st.caption(record.get("source_status", ""))
                                    else:
                                        st.warning("Structure unavailable")
                            st.write("Reported yield:", step.get("reported_yield_percent"), "%")
                            st.json(step.get("bond_change_assessment", {}))
                        st.divider()
                    st.json(content)
                    st.download_button(
                        f"Download {label}",
                        json.dumps(content, indent=2),
                        file_name=filename,
                        mime="application/json",
                        key=filename,
                    )
                except (OSError, ValueError) as exc:
                    st.error(f"Cannot read {filename}: {exc}")
            else:
                st.warning(f"File not found: {filename}")

with tab_overview:
    st.header("Platform Overview")
    st.write("Five integrated scientific intelligence engines")

    for engine in ENGINES:
        st.write(f"**{LABELS[engine]}**")

    st.divider()
    st.write(
        "Reaction informatics, stereochemical analysis, "
        "coordination chemistry, biopharma evidence QC, "
        "and Markush structure intelligence."
    )
    st.caption(
        "Demonstration data and unverified patent evidence "
        "are explicitly distinguished."
    )
