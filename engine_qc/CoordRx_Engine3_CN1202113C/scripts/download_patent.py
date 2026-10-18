from pathlib import Path
from urllib.request import Request, urlopen
import sys

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'patent_evidence' / 'CN1202113C.pdf'
url = 'https://patentimages.storage.googleapis.com/90/81/f0/9faeb3309f669f/CN1202113C.pdf'
if out.exists():
    print('PRESERVED existing PDF:', out)
    sys.exit(0)
try:
    with urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=45) as response:
        data = response.read()
    if not data.startswith(b'%PDF-'):
        raise ValueError('Response is not a PDF')
    out.write_bytes(data)
    print('DOWNLOADED:', out, 'bytes:', len(data))
except Exception as exc:
    print('DOWNLOAD FAILED:', exc)
    print('Download manually from:', url)
    sys.exit(1)
