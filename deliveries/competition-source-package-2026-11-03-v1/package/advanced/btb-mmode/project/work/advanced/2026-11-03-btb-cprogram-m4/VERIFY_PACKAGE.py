from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;bad=[];items=json.loads((H/'SHA256SUMS.json').read_text())
for x in items:
 p=(H/x['path']).resolve()
 if not p.is_relative_to(H) or not p.is_file() or p.is_symlink():bad.append(x['path']);continue
 if p.stat().st_size!=x['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:bad.append(x['path'])
print(json.dumps(dict(status='MATERIAL_HASH_PASS' if not bad else 'FAIL',files=len(items),mismatch=bad,not_functional_acceptance=True),indent=2));raise SystemExit(bool(bad))
