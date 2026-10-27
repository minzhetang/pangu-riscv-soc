from pathlib import Path
import sys,json,time,threading,subprocess
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;T=H/'tool-copy';sys.path.insert(0,str(T/'src'));sys.path.insert(0,str(T));import support;import RUN
real_popen=subprocess.Popen
mode=sys.argv[1];case=json.loads((T/'tests/cases/C0-default.json').read_text(encoding='utf-8-sig'));case['id']='A-'+mode;case['file']=str(T/'tests/cases/C0-default.json');case['limits']={'case_timeout_seconds':3,'cleanup_seconds':1,'worker_peak_working_set_bytes':16777216} if mode=='active-memory-guard' else {'case_timeout_seconds':1,'cleanup_seconds':1}
start=time.monotonic();observations=[];state={'pid':None,'kills':[],'finished':False}
def spy_popen(*a,**k):
 p=real_popen(*a,**k);state['pid']=p.pid;kill=p.kill
 def observed_kill():state['kills'].append(round(time.monotonic()-start,6));return kill()
 p.kill=observed_kill;return p
def observe():
 while not state['finished']:
  pid=state['pid']
  if pid:
   value=support.peak_working_set(pid)
   if value is not None:observations.append(dict(t=round(time.monotonic()-start,6),peak=value))
  time.sleep(.005)
thread=threading.Thread(target=observe,daemon=True);thread.start();RUN.subprocess.Popen=spy_popen
try:
 worker=H/'fixtures/memory_hold.py' if mode=='active-memory-guard' else T/'tests/fixtures/sleep_forever_worker.py'
 result,rc,out=RUN.execute_case(case,Path(sys.argv[2]),H/'outputs'/mode,support.normalize_limits(case['limits']),start,worker_path=worker)
finally:state['finished']=True;thread.join(1);RUN.subprocess.Popen=real_popen
elapsed=time.monotonic()-start
if mode=='active-memory-guard':
 over=[x for x in observations if x['peak']>16777216];passed=bool(over) and bool(state['kills']) and rc==5
 expected=dict(active_kill=True,rc=5);evidence=dict(observed_peak=max(x['peak'] for x in observations),over_limit_observations=len(over),over_limit_span_s=round(over[-1]['t']-over[0]['t'],6) if over else 0,worker_rc=result.get('worker_rc'),final_status=result.get('status'))
else:passed=bool(state['kills']) and state['kills'][0]<=1.1 and elapsed<=2.1 and rc==6;expected=dict(kill_by_s=1.1,total_by_s=2.1,rc=6);evidence=dict(worker_rc=result.get('worker_rc'),final_status=result.get('status'))
r=dict(id=mode,status='PASS' if passed else 'FAIL',expected=expected,evidence=evidence,kill_elapsed_s=state['kills'],elapsed_s=round(elapsed,6),observations=observations,actual_parent_function_rc=rc,guard_fixture_only=True,new_DUT=0,production_source_unchanged=True)
(H/'logs'/(mode+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in r.items() if k!='observations'}));raise SystemExit(0)
