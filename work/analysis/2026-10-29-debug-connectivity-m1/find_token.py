from pathlib import Path
import json,time,sys,ctypes.wintypes as w
import gui_control as g
H=Path(__file__).resolve().parent;U=g.U;U.EnumWindows.argtypes=[g.CB,w.LPARAM];U.EnumWindows.restype=w.BOOL
a=json.loads((H/'GUI-attempt.json').read_text());assert time.monotonic()<a['end']
rows=g.windows(json.loads((H/'OWN_GUI_PROCESS.json').read_text())['pid'])
assert len(rows)==1 and rows[0]['role']=='main' and rows[0]['client_size']==[1707,996]
token=sys.argv[1];assert token in ['stopped','write_error','stop_kind','eei_hold','sys_rst_n','u_CORES/drck_o','*trig0_d1*','*trig0_d1*136*','*stopped*','*stop_kind*','*write_error*']
hw=rows[0]['hwnd']
# Use the visually confirmed native Clear button; WM_CHAR backspace was ignored.
U.PostMessageW(hw,0x201,1,(135<<16)|249);U.PostMessageW(hw,0x202,0,(135<<16)|249);time.sleep(.15)
U.PostMessageW(hw,0x201,1,(136<<16)|160);U.PostMessageW(hw,0x202,0,(136<<16)|160)
for ch in token:U.PostMessageW(hw,0x102,ord(ch),0);time.sleep(.001)
U.PostMessageW(hw,0x100,13,0);U.PostMessageW(hw,0x101,13,0)
with (H/('FIND-'+str(len(list(H.glob('FIND-*.json')))+1)+'.json')).open('x') as f:json.dump(dict(token=token,elapsed=time.monotonic()-a['start']),f)
