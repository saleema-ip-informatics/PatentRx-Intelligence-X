from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
workbench=repo/'src'/'patentrx'/'workbench.py'
if not workbench.exists():
    raise SystemExit('STOP: cannot locate project src/patentrx/workbench.py')
text=workbench.read_text(encoding='utf-8')
if 'coordrx' not in text:
    raise SystemExit('STOP: workbench has no coordrx branch; inspect before integrating')
target=repo/'data'/'workbench_cases'
if not target.is_dir():
    raise SystemExit('STOP: data/workbench_cases directory not found')
files=sorted((root/'data').glob('*.json'))
for p in files:
    dest=target/('09_coord_'+p.name)
    if dest.exists():
        raise SystemExit(f'STOP: existing target would be overwritten: {dest}')
for p in files:
    dest=target/('09_coord_'+p.name)
    obj=json.loads(p.read_text(encoding='utf-8'))
    case={'case_id':'09_coord_'+obj['case_id'],'engine':'coordrx','inputs':obj['inputs'],'source':{'patent':'CN1202113C','source_verified':False,'provenance':obj['provenance']}}
    with dest.open('x',encoding='utf-8') as f:
        json.dump(case,f,indent=2)
        f.write('\n')
    print('CREATED:',dest)
print('PASS: created new controls only; existing cases preserved')
