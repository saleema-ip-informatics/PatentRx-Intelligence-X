import math

def pic50_from_nm(value):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<=0: raise ValueError('IC50 must be finite positive nM')
    return 9-math.log10(value)

def fold_difference(reference_nm,other_nm):
    pic50_from_nm(reference_nm);pic50_from_nm(other_nm)
    return other_nm/reference_nm

def comparable(a,b):
    return a.get('assay')==b.get('assay') and a.get('target')==b.get('target')
