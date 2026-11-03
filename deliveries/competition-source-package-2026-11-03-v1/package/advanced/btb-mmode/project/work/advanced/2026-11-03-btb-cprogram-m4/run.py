from execute import *
stage=sys.argv[1];frozen=json.loads((H/'FROZEN_REFERENCE.json').read_text());results=[]
if hashlib.sha256((H/'program.bin').read_bytes()).hexdigest()!=frozen['binary_sha256']:raise SystemExit('program changed')
for sync in [0,1]:
 for pred in [0,1]:
  name=f'{stage}-s{sync}-p{pred}';vvp=H/(name+'.vvp')
  if (H/'runs'/name).exists():raise SystemExit('output exists')
  rc=run('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb',f'-Ptb.PRED={pred}',f'-Ptb.SYNC={sync}','-o',vvp,*sorted((H/'source').glob('*.v')),H/'tb.sv'],H,35)
  if rc:raise SystemExit('TOOL_ERROR')
  for case in frozen['cases']:
   seed=case['seed'];d=H/'runs'/name/f'{seed:08x}';d.mkdir(parents=True);(d/'program.hex').write_bytes((H/'program.hex').read_bytes())
   rc=run(name+f'-{seed:08x}',[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp,f'+SEED={seed:08x}'],d,60)
   e=H/'expected'/f'{seed:08x}';lines=(d/'state.txt').read_text().splitlines();checks=dict(native=rc==0,unknown=not any(s.startswith(('UNKNOWN','BAD_','TRAP')) for s in lines));differences={}
   for actual,expected,tag in [('wb.txt','wb.txt',None),('store.txt','store.txt',None),('state.txt','regs.txt','REG '),('state.txt','memory.txt','MEM ')]:
    aa=(d/actual).read_text().splitlines();aa=[s for s in aa if s.startswith(tag)] if tag else aa;bb=(e/expected).read_text().splitlines();checks[expected]=aa==bb
    if aa!=bb:differences[expected]=dict(actual_count=len(aa),expected_count=len(bb),first=next((dict(index=i,actual=a,expected=b) for i,(a,b) in enumerate(zip(aa,bb)) if a!=b),None))
   end=[s.split()[1:] for s in lines if s.startswith('END ')];checks['done']=len(end)==1 and 0<int(end[0][1])<int(end[0][2])<300000
   result=dict(seed=seed,sync=sync,pred=pred,status='TIMEOUT' if rc=='TIMEOUT' else ('PASS' if all(checks.values()) else 'FAIL'),checks=checks,differences=differences,end=end,seconds=jobs[-1]['seconds']);results.append(result);(H/(stage+'-RESULTS.json')).write_text(json.dumps(results,indent=2));print(result,flush=True)
if any(x['status']!='PASS' for x in results):raise SystemExit(1)
