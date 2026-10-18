from patentrx.core.models import Finding,AuditReport

def audit_binding_record(record: dict) -> AuditReport:
    f=[]
    for key in ("record_id","protein_id","ligand_id","source_reference"):
        if not str(record.get(key,"")).strip():f.append(Finding("MISSING_"+key.upper(),"high",f"Missing {key}"))
    if not record.get('experimental_method'):
        f.append(Finding("METHOD_UNSPECIFIED","medium","No experimental method given"))
    if not record.get('structure_id'):
        f.append(Finding("NO_STRUCTURE_ID","medium","No PDB/mmCIF structure reference"))
    if record.get('binding_claim') and not record.get('assay_evidence'):
        f.append(Finding("UNSUPPORTED_BINDING_CLAIM","high","Binding claim lacks assay evidence"))
    return AuditReport("biorx",str(record.get('record_id','unknown')),f)
