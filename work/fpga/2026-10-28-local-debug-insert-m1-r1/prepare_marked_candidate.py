"""Prepare only D173-authorized nonfunctional debug comments; never invoke a tool."""
from pathlib import Path
import hashlib,json,difflib,shutil
H=Path(__file__).resolve().parent
BASE=H.parent/'2026-10-27-board-coremark8-bitstream-m1'/'source'
MARK=b' /* synthesis PAP_MARK_DEBUG="true" */'
changes={
 'cpu.v':[(b'wire        branch_taken;',b'wire        branch_taken'+MARK+b';')],
 'soc_top.sv':[(b'pc,inst,address,wdata,',b'pc,inst,address'+MARK+b',wdata,'),
               (b'wire wren,ram_we,',b'wire wren'+MARK+b',ram_we,')],
 'board_top.sv':[(b'wire stopped, write_error;',b'wire stopped'+MARK+b', write_error'+MARK+b';'),
                 (b'wire [1:0] stop_kind;',b'wire [1:0] stop_kind'+MARK+b';')]
}
def sha(b):return hashlib.sha256(b).hexdigest().upper()
for d in ['source-before','source']:(H/d).mkdir(exist_ok=False)
rows=[];diff=[]
for p in sorted(BASE.iterdir()):
 if not p.is_file():continue
 raw=p.read_bytes();new=raw
 for a,b in changes.get(p.name,[]):
  assert new.count(a)==1,(p.name,a)
  new=new.replace(a,b,1)
 assert new.replace(MARK,b'')==raw,p.name
 (H/'source-before'/p.name).write_bytes(raw);(H/'source'/p.name).write_bytes(new)
 assert p.read_bytes()==raw
 rows.append(dict(name=p.name,baseline_SHA256=sha(raw),before_SHA256=sha((H/'source-before'/p.name).read_bytes()),candidate_SHA256=sha(new),stripped_equals_baseline=True,changed=raw!=new))
 if raw!=new:diff.extend(difflib.unified_diff(raw.decode('utf-8-sig').splitlines(True),new.decode('utf-8-sig').splitlines(True),fromfile='source-before/'+p.name,tofile='source/'+p.name))
assert len(rows)==13
(H/'SOURCE_RECEIPTS.json').write_text(json.dumps(dict(status='PREPARED_NOT_SYNTHESIZED',scope='D173 nonfunctional metadata only',files=rows,changed_files=[r['name'] for r in rows if r['changed']],not_a_new_functional_acceptance=True),indent=2)+'\n',encoding='utf-8')
(H/'DEBUG_METADATA.patch').write_bytes(''.join(diff).encode('utf-8'))
print('13 baseline copies verified; only 3 metadata files changed; no synthesis or DUT')
