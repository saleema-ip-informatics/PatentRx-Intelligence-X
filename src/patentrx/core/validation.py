from .models import Evidence, Finding

ENGINES = {"reactionrx", "stereorx", "coordrx", "biorx", "markushrx"}
STATUSES = {"pending_review", "expert_verified", "rejected", "unresolved"}

def validate_evidence(record: Evidence) -> list[Finding]:
    issues = []
    if record.engine not in ENGINES:
        issues.append(Finding("INVALID_ENGINE", "high", "Unknown engine", record.evidence_id))
    if record.review_status not in STATUSES:
        issues.append(Finding("INVALID_REVIEW_STATUS", "high", "Unknown review status", record.evidence_id))
    for key in ("evidence_id", "source_id", "source_reference", "claim"):
        if not str(getattr(record, key)).strip():
            issues.append(Finding("MISSING_" + key.upper(), "high", f"Missing {key}", record.evidence_id))
    if record.review_status == "expert_verified":
        issues.append(Finding("UNAUTHENTICATED_EXPERT_VERIFICATION", "high", "This MVP has no authenticated expert-review workflow; label cannot be accepted", record.evidence_id))
    return issues
