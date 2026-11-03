"""Sequential bounded Windows builds/sims; never inspect or control other jobs.
Usage: python run.py cache | ai | verify
"""
import ctypes as C, ctypes.wintypes as W, hashlib, json, pathlib, re, subprocess, sys, time, _winapi, msvcrt, os
ROOT=pathlib.Path(__file__).resolve().parent
TOOLS=next(p/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/bin' for p in ROOT.parents
           if (p/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/bin/iverilog.exe').is_file())
LOG=ROOT/'logs'; LOG.mkdir(exist_ok=True)
# A Job Object bounds only children launched here, not the mainline.
class BASIC(C.Structure):
    _fields_=[('ProcessTime',C.c_int64),('JobTime',C.c_int64),('Flags',W.DWORD),('Min',C.c_size_t),('Max',C.c_size_t),('Active',W.DWORD),('Affinity',C.c_size_t),('Priority',W.DWORD),('Scheduling',W.DWORD)]
class IO(C.Structure):
    _fields_=[(n,C.c_uint64) for n in ('ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes')]
class EXT(C.Structure):
    _fields_=[('Basic',BASIC),('IO',IO),('ProcessMemory',C.c_size_t),('JobMemory',C.c_size_t),('PeakProcess',C.c_size_t),('PeakJob',C.c_size_t)]
K=C.WinDLL('kernel32',use_last_error=True)
K.CreateJobObjectW.restype=W.HANDLE
K.AssignProcessToJobObject.argtypes=[W.HANDLE,W.HANDLE]
K.SetInformationJobObject.argtypes=[W.HANDLE,C.c_int,C.c_void_p,W.DWORD]
K.CloseHandle.argtypes=[W.HANDLE]
K.TerminateJobObject.argtypes=[W.HANDLE,W.UINT]
K.ResumeThread.argtypes=[W.HANDLE]
K.ResumeThread.restype=W.DWORD
def size(): return sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
def bounded(label,args,timeout=20,expected_exit=0):
    log=LOG/(label+'.log'); receipt=LOG/(label+'.json')
    if log.exists() or receipt.exists(): raise RuntimeError('Refuse overwrite: '+label)
    job=K.CreateJobObjectW(None,None)
    limits=EXT(); limits.Basic.Flags=0x2000|0x100|0x200|0x8 # kill on close, process/job memory, active count
    limits.Basic.Active=4;limits.ProcessMemory=256*1024**2;limits.JobMemory=384*1024**2
    if not K.SetInformationJobObject(job,9,C.byref(limits),C.sizeof(limits)): raise C.WinError(C.get_last_error())
    start=time.monotonic(); reason=None;peak=0
    with log.open('wb') as f:
        # Launch suspended: even compiler descendants inherit the job limits.
        si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESTDHANDLES
        handle=msvcrt.get_osfhandle(f.fileno());os.set_handle_inheritable(handle,True)
        with open(os.devnull,'rb') as null:
            ih=msvcrt.get_osfhandle(null.fileno());os.set_handle_inheritable(ih,True)
            si.hStdInput=ih;si.hStdOutput=handle;si.hStdError=handle
            ph,th,pid,tid=_winapi.CreateProcess(None,subprocess.list2cmdline([str(a) for a in args]),None,None,True,0x4000|0x4|0x08000000,None,str(ROOT),si)
        os.set_handle_inheritable(handle,False)
        if not K.AssignProcessToJobObject(job,W.HANDLE(ph)):
            error=C.get_last_error();_winapi.TerminateProcess(ph,99);_winapi.CloseHandle(th);_winapi.CloseHandle(ph);K.CloseHandle(job);raise C.WinError(error)
        if K.ResumeThread(th)==0xffffffff:
            K.CloseHandle(job);_winapi.CloseHandle(th);_winapi.CloseHandle(ph);raise C.WinError(C.get_last_error())
        _winapi.CloseHandle(th)
        try:
            while _winapi.WaitForSingleObject(ph,0)!=_winapi.WAIT_OBJECT_0:
                elapsed=time.monotonic()-start; total=size();peak=max(peak,total)
                if elapsed>timeout: reason='wall timeout'
                elif log.stat().st_size>1024**2: reason='log limit'
                elif total>64*1024**2: reason='directory disk limit'
                if reason: K.TerminateJobObject(job,99);break
                time.sleep(.02)
            assert _winapi.WaitForSingleObject(ph,3000)==_winapi.WAIT_OBJECT_0
            returncode=_winapi.GetExitCodeProcess(ph)
        finally: K.CloseHandle(job);_winapi.CloseHandle(ph)
    result=dict(command=[str(a) for a in args],exit=returncode,reason=reason,seconds=time.monotonic()-start,
        priority='BELOW_NORMAL',wall_limit_seconds=timeout,process_memory_limit=256*1024**2,job_memory_limit=384*1024**2,
        log_limit=1024**2,directory_limit=64*1024**2,observed_directory_bytes=peak)
    receipt.write_text(json.dumps(result,indent=2))
    if reason or returncode!=expected_exit: raise RuntimeError(label+': '+str(result)+'\n'+log.read_text(errors='replace'))
    return log.read_text(errors='replace')
def verify(filename):
    for line in (ROOT/filename).read_text().splitlines():
        sha,name=line.split('  ',1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
def cache():
    verify('CACHE_FROZEN_SHA256.txt')
    bounded('cache_compile_v2',[TOOLS/'iverilog.exe','-g2012','-Wall','-s','cache_tb','-o','cache.vvp','cache.sv','backend.sv','cache_tb.sv'])
    expected=json.loads((ROOT/'vectors/expected.json').read_text()); results=[]
    for key,exp in expected.items():
        ro,name,bp=key.split('_')
        for delay in [0,3]:
            args=[TOOLS/'vvp.exe','cache.vvp',f'+RO={ro}',f'+BYPASS={bp}',f'+DELAY={delay}',f'+VEC=vectors/{key}.txt']
            if key=='0_protocol_0' and delay==3: args+=['+WAVE=cache_protocol.vcd']
            raw=bounded(f'cache_{key}_d{delay}_v1',args)
            m=re.search(r'METRIC requests=(\d+) cycles=(\d+) hits=(\d+) transactions=(\d+) bytes=(\d+) mmio=(\d+)',raw)
            assert m and 'PASS cache' in raw
            got=dict(zip(['requests','cycles','hits','transactions','bytes','mmio'],map(int,m.groups())))
            for field in ['requests','hits','transactions','bytes','mmio']: assert got[field]==exp[field],(key,field,got,exp)
            results.append(dict(key=key,delay=delay,**got,eligible_reads=exp['eligible_reads'],status='PASS'))
    bounded('cache_reset_concurrent_v1',[TOOLS/'vvp.exe','cache.vvp','+MODE=1','+DELAY=3','+WAVE=cache_reset.vcd'])
    (ROOT/'CACHE_RESULTS.json').write_text(json.dumps(results,indent=2))
    verify('CACHE_FROZEN_SHA256.txt')
    print('PASS cache: '+str(len(results))+' configurations plus reset/concurrency')
def cache_supplement():
    verify('CACHE_FROZEN_SHA256.txt');verify('CACHE_SUPPLEMENT_SHA256.txt')
    bounded('cache_compile_supplement_v1',[TOOLS/'iverilog.exe','-g2012','-Wall','-s','cache_tb','-o','cache_supplement.vvp','cache.sv','backend.sv','cache_tb.sv'])
    results=[]
    for key,exp in json.loads((ROOT/'vectors/supplement.json').read_text()).items():
        for delay in [0,3]:
            raw=bounded(f'cache_{key}_d{delay}_supplement',[TOOLS/'vvp.exe','cache_supplement.vvp','+RO=0',f'+BYPASS={key[-1]}',f'+DELAY={delay}',f'+VEC=vectors/{key}.txt'])
            m=re.search(r'METRIC requests=(\d+) cycles=(\d+) hits=(\d+) transactions=(\d+) bytes=(\d+) mmio=(\d+)',raw)
            assert m and 'PASS cache' in raw
            got=dict(zip(['requests','cycles','hits','transactions','bytes','mmio'],map(int,m.groups())))
            for f in ['requests','hits','transactions','bytes','mmio']:assert got[f]==exp[f],(f,got,exp)
            results.append(dict(key=key,delay=delay,**got,eligible_reads=exp['eligible_reads'],status='PASS'))
    raw=bounded('cache_held_valid_supplement',[TOOLS/'vvp.exe','cache_supplement.vvp','+MODE=2','+DELAY=3','+WAVE=cache_held.vcd'])
    assert 'HELD_VALID_PASS' in raw
    raw=bounded('cache_negative_supplement',[TOOLS/'vvp.exe','cache_supplement.vvp','+RO=0','+BYPASS=0','+VEC=vectors/negative.txt'],expected_exit=1)
    assert 'data ch' in raw
    (ROOT/'CACHE_SUPPLEMENT_RESULTS.json').write_text(json.dumps(results,indent=2))
    print('PASS cache supplement: 4 configurations, held-valid, expected negative rejection')
if __name__=='__main__':
    if sys.argv[1]=='cache': cache()
    elif sys.argv[1]=='cache-supplement': cache_supplement()
    elif sys.argv[1]=='verify':
        verify('CACHE_FROZEN_SHA256.txt')
        if (ROOT/'CACHE_SUPPLEMENT_SHA256.txt').exists(): verify('CACHE_SUPPLEMENT_SHA256.txt')
        if (ROOT/'AI_FROZEN_SHA256.txt').exists(): verify('AI_FROZEN_SHA256.txt')
        print('PASS frozen hashes')
    elif sys.argv[1]=='ai':
        from reference_ai import run_ai
        run_ai(bounded,TOOLS)
