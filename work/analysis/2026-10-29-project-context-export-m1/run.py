from pathlib import Path
import sys,time,json,hashlib,shutil,re,difflib
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2];B=H.parent/'2026-10-29-project-context-preflight-m0';R=P/'work/fpga/2026-10-28-local-debug-insert-m1-r4';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,indent=2)
scope=P/'deliveries/mainline-project-context-export-scope-2026-10-29-v1/IMPLEMENTATION_SCOPE.md';assert sha(scope)=='96D4AE9C010B5DAEAC47F5589A82E2F235AF60BEB85EFE7AE36639E84508AF51'
start=time.monotonic();save('STAGE_CLOCK.json',dict(start=start,deadline_monotonic=start+900));save('APPROVAL.json',dict(date='2026-10-29',decision='D189',scope_SHA256=sha(scope),native_processes=1,hardware='STOPPED'))
files=list((B/'mirror').rglob('*'));protected=[dict(path=str(p),SHA256=sha(p)) for p in files if p.is_file()]
protected+=json.loads((H.parent/'2026-10-29-postroute-netlist-export-r1/PROTECTED_INPUTS.json').read_text())
protected+=json.loads((B/'SOURCE_INVENTORY.json').read_text())
dep=json.loads((B/'NESTED_DEPENDENCY.json').read_text());protected.append(dep)
save('PROTECTED_INPUTS.json',protected)
shutil.copytree(B/'mirror',H/'execution',copy_function=shutil.copy2);(H/'logs').mkdir(exist_ok=False)
project=H/'execution/build/flow.pds';raw=project.read_bytes();before=raw.decode('utf-8-sig');needle='(_command cmd_gen_netlist';a=before.index(needle);depth=0;end=None
for i in range(a,len(before)):
 if before[i]=='(':depth+=1
 elif before[i]==')':
  depth-=1
  if depth==0:end=i;break
assert end is not None
added='\n            (_option func_sim_only (_switch ON))\n            (_option sdf_annotate (_boolean FALSE))\n        '
after=before[:end]+added+before[end:];assert after.replace(added,'',1)==before
assert re.findall(r'_gci_state\s+\(_integer \d+\)',after)==re.findall(r'_gci_state\s+\(_integer \d+\)',before)
project.write_bytes(after.encode('utf-8'))
with (H/'EXPORT_OPTIONS.patch').open('x',encoding='utf-8',newline='\n') as f:f.write(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='original/flow.pds',tofile='execution/flow.pds')))
save('PATCH_RECEIPT.json',dict(original_SHA256=hashlib.sha256(raw).hexdigest().upper(),execution_SHA256=sha(project),only_export_options=True,states_unchanged=True))
old=H.parent/'2026-10-29-postroute-netlist-export-m0'
for n in ['host_supervisor.py','stage_budget.py']:shutil.copyfile(old/n,H/n)
from host_supervisor import bounded
def resource():
 sizes=[p.stat().st_size for p in H.rglob('*') if p.is_file()]
 if sum(sizes)>256*1024**2 or max(sizes)>128*1024**2:raise RuntimeError('DISK_CAP')
def inspect(logdir,rc):
 for p in [logdir/'stdout.log',logdir/'stderr.log',H/'execution/build/flow.log']:
  if p.exists():
   text=p.read_text(errors='replace')
   if re.search(r'(?im)^Executing\s*:\s*(?:compile|synthesize|dev_map|pnr|report_timing|gen_bit_stream)\b',text):
    # flow.log includes old history; inspect only fresh stdout for action dispatch.
    if p.parent==logdir:raise RuntimeError('UNAUTHORIZED_UPSTREAM_DISPATCH')
try:save('NATIVE_EXIT.json',bounded(['D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe','-project',project,'-run','gen_netlist'],project.parent,'export-once',180,cap=1024**3,while_running=inspect,resource_probe=resource))
except Exception as e:save('HOST_ERROR.json',dict(error=str(e)))
finally:
 assert all(sha(Path(r['path']))==r['SHA256'] for r in protected)
 out=[dict(path=str(p.relative_to(H)),bytes=p.stat().st_size,SHA256=sha(p)) for p in (H/'execution').rglob('*') if p.is_file() and p.suffix.lower() in ['.v','.vm','.sdf'] and p.stat().st_mtime>=time.time()-(time.monotonic()-start)-2]
 save('POSTFLIGHT.json',dict(unchanged=True,protected_entries=len(protected),outputs=out,seconds=time.monotonic()-start,hardware='STOPPED'))
