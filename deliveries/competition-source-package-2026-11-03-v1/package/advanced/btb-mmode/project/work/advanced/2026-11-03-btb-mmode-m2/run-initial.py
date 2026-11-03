from execute import *
plan=json.loads((H/'PLAN.json').read_text());stage=sys.argv[1];results=[]
version='source-before' if stage=='before' else 'source'
for sync in [0,1]:
 for pred in [0,1]:
  name=f'{stage}-s{sync}-p{pred}';vvp=H/(name+'.vvp')
  if (H/'runs'/name).exists():raise SystemExit('Output exists: '+name)
  rc=run('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb',f'-Ptb.PRED={pred}',f'-Ptb.SYNC={sync}','-o',vvp,*sorted((H/version).glob('*.v')),H/'tb.sv'],H,35)
  if rc:raise SystemExit('TOOL_ERROR: '+str(rc))
  for t in plan['tests']:
   d=H/'runs'/name/t['name'];d.mkdir(parents=True)
   (d/'program.hex').write_bytes((H/'inputs'/t['name']/'program.hex').read_bytes())
   rc=run(name+'-'+t['name'],[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp],d,10)
   lines=(d/'events.txt').read_text().splitlines() if (d/'events.txt').exists() else []
   def rows(tag):return [l.split()[1:] for l in lines if l.startswith(tag+' ')]
   def hx(tag):return [[int(v,16) for v in r] for r in rows(tag)]
   wb=[[int(a),int(v,16)] for a,v in rows('WB')];stores=hx('STORE');regs=[0]*32;memory=[0]*2048
   for a,v in t['wb']:regs[a]=v
   for a,v,s in t['stores']:memory[a//4]=v
   trains=[r for r in rows('TRAIN') if int(r[1],16)==t['focus_pc']]
   resolves=[r for r in rows('RESOLVE') if int(r[1],16)==t['focus_pc']]
   checks=dict(native_exit=rc==0,end=rows('END')==[['400']],wb=wb==t['wb'],stores=stores==t['stores'],traps=hx('TRAP')==t['traps'],registers=[[int(a),int(v,16)] for a,v in rows('REG')]==[[i,v] for i,v in enumerate(regs)],memory=[[int(a),int(v,16)] for a,v in rows('MEM')]==[[i,v] for i,v in enumerate(memory)],focus_ifmiss=any(r[3]=='0' for r in rows('FOCUS_HOLD')),training_count=len(trains)==1,resolve_count=len(resolves)==1,no_training_during_stall=all(r[2]=='0' for r in rows('TRAIN')),no_redirect_during_stall=not rows('REDIRECT_HELD'),unknown=not any(l.startswith('UNKNOWN') for l in lines),privilege=rows('STATUS')==[['00000080','1']])
   result=dict(case=t['name'],sync=sync,pred=pred,status='PASS' if all(checks.values()) else 'FAIL',checks=checks,actual=dict(wb=wb,stores=stores,traps=hx('TRAP'),focus_hold=rows('FOCUS_HOLD'),focus_train=trains,focus_resolve=resolves,redirect_held=rows('REDIRECT_HELD'),status=rows('STATUS')),seconds=jobs[-1]['seconds'])
   results.append(result);print(result['status'],t['name'],[k for k,v in checks.items() if not v],flush=True)
   (H/(stage+'-RESULTS.json')).write_text(json.dumps(dict(stage=stage,plan_sha256=hashlib.sha256((H/'PLAN.json').read_bytes()).hexdigest(),results=results),indent=2))
if stage!='before' and any(x['status']!='PASS' for x in results):raise SystemExit(1)
