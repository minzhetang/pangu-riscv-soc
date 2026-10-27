from pathlib import Path
import json,hashlib,time,math,sys,re,shutil
sys.stdout.reconfigure(encoding='utf-8')
P=Path('D:/A_FPGA_Comp');H=P/'work/analysis/2026-10-27-coremark-longrun-budget-m0';H.mkdir(exist_ok=False)
A=P/'work/fpga/2026-10-26-coremark-stream-evidence-m1';R1=P/'work/fpga/2026-10-25-board-coremark-m1';R2=P/'work/fpga/2026-10-25-coremark-iter2-m1'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,v):
 with (H/name).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
protected=[]
def pin(p):
 if not any(x['path']==str(p) for x in protected):protected.append(dict(path=str(p),SHA256=sha(p)))
 return p
for root,names in [(A,['SUMMARY.json','SOURCE_RECEIPTS.json','tests/tb_board_coremark.sv','stream_io.py','check_coremark.py','models/cpu_program_reference.py','host_supervisor.py','run_capture_once.py']),(R2,['precompute.py','port/core_portme.c'])]:
 for name in names:pin(root/name)
for p in (A/'source').iterdir():
 if p.is_file():pin(p)
profiles=[];start=time.monotonic()
# Classify actual saved trace rows; never runs CPU/ISA/reference simulation.
for it,root in [(1,R1),(2,R2)]:
 for seed in ['performance','validation']:
  d=root/'runs'/(seed+'-N234');check=read(pin(d/'check-result.json'));proc=read(pin(root/'logs'/('run-'+seed+'-N234')/'process.json'))
  path=pin(d/'trace.log');pin(d/'bus.log');stamps=check['detail']['stamps'];lo,hi=stamps[2:]
  groups={k:dict(records=0,bytes=0,kinds={x:0 for x in ['EX','WB','READ','STORE']}) for k in ['before_compute','compute_window','after_compute']}
  count=0;total=0;last=0
  with path.open('rb') as f:
   for line in f:
    fields=line.split(b'|',2);kind=fields[0].decode('ascii');c=int(fields[1]);assert c>=last;last=c
    g=groups['before_compute' if c<=lo else 'compute_window' if c<=hi else 'after_compute'];g['records']+=1;g['bytes']+=len(line);g['kinds'][kind]+=1;count+=1;total+=len(line)
  assert total==path.stat().st_size and count==sum(check['trace_counts'].values())
  assert {k:sum(g['kinds'][k] for g in groups.values()) for k in check['trace_counts']}==check['trace_counts']
  profiles.append(dict(iterations=it,seed=seed,metrics=check['metrics'],counts=check['trace_counts'],steps=check['trace_counts']['EX'],trace_records=count,trace_bytes=total,bus_bytes=(d/'bus.log').stat().st_size,raw_ticks=check['detail']['raw_ticks'],stamps=stamps,host_DUT_seconds=proc['elapsed_seconds'],trace_groups=groups))
  print(it,seed,'trace profiles checked',count,flush=True)
new=read(A/'SUMMARY.json');perf2=next(r for r in profiles if r['iterations']==2 and r['seed']=='performance');extra_updates=2*(perf2['trace_records']+new['streams']['bus']['records'])
forecasts=[]
for seed in ['performance','validation']:
 one=next(r for r in profiles if r['iterations']==1 and r['seed']==seed);two=next(r for r in profiles if r['iterations']==2 and r['seed']==seed)
 def forecast(key,n):return one[key]+(n-1)*(two[key]-one[key])
 increment=two['raw_ticks']-one['raw_ticks'];min_it=1+max(0,math.ceil((270000000-one['raw_ticks'])/increment))
 for n in [8,32,160]:
  physical=forecast('metrics',n) if False else one['metrics']['physical']+(n-1)*(two['metrics']['physical']-one['metrics']['physical'])
  steps=forecast('steps',n);records=forecast('trace_records',n);raw=forecast('trace_bytes',n);ticks=forecast('raw_ticks',n)
  # Direct physical-clock scaling is a conditional planning estimate, not measured runtime.
  rate=new['new_DUT_host_seconds']/perf2['metrics']['physical'] if seed=='performance' else two['host_DUT_seconds']/two['metrics']['physical']*new['observed_host_time_ratio']
  forecasts.append(dict(seed=seed,iterations=n,conditional_ticks=ticks,conditional_seconds_at_nominal_27MHz=ticks/27000000,conditional_steps=steps,conditional_trace_records=records,conditional_trace_raw_bytes=raw,conditional_segments=math.ceil(records/32768),conditional_physical=physical,conditional_host_DUT_hours=physical*rate/3600,conditional_minimum_iteration_estimate=min_it,old_caps_exceeded=dict(reference_5M=steps>5000000,raw_512MiB=raw>536870912,records_16M=records>16000000,segments_1024=math.ceil(records/32768)>1024,cycles_8M=physical>8000000),not_DUT_or_oracle_or_guarantee=True))
 # Threshold crossings are conditional on two-point increments, not real tests.
 thresholds={k:1+max(0,math.floor((limit-one[key])/(two[key]-one[key]))+1) for k,key,limit in [('reference_steps','steps',5000000),('raw_bytes','trace_bytes',536870912),('trace_records','trace_records',16000000),('segment_capacity','trace_records',1024*32768)]}
 save(seed+'-thresholds.json',dict(seed=seed,two_point_conditional_first_exceeding_iteration=thresholds))
# Code-level risks from actual source, not fabricated observed resource failures.
anchors=[]
for name,patterns in [('stream_io.py',['RAW_CAP=','<=1024','<=16000000','2*1024*1024','self.deleted.append']),('check_coremark.py',['read_at={}','io_reads=[]','ref.steps<5000000','time.monotonic()-ref_started<600']),('host_supervisor.py',['if measured is not None','maximum<=cap','while_running','seconds']),('tests/tb_board_coremark.sv',['trace_total=trace_total+1','bus_total=bus_total+1','8000000'])]:
 for line,text in enumerate((A/name).read_text(encoding='utf-8-sig').splitlines(),1):
  if any(s in text for s in patterns):anchors.append(dict(file=name,line=line,text=text.strip()))
save('INPUTS.json',dict(files=protected,semantics='Read-only existing raw data, metadata and code; no prior outputs overwritten'))
save('TRACE_PROFILES.json',dict(window_definition='before: cycle<=start_ticks; compute: start_ticks<cycle<=end_ticks; after: cycle>end_ticks; trace row bytes only, not host wall-time attribution',profiles=profiles))
save('FORECASTS.json',dict(method='Linear extrapolation of two actual iteration points; format widths/report polling/data-dependent iteration costs may change. No prediction is a new executed result.',cases=forecasts))
save('CODE_ANCHORS.json',anchors)
summary=dict(status='READ_ONLY_BUDGET_AND_CAPTURE_COST_ANALYSIS',date_client='2026-10-27',originals=len(protected),host_analysis_seconds=round(time.monotonic()-start,6),new_DUT=0,new_compile=0,ISA_replay=0,PDS=0,hardware='STOPPED',observed_host_seconds=dict(old=two['host_DUT_seconds'] if False else perf2['host_DUT_seconds'],new=new['new_DUT_host_seconds'],ratio=new['observed_host_time_ratio'],causal_attribution=False),extra_SV_record_counter_updates=extra_updates,record_branch_guards_also_added=True,file_close_events=142,profile_missing='No per-segment compression timings or comparable controlled host load; cannot apportion the 128.923s difference to gzip versus VVP instructions.',conditional_dual160_DUT_hours=sum(f['conditional_host_DUT_hours'] for f in forecasts if f['iterations']==160),simulated_10seconds_is_hardware_score=False,current_pipeline_short_caps_not_longrun_ready=True,free_workspace_disk_bytes=shutil.disk_usage(P).free,recommended_next='Bounded production stream/guard and host-size controls plus one 8-iteration performance software calibration; not dual160 or hardware',forecast8=next(f for f in forecasts if f['iterations']==8 and f['seed']=='performance'))
save('SUMMARY.json',summary)
assert all(sha(Path(r['path']))==r['SHA256'] for r in protected)
save('POSTFLIGHT.json',dict(status='READ_ONLY_INPUTS_UNCHANGED',files=len(protected),new_DUT=0,new_compile=0,ISA_replay=0,hardware='STOPPED'))
print(json.dumps(summary,ensure_ascii=False))
