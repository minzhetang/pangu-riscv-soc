from execute import *
plan=json.loads((H/'FROZEN_PLAN.json').read_text());stage=sys.argv[1]
results=[]
for version in (['source-before'] if stage=='before' else ['source']):
 for pred in [0,1]:
  sync=1 if stage.startswith('after-sync') else 0
  name=f'{stage}-p{pred}';vvp=H/(name+'.vvp')
  replay='--recheck' in sys.argv
  rc=0 if replay else run('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb',f'-Ptb.PRED={pred}',f'-Ptb.SYNC={sync}','-o',vvp,*sorted((H/version).glob('*.v')),H/'tb-check.sv'],H,35)
  if rc:raise RuntimeError(('compile',rc))
  for t in plan['tests']:
   d=H/'runs'/name/t['name']
   if not replay:
    d.mkdir(parents=True,exist_ok=False)
    (d/'program.hex').write_bytes((H/'inputs'/t['name']/'program.hex').read_bytes())
    rc=run(name+'-'+t['name'],[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp,f'+IRQ={t["irq"]}',f'+REFRESH={t["refresh"]}'],d,10)
   else:rc=next(j['rc'] for j in jobs if j['name']==name+'-'+t['name'])
   lines=(d/'events.txt').read_text().splitlines() if (d/'events.txt').exists() else []
   def rows(tag):return [l.split()[1:] for l in lines if l.startswith(tag+' ')]
   wb=[[int(a),int(b,16)] for a,b in rows('WB')]
   stores=[[int(v,16) for v in r] for r in rows('STORE')]
   traps=[[int(v,16) for v in r] for r in rows('TRAP')]
   regs=[[int(a),int(b,16)] for a,b in rows('REG')]
   expected_regs=[0]*32
   for a,b in t['wb']:expected_regs[a]=b
   train_stalled=[r for r in rows('TRAIN') if r[2]!='0']
   unknown=[l for l in lines if l.startswith('UNKNOWN')]
   pre=rows('TRAP_PRE');bounded=all(int(r[0])<=92 for r in pre) if t['irq'] else True
   status=rows('STATUS')
   checks=dict(native_exit=rc==0,end=len(rows('END'))==1 and rows('END')[0][0]=='400',wb=wb==t['wb'],stores=stores==t['stores'],traps=traps==t['traps'],precise_trap_inputs=[[int(v,16) for v in r[1:]] for r in pre]==t['traps'],registers=regs==[[i,v] for i,v in enumerate(expected_regs)],unknown=not unknown,training_stalled=not train_stalled,irq_bound=bounded,stall_observed=bool(rows('STALL')) if t.get('require_stall') else True,
    mret=(status==[['00000088','3']] if t['name'].startswith('irq_') and t['name']!='irq_masked' else True))
   results.append(dict(case=t['name'],pred=pred,status='PASS' if all(checks.values()) else ('TIMEOUT' if rc=='TIMEOUT' else 'FAIL'),checks=checks,expected={k:t[k] for k in ['wb','stores','traps']},actual=dict(wb=wb,stores=stores,traps=traps,regs=regs,end=rows('END'),machine_status=status,train_during_stall=train_stalled),seconds=jobs[-1]['seconds']))
   print(results[-1]['status'],t['name'],[k for k,v in checks.items() if not v],flush=True)
   (H/(stage+('-RESULTS-rechecked.json' if replay else '-RESULTS.json'))).write_text(json.dumps(dict(stage=stage,plan_sha256=hashlib.sha256((H/'FROZEN_PLAN.json').read_bytes()).hexdigest(),results=results,jobs=jobs),indent=2))
