from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
items=json.loads((H/'SHA256SUMS.json').read_text());bad=[]
for a in items:
 p=H/a['path']
 if not p.is_file() or p.stat().st_size!=a['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=a['sha256']:bad.append(a['path'])
print(json.dumps(dict(items=len(items),mismatch=bad,pass_=not bad),indent=2));raise SystemExit(bool(bad))
