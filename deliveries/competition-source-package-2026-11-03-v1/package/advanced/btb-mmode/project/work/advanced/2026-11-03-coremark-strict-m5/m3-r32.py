from execute import *
stage=sys.argv[1];planfile=H/('CSR_PLAN-v2.json' if 'v2' in stage else 'PLAN.json');plan=json.loads(planfile.read_text());results=[]
source='source-before' if stage.startswith('before') else 'source'
for sync in [1]:
 for pred in [1]:
  name=f'{stage}-s{sync}-p{pred}';vvp=H/(name+'.vvp')
  if (H/'runs'/name).exists():raise SystemExit('Existing output')
  rc=run('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb',f'-Ptb.PRED={pred}',f'-Ptb.SYNC={sync}','-o',vvp,*sorted((H/source).glob('*.v')),H/'m3-r32-tb.sv'],H,35)
  if rc:raise SystemExit('TOOL_ERROR')
  for t in plan['tests']:
   d=H/'runs'/name/t['name'];d.mkdir(parents=True);(d/'program.hex').write_bytes((H/'inputs'/t['name']/'program.hex').read_bytes())
   rc=run(name+'-'+t['name'],[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp,f'+IRQ={t["mask"]}','+IRQ_AT=1'],d,10)
   lines=(d/'events.txt').read_text().splitlines() if (d/'events.txt').exists() else []
   def rows(tag):return [l.split()[1:] for l in lines if l.startswith(tag+' ')]
   wb=[[int(a),int(b,16)] for a,b in rows('WB')];stores=[[int(v,16) for v in r] for r in rows('STORE')];traps=[[int(v,16) for v in r] for r in rows('TRAP')]
   reg=[0]*32;mem=[0]*2048
   for a,v in t['wb']:reg[a]=v
   for a,v,s in t['stores']:mem[a//4]=v
   csr=[r for r in rows('CSR') if int(r[1],16)==t['enable_pc']];pre=rows('TRAP_PRE');vec=rows('VECTOR')
   expected_entry=[] if t['entry'] is None else [t['entry']]
   checks=dict(rc=rc==0,end=rows('END')==[['400','0']],wb=wb==t['wb'],stores=stores==t['stores'],traps=traps==t['traps'],precise_input=[[int(v,16) for v in r[1:]] for r in pre]==t['traps'],vector=[int(r[1],16) for r in vec]==expected_entry,redirect_post=[int(r[0],16) for r in rows('REDIRECT_POST')]==expected_entry,trap_status=rows('TRAP_STATUS')==([] if not t['traps'] else [['00001880','3']]),registers=[[int(a),int(v,16)] for a,v in rows('REG')]==[[i,v] for i,v in enumerate(reg)],memory=[[int(a),int(v,16)] for a,v in rows('MEM')]==[[i,v] for i,v in enumerate(mem)],status=rows('STATUS')==[t['status']],unknown=not any(l.startswith('UNKNOWN') for l in lines),response_bound=(len(csr)==1 and (not pre or 0<int(pre[0][0])-int(csr[0][0])<=3*(sync+1))),no_stalled_training=all(r[2]=='0' for r in rows('TRAIN')))
   result=dict(case=t['name'],sync=sync,pred=pred,status='TIMEOUT' if rc=='TIMEOUT' else ('PASS' if all(checks.values()) else 'FAIL'),checks=checks,actual=dict(wb=wb,stores=stores,traps=traps,status=rows('STATUS'),vector=vec,csr_enable=csr,trap_pre=pre),seconds=jobs[-1]['seconds']);results.append(result)
   (H/(stage+'-RESULTS.json')).write_text(json.dumps(dict(plan_sha256=hashlib.sha256(planfile.read_bytes()).hexdigest(),results=results),indent=2));print(result['status'],t['name'],[k for k,v in checks.items() if not v],flush=True)
if not stage.startswith('before') and any(x['status']!='PASS' for x in results):raise SystemExit(1)
