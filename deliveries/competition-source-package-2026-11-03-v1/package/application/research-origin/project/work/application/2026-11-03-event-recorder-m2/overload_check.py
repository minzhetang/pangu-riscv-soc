from pathlib import Path
import json,subprocess,time,os
from execute import H,R,I,compile_sw,save
# Frozen before compilation/execution, not inferred from the observed DUT result.
plan={'period':32,'count':32,'wait':6,'inputs':[0]*32,'expected':{'late':1,'fault':3,'frozen':1,'post':0,'count':1,'evicted':0,'rejected':0},'done_samples':'strictly less than32; matches actual GPIO loads','event':'one record at first observed begin-deadline>1000, with index=done_samples,state0,reason3','side_effect':'no later GPIO sampling; UART exact ledger; two reset runs identical'}
save(H/'OVERLOAD_PLAN.json',plan)
b=compile_sw('overload',32,32,6,0);cfg=json.loads((b/'BUILD.json').read_text());sy=cfg['symbols']
d=H/'runs/overload';d.mkdir(exist_ok=False);(d/'input.hex').write_text('00\n'*32);(d/'program.hex').write_bytes((b/'program.hex').read_bytes())
vvp=R/'work/application/2026-11-03-event-recorder-m1/app0.vvp';args=list(map(str,[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp]));env=dict(os.environ);env['IVERILOG_DUMPER']='none'
start=time.monotonic();p=subprocess.run(args,cwd=d,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
(d/'run.log').write_bytes(p.stdout);save(d/'COMMAND.json',dict(argv=args,cwd=str(d),process_env={'IVERILOG_DUMPER':'none'},rc=p.returncode,seconds=time.monotonic()-start));assert p.returncode==0
assert (d/'serial.txt').read_bytes()==(d/'accepted.txt').read_bytes();parts=(d/'serial.txt').read_bytes().decode().split('~');assert len(parts)==3
result=[]
for rep in range(2):
 ram=[]
 for l in (d/f'ram{rep}.hex').read_text().splitlines():
  if not l.startswith(('//','@')):ram.extend(int(v,16) for v in l.split())
 def w(k,n=1):a=(sy[k][0]-65536)//4;return ram[a:a+n]
 for k,v in plan['expected'].items():assert w(k)==[v]
 assert w('complete')==[1];done=w('done_samples')[0];assert done<32
 rd=[l.split() for l in (d/'reads.txt').read_text().splitlines() if l.split()[0]==str(rep)]
 gp=[x for x in rd if int(x[1],16)==0x20000010];assert len(gp)==done and all(int(x[2],16)==0 for x in gp)
 tv=[int(x[2],16) for x in rd if int(x[1],16)==0x20000100];assert all(int(x[2],16)==int(x[3],16) for x in rd if int(x[1],16)==0x20000100)
 t0=w('start_tick')[0];event=w('events',4);assert event==[tv[-2],done,0,3] and event[0]-t0-32*(done+1)>1000
 hx=lambda vs:''.join(f'{v:08x} ' for v in vs)
 expected='REC2 '+hx([32,32,6,done,0,t0,w('end_tick')[0],w('work_ticks')[0],1,1,0,0,3,1])+'\nE '+hx(event)+'\nEND\n'
 assert parts[rep]==expected.replace('\n','\r\n')
 result.append(dict(done_samples=done,fault=3,late=1,event=event))
assert result[0]==result[1];save(H/'OVERLOAD_RESULT.json',dict(status='PASS',repeats=result,ordinary_CPU_execution=True,new_hardware=False));print(result)
