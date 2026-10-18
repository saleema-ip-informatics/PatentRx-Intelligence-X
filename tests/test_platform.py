import pytest
from patentrx.chemistry import validate_molecule
from patentrx.core.models import Evidence
from patentrx.core.validation import validate_evidence
from patentrx.engines.reactionrx.engine import ReactionRecord,audit_reaction,mapped_bond_edits
from patentrx.engines.stereorx.engine import inspect_stereochemistry
from patentrx.engines.coordrx.engine import inspect_complex
from patentrx.engines.biorx.engine import audit_binding_record
from patentrx.engines.markushrx.engine import audit_markush_example

def codes(report):return {f.code for f in report.findings}
def test_chemistry():assert validate_molecule('CCO')['formula']=='C2H6O'
def test_bad_smiles():assert not validate_molecule('badsmiles')['valid']
def test_reaction_missing():
 r=ReactionRecord('P','R','example',reactants=['CCO']);assert {'MISSING_PRODUCTS','SOURCE_UNVERIFIED'}<=codes(audit_reaction(r))
def test_reaction_invalid_yield():
 r=ReactionRecord('P','R','example',reactants=['CCO'],products=['CC=O'],yield_percent=101);assert 'INVALID_YIELD' in codes(audit_reaction(r))
def test_reaction_valid_fields():
 r=ReactionRecord('P','R','example',reactants=['CCO'],products=['CC=O'],evidence_text='example',source_verified=True,yield_percent=80);assert audit_reaction(r).findings==[]
def test_mapped_edits():
 out=mapped_bond_edits('[CH3:1][CH2:2][OH:3]','[CH3:1].[CH2:2][OH:3]');assert out['broken']==[[1,2]]
def test_mapping_guard():
 with pytest.raises(ValueError):mapped_bond_edits('CC','CC')
def test_stereo():assert inspect_stereochemistry('C[C@H](O)C(=O)O')['centers']
def test_stereo_invalid():assert not inspect_stereochemistry('not_smiles')['valid']
def test_coord():assert inspect_complex('[Pt+2]')['metal_centers'][0]['element']=='Pt'
def test_coord_no_geometry():assert inspect_complex('[Pt+2]')['geometry']=='not_determined'
def test_bio():assert 'UNSUPPORTED_BINDING_CLAIM' in codes(audit_binding_record({'record_id':'x','protein_id':'EGFR','ligand_id':'x','source_reference':'demo','binding_claim':True}))
def test_markush_ok():assert audit_markush_example({'record_id':'x','source_reference':'demo','allowed_substituents':{'R':['H','Me']},'example_substituents':{'R':'Me'}}).findings==[]
def test_markush_bad():assert 'SUBSTITUENT_OUTSIDE_ENUMERATION' in codes(audit_markush_example({'source_reference':'demo','allowed_substituents':{'R':['H']},'example_substituents':{'R':'Me'}}))
def test_expert_review_not_self_certified():
 e=Evidence('x','reactionrx','src','page','claim',review_status='expert_verified',reviewer_id='name');assert any(f.code=='UNAUTHENTICATED_EXPERT_VERIFICATION' for f in validate_evidence(e))
def test_pending_evidence():assert validate_evidence(Evidence('x','reactionrx','src','page','claim'))==[]
