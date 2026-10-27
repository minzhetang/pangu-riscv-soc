"""Bounded own-process runner; no device enumeration or arbitrary-command CLI."""
from pathlib import Path
import sys,os,json,subprocess,time,threading,ctypes,ctypes.wintypes as w
from stage_budget import check,deadline,require,peak,measured_peak,k
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
class FT(ctypes.Structure):_fields_=[('low',w.DWORD),('high',w.DWORD)]
k.GetProcessTimes.argtypes=[w.HANDLE,*([ctypes.POINTER(FT)]*4)];k.GetCurrentProcess.restype=w.HANDLE
def cpu_times(handle):
 times=[FT() for _ in range(4)]
 if not k.GetProcessTimes(handle,*[ctypes.byref(t) for t in times]):return None
 return dict(kernel_s=((times[2].high<<32)|times[2].low)/1e7,user_s=((times[3].high<<32)|times[3].low)/1e7)
def save(path,value):
 with Path(path).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def bounded(argv,cwd,name,seconds,cap=512*1024**2,while_running=None,resource_probe=None):
 check();d=H/'logs'/name;d.mkdir(exist_ok=False);start=time.monotonic();end=deadline(seconds);state=dict(error=None,peak_child=0,peak_parent=0,child_samples=0);lock=threading.Lock();stop=threading.Event();parent_before=cpu_times(k.GetCurrentProcess())
 p=subprocess.Popen(list(map(str,argv)),cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
 def fail(message):
  with lock:
   if state['error'] is None:state['error']=message
  if p.poll() is None:
   try:
    q=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(p.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8)
    state['owned_tree_cleanup_rc']=q.returncode
   except Exception as exc:state['owned_tree_cleanup_error']=type(exc).__name__
   if p.poll() is None:
    try:p.kill()
    except OSError:pass
 def policy():
  check(end)
  if state['error'] is not None:raise RuntimeError(state['error'])
 def drain(pipe,path):
  count=0
  try:
   with path.open('xb') as out:
    while True:
     block=os.read(pipe.fileno(),65536)
     if not block:break
     allowed=max(0,32*1024**2-count)
     if allowed:out.write(block[:allowed]);out.flush();count+=min(len(block),allowed)
     if len(block)>allowed:fail('PROCESS_LOG_CAP');break
  except Exception as exc:fail('LOG_IO_ERROR:'+repr(exc))
  finally:pipe.close()
 def watch():
  try:
   while not stop.is_set():
    policy();own=measured_peak();state['peak_parent']=max(state['peak_parent'],own);require(own<=cap,'PARENT_MEMORY_CAP')
    if p.poll() is None:
     value=peak(p.pid)
     if value is None:
      require(p.poll() is not None,'CHILD_MEMORY_UNAVAILABLE')
     else:
      state['child_samples']+=1;state['peak_child']=max(state['peak_child'],value);require(value<=cap,'CHILD_MEMORY_CAP')
    if resource_probe:resource_probe()
    stop.wait(.025)
  except Exception as exc:fail(str(exc))
 threads=[threading.Thread(target=drain,args=(p.stdout,d/'stdout.log'),daemon=True),threading.Thread(target=drain,args=(p.stderr,d/'stderr.log'),daemon=True)]
 for t in threads:t.start()
 monitor=threading.Thread(target=watch,daemon=True);monitor.start()
 try:
  while p.poll() is None:
   policy()
   if while_running:while_running(d,None)
   time.sleep(.025)
 except Exception as exc:fail(str(exc))
 try:rc=p.wait(timeout=max(.001,min(8,end-time.monotonic())))
 except subprocess.TimeoutExpired:
  fail('PROCESS_WAIT_TIMEOUT');rc=p.wait(timeout=1)
 for t in threads:t.join(timeout=max(.001,min(2,end-time.monotonic())))
 if any(t.is_alive() for t in threads):fail('LOG_DRAIN_NOT_COMPLETE')
 if state['error'] is None:
  try:
   policy();require(state['child_samples']>0,'NO_CHILD_MEMORY_SAMPLE')
   if resource_probe:resource_probe()
   if while_running:while_running(d,rc)
   policy()
  except Exception as exc:fail(str(exc))
 stop.set();monitor.join(timeout=1)
 elapsed=time.monotonic()-start;child_cpu=cpu_times(p._handle);parent_after=cpu_times(k.GetCurrentProcess());err=state['error']
 result=dict(argv=list(map(str,argv)),cwd=str(cwd),returncode=rc,returncode_hex=f'0x{rc&0xffffffff:08X}',timed_out=err is not None and 'DEADLINE' in err,cap=err is not None and any(t in err for t in ['CAP','BUDGET']),error=err,termination='PROCESS_EXIT' if err is None else 'STOPPED',peak_working_set_bytes=state['peak_child'],parent_peak_working_set_bytes=state['peak_parent'],child_memory_samples=state['child_samples'],elapsed_seconds=round(elapsed,6),timeout_seconds=seconds,child_cpu=child_cpu,parent_cpu_before=parent_before,parent_cpu_after=parent_after,stdout=str(d/'stdout.log'),stderr=str(d/'stderr.log'),measurement_scope='PDS shell and this parent only; stage memory pool report retained separately, internal child peaks not separately measured',absolute_deadline_used=True)
 result['failure_cleanup']=dict(taskkill_rc=state.get('owned_tree_cleanup_rc'),error=state.get('owned_tree_cleanup_error'),tree_verified='NOT_INDEPENDENTLY_ENUMERATED');save(d/'process.json',result);print(json.dumps(dict(id=name,rc=rc,error=err,child_peak=state['peak_child'],parent_peak=state['peak_parent'],seconds=result['elapsed_seconds'])),flush=True)
 if rc!=0 or err is not None:raise RuntimeError(name+' stopped: '+str(err))
 return result
