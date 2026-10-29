"""Shared absolute stage deadlines and explicit nonoptimized execution policy."""
from pathlib import Path
import sys,time,json,hashlib,ctypes,ctypes.wintypes as w,os
if sys.flags.optimize:raise RuntimeError('OPTIMIZED_PYTHON_UNSUPPORTED')
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
CLOCK=json.loads((H/'RECOVERY_CLOCK.json').read_text(encoding='utf-8'))
STAGE_DEADLINE=CLOCK['deadline_monotonic']
def require(ok,text):
 if not ok:raise RuntimeError(text)
def check(deadline=None):
 require(time.monotonic()<=min(STAGE_DEADLINE,deadline if deadline is not None else STAGE_DEADLINE),'ABSOLUTE_DEADLINE')
def deadline(seconds):
 check();return min(STAGE_DEADLINE,time.monotonic()+seconds)
def json_read(path,cap=16*1024*1024):
 check();p=Path(path);require(p.is_file() and not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400,'JSON_PATH_LINK')
 require(p.stat().st_size<=cap,'JSON_CAP_BEFORE_READ')
 with p.open('rb') as f:data=f.read(cap+1)
 require(len(data)<=cap,'JSON_CAP_AFTER_READ');check();return json.loads(data.decode('utf-8-sig'))
class PMC(ctypes.Structure):
 _fields_=[('cb',w.DWORD),('PageFaultCount',w.DWORD),('PeakWorkingSetSize',ctypes.c_size_t),('WorkingSetSize',ctypes.c_size_t),('QuotaPeakPagedPoolUsage',ctypes.c_size_t),('QuotaPagedPoolUsage',ctypes.c_size_t),('QuotaPeakNonPagedPoolUsage',ctypes.c_size_t),('QuotaNonPagedPoolUsage',ctypes.c_size_t),('PagefileUsage',ctypes.c_size_t),('PeakPagefileUsage',ctypes.c_size_t)]
k=ctypes.windll.kernel32;p=ctypes.windll.psapi
k.OpenProcess.restype=w.HANDLE;k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.CloseHandle.argtypes=[w.HANDLE];p.GetProcessMemoryInfo.argtypes=[w.HANDLE,ctypes.POINTER(PMC),w.DWORD]
def peak(pid=None):
 h=k.OpenProcess(0x410,False,os.getpid() if pid is None else pid)
 if not h:return None
 try:
  r=PMC();r.cb=ctypes.sizeof(r)
  return r.PeakWorkingSetSize if p.GetProcessMemoryInfo(h,ctypes.byref(r),r.cb) else None
 finally:k.CloseHandle(h)
def measured_peak(pid=None):
 value=peak(pid);require(value is not None and value>0,'MEMORY_MEASUREMENT_UNAVAILABLE');return value
