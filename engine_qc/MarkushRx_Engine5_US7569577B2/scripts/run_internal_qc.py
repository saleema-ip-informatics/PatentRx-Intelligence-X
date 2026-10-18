from pathlib import Path
import json,subprocess,sys,importlib.util,hashlib
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
manifest=json.loads((ROOT/'manifest.json').read_text())
source=json.loads((ROOT/'patent_evidence/source_review.json').read_text())
checks={}
def run(label,cmd):
    print('\n===',label,'===',flush=True)
    p=subprocess.run(cmd,cwd=PROJECT)
    checks[label]={'exit_code':p.returncode,'passed':p.returncode==0}
    return p.returncode==0
ok=run('scientific_controls',[sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-p','test_*.py','-v'])
engine=manifest['engine']
print('\n=== existing engine import ===',flush=True)
spec=importlib.util.find_spec(f'patentrx.engines.{engine}.engine')
checks['engine_import']={'passed':spec is not None,'module':f'patentrx.engines.{engine}.engine'}
if spec is None: ok=False
else: print('PASS:',spec.origin)
if (PROJECT/'tests').is_dir(): ok=run('project_regression',[sys.executable,'-m','pytest','-q','tests']) and ok
else:
    checks['project_regression']={'passed':False,'error':'Project tests directory not found'};ok=False
pdf=ROOT/'patent_evidence'/f"{manifest['patent']}.pdf"
checks['patent_pdf']={'present':pdf.is_file(),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.is_file() else None}
checks['patent_source_review']={'complete':source.get('source_review_complete') is True,'structure_records':len(source.get('structure_records',[])),'assay_records':len(source.get('assay_records',[])),'claim_rules':len(source.get('claim_rules',[]))}
status='INTERNAL_QC_PASS' if ok and checks['patent_pdf']['present'] and checks['patent_source_review']['complete'] else ('COMPUTATIONAL_QC_PASS_SOURCE_REVIEW_PENDING' if ok else 'QC_FAIL')
report={'engine':engine,'patent':manifest['patent'],'status':status,'checks':checks,'limitations':['Automated controls do not prove patent structure/assay/claim mappings','Engine functionality beyond tested controls is not certified']}
out=ROOT/'reports/internal_qc_result.json'
if out.exists():
    print('STOP: report exists; preserving original:',out)
else:
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('CREATED:',out)
print('STATUS:',status)
if not ok: sys.exit(1)
