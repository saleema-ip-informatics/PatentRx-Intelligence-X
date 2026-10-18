from dataclasses import dataclass, field
from rdkit import Chem
from patentrx.core.models import AuditReport, Finding

@dataclass
class ReactionRecord:
    patent_id: str
    reaction_id: str
    source_reference: str
    reactants: list[str] = field(default_factory=list)
    products: list[str] = field(default_factory=list)
    reagents: list[str] = field(default_factory=list)
    catalysts: list[str] = field(default_factory=list)
    solvents: list[str] = field(default_factory=list)
    temperature_c: float | None = None
    reaction_time_h: float | None = None
    yield_percent: float | None = None
    evidence_text: str = ""
    qc_status: str = "pending_review"
    source_verified: bool = False

def audit_reaction(r: ReactionRecord) -> AuditReport:
    f=[]
    def add(code, severity, msg):f.append(Finding(code,severity,msg))
    if not r.reactants:add("MISSING_REACTANTS","high","No reactants recorded")
    if not r.products:add("MISSING_PRODUCTS","high","No products recorded")
    if not r.source_reference.strip():add("MISSING_SOURCE","high","No source reference")
    if not r.evidence_text.strip():add("MISSING_EVIDENCE_TEXT","medium","No supporting excerpt")
    if r.yield_percent is not None and not 0 <= r.yield_percent <= 100:add("INVALID_YIELD","high","Yield outside 0–100%")
    if r.reaction_time_h is not None and r.reaction_time_h < 0:add("INVALID_TIME","high","Negative reaction duration")
    if not r.source_verified:add("SOURCE_UNVERIFIED","medium","Source transcription not independently verified")
    return AuditReport("reactionrx",r.reaction_id,f)

def mapped_bond_edits(reactant_smiles: str, product_smiles: str) -> dict:
    """Report bond edits only for explicitly atom-mapped molecules with identical map-number sets."""
    def bonds(smiles):
        mol=Chem.MolFromSmiles(smiles)
        if mol is None:raise ValueError("Invalid mapped SMILES")
        nums=[a.GetAtomMapNum() for a in mol.GetAtoms()]
        if any(n==0 for n in nums) or len(set(nums))!=len(nums):raise ValueError("All atoms need unique positive map numbers")
        edges={tuple(sorted((b.GetBeginAtom().GetAtomMapNum(),b.GetEndAtom().GetAtomMapNum()))):str(b.GetBondType()) for b in mol.GetBonds()}
        return set(nums),edges
    rset,rb=bonds(reactant_smiles);pset,pb=bonds(product_smiles)
    if rset!=pset:raise ValueError("Atom map sets must match; no added/deleted atoms supported")
    return {"formed":sorted([list(k) for k in pb.keys()-rb.keys()]),"broken":sorted([list(k) for k in rb.keys()-pb.keys()]),"order_changed":sorted([{"atoms":list(k),"from":rb[k],"to":pb[k]} for k in rb.keys()&pb.keys() if rb[k]!=pb[k]],key=lambda x:x['atoms'])}
