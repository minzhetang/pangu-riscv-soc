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
def emulate(seed,directory):
 binary=(H/'program.bin').read_bytes();r=[0]*32;mem=bytearray(32768)
 mem[:8192]=b''.join(int(v,16).to_bytes(4,'little') for v in (H/'program.hex').read_text().splitlines())
 mem[0x2000:0x2004]=seed.to_bytes(4,'little');pc=0;wb=[];st=[];opcounts={}
 for steps in range(1000000):
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
   if addr+n>len(mem) or addr%n:raise ValueError(('data range/alignment',pc,addr))
   if op==3:
    value=int.from_bytes(mem[addr:addr+n],'little')
    if f<4:value=sext(value,n*8)
   else:
    mem[addr:addr+n]=(b&((1<<(8*n))-1)).to_bytes(n,'little');lane=addr%4
    st.append(f'STORE {addr:08x} {((b&((1<<(8*n))-1))<<(8*lane)):08x} {(((1<<n)-1)<<lane):x}')
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
  if value is not None and rd:r[rd]=value&MASK;wb.append(f'WB {rd} {r[rd]:08x}')
  r[0]=0;pc=nxt&MASK
  if st and st[-1]=='STORE 00003020 600d600d f':break
 else:raise ValueError('reference step limit')
 expected=algorithm(seed);actual=[int.from_bytes(mem[0x3004+i*4:0x3008+i*4],'little') for i in range(3)]
 if actual!=expected or int.from_bytes(mem[0x301c:0x3020],'little')!=0:raise ValueError(('independent algorithm mismatch',actual,expected))
 directory.mkdir(parents=True,exist_ok=False)
 for name,lines in [('wb.txt',wb),('store.txt',st),('regs.txt',[f'REG {i} {v:08x}' for i,v in enumerate(r)]),('memory.txt',[f'MEM {i} {int.from_bytes(mem[i*4:i*4+4],"little"):08x}' for i in range(8192)])]:(directory/name).write_text('\n'.join(lines)+'\n')
 return dict(seed=seed,algorithm_results=expected,instructions=steps+1,wb_count=len(wb),store_count=len(st),opcodes=opcounts,files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir()})
if __name__=='__main__':
 if (H/'FROZEN_REFERENCE.json').exists():raise SystemExit('Frozen reference exists')
 result=[emulate(seed,H/'expected'/f'{seed:08x}') for seed in [1,0xdeadbeef]]
 (H/'FROZEN_REFERENCE.json').write_text(json.dumps(dict(binary_sha256=hashlib.sha256((H/'program.bin').read_bytes()).hexdigest(),cases=result,scope='Sequential RV32I model + independent high-level algorithm; frozen before DUT, not CPU simulation',cycle_limit=300000,process_seconds=60),indent=2));print(json.dumps(result,indent=2))
