"""PDB fixed-column protein/ligand proximity QC. No binding or H-bond claims."""
from math import dist

def _atom(line):
    if not line.startswith(('ATOM  ','HETATM')) or len(line)<54: return None
    try:
        return {"record":line[:6].strip(), "name":line[12:16].strip(), "altloc":line[16:17].strip(),
                "resname":line[17:20].strip(), "chain":line[21:22].strip(), "resseq":line[22:26].strip(),
                "xyz":tuple(float(line[i:i+8]) for i in (30,38,46)),
                "occupancy":float(line[54:60]) if len(line)>=60 and line[54:60].strip() else None,
                "element":line[76:78].strip().upper() if len(line)>=78 else ''}
    except ValueError: return None

def audit_pdb_ligand(pdb_text: str, ligand_resname: str, chain: str|None=None, resseq: str|None=None, cutoff_angstrom: float=4.0) -> dict:
    if len(ligand_resname)!=3 or not ligand_resname.isalnum(): raise ValueError('Ligand residue code must have 3 alphanumeric characters')
    if not 0 < cutoff_angstrom <= 10: raise ValueError('Cutoff must be >0 and <=10 Å')
    atoms=[a for line in pdb_text.splitlines() if (a:=_atom(line)) is not None]
    lig=[a for a in atoms if a['record']=='HETATM' and a['resname']==ligand_resname and (chain is None or a['chain']==chain) and (resseq is None or a['resseq']==str(resseq))]
    keys=sorted(set((a['chain'],a['resseq']) for a in lig))
    if len(keys)>1 and (chain is None or resseq is None):
        return {"status":"ambiguous_ligand_instance", "instances":keys,"ligand_atoms":len(lig),"binding_confirmed":False}
    prot=[a for a in atoms if a['record']=='ATOM' and (not a['altloc'] or a['altloc']=='A')]
    lig=[a for a in lig if not a['altloc'] or a['altloc']=='A']
    contacts=[]
    for l in lig:
        for p in prot:
            d=dist(l['xyz'],p['xyz'])
            if d<=cutoff_angstrom:
                contacts.append({"ligand_atom":l['name'],"protein_chain":p['chain'],"protein_resname":p['resname'],"protein_resseq":p['resseq'],"protein_atom":p['name'],"distance_angstrom":round(d,3)})
    contacts.sort(key=lambda x:(x['distance_angstrom'],x['protein_chain'],x['protein_resseq'],x['ligand_atom']))
    return {"status":"coordinates_screened" if lig else "ligand_not_found", "ligand_atoms":len(lig),
            "protein_atoms":len(prot),"contacts":contacts,"contact_count":len(contacts),
            "low_occupancy_ligand_atoms":sum(a['occupancy'] is not None and a['occupancy']<1 for a in lig),
            "binding_confirmed":False,"affinity_inferred":False,
            "limitations":["Distances are proximity observations, not verified hydrogen bonds or affinities", "PDB parser supports fixed-column PDB only, not mmCIF", "Alternate locations other than blank/A excluded", "No symmetry mates, solvent, protonation or electron density assessment"]}
