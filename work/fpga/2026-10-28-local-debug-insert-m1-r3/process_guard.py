"""Query only the exact process created and identified by this stage's supervisor."""
import ctypes as c,ctypes.wintypes as w,time,json
class FT(c.Structure):_fields_=[('low',w.DWORD),('high',w.DWORD)]
def launch_allowed(marker,process_alive,identity_matches,aborted):
 return bool(marker and process_alive and identity_matches and not aborted)
def verify_waiting_pds(H):
 k=c.windll.kernel32
 k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE
 k.GetProcessTimes.argtypes=[w.HANDLE,*([c.POINTER(FT)]*4)]
 k.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];k.WaitForSingleObject.restype=w.DWORD;k.CloseHandle.argtypes=[w.HANDLE]
 r=json.loads((H/'logs/pds-flow-once/own-process.json').read_text())
 if r['argv'][0].replace('\\','/').lower()!='d:/pds/pds_2022.2-sp6.4/bin/pds_shell.exe':raise RuntimeError('UNEXPECTED_OWN_PDS_IMAGE')
 h=k.OpenProcess(0x100000|0x1000,False,r['pid'])
 if not h:raise RuntimeError('PDS_NOT_ALIVE_BEFORE_GUI')
 checks=[]
 try:
  for _ in range(2):
   times=[FT() for i in range(4)]
   ok=bool(k.GetProcessTimes(h,*[c.byref(t) for t in times]))
   identity=ok and ((times[0].high<<32)|times[0].low)==r['creation_ticks']
   active=k.WaitForSingleObject(h,0)==258
   marker=(H/'SYNTH_READY.json').is_file()
   allowed=launch_allowed(marker,active,identity,(H/'GUI_ABORT.json').exists())
   checks.append(dict(marker=marker,process_alive=active,creation_time_matches=identity,allowed=allowed))
   if not allowed:raise RuntimeError('PDS_LIVE_IDENTITY_GATE_REJECTED_GUI')
   time.sleep(.25)
 finally:k.CloseHandle(h)
 with (H/'GUI_LAUNCH_GATE.json').open('x',encoding='utf-8') as f:json.dump(dict(status='PASS',checks=checks,no_global_process_or_device_enumeration=True),f,indent=2)
