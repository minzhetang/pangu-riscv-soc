from native import *
from run_fast import frozen_check
import os
phase=sys.argv[1]
if phase not in ['on','off']:raise SystemExit('on/off only')
plan=frozen_check();capture=json.loads((H/'plans/TERMINAL_CAPTURE.json').read_text())
for rel,digest in capture['sha256'].items():
 if sha(H/rel)!=digest:raise RuntimeError('Capture identity')
for name in ['q2-performance','q2-validation','terminal-qualification-performance']:
 if json.loads((H/'runs'/name/'RESULT.json').read_text())['status']!='PASS':raise RuntimeError('Qualification incomplete')
for i in range(1,7):
 if json.loads((H/'runs'/f'q2-control-{i}'/'RESULT.json').read_text())['status']!='REJECTED_AS_EXPECTED':raise RuntimeError('Control incomplete')
startfile=H/'CAMPAIGN_START.json'
if phase=='on':
 if startfile.exists():raise SystemExit('Existing campaign. No automatic retry.')
 save(startfile,dict(unix=time.time(),monotonic=time.monotonic(),logical_cpus=os.cpu_count(),parallel_cases=2,total_wall_limit=plan['budget']['campaign_seconds'],case_limit=plan['budget']['case_seconds'],scope='192 dual seeds on first; off only after both pass'))
else:
 for mode in ['performance','validation']:
  d=H/'runs'/f'long-{mode}-p1'
  if json.loads((d/'RESULT.json').read_text())['status']!='PASS'or json.loads((d/'MEASUREMENT.json').read_text())['mtime_ticks']<270000000:raise RuntimeError('Prediction-on long runs not yet accepted')
started=json.loads(startfile.read_text());remaining=started['total_wall_limit']-(time.time()-started['unix'])
if remaining<started['case_limit']+60:raise SystemExit('Campaign remaining budget insufficient; preserve diagnostics, no new case')
save(H/f'CAMPAIGN_{phase}_ATTEMPT.json',dict(unix=time.time(),remaining_seconds=remaining,plan_sha256=sha(H/'plans/FROZEN-v2.json'),capture_sha256=sha(H/'plans/TERMINAL_CAPTURE.json'),qualified_prediction_seconds=[json.loads((H/'commands'/f'q2-{m}.json').read_text())['seconds']for m in ['performance','validation']]))
group=[];begin=time.monotonic();last=0;error=None
try:
 for mode in ['performance','validation']:
  pred=1 if phase=='on'else 0;name=f'long-{mode}-p{pred}'
  log=(H/'logs'/f'worker-{name}.log').open('xb');args=[sys.executable,'-X','utf8','-B',H/'worker.py',name,mode,'192',str(pred)]
  j=job.OwnedJob(list(map(str,args)),cwd=H,stdout=log,stderr=subprocess.STDOUT);group.append((name,j,log))
 while any(j.p.poll()is None for _,j,_ in group):
  if time.monotonic()-begin>started['case_limit']+20 or time.time()-started['unix']>started['total_wall_limit']:raise TimeoutError('CAMPAIGN_TIME_LIMIT')
  if any(j.p.poll()is not None and j.p.returncode!=0 for _,j,_ in group):raise RuntimeError('Worker failed; stop other current case and preserve partials')
  if time.monotonic()-last>=30:
   last=time.monotonic();progress=[]
   for name,j,_ in group:
    d=H/'runs'/name/'trace';files=list(d.glob('*.gz'))if d.exists()else []
    progress.append(dict(name=name,running=j.p.poll()is None,closed_trace_chunks=len(files),compressed_bytes=sum(p.stat().st_size for p in files)))
   print(json.dumps(dict(phase=phase,wall_seconds=round(time.monotonic()-begin,1),progress=progress)),flush=True)
  time.sleep(1)
 if any(j.p.returncode!=0 for _,j,_ in group):raise RuntimeError('Worker exit failure')
except BaseException as e:error=repr(e)
finally:
 results=[]
 for name,j,log in group:
  active=j.active()if j.job else [];j.close();j.p.wait(timeout=4);log.close()
  p=H/'runs'/name/'RESULT.json';r=json.loads(p.read_text())if p.exists()else None
  results.append(dict(name=name,rc=j.p.returncode,remaining_before_close=active,result=r))
 save(H/f'CAMPAIGN_{phase}_EXIT.json',dict(error=error,wall_seconds=time.monotonic()-begin,results=results))
if error or any(x['rc']!=0 or not x['result']or x['result']['status']!='PASS'for x in results):raise SystemExit(1)
print('CAMPAIGN',phase,'PASS',flush=True)
