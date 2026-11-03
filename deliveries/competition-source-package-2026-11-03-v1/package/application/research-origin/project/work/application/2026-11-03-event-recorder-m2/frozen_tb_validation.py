"""New firmware executions on the unchanged, successfully compiled M1 CPU/SoC/TB.
Not a claim that the new parameterized M2 TB compiled. Fast32 profile only.
"""
from pathlib import Path
import json,hashlib,os,subprocess,time
from execute import H,R,I,compile_sw,save
OLD=R/'work/application/2026-11-03-event-recorder-m1'
plan=json.loads((H/'FROZEN_PLAN.json').read_text())['cases']
vvp=OLD/'app0.vvp'
save(H/'FROZEN_TB_IDENTITY.json',{'vvp':str(vvp),'vvp_sha256':hashlib.sha256(vvp.read_bytes()).hexdigest().upper(),'source_tb':str(OLD/'tb.sv'),'source_tb_sha256':hashlib.sha256((OLD/'tb.sv').read_bytes()).hexdigest().upper(),'profile':'fixed PERIOD12000 COUNT32 REPEATS2','new_firmware':True,'new_RTL_compile':False})
results=[]
try:
 for mode in [0,1]:
  b=compile_sw('validated-fast'+str(mode),12000,32,6,mode)
  cfg=json.loads((b/'BUILD.json').read_text());sy=cfg['symbols']
  names=list(plan) if mode==0 else ['normal']
  for name in names:
   c=plan[name];d=H/'runs'/('frozen-'+name+'-'+str(mode));d.mkdir(exist_ok=False)
   (d/'input.hex').write_text(''.join(f'{s:02x}\n' for s in c['input']));(d/'program.hex').write_bytes((b/'program.hex').read_bytes())
   args=list(map(str,[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp]));env=dict(os.environ);env['IVERILOG_DUMPER']='none'
   start=time.monotonic()
   try:p=subprocess.run(args,cwd=d,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45);rc=p.returncode;out=p.stdout
   except subprocess.TimeoutExpired as e:rc='TIMEOUT';out=e.stdout or b''
   (d/'run.log').write_bytes(out);save(d/'COMMAND.json',dict(argv=args,cwd=str(d),process_env={'IVERILOG_DUMPER':'none'},rc=rc,seconds=time.monotonic()-start,timeout=45))
   if rc:raise RuntimeError((name,rc))
   wire=(d/'serial.txt').read_bytes();accepted=(d/'accepted.txt').read_bytes();assert wire==accepted
   parts=wire.decode().split('~');assert len(parts)==3 and parts[-1]==''
   repeated=[]
   for rep in range(2):
    ram=[]
    for l in (d/f'ram{rep}.hex').read_text().splitlines():
     if not l.startswith(('//','@')):ram.extend(int(v,16) for v in l.split())
    def words(k,n=1):q=(sy[k][0]-65536)//4;return ram[q:q+n]
    read=[s.split() for s in (d/'reads.txt').read_text().splitlines() if s.split()[0]==str(rep)]
    observations=[];pending=None
    for row in read:
     _,address,value,timer=row;address=int(address,16);value=int(value,16);timer=int(timer,16)
     if address==0x20000010:
      assert pending is None;pending=value&7
     elif address==0x20000100:
      assert value==timer
      if pending is not None:observations.append([value,pending]);pending=None
    assert [s for t,s in observations]==c['input'] and pending is None
    t0=words('start_tick')[0];ts=[t for t,s in observations]
    assert all(12000*(i+1)<=t-t0<=12000*(i+1)+1000 for i,t in enumerate(ts))
    assert words('late')==[0] and words('done_samples')==[32] and words('complete')==[1]
    count=words('count')[0];head=words('head')[0];ev=words('events',32)
    actual=[ev[4*((head+8-count+k)&7):4*((head+8-count+k)&7)+4] for k in range(count)]
    expected=[[ts[i],i,s,why] for i,s,why in c['events']];assert actual==expected
    for k in ['fault','evicted','rejected','frozen']:assert words(k)==[c[k]]
    if mode:assert words('raw',64)==[v for pair in observations for v in pair]
    else:assert 'samples' not in sy and 'raw' not in sy
    hx=lambda vs:''.join(f'{v:08x} ' for v in vs)
    report='REC2 '+hx([12000,32,6,32,mode,t0,words('end_tick')[0],words('work_ticks')[0],0,count,c['evicted'],c['rejected'],c['fault'],c['frozen']])+'\n'
    if mode:
     for i,(t,s) in enumerate(observations):report+='S '+hx([i,t,s])+'\n'
    for e in expected:report+='E '+hx(e)+'\n'
    report+='END\n';assert parts[rep]==report.replace('\n','\r\n')
    repeated.append(dict(observations=observations,events=actual,uart_characters=len(report),work_ticks=words('work_ticks')[0]))
   assert repeated[0]==repeated[1]
   results.append(dict(case=name,mode=mode,status='PASS',repeats=repeated))
   save(H/'FAST_RESULTS.json',dict(status='IN_PROGRESS',results=results))
 save(H/'FAST_RESULTS.json',dict(status='FROZEN_TB_NEW_FIRMWARE_LIMITED_PASS',results=results,new_cpu_or_soc=False,slow_profile_runtime='NOT_RUN',parameterized_tb='TOOL_ERROR'))
except Exception as e:save(H/'FAST_RESULTS.json',dict(status='FAILED_OR_TOOL_ERROR',error=repr(e),results=results));raise
print('PASS',len(results),'fast firmware cases, no audit arrays; slow profile remains compile-only')
