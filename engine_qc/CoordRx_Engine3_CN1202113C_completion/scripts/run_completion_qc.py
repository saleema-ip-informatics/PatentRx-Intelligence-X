"""Non-destructive CoordRx internal QC runner; creates report only if all checks pass."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
EXISTING = REPO / 'engine_qc' / 'CoordRx_Engine3_CN1202113C'
REPORT = ROOT / 'internal_qc_result.json'

def run(label, args):
    print(f'\n=== {label} ===', flush=True)
    result = subprocess.run([sys.executable, *args], cwd=REPO, check=False)
    if result.returncode:
        raise SystemExit(f'STOP: {label} failed (exit {result.returncode}); no PASS report created')

if REPORT.exists():
    raise SystemExit('STOP: report exists; nothing overwritten')
assert EXISTING.is_dir(), f'Missing existing package: {EXISTING}'
assert (EXISTING / 'patent_evidence' / 'CN1202113C.pdf').is_file(), 'Patent PDF missing'
reference = json.loads((ROOT / 'patent_evidence' / 'experimental_reference.json').read_text(encoding='utf-8'))
assert len(reference['examples']) == 12
assert all(15 <= e['pdf_page'] <= 20 for e in reference['examples'])
run('Existing 7-case validator', [str(EXISTING / 'scripts' / 'validate_cases.py')])
run('CoordRx additional controls', ['-m', 'pytest', '-q', str(ROOT / 'tests' / 'test_coordrx_internal.py')])
run('Project regression suite', ['-m', 'pytest', '-q', 'tests'])
report = {
    'engine': 'CoordRx', 'patent': 'CN1202113C',
    'status': 'INTERNAL_QC_PASS',
    'scope': 'existing engine metal detection, explicitly encoded neighbor checks, and project regression',
    'existing_case_validation': 'PASS', 'additional_controls': 'PASS',
    'project_regression': 'PASS', 'reference_examples': len(reference['examples']),
    'patent_pdf_present': True,
    'patent_structure_mapping': 'NOT_FULLY_VALIDATED',
    'cis_trans_geometry_prediction': 'NOT_SUPPORTED',
    'ncs_linkage_from_spectra': 'PATENT_REPORTED_ONLY',
    'limitations': reference['limitations']
}
REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('\nCREATED:', REPORT)
print('STATUS: INTERNAL_QC_PASS (limited scope; see report)')
