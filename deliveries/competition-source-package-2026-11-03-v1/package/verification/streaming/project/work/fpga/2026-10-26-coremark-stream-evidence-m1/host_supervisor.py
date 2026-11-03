from pathlib import Path
import ctypes,ctypes.wintypes as w,subprocess,time,sys,json
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
class PMC(ctypes.Structure):
    _fields_=[('cb',w.DWORD),('PageFaultCount',w.DWORD),('PeakWorkingSetSize',ctypes.c_size_t),('WorkingSetSize',ctypes.c_size_t),('QuotaPeakPagedPoolUsage',ctypes.c_size_t),('QuotaPagedPoolUsage',ctypes.c_size_t),('QuotaPeakNonPagedPoolUsage',ctypes.c_size_t),('QuotaNonPagedPoolUsage',ctypes.c_size_t),('PagefileUsage',ctypes.c_size_t),('PeakPagefileUsage',ctypes.c_size_t)]
ctypes.windll.kernel32.OpenProcess.restype=w.HANDLE
ctypes.windll.kernel32.CloseHandle.argtypes=[w.HANDLE]
ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[w.HANDLE,ctypes.POINTER(PMC),w.DWORD]
def peak(pid):
    h=ctypes.windll.kernel32.OpenProcess(0x410,False,pid)
    if not h:return None
    try:
        p=PMC();p.cb=ctypes.sizeof(p)
        return p.PeakWorkingSetSize if ctypes.windll.psapi.GetProcessMemoryInfo(h,ctypes.byref(p),p.cb) else None
    finally:ctypes.windll.kernel32.CloseHandle(h)
def save(p,o):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def bounded(argv,cwd,name,seconds,cap=512*1024*1024,while_running=None):
    d=H/'logs'/name;d.mkdir(exist_ok=False);start=time.monotonic();maximum=0;reason='PROCESS_EXIT';error=None
    with (d/'stdout.log').open('xb') as out,(d/'stderr.log').open('xb') as err:
        proc=subprocess.Popen(list(map(str,argv)),cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            while True:
                code=proc.poll();measured=peak(proc.pid)
                if measured is not None:maximum=max(maximum,measured)
                assert time.monotonic()-start<=seconds,'PROCESS_TIMEOUT'
                assert maximum<=cap,'PROCESS_MEMORY_CAP'
                assert all((d/n).stat().st_size<=8*1024*1024 for n in ['stdout.log','stderr.log']),'PROCESS_LOG_CAP'
                if while_running:while_running(d,code)
                if code is not None:break
                time.sleep(.05)
        except Exception as exc:
            error=str(exc);reason='STOPPED';
            if proc.poll() is None:proc.kill()
        try:rc=proc.wait(timeout=8)
        except subprocess.TimeoutExpired:rc=None;error=(error or '')+';wait timeout';reason='STOPPED'
    result=dict(argv=list(map(str,argv)),cwd=str(cwd),returncode=rc,returncode_hex=None if rc is None else f'0x{rc&0xffffffff:08X}',timed_out=error=='PROCESS_TIMEOUT',cap=error in ['PROCESS_MEMORY_CAP','PROCESS_LOG_CAP'],error=error,termination=reason,peak_working_set_bytes=maximum,elapsed_seconds=round(time.monotonic()-start,6),timeout_seconds=seconds,stdout=str(d/'stdout.log'),stderr=str(d/'stderr.log'))
    save(d/'process.json',result)
    print(json.dumps(dict(id=name,rc=rc,reason=reason,error=error,peak=maximum,host_seconds=result['elapsed_seconds'])),flush=True)
    if rc or error or reason!='PROCESS_EXIT':raise RuntimeError(name+' stopped: '+str(error))
    return result
if __name__=='__main__':
    for label,args in [('model-v2',['model']),('replay-performance',['replay','performance']),('replay-validation',['replay','validation'])]:
        bounded([sys.executable,'-B',H/'host_worker.py',*args],H,label,600)

