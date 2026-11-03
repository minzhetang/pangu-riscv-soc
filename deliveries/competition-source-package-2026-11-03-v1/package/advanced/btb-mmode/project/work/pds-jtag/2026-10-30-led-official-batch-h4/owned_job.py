"""Ordinary-user Windows job; assign suspended child before any child code runs."""
import ctypes as c,ctypes.wintypes as w,subprocess,time
K=c.WinDLL('kernel32',use_last_error=True)
class BASIC(c.Structure):
 _fields_=[('pt',c.c_longlong),('jt',c.c_longlong),('flags',w.DWORD),('min',c.c_size_t),('max',c.c_size_t),('active',w.DWORD),('affinity',c.c_size_t),('priority',w.DWORD),('scheduling',w.DWORD)]
class IO(c.Structure):_fields_=[(n,c.c_ulonglong) for n in ['ro','wo','oo','rt','wt','ot']]
class EXT(c.Structure):_fields_=[('basic',BASIC),('io',IO),('pm',c.c_size_t),('jm',c.c_size_t),('peakp',c.c_size_t),('peakj',c.c_size_t)]
class THREAD(c.Structure):_fields_=[('size',w.DWORD),('usage',w.DWORD),('tid',w.DWORD),('pid',w.DWORD),('priority',w.LONG),('delta',w.LONG),('flags',w.DWORD)]
class PIDLIST(c.Structure):_fields_=[('assigned',w.DWORD),('count',w.DWORD),('pids',c.c_size_t*1024)]
K.CreateJobObjectW.argtypes=[c.c_void_p,w.LPCWSTR];K.CreateJobObjectW.restype=w.HANDLE
K.SetInformationJobObject.argtypes=[w.HANDLE,c.c_int,c.c_void_p,w.DWORD];K.SetInformationJobObject.restype=w.BOOL
K.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE];K.AssignProcessToJobObject.restype=w.BOOL
K.QueryInformationJobObject.argtypes=[w.HANDLE,c.c_int,c.c_void_p,w.DWORD,c.c_void_p];K.QueryInformationJobObject.restype=w.BOOL
K.TerminateJobObject.argtypes=[w.HANDLE,w.UINT];K.TerminateJobObject.restype=w.BOOL
K.CloseHandle.argtypes=[w.HANDLE];K.CloseHandle.restype=w.BOOL
K.CreateToolhelp32Snapshot.argtypes=[w.DWORD,w.DWORD];K.CreateToolhelp32Snapshot.restype=w.HANDLE
for n in ['Thread32First','Thread32Next']:
 f=getattr(K,n);f.argtypes=[w.HANDLE,c.POINTER(THREAD)];f.restype=w.BOOL
K.OpenThread.argtypes=[w.DWORD,w.BOOL,w.DWORD];K.OpenThread.restype=w.HANDLE
K.ResumeThread.argtypes=[w.HANDLE];K.ResumeThread.restype=w.DWORD
K.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];K.OpenProcess.restype=w.HANDLE
K.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];K.WaitForSingleObject.restype=w.DWORD
K.QueryFullProcessImageNameW.argtypes=[w.HANDLE,w.DWORD,w.LPWSTR,c.POINTER(w.DWORD)];K.QueryFullProcessImageNameW.restype=w.BOOL
def check(ok):
 if not ok:raise c.WinError(c.get_last_error())
class OwnedJob:
 def __init__(self,args,**kwargs):
  self.p=None;self.job=K.CreateJobObjectW(None,None);check(self.job)
  try:
   limits=EXT();limits.basic.flags=0x2000
   check(K.SetInformationJobObject(self.job,9,c.byref(limits),c.sizeof(limits)))
   self.p=subprocess.Popen(args,creationflags=0x00000004|subprocess.CREATE_NO_WINDOW,**kwargs)
   check(K.AssignProcessToJobObject(self.job,int(self.p._handle)))
   snap=K.CreateToolhelp32Snapshot(4,0);check(snap not in [None,c.c_void_p(-1).value]);ids=[]
   try:
    e=THREAD();e.size=c.sizeof(e);ok=K.Thread32First(snap,c.byref(e))
    while ok:
     if e.pid==self.p.pid:ids.append(e.tid)
     ok=K.Thread32Next(snap,c.byref(e))
    if c.get_last_error()!=18:raise RuntimeError('Incomplete thread snapshot')
   finally:K.CloseHandle(snap)
   if len(ids)!=1:raise RuntimeError('Suspended child primary thread ambiguous')
   thread=K.OpenThread(2,False,ids[0]);check(thread)
   try:check(K.ResumeThread(thread)!=0xffffffff)
   finally:K.CloseHandle(thread)
  except BaseException:
   if self.p and self.p.poll() is None:self.p.kill();self.p.wait(timeout=2)
   K.CloseHandle(self.job);self.job=None;raise
 def active(self):
  v=PIDLIST();check(K.QueryInformationJobObject(self.job,3,c.byref(v),c.sizeof(v),None))
  if v.count>1024:raise RuntimeError('Job process list truncated')
  live=[]
  for pid in v.pids[:v.count]:
   handle=K.OpenProcess(0x00100000,False,pid)
   if not handle:
    if c.get_last_error()==87:continue
    check(False)
   try:
    status=K.WaitForSingleObject(handle,0)
    if status==258:live.append(pid)
    elif status!=0:check(False)
   finally:K.CloseHandle(handle)
  return live
 def close(self):
  active=self.active();names=[]
  for pid in active:
   handle=K.OpenProcess(0x1000,False,pid)
   if not handle:
    if c.get_last_error()!=87:names.append('unknown')
    continue
   try:
    buf=c.create_unicode_buffer(2048);size=w.DWORD(2048)
    names.append(buf.value.rsplit('\\',1)[-1].lower() if K.QueryFullProcessImageNameW(handle,0,buf,c.byref(size)) else 'unknown')
   finally:K.CloseHandle(handle)
  forced=bool(active);functional=any(n!='conhost.exe' for n in names)
  try:
   if forced:check(K.TerminateJobObject(self.job,1))
   end=time.monotonic()+5
   while self.active() and time.monotonic()<end:time.sleep(.05)
   empty=not self.active()
   self.p.wait(timeout=1)
   return dict(job_empty=empty,forced_cleanup=forced,forced_non_console_cleanup=functional,remaining_names_before_cleanup=names,root_exit_code=self.p.returncode)
  finally:check(K.CloseHandle(self.job));self.job=None
