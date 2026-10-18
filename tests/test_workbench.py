import json
from pathlib import Path
import pytest
from patentrx.workbench import analyze_case,analyze_file,save_report,ENGINES
from patentrx.reporting import render_markdown
ROOT=Path(__file__).resolve().parents[1]
CASES=sorted((ROOT/'data'/'workbench_cases').glob('*.json'))

@pytest.mark.parametrize('path',CASES,ids=lambda p:p.stem)
def test_each_engine_case(path):
    result=analyze_file(path)
    assert result['engine'] in ENGINES
    assert result['scientific_review_status']=='not_expert_verified'
    assert len(result['input_sha256'])==64
    assert result['computational_outputs']

@pytest.mark.parametrize('engine',ENGINES)
def test_each_engine_is_represented(engine):
    assert any(json.loads(p.read_text())['engine']==engine for p in CASES)

def test_unverified_patent_remains_unverified():
    report=analyze_file(ROOT/'data/workbench_cases/06_patent_unverified.json')
    assert report['case_type']=='unverified_patent_transcription'
    codes=[f['code'] for f in report['computational_outputs']['record_qc']['findings']]
    assert 'MISSING_PRODUCTS' in codes
    assert 'SOURCE_UNVERIFIED' in codes

def test_report_export(tmp_path):
    out=tmp_path/'qc.json'
    result=save_report(CASES[0],out)
    assert json.loads(out.read_text())['case_id']==result['case_id']
    md=render_markdown(result)
    assert 'not_expert_verified' in md
    assert 'Computational outputs' in md

def test_reject_unknown_engine():
    with pytest.raises(ValueError,match='Unknown engine'):
        analyze_case({'case_id':'x','engine':'imaginary','inputs':{}})

def test_reject_missing_case_id():
    with pytest.raises(ValueError,match='case_id required'):
        analyze_case({'engine':'stereorx','inputs':{'smiles':'CCO'}})
