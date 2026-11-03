from execute import *
import itertools
stage=sys.argv[1];frozen=json.loads((H/'FROZEN_REFERENCE.json').read_text());results=[]
for pred in [0,1]:
 name=f'{stage}-p{pred}';vvp=H/(name+'.vvp')
 if (H/'runs'/name).exists():raise SystemExit('Existing output')
 rc=run('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb',f'-Ptb.PRED={pred}','-o',vvp,*sorted((H/'source').glob('*.v')),H/'tb.sv'],H,35)
 if rc:raise SystemExit('TOOL_ERROR')
 for t in frozen['cases']:
  mode=t['mode'];d=H/'runs'/name/mode;d.mkdir(parents=True);(d/'program.hex').write_bytes((H/'build'/mode/'program.hex').read_bytes());symbols=json.loads((H/'build'/mode/'symbols.json').read_text())
  rc=run(name+'-'+mode,[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp,f'+PHASE={symbols["timing_phase"]:x}'],d,600)
  state=(d/'state.txt').read_text().splitlines() if (d/'state.txt').exists() else [];e=H/'expected'/mode;checks=dict(native=rc==0,unknown=not any(x.startswith(('BAD_','UNKNOWN','TRAP')) for x in state));diff={}
  for fn,tag in [('wb.txt',None),('store.txt',None),('regs.txt','REG '),('memory.txt','MEM '),('uart.txt',None)]:
   actual=(d/('state.txt' if tag else fn)).open();expected=(e/fn).open();count=0;first=None
   try:
    stream=(s for s in actual if s.startswith(tag)) if tag else actual
    for i,(a,b) in enumerate(itertools.zip_longest(stream,expected)):
     count+=1
     if a!=b and first is None:first=dict(index=i,actual=a,expected=b)
   finally:actual.close();expected.close()
   checks[fn]=first is None
   if first:diff[fn]=dict(first=first,records=count)
  end=[list(map(int,s.split()[1:])) for s in state if s.startswith('END ')];checks['bounded_completion']=len(end)==1 and 0<end[0][1]<end[0][2]<end[0][3]<4000000
  r=dict(mode=mode,pred=pred,status='TIMEOUT' if rc=='TIMEOUT' else ('PASS' if all(checks.values()) else 'FAIL'),checks=checks,differences=diff,end=end,seconds=jobs[-1]['seconds']);results.append(r);print(r,flush=True);(H/(stage+'-RESULTS.json')).write_text(json.dumps(results,indent=2))
if any(x['status']!='PASS' for x in results):raise SystemExit(1)
