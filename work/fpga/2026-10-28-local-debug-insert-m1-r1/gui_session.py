"""Bounded own-process Inserter session. Commands are explicit reviewed UI actions."""
from pathlib import Path
import ctypes as c, ctypes.wintypes as w, subprocess, time, json, hashlib, sys, os, re
from PIL import Image
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
U=c.windll.user32; G=c.windll.gdi32
U.GetWindowThreadProcessId.argtypes=[w.HWND,c.POINTER(w.DWORD)]
U.GetWindowTextW.argtypes=[w.HWND,w.LPWSTR,c.c_int]
U.GetWindowRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
U.IsWindowVisible.argtypes=[w.HWND]
U.PrintWindow.argtypes=[w.HWND,w.HDC,w.UINT]
U.GetWindowDC.argtypes=[w.HWND]; U.GetWindowDC.restype=w.HDC
U.ReleaseDC.argtypes=[w.HWND,w.HDC]
U.PostMessageW.argtypes=[w.HWND,w.UINT,w.WPARAM,w.LPARAM]
G.CreateCompatibleDC.argtypes=[w.HDC];G.CreateCompatibleDC.restype=w.HDC
G.CreateCompatibleBitmap.argtypes=[w.HDC,c.c_int,c.c_int];G.CreateCompatibleBitmap.restype=w.HBITMAP
G.SelectObject.argtypes=[w.HDC,w.HGDIOBJ];G.SelectObject.restype=w.HGDIOBJ
G.GetDIBits.argtypes=[w.HDC,w.HBITMAP,w.UINT,w.UINT,c.c_void_p,c.c_void_p,w.UINT]
G.DeleteObject.argtypes=[w.HGDIOBJ];G.DeleteDC.argtypes=[w.HDC]
CB=c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
def save(name,value):
    (H/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def windows(pid):
    rows=[]
    @CB
    def fn(hwnd,_):
        owner=w.DWORD();U.GetWindowThreadProcessId(hwnd,c.byref(owner))
        if owner.value==pid and U.IsWindowVisible(hwnd):
            title=c.create_unicode_buffer(512);U.GetWindowTextW(hwnd,title,512)
            rect=w.RECT();U.GetWindowRect(hwnd,c.byref(rect))
            safe_title=re.sub(r'\(on [^)]+\)','(on [HOST_REDACTED])',title.value)
            rows.append(dict(hwnd=int(hwnd),title=safe_title,size=[rect.right-rect.left,rect.bottom-rect.top]))
        return True
    U.EnumWindows(fn,0)
    return rows
def capture(row,n):
    hwnd=row['hwnd'];width,height=row['size']
    if not(0<width<=4096 and 0<height<=2160):raise RuntimeError('Window dimensions')
    dc=U.GetWindowDC(hwnd);mem=G.CreateCompatibleDC(dc);bmp=G.CreateCompatibleBitmap(dc,width,height);old=G.SelectObject(mem,bmp)
    try:
        if not U.PrintWindow(hwnd,mem,2):raise RuntimeError('PrintWindow unavailable')
        header=(c.c_uint32*10)(40,width,(-height)&0xffffffff,0x200001,0,width*height*4,0,0,0,0)
        data=c.create_string_buffer(width*height*4)
        if G.GetDIBits(mem,bmp,0,height,data,header,0)!=height:raise RuntimeError('GetDIBits failed')
        Image.frombuffer('RGB',(width,height),data.raw,'raw','BGRX',0,1).save(H/f'window-{n}.png')
    finally:G.SelectObject(mem,old);G.DeleteObject(bmp);G.DeleteDC(mem);U.ReleaseDC(hwnd,dc)
exe=Path('D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe')
assert hashlib.sha256(exe.read_bytes()).hexdigest().upper()=='B526DA86DA96B84A591F63D1E35F3B4CA50433F14DA9D136F7BF10DD50F07D94'
assert not c.windll.shell32.IsUserAnAdmin()
assert not (H/'GUI_START.json').exists()
start=time.monotonic();deadline=start+550
save('GUI_START.json',dict(start=start,deadline=deadline,max_seconds=600,launches=2,prior_seconds=19.140999999945052))
out=(H/'gui-stdout.log').open('xb');err=(H/'gui-stderr.log').open('xb')
p=subprocess.Popen([str(exe)],cwd=H,stdout=out,stderr=err,stdin=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
save('GUI_PROCESS.json',dict(pid=p.pid,argv=[str(exe)]))
seen=set();actions=[];reason='PROCESS_EXIT'
try:
    while p.poll() is None and time.monotonic()<deadline:
        if out.tell()>1048576 or err.tell()>1048576:reason='LOG_CAP';break
        for cmd in sorted(H.glob('gui-command-*.json')):
            if cmd.name in seen:continue
            seen.add(cmd.name);a=json.loads(cmd.read_text(encoding='utf-8'));rows=windows(p.pid)
            row=next((r for r in rows if r['title']==a['title']),None)
            if row is None:raise RuntimeError('Exact own window title not found')
            op=a['op']
            if op=='capture':capture(row,cmd.stem)
            elif op=='restore':
                U.ShowWindow(w.HWND(row['hwnd']),9)
            elif op=='click':
                x,y=a['x'],a['y']
                # Client coordinates, used only after visual verification.
                U.PostMessageW(row['hwnd'],0x201,1,(y<<16)|x);U.PostMessageW(row['hwnd'],0x202,0,(y<<16)|x)
            elif op=='key':
                key=int(a['key']);U.PostMessageW(row['hwnd'],0x100,key,0);U.PostMessageW(row['hwnd'],0x101,key,0)
            elif op=='close':U.PostMessageW(row['hwnd'],0x10,0,0)
            else:raise RuntimeError('Unsupported action')
            actions.append(dict(command=cmd.name,action=a,elapsed=time.monotonic()-start));save('GUI_ACTIONS.json',actions)
            time.sleep(.2)
        save('GUI_WINDOWS.json',windows(p.pid));time.sleep(.15)
    if p.poll() is None:reason=reason if reason!='PROCESS_EXIT' else 'GUI_BUDGET_STOP'
except Exception as e:reason=type(e).__name__+': '+str(e)
finally:
    if p.poll() is None:
        for r in windows(p.pid):U.PostMessageW(r['hwnd'],0x10,0,0)
        try:p.wait(timeout=2)
        except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=3)
    out.close();err.close()
    save('GUI_RESULT.json',dict(reason=reason,rc=p.returncode,seconds=time.monotonic()-start,root_exited=p.poll() is not None,remaining_own_windows=windows(p.pid),new_PDS=0,hardware='STOPPED'))
print(json.dumps(json.loads((H/'GUI_RESULT.json').read_text(encoding='utf-8')),ensure_ascii=False))
