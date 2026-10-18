"""Unified CLI: python -m patentrx.workbench_cli ..."""
import argparse,json
from pathlib import Path
from patentrx.workbench import analyze_file,save_report
from patentrx.reporting import save_markdown

def main():
    p=argparse.ArgumentParser(description='PatentRx five-engine QC workbench')
    p.add_argument('case',help='Path to case JSON')
    p.add_argument('--output',help='JSON report path')
    p.add_argument('--markdown',help='Markdown report path')
    a=p.parse_args()
    result=save_report(a.case,a.output) if a.output else analyze_file(a.case)
    if a.markdown:save_markdown(result,a.markdown)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
