from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'PLAN.json').exists():raise SystemExit('Frozen plan exists')
def a(rd,rs,n):return ((n&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def c(addr,rs,rd=0,f=1):return (addr<<20)|(rs<<15)|(f<<12)|(rd<<7)|0x73
def sw(rs,off):return ((off>>5)<<25)|(rs<<20)|0x2023|((off&31)<<7)
tests=[]
def put(name,mask,cause,vector,order='global',mode='irq'):
 base=256+vector;code=[a(1,0,base),c(0x305,1),a(2,0,mask//2),a(2,2,mask-mask//2)]
 wb=[[1,base],[2,mask//2],[2,mask]]
 if order=='global':code +=[c(0x304,2),a(3,0,8),c(0x300,3)];wb +=[[3,8]]
 else:code +=[a(3,0,8),c(0x300,3),c(0x304,2)];wb +=[[3,8]]
 if mode=='disable':
  code +=[c(0x300,0),a(4,0,91),sw(4,512),0x6f];wb +=[[4,91]];stores=[[512,91,15]];traps=[];endstatus=['00000000','3'];entry=None
 else:
  epc=len(code)*4
  if mode=='exception':code +=[0x73,sw(1,600)];cause=11;trapcause=11;entry=256;handler=[a(11,0,111),sw(11,516),0x6f];wb +=[[11,111]];stores=[[516,111,15]];endstatus=['00001880','3']
  else:
   code +=[a(4,0,91),sw(4,512),0x6f];trapcause=0x80000000|cause;entry=256+(4*cause if vector else 0)
   handler=[c(0x341,0,10,2),a(11,0,cause),sw(11,516),0x30200073];wb +=[[10,epc],[11,cause],[4,91]];stores=[[516,cause,15],[512,91,15]];endstatus=['00000088','3']
  traps=[[epc,trapcause,0]]
 rom=[0x13]*1024;rom[:len(code)]=code
 if entry is not None:rom[entry//4:entry//4+len(handler)]=handler
 # Unselected entries store a distinct forbidden signature, then loop.
 for p in [256,268,284,300]:
  if entry is None or not(entry<=p<entry+len(handler)*4):rom[p//4]=sw(1,604);rom[p//4+1]=0x6f
 d=H/'inputs'/name;d.mkdir(parents=True);p=d/'program.hex';p.write_text(''.join(f'{x:08x}\n' for x in rom))
 tests.append(dict(name=name,mask=mask,wb=wb,stores=stores,traps=traps,entry=entry,status=endstatus,enable_pc=24,irq_from_cycle=1,program_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),mode=mode))
for cause,mask in [(3,8),(7,128),(11,2048)]:
 for vector in [0,1]:put(f'irq_{cause}_vector{vector}',mask,cause,vector)
put('priority_external',2184,11,1)
put('priority_software',136,3,1)
put('mie_enable_pending',128,7,1,order='mie')
put('disable_adjacent_pending',128,7,1,mode='disable')
put('exception_beats_pending_vectored',128,7,1,mode='exception')
(H/'PLAN.json').write_text(json.dumps(dict(version='1.0.0',frozen_before_dut=True,scope='Finite M-mode direct/vector traps, enabling CSR response, masking, priority, MRET. Inputs held pending from first cycle until first accepted trap; no S/U.',response_pipeline_steps=3,tests=tests),indent=2));print(len(tests),hashlib.sha256((H/'PLAN.json').read_bytes()).hexdigest())
