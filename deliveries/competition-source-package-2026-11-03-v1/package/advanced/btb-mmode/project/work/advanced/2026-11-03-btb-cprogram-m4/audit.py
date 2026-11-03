from pathlib import Path
import json,hashlib,ast,itertools,zlib,struct
H=Path(__file__).resolve().parent;R=H.parents[2];M3=H.parent/'2026-11-03-mmode-vector-m3';M1=H.parent/'2026-11-03-btb-mmode-m1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cases=json.loads((H/'FROZEN_REFERENCE.json').read_text());runs=json.loads((H/'first-RESULTS.json').read_text());irqs=json.loads((H/'irq-final-RESULTS.json').read_text())['results']
def matches(actual,expected):
 sentinel=object()
 return all(a==b for a,b in itertools.zip_longest(actual,expected,fillvalue=sentinel))
def lines(p):
 with p.open() as f:
  for l in f:yield l.rstrip('\r\n')
checks=[];metrics=[]
for r in runs:
 seed=f'{r["seed"]:08x}';d=H/'runs'/f'first-s{r["sync"]}-p{r["pred"]}'/seed;e=H/'expected'/seed
 state=list(lines(d/'state.txt'));files={name:matches(lines(d/name),lines(e/name)) for name in ['wb.txt','store.txt']}
 for name,tag in [('regs.txt','REG '),('memory.txt','MEM ')]:files[name]=matches((s for s in state if s.startswith(tag)),lines(e/name))
 checks.append(dict(seed=seed,sync=r['sync'],pred=r['pred'],checks=files,pass_=all(files.values())))
 cycles,start,done,*other=map(int,r['end'][0]);metrics.append(dict(seed=seed,sync=r['sync'],pred=r['pred'],reset_to_done=done,compute_cycles=done-start,start_cycle=start,wall_seconds=r['seconds'],wb_count=next(x['wb_count'] for x in cases['cases'] if x['seed']==r['seed']),store_count=next(x['store_count'] for x in cases['cases'] if x['seed']==r['seed'])))
comparisons=[]
for seed in ['00000001','deadbeef']:
 for sync in [0,1]:
  a=next(x for x in metrics if x['seed']==seed and x['sync']==sync and x['pred']==0);b=next(x for x in metrics if x['seed']==seed and x['sync']==sync and x['pred']==1)
  comparisons.append(dict(seed=seed,sync=sync,off=a['compute_cycles'],on=b['compute_cycles'],saved=a['compute_cycles']-b['compute_cycles'],cycle_reduction_percent=100*(a['compute_cycles']-b['compute_cycles'])/a['compute_cycles']))
controls=[]
sample=list(lines(H/'expected/00000001/wb.txt'))
for name,mut in [('duplicate',sample[:4]+[sample[3]]+sample[4:]),('missing',sample[:3]+sample[4:]),('wrong_value',sample[:3]+['WB 5 12345678']+sample[4:]),('swapped',sample[:3]+sample[3:5][::-1]+sample[5:]),('truncated',sample[:-1]),('extra',sample+['WB 31 00000001'])]:controls.append(dict(name='wb_'+name,rejected=not matches(mut,sample)))
sample=list(lines(H/'expected/00000001/store.txt'))
for name,mut in [('duplicate',sample+[sample[-1]]),('wrong_mask',sample[:-1]+['STORE 00003020 600d600d 1']),('early_done',sample[-1:]+sample[:-1]),('missing',sample[:-1])]:controls.append(dict(name='store_'+name,rejected=not matches(mut,sample)))
algorithm=[]
for t in cases['cases']:
 x=t['seed'];data=[]
 for _ in range(32):
  x=(x^(x<<13))&0xffffffff;x^=x>>17;x=(x^(x<<5))&0xffffffff;data.append(x&65535)
 payload=b''.join(struct.pack('<I',v) for v in sorted(data));actual=zlib.crc32(payload);algorithm.append(dict(seed=t['seed'],zlib_crc=actual,expected=t['algorithm_results'][1],pass_=actual==t['algorithm_results'][1]))
tree=ast.parse((M1/'audit.py').read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='vcd_at');ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'vcd_parser','exec'),ns)
wave=[]
for r in runs:
 d=H/'runs'/f'first-s{r["sync"]}-p{r["pred"]}'/f'{r["seed"]:08x}';cycle=int(r['end'][0][2]);ps=55000+10000*(cycle-1)+1;snap=ns['vcd_at'](d/'window.vcd',ps)
 # Dump is enabled after the accepted DONE store. Verify values at its end
 # separately from architectural retirement claims.
 # The accepted STORE is checked in its pre-NBA ledger. Post-edge address
 # wires may already describe the next slot, especially with SYNC=0.
 exp={'tb.donecycle':cycle,'tb.trap':0,'tb.rst':1};act={k:snap.get(k) for k in exp};wave.append(dict(seed=r['seed'],sync=r['sync'],pred=r['pred'],done_cycle=cycle,time_ps=ps,phase='post_edge_completion_marker_not_store_acceptance',expected=exp,actual=act,pass_=act==exp))
source=[dict(file=p.name,unchanged=sha(p)==sha(M3/'source'/p.name),sha256=sha(p)) for p in sorted((H/'source').glob('*.v'))]
protected=[dict(path=x['path'],unchanged=sha(R/x['path']).upper()==x['sha256']) for x in json.loads((R/'work/fpga/2026-11-03-event-recorder-m3/PROTECTED_INPUTS.json').read_text())]
oldmanifest=json.loads((M3/'SHA256SUMS.json').read_text());oldbad=[x['path'] for x in oldmanifest if sha(M3/x['path'])!=x['sha256']]
jobs=json.loads((H/'COMMANDS.json').read_text());binding=[dict(job=j['name'],matches=all(sha(Path(p))==v for p,v in j['input_sha256'].items())) for j in jobs if j['name'].startswith('compile-')]
result=dict(stream_comparison=checks,metrics=metrics,comparisons=comparisons,negative_controls=controls,algorithm_crc_crosscheck=algorithm,vcd_done=wave,source=source,protected=protected,m3_manifest_count=len(oldmanifest),m3_manifest_mismatch=oldbad,compile_binding=binding,irq_results=irqs)
result['pass_']=len(runs)==8 and all(r['status']=='PASS' for r in runs+irqs) and all(x['pass_'] for x in checks+wave+algorithm) and all(x['unchanged'] for x in source+protected) and all(x['matches'] for x in binding) and all(x['rejected'] for x in controls) and not oldbad
(H/'AUDIT.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(pass_=result['pass_'],comparisons=comparisons,wave_pass=[x['pass_'] for x in wave],negative_controls=len(controls)),indent=2))
if not result['pass_']:raise SystemExit(1)
