from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'IRQ_PLAN.json').exists():raise SystemExit('plan frozen')
def a(rd,rs,n):return ((n&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def c(addr,rs,rd=0,f=1):return (addr<<20)|(rs<<15)|(f<<12)|(rd<<7)|0x73
def sw(rs,off):return ((off>>5)<<25)|(rs<<20)|0x2023|((off&31)<<7)
handler=[c(0x341,0,10,2),a(11,0,7),sw(11,516),0x30200073];tests=[]
code=[a(1,0,257),c(0x305,1),a(2,0,128),c(0x304,2),a(3,0,4),a(3,3,4),c(0x300,3),sw(1,512),a(4,0,91),0x6f]
tests.append(dict(name='interrupt_before_store',code=code,wb=[[1,257],[2,128],[3,4],[3,8],[10,28],[11,7],[4,91]],stores=[[516,7,15],[512,257,15]],traps=[[28,0x80000007,0]],enable_pc=24))
code=[a(1,0,257),c(0x305,1),a(2,0,128),c(0x304,2),0x000021b7,a(3,3,-1920),c(0x300,3),a(4,0,128),c(0x341,4),0x30200073]
tests.append(dict(name='mret_pending_response',code=code,wb=[[1,257],[2,128],[3,8192],[3,0x1880],[4,128],[10,128],[11,7],[5,91]],stores=[[516,7,15],[512,91,15]],traps=[[128,0x80000007,0]],enable_pc=36,mret=True))
for t in tests:
 code=t.pop('code');rom=[0x13]*1024;rom[:len(code)]=code;rom[71:75]=handler
 if t.get('mret'):rom[32:35]=[a(5,0,91),sw(5,512),0x6f]
 d=H/'inputs'/t['name'];d.mkdir(parents=True);p=d/'program.hex';p.write_text(''.join(f'{v:08x}\n' for v in rom))
 t.update(mask=128,entry=284,status=['00000088','3'],program_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
(H/'IRQ_PLAN.json').write_text(json.dumps(dict(scope='Finite MRET immediate-pending response and interrupt before STORE',tests=tests),indent=2))
