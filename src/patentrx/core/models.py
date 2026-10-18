from dataclasses import dataclass, field, asdict
from typing import Literal

Engine = Literal["reactionrx", "stereorx", "coordrx", "biorx", "markushrx"]
ReviewStatus = Literal["pending_review", "expert_verified", "rejected", "unresolved"]

@dataclass
class Evidence:
    evidence_id: str
    engine: Engine
    source_id: str
    source_reference: str
    claim: str
    evidence_text: str = ""
    review_status: ReviewStatus = "pending_review"
    reviewer_id: str = ""
    reviewer_notes: str = ""
    source_kind: str = "unspecified"

@dataclass
class Finding:
    code: str
    severity: str
    message: str
    evidence_id: str = ""

@dataclass
class AuditReport:
    engine: str
    record_id: str
    findings: list[Finding] = field(default_factory=list)
    def to_dict(self):
        return asdict(self)
