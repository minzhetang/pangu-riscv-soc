"""Offline only: verify a byte-identical mirror of the existing completed project."""
from pathlib import Path
import hashlib,json,re,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2];R=P/'work/fpga/2026-10-28-local-debug-insert-m1-r4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,ensure_ascii=False,indent=2)
tokens=re.compile(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+')
def parse(text):
 stack=[];roots=[]
 for match in tokens.finditer(text):
  t=match.group()
  if t=='(':
   node=[]
   if stack:stack[-1].append(node)
   else:roots.append(node)
   stack.append(node)
  elif t==')':
   if not stack:raise ValueError('Unbalanced project data')
   stack.pop()
  else:
   if not stack:raise ValueError('Atom outside project node')
   stack[-1].append(t[1:-1] if t.startswith('"') else t)
 if stack:raise ValueError('Unclosed project node')
 return roots
def walk(node):
 if isinstance(node,list):
  yield node
  for child in node:
   if isinstance(child,list):yield from walk(child)
original=R/'build';dest=H/'mirror/build';assert not dest.exists()
source_files=sorted(p for p in original.rglob('*') if p.is_file())
assert all(not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400 for p in original.rglob('*'))
assert sum(p.stat().st_size for p in source_files)<256*1024**2
before=[dict(path=str(p),SHA256=sha(p),bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns) for p in source_files]
save('SOURCE_INVENTORY.json',before)
shutil.copytree(original,dest,copy_function=shutil.copy2)
shutil.copy2(R/'debug.fic',H/'mirror/debug.fic')
for row in before:
 p=Path(row['path']);q=dest/p.relative_to(original)
 assert sha(q)==row['SHA256'] and q.stat().st_mtime_ns==row['mtime_ns']
assert sha(R/'debug.fic')==sha(H/'mirror/debug.fic')
project=dest/'flow.pds';tree=parse(project.read_text(encoding='utf-8-sig'));nodes=list(walk(tree))
commands={}
for node in nodes:
 if len(node)>1 and node[0]=='_command':
  st=[x for x in node[2:] if isinstance(x,list) and x[0]=='_gci_state']
  if st:commands[node[1]]=int(st[0][1][1])
required=['cmd_compile','cmd_synthesize','cmd_devmap','cmd_pnr']
assert all(commands.get(n)==2 for n in required)
assert commands['cmd_gen_netlist']==0
refs=[]
for node in nodes:
 if len(node)>1 and node[0]=='_file':
  ref=node[1];q=(project.parent/ref).resolve()
  inside=q.is_relative_to((H/'mirror').resolve())
  row=dict(reference=ref,inside_mirror=inside,exists=q.is_file())
  if inside and q.is_file():row.update(SHA256=sha(q),bytes=q.stat().st_size)
  refs.append(row)
save('PROJECT_REFERENCES.json',refs)
active=[]
for n in ['flow.pds','impl.tcl','flow.tcl','board_pins.fdc','clock_27mhz.fdc']:
 text=(dest/n).read_text(encoding='utf-8-sig',errors='replace')
 hits=[i+1 for i,line in enumerate(text.splitlines()) if R.as_posix().lower() in line.replace('\\','/').lower()]
 active.append(dict(file=n,original_root_reference_lines=hits))
fic=(H/'mirror/debug.fic').read_text(errors='replace')
old_fic_reference=R.as_posix().lower() in fic.replace('\\','/').lower()
save('PATH_AUDIT.json',dict(active_files=active,FIC_contains_original_root=old_fic_reference,FIC_not_changed=True,interpretation='Original-source references need classification; no native loader executed'))
assert all(sha(Path(x['path']))==x['SHA256'] for x in before)
result=dict(date='2026-10-29',status='OFFLINE_MIRROR_VERIFIED_NATIVE_LOAD_NOT_RUN',files=len(before)+1,bytes=sum(x['bytes'] for x in before)+(R/'debug.fic').stat().st_size,project_byte_identical=sha(project)==sha(original/'flow.pds'),timestamps_preserved=True,command_states=commands,references=len(refs),missing_references=[r['reference'] for r in refs if not r['exists']],outside_mirror=[r['reference'] for r in refs if not r['inside_mirror']],init_include_present=(dest/'source/init_tables.svh').is_file(),native_calls=0,new_DUT=0,hardware='STOPPED')
save('SUMMARY.json',result);print(json.dumps(result))
