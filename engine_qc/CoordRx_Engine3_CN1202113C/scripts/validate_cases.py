from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[1]
try:
    from patentrx.engines.coordrx.engine import inspect_complex
except ImportError:
    repo=root.parents[1]
    sys.path.insert(0,str(repo/'src'))
    from patentrx.engines.coordrx.engine import inspect_complex

failures=[]
for p in sorted((root/'data').glob('*.json')):
    c=json.loads(p.read_text(encoding='utf-8'))
    out=inspect_complex(c['inputs']['smiles'])
    exp=c['expected']
    checks=[out.get('valid')==exp['valid']]
    if exp['valid']:
        metals=out.get('metal_centers',[])
        checks.append(len(metals)==exp['metal_count'])
        checks.append(out.get('geometry')==exp['geometry'])
        if exp['metal_element'] is not None and metals:
            checks.append(metals[0]['element']==exp['metal_element'])
            checks.append(len(metals[0]['explicit_neighbors'])==exp['first_metal_explicit_neighbor_count'])
    passed=all(checks)
    print(('PASS' if passed else 'FAIL'),c['case_id'])
    if not passed:failures.append(c['case_id'])
print(f'{len(list((root/"data").glob("*.json")))-len(failures)}/{len(list((root/"data").glob("*.json")))} passed')
if failures:sys.exit(1)
