import ctypes.wintypes as w,time,json
from pathlib import Path
import gui_control as g
H=Path(__file__).resolve().parent;U=g.U;U.EnumWindows.argtypes=[g.CB,w.LPARAM];U.EnumWindows.restype=w.BOOL
a=json.loads((H/'GUI-attempt.json').read_text());assert time.monotonic()<a['end']
r=g.windows(json.loads((H/'OWN_GUI_PROCESS.json').read_text())['pid']);assert len(r)==1 and r[0]['role']=='main' and r[0]['client_size']==[1707,996]
hw=r[0]['hwnd'];assert not (H/'WIDEN_LAYOUT.json').exists()
U.PostMessageW(hw,0x201,1,(470<<16)|293)
for x in range(293,795,25):U.PostMessageW(hw,0x200,1,(470<<16)|x);time.sleep(.015)
U.PostMessageW(hw,0x202,0,(470<<16)|793)
with (H/'WIDEN_LAYOUT.json').open('x') as f:json.dump(dict(operation='Resize visible browser splitter only',elapsed=time.monotonic()-a['start']),f)
