from pathlib import Path
import ctypes.wintypes as w,json,time,hashlib
import gui_control as g
H=Path(__file__).resolve().parent;U=g.U
U.EnumWindows.argtypes=[g.CB,w.LPARAM];U.EnumWindows.restype=w.BOOL
assert time.monotonic()<json.loads((H/'GUI-attempt.json').read_text())['end']
pid=json.loads((H/'OWN_GUI_PROCESS.json').read_text())['pid']
rows=g.windows(pid);load=[r for r in rows if r['role']=='load']
assert len(load)==1 and all(r['role'] in ['main','load'] for r in rows)
r=load[0];assert r['client_size']==[400,281] and not r['minimized']
files=['board_top_pnr.adf','board_top_rtp.adf','rtr.db']
receipts={Path(x['copy']).name:x for x in json.loads((H/'COPY_RECEIPT.json').read_text())}
assert not (H/'FILL_RECEIPT.json').exists()
for name,y in zip(files,[42,102,162]):
 p=H/'inputs'/name;assert hashlib.sha256(p.read_bytes()).hexdigest().upper()==receipts[name]['SHA256']
 U.PostMessageW(r['hwnd'],0x201,1,(y<<16)|120);U.PostMessageW(r['hwnd'],0x202,0,(y<<16)|120)
 for ch in p.as_posix():U.PostMessageW(r['hwnd'],0x102,ord(ch),0);time.sleep(.002)
 time.sleep(.2)
with (H/'FILL_RECEIPT.json').open('x') as f:json.dump(dict(files=files,version_check_unchanged=True,original_DBs_not_opened=True),f,indent=2)
