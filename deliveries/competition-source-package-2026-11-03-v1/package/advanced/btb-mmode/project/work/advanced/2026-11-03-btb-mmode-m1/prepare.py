from pathlib import Path
import json,hashlib,shutil
H=Path(__file__).resolve().parent
if (H/'FROZEN_PLAN.json').exists():raise SystemExit('Frozen plan exists. Use a new isolated directory; do not overwrite evidence.')
def add(rd,rs,imm):return ((imm&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def csr(a,rs,rd=0,f=1):return (a<<20)|(rs<<15)|(f<<12)|(rd<<7)|0x73
def jal(rd,o):return (((o>>20)&1)<<31)|(((o>>1)&1023)<<21)|(((o>>11)&1)<<20)|(((o>>12)&255)<<12)|(rd<<7)|0x6f
def br(f,a,b,o):return (((o>>12)&1)<<31)|(((o>>5)&63)<<25)|(b<<20)|(a<<15)|(f<<12)|(((o>>1)&15)<<8)|(((o>>11)&1)<<7)|0x63
def sw(rs,base,off=0):return (((off>>5)&127)<<25)|(rs<<20)|(base<<15)|(2<<12)|((off&31)<<7)|0x23
def lui(rd,v):return (v&0xfffff000)|(rd<<7)|0x37
base=[add(1,0,256),csr(0x305,1)]
tests=[]
def case(name,code,wb,stores=(),traps=(),handler=None,**kw):
 rom=[0x13]*1024;rom[:len(code)]=code
 h=handler or [jal(0,0)];rom[64:64+len(h)]=h
 t=dict(name=name,rom=rom,wb=wb,stores=list(stores),traps=list(traps),irq=0,refresh=0,**kw)
 tests.append(t)
for name,body,epc,target in [('jal',[jal(5,2)],8,10),('jalr',[add(2,0,14),0x000102e7],12,14),('taken_branch',[br(0,0,0,2)],8,10)]:
 wb=[[1,256]]+([[2,14]] if name=='jalr' else [])+[[10,512]]
 case(name,base+body,wb,[[512,0,15]],[[epc,0,target]],handler=[add(10,0,512),sw(5,10),jal(0,0)])
case('not_taken_misaligned',base+[br(1,0,0,2),add(6,0,9),jal(0,0)],[[1,256],[6,9]])
case('jal_link_flush',base+[jal(5,8),sw(1,0,600),add(6,5,1),sw(6,0,512),jal(0,0)],[[1,256],[5,12],[6,13]],[[512,13,15]])
case('jalr_link_flush',base+[add(2,0,20),0x000102e7,sw(1,0,600),add(6,5,1),sw(6,0,512),jal(0,0)],[[1,256],[2,20],[5,16],[6,17]],[[512,17,15]])
# Hand calculation: x2=5..0, five decrements; branch at24 taken four times.
loop=base+[add(2,0,5),add(3,0,0),add(3,3,2),add(2,2,-1),br(1,2,0,-8),sw(3,0,512),jal(0,0)]
wb=[[1,256],[2,5],[3,0]]
for i in range(5):wb += [[3,(i+1)*2],[2,4-i]]
case('branch_loop',loop,wb,[[512,10,15]])
for name,body,cause,tval in [('illegal',[0xffffffff],2,0xffffffff),('ecall',[0x73],11,0),('ebreak',[0x00100073],3,8),('load_misaligned',[0x00202283],4,2),('store_misaligned',[sw(1,0,2)],6,2)]:
 case(name,base+body,[[1,256]],traps=[[8,cause,tval]])
# Every interrupt is raised at edge80, after the one-instruction loop is warm.
# The handler reads mepc, marks completion and MRETs. IRQ falls on trap entry.
for name,mask,cause in [('timer',128,7),('software',8,3),('external',2048,11),('priority',2184,11)]:
 code=base+[lui(2,mask),add(2,2,mask&4095) if mask<2048 else add(2,2,mask-4096),csr(0x304,2),add(3,0,8),csr(0x300,3),jal(0,0)]
 # Avoid LUI/sign corner by build small mask via two positive ADDIs for >=2048.
 code=base+[add(2,0,mask//2),add(2,2,mask-mask//2),csr(0x304,2),add(3,0,8),csr(0x300,3),jal(0,0)]
 case('irq_'+name,code,[[1,256],[2,mask//2],[2,mask],[3,8],[10,28],[11,77]],traps=[[28,0x80000000|cause,0]],handler=[csr(0x341,0,10,2),add(11,0,77),0x30200073],irq_mask=mask)
 tests[-1]['irq']=mask
case('irq_masked',base+[add(2,0,128),csr(0x304,2),jal(0,0)],[[1,256],[2,128]])
tests[-1]['irq']=128
# An external instruction-port refresh changes the warm JAL at8 to an ADDI.
# This is a predictor recovery diagnostic, not an instruction-cache/FENCE.I claim.
case('stale_nonbranch',base+[jal(0,0),sw(10,0,512),jal(0,0)],[[1,256],[10,7]],[[512,7,15]])
tests[-1]['refresh']=1
# Natural MPRV data-translation miss, CPU still executes M-mode instructions.
# PMP NAPOT all; constant root superpage PTE maps both virtual pages to PA0.
code=base+[add(2,0,-1),csr(0x3b0,2),add(2,0,31),csr(0x3a0,2),lui(2,0x80000000),csr(0x180,2),lui(2,0x20000),add(2,2,0x800-4096),add(2,2,2047),add(2,2,1)]
# mstatus=0x20800: MPRV=1,MPP=S. Set exactly with LUI+ADDI pair.
code=base+[add(2,0,-1),csr(0x3b0,2),add(2,0,31),csr(0x3a0,2),lui(2,0x80000000),csr(0x180,2),lui(2,0x21000),add(2,2,-2048),csr(0x300,2),lui(4,0x400000),add(3,0,55),sw(3,0,512),0x00022283,sw(5,0,516),jal(0,0)]
case('mprv_store_hold',code,[[1,256],[2,0xffffffff],[2,31],[2,0x80000000],[2,0x21000],[2,0x20800],[4,0x400000],[3,55],[5,0]],[[512,55,15],[516,0,15]],require_stall=True)
plan=dict(version='1.0.0',frozen_before_dut=True,limits=dict(cycles=400,compile_seconds=35,run_seconds=10),tests=tests,
 scope='Finite M-mode/BTB simulation, plus one MPRV stall diagnostic; no complete S/U/MMU/PMP verification')
(H/'FROZEN_PLAN.json').write_text(json.dumps(plan,indent=2))
for t in tests:
 d=H/'inputs'/t['name'];d.mkdir(parents=True,exist_ok=True)
 (d/'program.hex').write_text(''.join(f'{v:08x}\n' for v in t['rom']))
print(len(tests),hashlib.sha256((H/'FROZEN_PLAN.json').read_bytes()).hexdigest())
