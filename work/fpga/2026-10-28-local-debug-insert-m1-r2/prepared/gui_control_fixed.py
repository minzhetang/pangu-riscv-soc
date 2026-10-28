"""One bounded Inserter session; stable owned-window identity, not fixed document title."""
from pathlib import Path
import ctypes as c,ctypes.wintypes as w,json,subprocess,sys,time,threading,os,re,hashlib
from PIL import Image,ImageDraw
from window_policy import decide
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
def classify(title,klass,owner,target):
 if owner!=target or not klass.startswith('Qt5152QWindow'):return 'REJECT'
 if title=='Expiration Reminder':return 'reminder'
 if re.match(r'^Fabric Inserter 2022\.2-SP6\.4(?: - .+)? \(on [^)]+\)$',title):return 'main'
 return 'REJECT'
def selfcheck():
 tests=[('Fabric Inserter 2022.2-SP6.4 (on TEST)','Qt5152QWindowIcon',7,7,'main'),('Fabric Inserter 2022.2-SP6.4 - D:/new.fic (on TEST)','Qt5152QWindowIcon',7,7,'main'),('Expiration Reminder','Qt5152QWindowIcon',7,7,'reminder'),('License Finder','Qt5152QWindowIcon',7,7,'REJECT'),('Fabric Inserter 2022.2-SP6.4 (on TEST)','Qt5152QWindowIcon',8,7,'REJECT'),('Other','Qt5152QWindowIcon',7,7,'REJECT')]
 for args in tests:
  if classify(*args[:4])!=args[4]:raise RuntimeError('ROLE_CLASSIFIER_SELFTEST')
 print('6/6 synthetic owned-window role checks PASS; no vendor process')
if __name__=='__main__' and sys.argv[1:] == ['selfcheck']:selfcheck();raise SystemExit(0)
U=c.windll.user32;G=c.windll.gdi32
U.GetWindowThreadProcessId.argtypes=[w.HWND,c.POINTER(w.DWORD)]
U.GetWindowTextW.argtypes=[w.HWND,w.LPWSTR,c.c_int];U.GetClassNameW.argtypes=[w.HWND,w.LPWSTR,c.c_int]
U.GetWindowRect.argtypes=[w.HWND,c.POINTER(w.RECT)];U.GetClientRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
U.IsWindowVisible.argtypes=[w.HWND];U.IsIconic.argtypes=[w.HWND]
U.PostMessageW.argtypes=[w.HWND,w.UINT,w.WPARAM,w.LPARAM]
U.ShowWindow.argtypes=[w.HWND,c.c_int];U.SetForegroundWindow.argtypes=[w.HWND]
U.PrintWindow.argtypes=[w.HWND,w.HDC,w.UINT];U.GetWindowDC.argtypes=[w.HWND];U.GetWindowDC.restype=w.HDC;U.ReleaseDC.argtypes=[w.HWND,w.HDC]
G.CreateCompatibleDC.argtypes=[w.HDC];G.CreateCompatibleDC.restype=w.HDC
G.CreateCompatibleBitmap.argtypes=[w.HDC,c.c_int,c.c_int];G.CreateCompatibleBitmap.restype=w.HBITMAP
G.SelectObject.argtypes=[w.HDC,w.HGDIOBJ];G.SelectObject.restype=w.HGDIOBJ
G.GetDIBits.argtypes=[w.HDC,w.HBITMAP,w.UINT,w.UINT,c.c_void_p,c.c_void_p,w.UINT]
G.DeleteObject.argtypes=[w.HGDIOBJ];G.DeleteDC.argtypes=[w.HDC]
CB=c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
def save(n,o):
 (H/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def windows(pid):
 rows=[]
 @CB
 def cb(hwnd,_):
  owner=w.DWORD();U.GetWindowThreadProcessId(hwnd,c.byref(owner))
  if owner.value==pid and U.IsWindowVisible(hwnd):
   title=c.create_unicode_buffer(700);klass=c.create_unicode_buffer(160)
   U.GetWindowTextW(hwnd,title,700);U.GetClassNameW(hwnd,klass,160)
   role=classify(title.value,klass.value,owner.value,pid)
   safe=re.sub(r'\(on [^)]+\)','(on [HOST_REDACTED])',title.value)
   # Unknown dialogs: retain only class/role; do not read body or edit values.
   if role=='REJECT':safe='[UNRECOGNIZED_OWN_WINDOW_TITLE_NOT_RECORDED]'
   rect=w.RECT();client=w.RECT();U.GetWindowRect(hwnd,c.byref(rect));U.GetClientRect(hwnd,c.byref(client))
   rows.append(dict(hwnd=int(hwnd),title=safe,role=role,klass=klass.value,size=[rect.right-rect.left,rect.bottom-rect.top],client_size=[client.right,client.bottom],minimized=bool(U.IsIconic(hwnd))))
  return True
 if not U.EnumWindows(cb,0):raise RuntimeError('OWN_WINDOW_ENUMERATION_FAILED')
 return rows
def capture(row,name):
 width,height=row['size'];hwnd=row['hwnd']
 if row['minimized'] or not(300<=width<=4096 and 80<=height<=2160):raise RuntimeError('CAPTURE_GEOMETRY_UNSAFE')
 dc=U.GetWindowDC(hwnd);mem=G.CreateCompatibleDC(dc);bmp=G.CreateCompatibleBitmap(dc,width,height);old=G.SelectObject(mem,bmp)
 try:
  if not U.PrintWindow(hwnd,mem,2):raise RuntimeError('OWN_CAPTURE_FAILED')
  header=(c.c_uint32*10)(40,width,(-height)&0xffffffff,0x200001,0,width*height*4,0,0,0,0);buf=c.create_string_buffer(width*height*4)
  if G.GetDIBits(mem,bmp,0,height,buf,header,0)!=height:raise RuntimeError('OWN_BITMAP_FAILED')
  im=Image.frombuffer('RGB',(width,height),buf.raw,'raw','BGRX',0,1)
  ImageDraw.Draw(im).rectangle((0,0,width,32),fill='white')
  im.save(H/(name+'.png'))
 finally:G.SelectObject(mem,old);G.DeleteObject(bmp);G.DeleteDC(mem);U.ReleaseDC(hwnd,dc)
def main():
 selfcheck();assert not c.windll.shell32.IsUserAnAdmin();assert not (H/'GUI-attempt.json').exists()
 exe=Path('D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe')
 assert hashlib.sha256(exe.read_bytes()).hexdigest().upper()=='B526DA86DA96B84A591F63D1E35F3B4CA50433F14DA9D136F7BF10DD50F07D94'
 stage=json.loads((H/'STAGE_CLOCK.json').read_text());start=time.monotonic();end=min(start+590,stage['deadline_monotonic']-5)
 save('GUI-attempt.json',dict(launches=1,maximum=1,start=start,end=end,seconds_limit=600))
 p=subprocess.Popen([str(exe)],cwd=H,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
 save('OWN_GUI_PROCESS.json',dict(pid=p.pid,argv=[str(exe)]));errors=[];threads=[]
 def drain(pipe,name):
  count=0
  with (H/name).open('xb') as f:
   while True:
    b=os.read(pipe.fileno(),8192)
    if not b:break
    allowed=max(0,4*1024**2-count);f.write(b[:allowed]);f.flush();count+=min(allowed,len(b))
    if len(b)>allowed:errors.append('GUI_LOG_CAP');p.terminate();break
  pipe.close()
 for pipe,name in [(p.stdout,'gui-stdout.log'),(p.stderr,'gui-stderr.log')]:
  t=threading.Thread(target=drain,args=(pipe,name),daemon=True);t.start();threads.append(t)
 seen=set();actions=[];reason='PROCESS_EXIT';failure=None
 try:
  while p.poll() is None and time.monotonic()<end:
   rows=windows(p.pid);save('GUI_WINDOWS.json',rows)
   if any(r['role']=='REJECT' for r in rows):raise RuntimeError('UNRECOGNIZED_OWN_DIALOG')
   for q in sorted((H/'gui-commands').glob('*.json')):
    if q.name in seen:continue
    a=json.loads(q.read_text(encoding='utf-8-sig'))
    current=windows(p.pid);decision=decide(a,current)
    if decision.startswith('WAIT_'):
     save('GUI_PENDING.json',dict(command=q.name,decision=decision,elapsed=time.monotonic()-start));continue
    if decision!='EXECUTE':raise RuntimeError(decision)
    matches=[r for r in current if r['role']==a['role']]
    row=matches[0];op=a['op'];hwnd=row['hwnd'];seen.add(q.name)
    if op=='restore':U.ShowWindow(hwnd,3);U.SetForegroundWindow(hwnd)
    elif op=='capture':capture(row,q.stem)
    elif op=='click':
     if row['minimized'] or row['client_size']!=a['expected_client_size']:raise RuntimeError('CLICK_GEOMETRY_CHANGED')
     x,y=a['x'],a['y'];assert 0<=x<row['client_size'][0] and 0<=y<row['client_size'][1]
     U.PostMessageW(hwnd,0x201,1,(y<<16)|x);U.PostMessageW(hwnd,0x202,0,(y<<16)|x)
    elif op=='source':
     if row['role']!='main' or row['minimized'] or row['client_size']!=a['expected_client_size']:raise RuntimeError('SOURCE_CONTEXT_CHANGED')
     script=(H/'scripts'/a['script']).resolve();assert script.parent==H/'scripts' and script.is_file()
     text='source {'+script.as_posix()+'}'
     for ch in text:U.PostMessageW(hwnd,0x102,ord(ch),0);time.sleep(.001)
     U.PostMessageW(hwnd,0x100,13,0);U.PostMessageW(hwnd,0x101,13,0)
    elif op=='close':U.PostMessageW(hwnd,0x10,0,0)
    else:raise RuntimeError('UNSUPPORTED_GUI_OPERATION')
    actions.append(dict(command=q.name,operation=a,elapsed_seconds=time.monotonic()-start,stable_role=row['role'],window_title=row['title']));save('GUI_ACTIONS.json',actions);time.sleep(.25)
   if errors:raise RuntimeError(errors[0])
   time.sleep(.1)
  if p.poll() is None:reason='GUI_DEADLINE'
 except Exception as e:failure=type(e).__name__+': '+str(e);reason='SUPERVISOR_STOP'
 finally:
  if p.poll() is None:
   for r in windows(p.pid):U.PostMessageW(r['hwnd'],0x10,0,0)
   try:p.wait(timeout=2)
   except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=2)
  for t in threads:t.join(timeout=1)
  result=dict(reason=reason,error=failure,rc=p.returncode,seconds=time.monotonic()-start,root_exited=p.poll() is not None,remaining_own_windows=windows(p.pid),hardware='STOPPED')
  save('GUI_RESULT.json',result)
  if failure or reason=='GUI_DEADLINE':save('GUI_ABORT.json',dict(reason=reason,error=failure))
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
