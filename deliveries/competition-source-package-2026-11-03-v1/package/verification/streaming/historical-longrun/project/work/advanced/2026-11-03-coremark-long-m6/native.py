from pathlib import Path
import importlib.util,subprocess,time,json,ctypes as c,hashlib,sys
H=Path(__file__).resolve().parent;R=H.parents[2]
s=importlib.util.spec_from_file_location('job',R/'work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py');job=importlib.util.module_from_spec(s);s.loader.exec_module(job)
class PMC(c.Structure):
 _fields_=[('cb',c.c_ulong),('faults',c.c_ulong)]+[(n,c.c_size_t) for n in ['peak_working','working','peak_paged','paged','peak_nonpaged','nonpaged','pagefile','peak_pagefile']]
P=c.WinDLL('psapi',use_last_error=True)
P.GetProcessMemoryInfo.argtypes=[c.c_void_p,c.POINTER(PMC),c.c_ulong];P.GetProcessMemoryInfo.restype=c.c_bool
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def save(p,o):
 with Path(p).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def native(name,args,cwd=H,limit=60,housekeeping=None,memory=1024**3):
 rec=H/'commands'/f'{name}.json';attempt=H/'commands'/f'{name}-attempt.json'
 if rec.exists()or attempt.exists():raise RuntimeError('Existing attempt '+name)
 argv=list(map(str,args));save(attempt,dict(argv=argv,cwd=str(cwd),timeout=limit,memory_limit=memory,log_limit=1048576,unix=time.time()))
 start=time.monotonic();log=H/'logs'/f'{name}.log';error=None;peak=0;active=[];forced=False
 with log.open('xb') as out:
  j=job.OwnedJob(argv,cwd=cwd,stdout=out,stderr=subprocess.STDOUT)
  try:
   limits=job.EXT();limits.basic.flags=0x2100;limits.pm=memory
   job.check(job.K.SetInformationJobObject(j.job,9,c.byref(limits),c.sizeof(limits)))
   while j.p.poll()is None:
    v=PMC();v.cb=c.sizeof(v)
    if not P.GetProcessMemoryInfo(int(j.p._handle),c.byref(v),c.sizeof(v)):raise c.WinError(c.get_last_error())
    peak=max(peak,v.peak_working,v.peak_pagefile)
    if peak>memory:raise RuntimeError('MEMORY_LIMIT')
    if log.stat().st_size>1048576:raise RuntimeError('LOG_LIMIT')
    if time.monotonic()-start>limit:raise TimeoutError('TIMEOUT')
    if housekeeping:housekeeping()
    time.sleep(.1)
   rc=j.p.returncode
  except BaseException as e:
   error=repr(e);forced=True;j.close();j.p.wait(timeout=4);rc=j.p.returncode
  finally:
   if j.job:
    for _ in range(20):
     active=j.active()
     if not active:break
     time.sleep(.05)
    forced|=bool(active);j.close()
 if housekeeping:
  try:housekeeping()
  except BaseException as e:error=error or repr(e)
 result=dict(name=name,argv=argv,cwd=str(cwd),seconds=time.monotonic()-start,rc=rc,error=error,forced_cleanup=forced,remaining_before_close=active,peak_bytes=peak,log_bytes=log.stat().st_size,log_sha256=sha(log),input_sha256={str(Path(a)):sha(a) for a in args if Path(str(a)).is_file()})
 save(rec,result);print(name,rc,result['seconds'],error,flush=True)
 if error or rc!=0 or active:raise RuntimeError('Native command failed: '+name)
 return result
if __name__=='__main__':
 g=Path('D:/mingw64/bin/g++.exe')
 native('compile-replay',[g,'-std=c++17','-O3','-Wall','-Wextra','-static-libgcc','-static-libstdc++','-DREPLAY',H/'checker.cpp','-o',H/'replay.exe'])
 native('compile-vpi',[g,'-std=c++17','-O3','-Wall','-Wextra','-static-libgcc','-static-libstdc++','-shared','-I'+str(H/'vpi-deps'),H/'checker.cpp',H/'vpi-deps/libvpi.a','-o',H/'checker.vpi'])
