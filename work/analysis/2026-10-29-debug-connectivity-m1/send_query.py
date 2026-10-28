"""Send a reviewed read-only command to the same supervised DE console."""
import json,time,sys,ctypes as c,ctypes.wintypes as w
from pathlib import Path
import gui_control as g
H=Path(__file__).resolve().parent;U=g.U
U.EnumWindows.argtypes=[g.CB,w.LPARAM];U.EnumWindows.restype=w.BOOL
a=json.loads((H/'GUI-attempt.json').read_text());assert time.monotonic()<a['end']
pid=json.loads((H/'OWN_GUI_PROCESS.json').read_text())['pid']
assert not (H/'GUI_RESULT.json').exists()
rows=g.windows(pid);assert len(rows)==1 and rows[0]['role']=='main'
command=sys.argv[1]
assert command in ['help','help source','help open_design','help report_net','help get_pins','help get_nets']
old=list(H.glob('QUERY-*.json'));assert len(old)<6
with (H/('QUERY-'+str(len(old)+1)+'.json')).open('x',encoding='utf-8') as f:json.dump(dict(command=command,elapsed=time.monotonic()-a['start'],kind='read-only native help'),f)
for ch in command:U.PostMessageW(rows[0]['hwnd'],0x102,ord(ch),0);time.sleep(.001)
U.PostMessageW(rows[0]['hwnd'],0x100,13,0);U.PostMessageW(rows[0]['hwnd'],0x101,13,0)
print('Sent read-only native help in existing session; no new vendor process')
