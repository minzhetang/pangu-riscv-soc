from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
OLD=H/'UNUSED_BASELINE_NOT_AUTHORIZED'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    d=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):d.update(b)
    return d.hexdigest().upper()
def log(p):
    data=Path(p).read_bytes();assert len(data)<=8*1024*1024
    return data.decode('utf-8-sig').replace('\r\n','\n')
