from pathlib import Path
import hashlib,json,shutil,tarfile
H=Path(__file__).resolve().parent;R=H.parents[2];P=H.parent/'2026-11-03-coremark-strict-m5'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if (H/'INPUTS.json').exists():raise SystemExit('Already prepared')
items=[]
for folder in ['source','upstream','port','firmware']:
 for p in sorted((P/folder).iterdir()):
  if not p.is_file():continue
  q=H/folder/p.name;q.parent.mkdir(exist_ok=True);shutil.copyfile(p,q)
  if sha(p)!=sha(q):raise RuntimeError('copy mismatch')
  items.append(dict(source=str(p),copy=str(q.relative_to(H)),sha256=sha(q)))
archive=R/'work/icarus/2026-10-15-msys2-baseline/inspected-tars/iverilog.tar'
with tarfile.open(archive) as t:
 for name in ['ucrt64/include/iverilog/vpi_user.h','ucrt64/include/iverilog/_pli_types.h','ucrt64/lib/libvpi.a']:
  m=t.getmember(name)
  if not m.isfile():raise RuntimeError('Not regular dependency')
  q=H/'vpi-deps'/Path(name).name;q.parent.mkdir(exist_ok=True)
  q.write_bytes(t.extractfile(m).read());items.append(dict(source=str(archive)+'::'+name,copy=str(q.relative_to(H)),sha256=sha(q)))
(H/'INPUTS.json').write_text(json.dumps(dict(files=items,archive_sha256=sha(archive),note='Only existing archive VPI headers/import library copied into this independent source tree; no installation or PATH change'),indent=2))
for folder in ['logs','commands','runs','build','host','plans']: (H/folder).mkdir(exist_ok=True)
print('prepared',len(items))
