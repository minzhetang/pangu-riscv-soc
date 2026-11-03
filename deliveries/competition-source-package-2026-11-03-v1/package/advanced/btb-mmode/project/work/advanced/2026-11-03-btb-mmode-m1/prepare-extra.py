from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'FROZEN_EXTRA_PLAN.json').exists():raise SystemExit('Frozen extra plan exists. Use a new isolated directory.')
def a(rd,rs,n):return ((n&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def c(addr,rs,rd=0,f=1):return (addr<<20)|(rs<<15)|(f<<12)|(rd<<7)|0x73
def j(rd,n):return (((n>>20)&1)<<31)|(((n>>1)&1023)<<21)|(((n>>11)&1)<<20)|(((n>>12)&255)<<12)|(rd<<7)|0x6f
def s(rs,off):return (((off>>5)&127)<<25)|(rs<<20)|0x2023|((off&31)<<7)
def l(rd,v):return (v&0xfffff000)|(rd<<7)|0x37
tests=[]
def put(name,code,wb,stores,traps=(),handler=None,**kw):
 rom=[0x13]*1024;rom[:len(code)]=code;h=handler or [j(0,0)];rom[64:64+len(h)]=h
 t=dict(name=name,rom=rom,wb=wb,stores=stores,traps=list(traps),irq=0,refresh=0,**kw);tests.append(t)
 d=H/'inputs'/name;d.mkdir(parents=True,exist_ok=False);(d/'program.hex').write_text(''.join(f'{v:08x}\n' for v in rom))
base=[a(1,0,256),c(0x305,1)]
code=base+[a(2,0,32),j(5,8),s(1,600),0x00010367,0x13,0x13,a(2,0,48),j(0,-16),0x13,0x13,s(6,512),j(0,0)]
put('jalr_target_change',code,[[1,256],[2,32],[5,16],[6,24],[2,48],[6,24]],[[512,24,15]])
code=base+[a(2,0,128),c(0x304,2),a(2,0,-1),c(0x3b0,2),a(2,0,31),c(0x3a0,2),l(2,0x80000000),c(0x180,2),l(2,0x21000),a(2,2,-2040),c(0x300,2),l(4,0x400000),a(3,0,55),s(3,512),0x00022283,s(5,516),j(0,0)]
put('irq_during_walk',code,[[1,256],[2,128],[2,0xffffffff],[2,31],[2,0x80000000],[2,0x21000],[2,0x20808],[4,0x400000],[3,55],[10,64]],[[512,55,15],[516,64,15]],[[64,0x80000007,0]],handler=[c(0x341,0,10,2),s(10,516),j(0,0)],expect_mret=False,irq_at=23,require_stall=True)
tests[-1]['irq']=128
p=H/'FROZEN_EXTRA_PLAN.json';p.write_text(json.dumps(dict(version='1.0.0',frozen_before_dut=True,tests=tests),indent=2));print(hashlib.sha256(p.read_bytes()).hexdigest())
