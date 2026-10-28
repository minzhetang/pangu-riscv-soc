from pathlib import Path
import ctypes.wintypes as w,time,json
import gui_control as g
H=Path(__file__).resolve().parent;U=g.U;U.EnumWindows.argtypes=[g.CB,w.LPARAM];U.EnumWindows.restype=w.BOOL
a=json.loads((H/'GUI-attempt.json').read_text());assert time.monotonic()<a['end']
rows=g.windows(json.loads((H/'OWN_GUI_PROCESS.json').read_text())['pid'])
assert len(rows)==1 and rows[0]['role']=='main' and rows[0]['client_size']==[1707,996]
hw=rows[0]['hwnd'];p=H/'scripts/catalog.tcl';assert p.is_file() and ' ' not in p.as_posix()
assert not (H/'PLAIN_SOURCE.json').exists()
U.PostMessageW(hw,0x201,1,(934<<16)|392);U.PostMessageW(hw,0x202,0,(934<<16)|392)
command='source '+p.as_posix()
for ch in command:U.PostMessageW(hw,0x102,ord(ch),0);time.sleep(.001)
U.PostMessageW(hw,0x100,13,0);U.PostMessageW(hw,0x101,13,0)
with (H/'PLAIN_SOURCE.json').open('x') as f:json.dump(dict(command=command,elapsed=time.monotonic()-a['start'],reason='Native console treated Tcl braces as filename characters; same reviewed script with unquoted no-space path'),f,indent=2)
