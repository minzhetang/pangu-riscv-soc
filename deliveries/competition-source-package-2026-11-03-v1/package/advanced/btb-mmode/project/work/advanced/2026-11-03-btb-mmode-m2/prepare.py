from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'PLAN.json').exists():raise SystemExit('Existing frozen plan; use a new directory.')
def a(rd,rs,n):return ((n&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def c(addr,rs):return (addr<<20)|(rs<<15)|0x1073
def j(rd,n):return (((n>>20)&1)<<31)|(((n>>1)&1023)<<21)|(((n>>11)&1)<<20)|(((n>>12)&255)<<12)|(rd<<7)|0x6f
def b(f,n):return (((n>>12)&1)<<31)|(((n>>5)&63)<<25)|(f<<12)|(((n>>1)&15)<<8)|(((n>>11)&1)<<7)|0x63
def s(rs,off):return (((off>>5)&127)<<25)|(rs<<20)|0x2023|((off&31)<<7)
setup=[a(1,0,256),c(0x305,1),a(2,0,-1),c(0x3b0,2),a(2,0,31),c(0x3a0,2),0x80000137,c(0x180,2),0x00001137,a(2,2,-12),c(0x341,2),a(2,0,1024),a(2,2,1024),c(0x300,2),0x00002337,0x30200073]
basewb=[[1,256],[2,0xffffffff],[2,31],[2,0x80000000],[2,4096],[2,0xff4],[2,1024],[2,2048],[6,8192],[7,99]]
tests=[]
for name,ins,link,taken in [('jal_ifmiss',j(5,0x1008),True,True),('jalr_ifmiss',0x000302e7,True,True),('beq_ifmiss',b(0,0x1008),False,True),('bne_hold_training',b(1,8),False,False)]:
 rom=[0x13]*4096;rom[:len(setup)]=setup;rom[64]=j(0,0)
 rom[0xff4//4]=a(7,0,99);rom[0xff8//4]=ins
 wb=basewb.copy()
 if taken:
  rom[0xffc//4]=s(7,600);rom[0x2000//4]=s(5,512);rom[0x2004//4]=s(7,516);rom[0x2008//4]=j(0,0)
  if link:wb=wb+[[5,0xffc]]
  stores=[[512,0xffc if link else 0,15],[516,99,15]]
 else:
  rom[0xffc//4]=a(7,7,1);rom[0x1000//4]=s(7,512);rom[0x1004//4]=s(7,516);rom[0x1008//4]=j(0,0)
  wb=wb+[[7,100]];stores=[[512,100,15],[516,100,15]]
 d=H/'inputs'/name;d.mkdir(parents=True,exist_ok=False);p=d/'program.hex';p.write_text(''.join(f'{x:08x}\n' for x in rom))
 tests.append(dict(name=name,wb=wb,stores=stores,traps=[],focus_pc=0xff8,focus_train=1,require_focus_ifmiss=True,program_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
p=H/'PLAN.json';p.write_text(json.dumps(dict(version='1.0.0',scope='Existing supervisor translation exercised only as a natural IF-stall fixture, no new S/U/MMU implementation or conformance claim',cycles=400,tests=tests),indent=2));print(hashlib.sha256(p.read_bytes()).hexdigest())
