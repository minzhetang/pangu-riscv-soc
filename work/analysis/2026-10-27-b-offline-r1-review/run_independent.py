from pathlib import Path
import sys,json,time,hashlib,subprocess,shutil
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
P=Path('D:/A_FPGA_Comp');H=Path(__file__).resolve().parent;T=H/'tool-copy';INPUT=P/'deliveries/mainline-b-verify-offline-m0-2026-10-26-v1';sys.path.insert(0,str(T/'src'));import support
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
plan=read(H/'FROZEN_PLAN.json');start=time.monotonic();rows=[]
def treesha(root):return {p.relative_to(root).as_posix():support.sha256_file(p) for p in root.rglob('*') if p.is_file()}
def call(cid,args,out=None):
 assert time.monotonic()-start<900
 d=H/'logs'/cid;d.mkdir();s=time.monotonic();peak=0;observed_log=0
 with (d/'stdout.log').open('xb') as stdout,(d/'stderr.log').open('xb') as stderr:
  p=subprocess.Popen(list(map(str,args)),cwd=H,stdout=stdout,stderr=stderr)
  while p.poll() is None:
   value=support.peak_working_set(p.pid)
   if value is not None:peak=max(peak,value)
   if out is not None:
    log=out/'worker.stdout.log'
    if log.exists():observed_log=max(observed_log,log.stat().st_size)
   if time.monotonic()-s>120 or peak>512*1024**2 or stdout.tell()>8*1024**2 or stderr.tell()>8*1024**2:
    p.kill();p.wait(2);raise RuntimeError('A independent outer budget exceeded')
   time.sleep(.001)
  rc=p.wait(2)
 r=dict(argv=['<EXISTING_PYTHON>' if i==0 else str(x) for i,x in enumerate(args)],rc=rc,seconds=round(time.monotonic()-s,6),peak=peak,independent_peak_worker_log_size=observed_log)
 (d/'process.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');return r
for e in plan['cases']:
 cid=e['id'];out=H/'outputs'/cid;argv=[sys.executable,'-B',T/'RUN.py'];exp=e['expected'];details={};passed=False
 if e['kind']=='resource_fixture_internal':
  proc=call(cid+'-driver',[sys.executable,'-B',H/'resource_probe.py',cid,INPUT]);r=read(H/'logs'/(cid+'.json'));rows.append({k:v for k,v in r.items() if k!='observations'});print(cid,r['status'],flush=True);continue
 case=H/'cases'/(cid+'.json')
 if e['kind']=='CLI':
  obj=e['case'];assert obj;case.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8');argv += ['--case-file',case,'--input-root',INPUT,'--out',out]
  if e.get('fixture_worker'):argv+=['--fixture-worker',e['fixture_worker']]
  proc=call(cid,argv,out);r=read(out/'result.json') if (out/'result.json').is_file() else None
  cli=json.loads((H/'logs'/cid/'stdout.log').read_text(encoding='utf-8-sig').splitlines()[-1]);checks={'parent_rc':proc['rc']==exp['native_rc'],'CLI_status':cli['status']==exp['run_status']}
  for k in ['checked','expected_records','actual_records']:
   if k in exp:checks[k]=r is not None and r.get(k)==exp[k]
  if 'first' in exp:
   for k,v in exp['first'].items():checks['first_'+k]=r is not None and r.get('first_difference',{}).get(k)==v
  if 'expect_worker_started' in exp:checks['worker_started']=bool(r.get('worker_started'))==exp['expect_worker_started'] if r else (out/'worker.stdout.log').exists()==exp['expect_worker_started']
  for name in ['result.json','worker-result.json']:
   q=out/name
   if q.exists():checks[name+'_bounded']=q.stat().st_size<=obj.get('limits',{}).get('max_result_bytes',1048576)
  if cid=='C2-result-size':checks['no_result_files']=not (out/'result.json').exists() and not (out/'worker-result.json').exists()
  if cid=='R1-LOG-FLOOD':checks['no_transient_overlimit_log']=proc['independent_peak_worker_log_size']<=4096
  details=dict(native_rc=proc['rc'],CLI_status=cli['status'],checked=r.get('checked') if r else None,worker_rc=r.get('worker_rc') if r else None,worker_started=r.get('worker_started') if r else None,raw_worker_log_bytes=r.get('raw_stdout_bytes') if r else None,independent_peak_worker_log_size=proc['independent_peak_worker_log_size'],seconds=proc['seconds'],checks=checks)
  passed=all(checks.values())
 elif e['kind']=='protected':
  before=treesha(T);out=T/('forbidden-'+cid);case=H/'cases/protected.json';case.write_text('{not-valid-json' if cid=='invalid-JSON-protected' else (T/'tests/cases/C0-default.json').read_text(encoding='utf-8-sig'),encoding='utf-8')
  flag='-OO' if cid=='C3-OO-protected' else '-O' if cid=='C3-O-protected' else '-B';argv=[sys.executable,flag,'-B',T/'RUN.py','--case-file',case,'--input-root',INPUT,'--out',out]
  proc=call(cid,argv);unchanged=treesha(T)==before;passed=proc['rc']==exp['rc'] and unchanged and not out.exists();details=dict(rc=proc['rc'],protected_tree_unchanged=unchanged,output_created=out.exists())
 elif cid=='oversized-CASE':
  with case.open('xb') as f:f.seek(1048576);f.write(b'X')
  proc=call(cid,[*argv,'--case-file',case,'--input-root',INPUT,'--out',out]);passed=proc['rc']==3 and not out.exists();details=dict(rc=proc['rc'],output_created=out.exists())
 rows.append(dict(id=cid,status='PASS' if passed else 'FAIL',kind=e['kind'],expected=exp,actual=details));print(cid,rows[-1]['status'],flush=True)
 (H/'checkpoint.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=dict(status='INDEPENDENT_REVIEW_WITH_FAILURES' if any(x['status']!='PASS' for x in rows) else 'PASS_SCOPED',cases=rows,total=len(rows),PASS=sum(x['status']=='PASS' for x in rows),FAIL=sum(x['status']=='FAIL' for x in rows),seconds=round(time.monotonic()-start,6),new_DUT=0,hardware='STOPPED',not_full54=True)
(H/'RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='cases'}))
