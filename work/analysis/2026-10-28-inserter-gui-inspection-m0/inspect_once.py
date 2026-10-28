"""One authorized <=180s own-process GUI inspection; never invoke controls."""
from pathlib import Path
import ctypes,ctypes.wintypes as w,hashlib,json,re,subprocess,sys,threading,time,os
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
EXE=Path('D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def redact(t):
    t=re.sub(r'(?i)C:[\\/]+Users[\\/]+[^\s<>"\']+','[PROFILE_PATH_REDACTED]',t)
    t=re.sub(r'(?i)(?<![0-9a-f])(?:[0-9a-f]{2}[-:]){5}[0-9a-f]{2}','[IDENTIFIER_REDACTED]',t)
    return t[:1500]
assert not ctypes.windll.shell32.IsUserAnAdmin()
assert not (H/'START.json').exists()
assert sha(EXE)=='B526DA86DA96B84A591F63D1E35F3B4CA50433F14DA9D136F7BF10DD50F07D94'
old=P/'work/fpga/2026-10-28-local-debug-insert-m1/PROTECTED_ORIGINALS.json'
protected=json.loads(old.read_text(encoding='utf-8-sig'))['files']
assert all(sha(Path(r['path']))==r['SHA256'] for r in protected)
(H/'logs').mkdir(exist_ok=False)
save('APPROVAL.json',dict(date_client='2026-10-28',decision='D171',user_reply='批准',scope='One local Inserter GUI read-only inspection <=180 seconds; no builds/insertion/license configuration/hardware',argv=[str(EXE)],external_route='SEPARATE_SYSTEM_REVIEW'))
save('FROZEN_INPUTS.json',dict(files=[dict(path=str(p),SHA256=sha(p)) for p in [Path(__file__),H/'read_window.ps1',EXE,old]]))
u=ctypes.windll.user32
u.GetWindowThreadProcessId.argtypes=[w.HWND,ctypes.POINTER(w.DWORD)]
u.GetWindowTextW.argtypes=[w.HWND,w.LPWSTR,ctypes.c_int]
u.GetClassNameW.argtypes=[w.HWND,w.LPWSTR,ctypes.c_int]
u.IsWindowVisible.argtypes=[w.HWND]
u.PostMessageW.argtypes=[w.HWND,w.UINT,w.WPARAM,w.LPARAM]
callback_type=ctypes.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
def windows(pid):
    rows=[]
    @callback_type
    def cb(hwnd,lparam):
        owner=w.DWORD();u.GetWindowThreadProcessId(hwnd,ctypes.byref(owner))
        if owner.value==pid and u.IsWindowVisible(hwnd):
            title=ctypes.create_unicode_buffer(1600);klass=ctypes.create_unicode_buffer(160)
            u.GetWindowTextW(hwnd,title,len(title));u.GetClassNameW(hwnd,klass,len(klass))
            rows.append(dict(hwnd=int(hwnd),title=redact(title.value),window_class=klass.value))
        return True
    u.EnumWindows.argtypes=[callback_type,w.LPARAM]
    if not u.EnumWindows(cb,0):raise OSError('Own-window enumeration unavailable')
    return rows
start=time.monotonic();deadline=start+180
save('START.json',dict(pid_scope='only newly created child; exact PID saved in local process receipt',started_monotonic=start,deadline_monotonic=deadline,GUI_launch_budget=1))
p=subprocess.Popen([str(EXE)],cwd=H,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
save('OWN_PROCESS.json',dict(pid=p.pid,executable=str(EXE),argv=[str(EXE)]))
done=threading.Event();caps=[]
def drain(pipe,name):
    count=0
    with (H/'logs'/name).open('xb') as f:
        while True:
            b=os.read(pipe.fileno(),4096)
            if not b:break
            allowed=max(0,1048576-count)
            if allowed:f.write(b[:allowed]);count+=min(allowed,len(b))
            if len(b)>allowed:
                caps.append(name)
                if p.poll() is None:p.terminate()
                break
    pipe.close()
def watchdog():
    if not done.wait(max(.01,deadline-time.monotonic())) and p.poll() is None:p.terminate()
threads=[threading.Thread(target=drain,args=(p.stdout,'stdout.log'),daemon=True),threading.Thread(target=drain,args=(p.stderr,'stderr.log'),daemon=True)]
for t in threads:t.start()
watch=threading.Thread(target=watchdog,daemon=True);watch.start()
result=dict(status='NOT_YET_OBSERVED',windows=[],read_only=True,GUI_launches=1,control_invocations=0,new_PDS=0,new_DUT=0,hardware='STOPPED')
try:
    while p.poll() is None and time.monotonic()<min(deadline-10,start+20):
        found=windows(p.pid)
        if found:
            result['windows']=found
            if any(re.search(r'license|许可证|授权|机器码',x['title'],re.I) for x in found):
                result['status']='LICENSE_WINDOW_STOPPED_WITHOUT_CONTENT_OR_CONFIGURATION';break
            if any(re.search(r'open\s+(?:file|design)|save\s+(?:file|as)|选择.*文件|打开.*文件|保存.*文件',x['title'],re.I) for x in found):
                result['status']='FILE_DIALOG_STOPPED_WITHOUT_READING_USER_FILES';break
            time.sleep(.5)
            inspections=[]
            for row in found[:3]:
                left=deadline-time.monotonic()-5
                if left<=0:raise TimeoutError('Inspection deadline')
                command=['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-File',str(H/'read_window.ps1'),'-TargetWindow',str(row['hwnd'])]
                helper=subprocess.run(command,capture_output=True,timeout=min(12,left),creationflags=subprocess.CREATE_NO_WINDOW)
                if helper.returncode:
                    inspections.append(dict(status='UIA_UNAVAILABLE',rc=helper.returncode));continue
                if len(helper.stdout)>131072:raise RuntimeError('UIA_OUTPUT_CAP')
                inspections.append(json.loads(helper.stdout.decode('utf-8-sig')))
            result['UIA']=inspections;result['status']='GUI_READ_ONLY_OBSERVED';break
        time.sleep(.1)
    if result['status']=='NOT_YET_OBSERVED':result['status']='NO_VISIBLE_WINDOW_BEFORE_EXIT_OR_WAIT_LIMIT'
except Exception as e:
    result.update(status='INSPECTION_STOPPED',error_type=type(e).__name__,error=redact(str(e)))
finally:
    result['WM_CLOSE_posts']=0
    if p.poll() is None:
        try:
            for row in windows(p.pid):
                if u.PostMessageW(row['hwnd'],0x10,0,0):result['WM_CLOSE_posts']+=1
        except Exception as e:result['close_guard_error']=type(e).__name__
    try:p.wait(timeout=max(.1,min(3,deadline-time.monotonic())))
    except subprocess.TimeoutExpired:
        result['own_process_terminated_after_close_wait']=True;p.terminate();p.wait(timeout=2)
    done.set();watch.join(timeout=.2)
    for t in threads:t.join(timeout=1)
    result.update(returncode=p.returncode,elapsed_seconds=round(time.monotonic()-start,3),within_180_seconds=time.monotonic()<=deadline,log_caps=caps,root_exited=p.poll() is not None)
    result['remaining_own_visible_windows']=windows(p.pid)
    result['protected_originals_unchanged']=all(sha(Path(r['path']))==r['SHA256'] for r in protected)
    result['protected_originals']=len(protected)
    assert result['protected_originals_unchanged']
    save('RESULT.json',result)
print(json.dumps(result,ensure_ascii=False))
