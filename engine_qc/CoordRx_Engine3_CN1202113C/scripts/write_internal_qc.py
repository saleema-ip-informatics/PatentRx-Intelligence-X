from pathlib import Path
import json,datetime,sys
root=Path(__file__).resolve().parents[1]
out=root/'qc_reports'/'internal_qc_report.json'
if out.exists():raise SystemExit('STOP: existing report preserved')
report={'engine':'CoordRx','patent':'CN1202113C','review_type':'INTERNAL_SCIENTIFIC_QC','status':'PENDING_VERIFIED_RESULTS','automated_case_results':'NOT_RECORDED','project_regression':'NOT_RECORDED','patent_drawing_review':'PENDING','selected_patent_structures_verified':0,'limitations':['SMILES connectivity does not prove coordination geometry','Metal oxidation state not established from SMILES alone','Linkage and geometric isomers require source-specific evidence'],'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('CREATED pending review report:',out)
