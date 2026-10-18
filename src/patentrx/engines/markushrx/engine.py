from patentrx.core.models import AuditReport,Finding

def audit_markush_example(record: dict) -> AuditReport:
    f=[]
    allowed=record.get('allowed_substituents',{})
    selected=record.get('example_substituents',{})
    for label,value in selected.items():
        if label not in allowed:
            f.append(Finding('UNKNOWN_R_GROUP','high',f'{label} not declared'))
        elif value not in allowed[label]:
            f.append(Finding('SUBSTITUENT_OUTSIDE_ENUMERATION','high',f'{label}={value} not enumerated'))
    for label in allowed:
        if label not in selected:f.append(Finding('MISSING_R_GROUP','medium',f'{label} not assigned'))
    if not record.get('source_reference'):
        f.append(Finding('MISSING_SOURCE','high','No source claim/example reference'))
    return AuditReport('markushrx',str(record.get('record_id','unknown')),f)
