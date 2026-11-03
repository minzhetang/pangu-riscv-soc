from pathlib import Path
import json,hashlib,itertools,re
H=Path(__file__).resolve().parent;R=H.parents[2];M4=H.parent/'2026-11-03-btb-cprogram-m4';F=R/'work/fpga/2026-11-03-advanced-btb-offline-m1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def compare(a,b,tag=None):
 with a.open() as aa,b.open() as bb:
  it=(s for s in aa if s.startswith(tag)) if tag else aa
  return all(x==y for x,y in itertools.zip_longest(it,bb))
full=[];timing=[]
for resultfile,prefix,expectedroot in [('strict-RESULTS.json','strict','expected'),('TIMED_RESULTS.json','timed','timed-expected'),('TIMED32_RESULTS.json','timed32','timed-expected')]:
 rs=json.loads((H/resultfile).read_text())
 for r in rs:
  d=H/'runs'/f'{prefix}-p{r["pred"]}'/r['mode'];e=H/expectedroot
  if prefix!='strict':e=e/f'{prefix}-p{r["pred"]}'
  e=e/r['mode'];checks={}
  for fn,tag in [('wb.txt',None),('store.txt',None),('regs.txt','REG '),('memory.txt','MEM '),('uart.txt',None)]:checks[fn]=compare(d/('state.txt' if tag else fn),e/fn,tag)
  text=(d/'uart.txt').read_text();crcs=[re.search(r'\[0\]'+n+r'\s*:\s*(0x[0-9a-f]+)',text)[1] for n in ['crclist','crcmatrix','crcstate']];known=['0xe714','0x1fd7','0x8e3a'] if r['mode']=='performance' else ['0xe3c1','0x0747','0x8d84'];checks['known_crc']=crcs==known
  ram={int(s.split()[1]):int(s.split()[2],16) for s in (d/'state.txt').read_text().splitlines() if s.startswith('MEM ')};symbols=json.loads((H/'build'/r['mode']/'symbols.json').read_text())
  expected_ports=dict(port_error=0,ram_log_overflow=0,timer_error=0,port_finished=1,timer_start_calls=1,timer_stop_calls=1,timing_phase=4,seed4_volatile=1,seed3_volatile=0x66,seed5_volatile=0,seed1_volatile=0 if r['mode']=='performance' else 0x3415,seed2_volatile=0 if r['mode']=='performance' else 0x3415)
  checks['port_and_seed_state']=all(ram[symbols[n]//4]==v for n,v in expected_ports.items()) and ram[0x17ff8//4]==0 and ram[0x17ffc//4]==0x600d600d
  if prefix!='strict':
   reads=[]
   for s in (d/'timer-reads.txt').read_text().splitlines():
    _,cy,addr,val=s.split();reads.append((int(cy),int(addr,16),int(val,16)))
   checks['clock_oracle']=len(reads)==12 and all(v==(cy-2 if a==0x20000100 else 0) for cy,a,v in reads)
   delta=reads[10][2]-reads[7][2];phase=r['end'][0][2]-r['end'][0][1];checks['timer_vs_phase']=phase-delta==4
   timing.append(dict(mode=r['mode'],entries=32 if prefix=='timed32' else (64 if r['pred'] else 0),phase_cycles=phase,mtime_delta=delta,simulated_seconds_at_27MHz=delta/27000000,full_cycles=r['end'][0][3]))
  full.append(dict(resultfile=resultfile,mode=r['mode'],pred=r['pred'],checks=checks,status=r['status'],pass_=all(checks.values()) and r['status']=='PASS'))
comparisons=[]
for mode in ['performance','validation']:
 baseline=next(x for x in timing if x['mode']==mode and x['entries']==0)
 for entries in [64,32]:
  x=next(x for x in timing if x['mode']==mode and x['entries']==entries)
  comparisons.append(dict(mode=mode,entries=entries,off_cycles=baseline['phase_cycles'],on_cycles=x['phase_cycles'],cycle_reduction_percent=100*(baseline['phase_cycles']-x['phase_cycles'])/baseline['phase_cycles'],speedup=baseline['phase_cycles']/x['phase_cycles']))
# Cheap independent negative controls on real old streams; no extra DUT.
e=H/'expected/performance';wb=(e/'wb.txt').read_text().splitlines();st=(e/'store.txt').read_text().splitlines();u=(e/'uart.txt').read_text();controls=[]
def reject(n,a,b):controls.append(dict(name=n,rejected=not all(x==y for x,y in itertools.zip_longest(a,b))))
reject('WB_duplicate',itertools.chain(wb,[wb[-1]]),wb);reject('WB_missing',wb[:-1],wb);reject('WB_wrong_first',['WB 10 deadbeef']+wb[1:],wb);reject('STORE_duplicate',itertools.chain(st,[st[-1]]),st);reject('STORE_missing',st[:-1],st);reject('STORE_wrong_mask',st[:-1]+['STORE 00017ffc 600d600d 1'],st);reject('UART_bad_crc',u.replace('e714','ffff'),u);reject('UART_truncated',u[:-1],u);reject('timer_off_by_one',[1],[0]);reject('extra_register_side_effect',itertools.chain(wb,['WB 31 00000001']),wb)
r32=[]
for stage in ['final-r32-m1-r2-sync','final-r32-extra-r2-sync','after-r32-if-r2-v2','after-r32-if-r2-trap','after-r32-csr-r2-v2','irq-r32-r2','fault-r32-r2']:
 r32+=json.loads((H/(stage+'-RESULTS.json')).read_text())['results']
fault=json.loads((H/'fault-final-RESULTS.json').read_text())['results']
source=[dict(file=p.name,same_as_M4=sha(p)==sha(M4/'source'/p.name),PDS_sources_match=all(sha(p)==sha(F/f'pred{pred}/source'/p.name) for pred in [0,1,32]),sha256=sha(p)) for p in (H/'source').glob('*.v')]
B=R/'deliveries/task2-review-20261101-v01/extracted/HANDOFF_TASK2_DYNAMIC_PREDICTION_TRAPS_20261101_v01/final_hl4/sw/coremark/upstream'
upstream=[dict(file=p.name,unchanged=sha(p)==sha(B/p.name)) for p in (H/'upstream').glob('*') if p.is_file()]
protected=[dict(path=x['path'],unchanged=sha(R/x['path']).upper()==x['sha256']) for x in json.loads((R/'work/fpga/2026-11-03-event-recorder-m3/PROTECTED_INPUTS.json').read_text())]
pool={}
for p in list(H.glob('COMMANDS-observed*.json'))+[H/'COMMANDS_RECOVERED.json']:
 for item in json.loads(p.read_text()):pool[item['name']]=item
for p in (H/'command-records').glob('*.json'):
 item=json.loads(p.read_text());pool[item['name']]=item
(H/'COMMANDS_FINAL.json').write_text(json.dumps(list(pool.values()),indent=2))
native_ok=all(x['rc']==0 and not x['remaining_before_close'] for x in pool.values())
fa=json.loads((F/'AUDIT.json').read_text())
result=dict(coremark=full,timing=timing,comparisons=comparisons,negative_controls=controls,r32_regression_count=len(r32),r32_all_pass=all(x['status']=='PASS' for x in r32),fault_cases_count=len(fault),fault_all_pass=all(x['status']=='PASS' for x in fault),source_identity=source,upstream=upstream,protected=protected,native_command_count=len(pool),native_success=native_ok,offline_PDS_status=fa['status'],recommended_entries=32,limitations=['No board run planned','No formal CoreMark score: one iteration and <10 target seconds','Full S/U/PMP/Sv32 remains unaccepted','UART is an accepted byte-write model, not serial waveform replay','r32 first metadata overwritten in shared journal; r2 uses per-command immutable records','Old timed-result model.timer string says zero mock in error; actual TIMED_PLAN/read values and validated clock oracle govern; original result preserved'])
result['pass_']=len(full)==10 and all(x['pass_'] for x in full) and all(x['rejected'] for x in controls) and len(r32)==46 and result['r32_all_pass'] and len(fault)==24 and result['fault_all_pass'] and all(x['same_as_M4'] and x['PDS_sources_match'] for x in source) and all(x['unchanged'] for x in upstream+protected) and native_ok and fa['status'].startswith('OFFLINE_STA_RESOURCE_PAIR_PASS')
(H/'AUDIT.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(pass_=result['pass_'],CoreMark_runs=len(full),comparisons=comparisons,r32=len(r32),fault_cases=len(fault),native_commands=len(pool),timing=timing),indent=2))
if not result['pass_']:raise SystemExit(1)
