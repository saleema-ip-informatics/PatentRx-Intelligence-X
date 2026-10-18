from rdkit import Chem
CORE=Chem.MolFromSmiles('c1ccc2ncncc2c1')

def core_screen(smiles):
    mol=Chem.MolFromSmiles(smiles)
    if mol is None: return {'valid':False,'has_quinazoline_core':False}
    return {'valid':True,'has_quinazoline_core':bool(mol.HasSubstructMatch(CORE))}
