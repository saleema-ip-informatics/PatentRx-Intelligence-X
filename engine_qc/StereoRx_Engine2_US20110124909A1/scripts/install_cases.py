#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil
parser=argparse.ArgumentParser()
parser.add_argument('project_root',type=Path)
args=parser.parse_args()
root=args.project_root
target=root/'data'/'workbench_cases'
assert (root/'src'/'patentrx'/'workbench.py').is_file(), 'STOP: not a compatible project root'
assert target.is_dir(), 'STOP: workbench_cases directory missing'
sources=sorted((Path(__file__).resolve().parents[1]/'data').glob('*.json'))
destinations=[target/('08_stereo_'+p.name) for p in sources]
assert all(not d.exists() for d in destinations), 'STOP: at least one destination already exists; no files copied'
for src,dst in zip(sources,destinations):
    shutil.copy2(src,dst)
    print('CREATED',dst)
print('PASS: only new StereoRx case files copied')
