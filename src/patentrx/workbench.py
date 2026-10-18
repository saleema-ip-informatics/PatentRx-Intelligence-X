"""Unified, conservative scientific workbench for five existing engines.

A report's status describes computational checks, never experimental verification.
"""
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import Descriptors
from patentrx.core.models import Evidence
from patentrx.core.validation import validate_evidence
from patentrx.engines.reactionrx.engine import ReactionRecord, audit_reaction
from patentrx.engines.reactionrx.advanced import audit_atom_mapping
from patentrx.engines.stereorx.engine import inspect_stereochemistry
from patentrx.engines.stereorx.qc3d import audit_organic_3d
from patentrx.engines.coordrx.engine import inspect_complex
from patentrx.engines.coordrx.advanced import coordination_bond_inventory
from patentrx.engines.coordrx.qc3d import audit_metal_coordinates
from patentrx.engines.biorx.engine import audit_binding_record
from patentrx.engines.biorx.qc_structure import audit_pdb_ligand
from patentrx.engines.markushrx.engine import audit_markush_example
from patentrx.engines.markushrx.advanced import match_enumerated_structures

ENGINES=('reactionrx','stereorx','coordrx','biorx','markushrx')

def analyze_case(case: dict) -> dict:
    """Analyze one explicitly typed case; no network access, no inferred provenance."""
    if not isinstance(case,dict): raise ValueError('Case must be an object')
    engine=case.get('engine')
    if engine not in ENGINES: raise ValueError('Unknown engine')
    inputs=case.get('inputs')
    if not isinstance(inputs,dict): raise ValueError('inputs must be an object')
    cid=str(case.get('case_id','')).strip()
    if not cid: raise ValueError('case_id required')
    source=case.get('source',{})
    if not isinstance(source,dict): raise ValueError('source must be an object')
    outputs={}
    if engine=='reactionrx':
        r=ReactionRecord(**inputs['reaction'])
        outputs['record_qc']=audit_reaction(r).to_dict()
        if 'mapped_reactants' in inputs and 'mapped_products' in inputs:
            outputs['atom_map_qc']=audit_atom_mapping(inputs['mapped_reactants'],inputs['mapped_products'])
    elif engine=='stereorx':
        s=inputs['smiles']
        outputs['stereochemistry']=inspect_stereochemistry(s)
        if inputs.get('compute_3d',False):
            outputs['computed_3d']=audit_organic_3d(s)
    elif engine=='coordrx':
        outputs['connectivity']=inspect_complex(inputs['smiles'])
        outputs['bond_inventory']=coordination_bond_inventory(inputs['smiles'])
        if 'molblock_3d' in inputs:
            outputs['coordinate_qc']=audit_metal_coordinates(inputs['molblock_3d'])
    elif engine=='biorx':
        outputs['evidence_qc']=audit_binding_record(inputs['binding_record']).to_dict()
        if 'pdb_text' in inputs:
            outputs['structure_qc']=audit_pdb_ligand(inputs['pdb_text'],inputs['ligand_resname'],
                chain=inputs.get('chain'),resseq=inputs.get('resseq'))
    elif engine=='markushrx':
        outputs['substituent_qc']=audit_markush_example(inputs['markush_record']).to_dict()
        if 'example_smiles' in inputs:
            outputs['exact_enumeration']=match_enumerated_structures(inputs['example_smiles'],inputs['enumerated_smiles'])
    evidence=case.get('evidence')
    if evidence is not None:
        outputs['evidence_validation']=[asdict(f) for f in validate_evidence(Evidence(**evidence))]
    return {'case_id':cid,'engine':engine,'case_type':case.get('case_type','demonstration'),
            'source':source,'scientific_review_status':'not_expert_verified',
            'computational_outputs':outputs,
            'disclaimer':'Automated QC is not experimental or authenticated expert verification.'}

def analyze_file(path: str | Path) -> dict:
    path=Path(path)
    data=path.read_bytes()
    case=json.loads(data)
    result=analyze_case(case)
    result['input_sha256']=hashlib.sha256(data).hexdigest()
    return result

def save_report(case_path: str | Path, report_path: str | Path) -> dict:
    result=analyze_file(case_path)
    out=Path(report_path)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return result
