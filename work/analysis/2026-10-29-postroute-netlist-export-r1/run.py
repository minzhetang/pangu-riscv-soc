from pathlib import Path
import json,hashlib,shutil,time,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2];OLD=H.parent/'2026-10-29-postroute-netlist-export-m0'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,indent=2)
scope=P/'deliveries/mainline-postroute-netlist-export-r1-scope-2026-10-29-v1/IMPLEMENTATION_SCOPE.md'
assert sha(scope)=='DB2B53DF7EBFF0E8531C705281FC5A811A6603F1CA514396824E20EBAB5F40A3'
start=time.monotonic();save('STAGE_CLOCK.json',dict(start=start,deadline_monotonic=start+900))
save('APPROVAL.json',dict(date='2026-10-29',decision='D186',scope_SHA256=sha(scope),native_processes=1,seconds=180,hardware='STOPPED'))
protected=json.loads((OLD/'PROTECTED_INPUTS.json').read_text());save('PROTECTED_INPUTS.json',protected)
for d in ['inputs','logs']:(H/d).mkdir(exist_ok=False)
p=P/'work/fpga/2026-10-28-local-debug-insert-m1-r4/build/place_route/board_top_pnr.adf';q=H/'inputs/board_top_pnr.adf';shutil.copyfile(p,q);assert sha(p)==sha(q)
save('COPY_RECEIPT.json',dict(source=str(p),copy=str(q),SHA256=sha(p)))
for n in ['host_supervisor.py','stage_budget.py']:shutil.copyfile(OLD/n,H/n)
script='set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676\ngen_netlist -input_db_file {'+q.as_posix()+'} -func_sim_only -sdf_annotate FALSE\n'
with (H/'export.tcl').open('x',encoding='utf-8',newline='\n') as f:f.write(script)
from host_supervisor import bounded
def caps():
 sizes=[p.stat().st_size for p in H.rglob('*') if p.is_file()]
 if sum(sizes)>256*1024**2 or max(sizes)>128*1024**2:raise RuntimeError('DISK_CAP')
try:
 r=bounded(['D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe','-file',H/'export.tcl'],H,'export-once',180,cap=1024**3,resource_probe=caps);save('NATIVE_EXIT.json',r)
except Exception as e:save('HOST_ERROR.json',dict(error=str(e)))
finally:
 assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
 assert sha(p)==sha(q)
 outputs=[dict(path=str(x.relative_to(H)),bytes=x.stat().st_size,SHA256=sha(x)) for x in H.rglob('*') if x.is_file() and x.suffix.lower() in ['.v','.vm','.sdf']]
 save('POSTFLIGHT.json',dict(protected_entries=len(protected),unchanged=True,outputs=outputs,seconds=time.monotonic()-start,hardware='STOPPED'))
