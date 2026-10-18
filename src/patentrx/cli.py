import argparse,json
from dataclasses import asdict
from pathlib import Path
from patentrx.chemistry import validate_molecule
from patentrx.core.models import Evidence
from patentrx.core.validation import validate_evidence
from patentrx.engines.reactionrx.engine import ReactionRecord,audit_reaction
from patentrx.engines.stereorx.engine import inspect_stereochemistry
from patentrx.engines.coordrx.engine import inspect_complex
from patentrx.engines.biorx.engine import audit_binding_record
from patentrx.engines.markushrx.engine import audit_markush_example

def main():
    p=argparse.ArgumentParser(prog='patentrx')
    s=p.add_subparsers(dest='command',required=True)
    s.add_parser('demo')
    for name in ('audit','validate-evidence','stereo','coord','bio','markush','molecule'):
        a=s.add_parser(name);a.add_argument('input')
    a=p.parse_args()
    if a.command=='demo':
        print(json.dumps({'molecule':validate_molecule('CCO'),'stereo':inspect_stereochemistry('C[C@H](O)C(=O)O'),'engines':['reactionrx','stereorx','coordrx','biorx','markushrx']},indent=2));return
    if a.command in ('stereo','coord','molecule'):
        out={'stereo':inspect_stereochemistry,'coord':inspect_complex,'molecule':validate_molecule}[a.command](a.input)
    else:
        d=json.loads(Path(a.input).read_text(encoding='utf8'))
        if a.command=='audit':out=audit_reaction(ReactionRecord(**d)).to_dict()
        elif a.command=='validate-evidence':out=[asdict(f) for f in validate_evidence(Evidence(**d))]
        elif a.command=='bio':out=audit_binding_record(d).to_dict()
        else:out=audit_markush_example(d).to_dict()
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
