from pathlib import Path
import subprocess,json,time,re,importlib.util,sys,hashlib
R=Path('D:/A_FPGA_Comp');W=Path(__file__).resolve().parent;B=R/'work/icarus/2026-10-21-cpu-shifti-reject';H=W/'regression763';H.mkdir(exist_ok=False)
if not __debug__:raise SystemExit('No -O')
plan=json.loads((B/'validation-v2/plan.json').read_text());expected=json.loads((B/'expected-traces.json').read_text());groups=json.loads((B/'compile-batch-plan.json').read_text())['requests'];byid={x['id']:x for x in plan['cases']};jobs=[];rows=[];frozen={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'validation-v2/plan.json',B/'expected-traces.json',B/'models/cpu_trace_oracle.py']}
s=importlib.util.spec_from_file_location('frozen_oracle',B/'models/cpu_trace_oracle.py');oracle=importlib.util.module_from_spec(s);s.loader.exec_module(oracle)
s=importlib.util.spec_from_file_location('owned',R/'work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py');J=importlib.util.module_from_spec(s);s.loader.exec_module(J)
def run(argv,cwd,label,limit):
 t=time.monotonic();j=J.OwnedJob(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 try:data,_=j.p.communicate(timeout=limit);rc=j.p.returncode
 except subprocess.TimeoutExpired:data=b'TIMEOUT';rc='TIMEOUT'
 time.sleep(.05);cl=j.close();(cwd/(label+'.log')).write_bytes(data);jobs.append(dict(argv=argv,cwd=str(cwd),rc=rc,seconds=time.monotonic()-t,cleanup=cl));assert rc==0 and cl['job_empty'] and not cl['forced_non_console_cleanup'],(label,rc,cl)
 return data.decode(errors='replace').replace('\r\n','\n')
for g in groups:
 d=H/('group%02d'%g['index']);d.mkdir();q=json.loads(Path(g['request']).read_text());vvp=d/'tb.vvp';argv=[q['executable']]+[str(vvp) if a==g['output_artifact'] else str(W/'source'/Path(a).name) if a in g['input_SHA256'] and Path(a).name in ['cpu.v','alu.v','control.v','regfile.v'] else a for a in q['arguments']];run(argv,d,'compile',60)
 for cid in g['case_ids']:
  c=byid[cid];cd=d/cid;cd.mkdir();args=[str(R/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/bin/vvp.exe'),'-N','-M-', '-M'+str(R/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/lib/ivl'),str(vvp),'+case='+cid,'+inputs='+(B/'cases'/cid).as_posix()]
  if 'expected_stop' in c:args+=['+stop_kind='+str((c['expected_stop'] or {}).get('kind',0)),'+stop_pc='+format((c['expected_stop'] or {}).get('pc',0),'x')]
  if c.get('reset_check'):args+=['+reset_check']
  t=run(args,cd,'run',30);ver=re.findall(r'^CASE_RESULT\|([^|]+)\|(PASS|FAIL|TIMEOUT)$',t,re.M);assert ver==[(cid,'PASS')],(cid,ver)
  trace=oracle.compare(t,expected[cid],'PASS');assert trace['strict_status']=='PASS',(cid,trace)
  regs={int(i):v for i,v in re.findall(r'^REG\|(\d+)\|([0-9a-fxz]+)$',t,re.M)};mem={int(i):v for i,v in re.findall(r'^MEM\|(\d+)\|([0-9a-fxz]+)$',t,re.M)};assert len(regs)==32 and len(mem)==64
  assert all(regs[i]==f'{v:08x}' for i,v in enumerate(c['expected_regs'])) and all(mem[i*4]==f'{v:08x}' for i,v in enumerate(c['expected_mem'])),cid
  assert not re.findall(r'^PROTOCOL_ERROR\|',t,re.M)
  ms=re.findall(r'^METRICS\|(.*)$',t,re.M);assert len(ms)==1;mt=dict(x.split('=',1) for x in ms[0].split('|'));checks={}
  for k in ['stall','flush']:
   want=plan[k+'_expectations'].get(cid);actual=int(mt[k+'_cycles']);assert want is None or want==actual,(cid,k,want,actual);checks[k]=dict(expected=want,actual=actual,status='NOT_SPECIFIED' if want is None else 'PASS')
  for key,pat,fields in [('loads',r'^READ\|cycle=(\d+)\|rd=(\d+)\|f3=(\d+)\|addr=([0-9a-f]{8})\|raw=([0-9a-f]{8})$',('rd','funct3','address','raw')),('bus_stores',r'^WSTORE\|cycle=(\d+)\|addr=([0-9a-f]{8})\|mask=([0-9a-f])\|data=([0-9a-f]{8})$',('address','mask','data'))]:
   if key in expected[cid]:
    got=[dict(zip(fields,[int(v) if k in ['rd','funct3'] else v for k,v in zip(fields,a[1:])])) for a in re.findall(pat,t,re.M)];assert got==[{k:a[k] for k in fields} for a in expected[cid][key]],(cid,key)
  if 'manual_ram_events' in c:
   got=[dict(kind=k,pc=int(pc,16),word=w,address=a,data=x,mask=m,after=z) for cy,k,pc,w,a,x,m,z in re.findall(r'^RAM\|cycle=(\d+)\|kind=([RWF])\|pc=([0-9a-f]{8})\|word=([0-9a-f]{8})\|addr=([0-9a-f]{8})\|data=([0-9a-f]{8})\|mask=([0-9a-f])\|after=([0-9a-f]{8})$',t,re.M)];assert got==c['manual_ram_events'],cid
  if 'expected_stop' in c:
   got=[dict(kind=int(k),pc=int(pc,16)) for k,pc in re.findall(r'^STOP_EVENT\|cycle=\d+\|kind=(\d+)\|pc=([0-9a-f]{8})$',t,re.M)];assert got==([] if c['expected_stop'] is None else [c['expected_stop']]),cid
  rows.append(dict(id=cid,status='PASS',checks=checks,metrics=mt,WB=len(trace['actual_writebacks']),STORE=len(trace['actual_stores']),log=str(cd/'run.log'),wave=str(cd/'wave.vcd')))
  if len(rows)%100==0:print('PASS',len(rows),flush=True)
  (H/'CHECKPOINT.json').write_text(json.dumps(dict(completed=len(rows),last=cid)))
assert len(rows)==763
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in frozen.items())
(H/'RESULTS.json').write_text(json.dumps(dict(status='763_FROZEN_REGRESSION_PASS',rows=rows,jobs=jobs,expected_unchanged=frozen,NOT_SPECIFIED_retained=True),indent=2));print('763 frozen cases PASS, full states + every ordered WB/STORE + side effects/stalls/stops; no expectation changes',flush=True)
