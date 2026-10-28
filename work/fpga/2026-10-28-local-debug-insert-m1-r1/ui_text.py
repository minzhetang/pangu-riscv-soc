"""Type approved ASCII into a visually focused own Inserter control; no clipboard."""
from pathlib import Path
import ctypes as c, ctypes.wintypes as w, json,sys,time
H=Path(__file__).resolve().parent
a=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
pid=json.loads((H/'GUI_PROCESS.json').read_text())['pid']
rows=json.loads((H/'GUI_WINDOWS.json').read_text())
row=next(r for r in rows if r['title']==a['title'])
u=c.windll.user32;u.GetWindowThreadProcessId.argtypes=[w.HWND,c.POINTER(w.DWORD)];u.PostMessageW.argtypes=[w.HWND,w.UINT,w.WPARAM,w.LPARAM]
owner=w.DWORD();u.GetWindowThreadProcessId(row['hwnd'],c.byref(owner));assert owner.value==pid
assert all(32<=ord(ch)<127 for ch in a['text'])
for ch in a['text']:u.PostMessageW(row['hwnd'],0x102,ord(ch),0);time.sleep(.001)
if a.get('enter'):u.PostMessageW(row['hwnd'],0x100,13,0);u.PostMessageW(row['hwnd'],0x101,13,0)
(H/(Path(sys.argv[1]).stem+'-receipt.json')).write_text(json.dumps({'own_pid_verified':True,'characters':len(a['text']),'enter':a.get('enter',False),'action_file':Path(sys.argv[1]).name}),encoding='utf-8')
