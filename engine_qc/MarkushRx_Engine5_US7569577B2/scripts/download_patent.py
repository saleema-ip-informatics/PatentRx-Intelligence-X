from pathlib import Path
from urllib.request import urlopen, Request
import re
ROOT=Path(__file__).resolve().parents[1]
PATENT=ROOT.name.split('_')[-1]
page=f'https://patents.google.com/patent/{PATENT}/en'
html=urlopen(Request(page,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8','replace')
match=re.search(r'<meta[^>]*citation_pdf_url[^>]*content="([^"]+)"',html)
if not match:
    match=re.search(r'<meta[^>]*content="([^"]+)"[^>]*citation_pdf_url',html)
if not match:
    raise SystemExit('PDF URL not found; download PDF manually from '+page)
url=match.group(1).replace('&amp;','&')
out=ROOT/'patent_evidence'/f'{PATENT}.pdf'
if out.exists(): raise SystemExit('STOP: PDF exists; no overwrite: '+str(out))
raw=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read()
if not raw.startswith(b'%PDF'): raise SystemExit('Downloaded data is not a PDF')
out.write_bytes(raw)
print('DOWNLOADED:',out,'bytes:',len(raw))
