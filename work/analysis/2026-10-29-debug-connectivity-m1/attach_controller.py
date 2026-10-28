"""Supervise the ONE already-started DE process; never create a vendor process."""
from pathlib import Path
import ctypes as c, ctypes.wintypes as w, json,time,sys,re
import gui_control as g
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
U=g.U;U.EnumWindows.argtypes=[g.CB,w.LPARAM];U.EnumWindows.restype=w.BOOL
k=c.WinDLL('kernel32',use_last_error=True)
k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE
k.QueryFullProcessImageNameW.argtypes=[w.HANDLE,w.DWORD,w.LPWSTR,c.POINTER(w.DWORD)]
k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)]
k.TerminateProcess.argtypes=[w.HANDLE,w.UINT];k.CloseHandle.argtypes=[w.HANDLE]
r=json.loads((H/'OWN_GUI_PROCESS.json').read_text());pid=r['pid']
attempt=json.loads((H/'GUI-attempt.json').read_text());start=attempt['start'];end=attempt['end']
assert time.monotonic()<end and not (H/'ATTACH_RECEIPT.json').exists()
handle=k.OpenProcess(0x101001,False,pid);assert handle
b=c.create_unicode_buffer(4096);n=w.DWORD(4096)
assert k.QueryFullProcessImageNameW(handle,0,b,c.byref(n)) and Path(b.value).as_posix().lower()=='d:/pds/pds_2022.2-sp6.4/bin/de.exe'
def poll():
 code=w.DWORD();assert k.GetExitCodeProcess(handle,c.byref(code))
 return None if code.value==259 else code.value
rows=g.windows(pid)
assert len(rows)==1 and rows[0]['role']=='main' and poll() is None
with (H/'ATTACH_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(dict(same_original_PID=True,image_matches=True,elapsed=time.monotonic()-start,budget_extended=False,new_vendor_launches=0,reason='Original monitor returned on initial EnumWindows failure; explicit API prototype and current owned-main identity verified'),f,indent=2)
seen=set();actions=[];failure=None;reason='PROCESS_EXIT'
try:
 while poll() is None and time.monotonic()<end:
  rows=g.windows(pid);g.save('GUI_WINDOWS.json',rows)
  if any(r['role']=='REJECT' for r in rows):raise RuntimeError('UNRECOGNIZED_OWN_DIALOG')
  for q in sorted((H/'gui-commands').glob('*.json')):
   if q.name in seen:continue
   a=json.loads(q.read_text(encoding='utf-8-sig'));decision=g.decide(a,g.windows(pid))
   if decision.startswith('WAIT_'):continue
   if decision!='EXECUTE':raise RuntimeError(decision)
   row=[r for r in g.windows(pid) if r['role']==a['role']][0];hwnd=row['hwnd'];op=a['op'];seen.add(q.name)
   if op=='restore':U.ShowWindow(hwnd,3);U.SetForegroundWindow(hwnd)
   elif op=='capture':g.capture(row,q.stem)
   elif op=='click':
    assert not row['minimized'] and row['client_size']==a['expected_client_size']
    x,y=a['x'],a['y'];assert 0<=x<row['client_size'][0] and 0<=y<row['client_size'][1]
    U.PostMessageW(hwnd,0x201,1,(y<<16)|x);U.PostMessageW(hwnd,0x202,0,(y<<16)|x)
   elif op=='source':
    assert row['role']=='main' and not row['minimized'] and row['client_size']==a['expected_client_size']
    p=(H/'scripts'/a['script']).resolve();assert p.parent==H/'scripts' and p.is_file()
    for ch in 'source {'+p.as_posix()+'}':U.PostMessageW(hwnd,0x102,ord(ch),0);time.sleep(.001)
    U.PostMessageW(hwnd,0x100,13,0);U.PostMessageW(hwnd,0x101,13,0)
   elif op=='close':U.PostMessageW(hwnd,0x10,0,0)
   else:raise RuntimeError('UNSUPPORTED_ACTION')
   actions.append(dict(command=q.name,operation=a,elapsed_seconds=time.monotonic()-start,window_title=row['title']));g.save('GUI_ACTIONS.json',actions);time.sleep(.25)
  time.sleep(.1)
 if poll() is None:reason='GUI_DEADLINE'
except Exception as e:failure=type(e).__name__+': '+str(e);reason='SUPERVISOR_STOP'
finally:
 if poll() is None:
  try:
   for r in g.windows(pid):U.PostMessageW(r['hwnd'],0x10,0,0)
  except Exception as e:failure=(failure or '')+'; CLOSE_ENUM: '+type(e).__name__
  finish=min(end+5,time.monotonic()+3)
  while poll() is None and time.monotonic()<finish:time.sleep(.05)
  if poll() is None:k.TerminateProcess(handle,1)
  finish=time.monotonic()+2
  while poll() is None and time.monotonic()<finish:time.sleep(.05)
 result=dict(reason=reason,error=failure,rc=poll(),seconds=time.monotonic()-start,root_exited=poll() is not None,remaining_own_windows=g.windows(pid),hardware='STOPPED',vendor_launches=1,initial_monitor_error_retained=True)
 g.save('GUI_RESULT.json',result);k.CloseHandle(handle)
print(json.dumps(result))
