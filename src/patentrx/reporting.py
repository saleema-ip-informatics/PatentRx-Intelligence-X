"""Human-readable, traceable summaries. Not a scientific certification."""
import json
from pathlib import Path

def render_markdown(report:dict)->str:
    lines=[f"# PatentRx QC — {report['case_id']}", '',
        f"**Engine:** {report['engine']}",
        f"**Case type:** {report.get('case_type','unspecified')}",
        f"**Scientific review:** {report['scientific_review_status']}",
        f"**Source:** {report.get('source',{})}",
        f"**Input SHA-256:** {report.get('input_sha256','not supplied')}", '',
        '## Computational outputs', '', '```json',
        json.dumps(report['computational_outputs'],indent=2), '```', '',
        '## Interpretation boundary', '',report['disclaimer']]
    return '\n'.join(lines)+'\n'

def save_markdown(report:dict, path:str|Path)->None:
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(render_markdown(report),encoding='utf-8')
