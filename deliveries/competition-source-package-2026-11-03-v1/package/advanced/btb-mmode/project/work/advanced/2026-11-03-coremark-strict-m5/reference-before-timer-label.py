from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;MASK=0xffffffff
def signed(x):return x-0x100000000 if x&0x80000000 else x
def sext(x,n):return x-(1<<n) if x&(1<<(n-1)) else x
def algorithm(seed):
 a=[];x=seed
 for _ in range(32):
  x=(x^(x<<13))&MASK;x^=x>>17;x=(x^(x<<5))&MASK;a.append(x&65535)
 a.sort();sm=sum(a)&MASK;crc=MASK
 for v in a:
  for _ in range(4):
   crc^=v&255;v>>=8
   for _ in range(8):crc=((crc>>1)^(0xedb88320 if crc&1 else 0))&MASK
 x=sm
 for i in range(64):
  x^=a[i&31]
  x=(((x>>2)+(x<<5)+0x2468ace0) if i&1 else ((x<<3)^(x>>7)^0x13579bdf))&MASK
 return [sm,(~crc)&MASK,x]
def emulate(mode,directory,timer_reads=None):
 binary=(H/'build'/mode/'program.bin').read_bytes();r=[0]*32;mem=bytearray(0x18000)
 mem[:32768]=b''.join(int(v,16).to_bytes(4,'little') for v in (H/'build'/mode/'program.hex').read_text().splitlines())
 pc=0;wb_count=0;store_count=0;opcounts={};directory.mkdir(parents=True,exist_ok=False);timer_index=0
 fw=(directory/'wb.txt').open('w');fs=(directory/'store.txt').open('w');uart=[];complete=False
 for steps in range(5000000):
  if pc%4 or pc+4>len(binary):raise ValueError(('fetch range',pc))
  ins=int.from_bytes(binary[pc:pc+4],'little');op=ins&127;rd=(ins>>7)&31;rs1=(ins>>15)&31;rs2=(ins>>20)&31;f=(ins>>12)&7;hi=ins>>25;a=r[rs1];b=r[rs2];nxt=pc+4;value=None
  opcounts[str(op)]=opcounts.get(str(op),0)+1
  if op==0x37:value=ins&0xfffff000
  elif op==0x17:value=pc+(ins&0xfffff000)
  elif op==0x6f:
   imm=sext(((ins>>31)<<20)|(((ins>>12)&255)<<12)|(((ins>>20)&1)<<11)|(((ins>>21)&1023)<<1),21);value=pc+4;nxt=pc+imm
  elif op==0x67:value=pc+4;nxt=(a+sext(ins>>20,12))&~1
  elif op==0x63:
   imm=sext(((ins>>31)<<12)|(((ins>>7)&1)<<11)|(((ins>>25)&63)<<5)|(((ins>>8)&15)<<1),13)
   taken={0:a==b,1:a!=b,4:signed(a)<signed(b),5:signed(a)>=signed(b),6:a<b,7:a>=b}[f]
   if taken:nxt=pc+imm
  elif op in [0x03,0x23]:
   imm=sext(ins>>20,12) if op==3 else sext(((ins>>25)<<5)|((ins>>7)&31),12);addr=(a+imm)&MASK;n={0:1,1:2,2:4,4:1,5:2}[f]
   mmio=addr in [0x20000000,0x20000008,0x20000100,0x20000104]
   if (not mmio and (addr+n>len(mem) or not (addr<0x8000 or addr>=0x10000))) or addr%n:raise ValueError(('data range/alignment',pc,addr))
   if op==3:
    if timer_reads is not None and addr in [0x20000100,0x20000104]:
     expected_addr,value=timer_reads[timer_index];timer_index+=1
     if addr!=expected_addr:raise ValueError('timer transaction order mismatch')
    else:value=(1 if addr==0x20000008 else 0) if mmio else int.from_bytes(mem[addr:addr+n],'little')
    if f<4:value=sext(value,n*8)
   else:
    if mmio:
     if addr!=0x20000000:raise ValueError('MMIO write not allowed')
     uart.append(b&255)
    else:
     if addr<0x10000:raise ValueError('write to ROM/hole')
     mem[addr:addr+n]=(b&((1<<(8*n))-1)).to_bytes(n,'little')
    lane=addr%4;fs.write(f'STORE {addr:08x} {((b&((1<<(8*n))-1))<<(8*lane)):08x} {(((1<<n)-1)<<lane):x}\n');store_count+=1
    if addr==0x17ffc and b==0x600d600d:complete=True
  elif op in [0x13,0x33]:
   rhs=sext(ins>>20,12) if op==0x13 else b;sh=rhs&31
   if f==0:value=a-rhs if op==0x33 and hi==32 else a+rhs
   elif f==1:value=a<<sh
   elif f==2:value=int(signed(a)<signed(rhs&MASK))
   elif f==3:value=int(a<(rhs&MASK))
   elif f==4:value=a^rhs
   elif f==5:value=signed(a)>>sh if hi==32 else a>>sh
   elif f==6:value=a|rhs
   elif f==7:value=a&rhs
  else:raise ValueError(('unsupported instruction',pc,hex(ins)))
  if value is not None and rd:r[rd]=value&MASK;fw.write(f'WB {rd} {r[rd]:08x}\n');wb_count+=1
  r[0]=0;pc=nxt&MASK
  if complete:break
 else:raise ValueError('reference step limit')
 fw.close();fs.close();text=bytes(uart).decode('ascii');(directory/'uart.txt').write_text(text)
 if timer_reads is not None and timer_index!=len(timer_reads):raise ValueError('unexpected extra timer reads')
 expected=['0xe714','0x1fd7','0x8e3a'] if mode=='performance' else ['0xe3c1','0x0747','0x8d84']
 import re
 crcs=[re.search(r'\[0\]'+name+r'\s*:\s*(0x[0-9a-f]+)',text).group(1) for name in ['crclist','crcmatrix','crcstate']]
 if crcs!=expected or int.from_bytes(mem[0x17ff8:0x17ffc],'little')!=0:raise ValueError(('CRC/return mismatch',crcs,expected))
 if 'ERROR! Must execute for at least 10 secs for a valid result!' not in text or re.search(r'ERROR! (?!Must execute)',text):raise ValueError('unexpected CoreMark error')
 for name,ls in [('regs.txt',[f'REG {i} {v:08x}' for i,v in enumerate(r)]),('memory.txt',[f'MEM {i} {int.from_bytes(mem[i*4:i*4+4],"little"):08x}' for i in range(0x18000//4)])]:(directory/name).write_text('\n'.join(ls)+'\n')
 return dict(mode=mode,crcs=crcs,instructions=steps+1,wb_count=wb_count,store_count=store_count,opcodes=opcounts,files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir()},timer='Constant zero mock, ONLY deterministic functional/cycle comparison; no target elapsed time or score')
if __name__=='__main__':
 if (H/'FROZEN_REFERENCE.json').exists():raise SystemExit('Frozen reference exists')
 result=[emulate(mode,H/'expected'/mode) for mode in ['performance','validation']]
 (H/'FROZEN_REFERENCE.json').write_text(json.dumps(dict(cases=result,scope='Sequential RV32I model and upstream known CRC, frozen before DUT. Constant timer mock means no formal CoreMark score.',cycle_limit=4000000,process_seconds=600),indent=2));print(json.dumps(result,indent=2))
