"""Finite architectural oracle for THIS firmware, not ISA/CPU certification.
MMIO reads are injected only through an explicit callback. For DUT comparison
the callback MUST use a previously frozen, independent peripheral timing model,
not the DUT's returned data. The standalone selftest uses a labelled synthetic
environment and does not demonstrate any CPU or B module execution.
"""
from pathlib import Path
import json,struct
MASK=0xffffffff
def sx(v,b):return ((v&((1<<b)-1))^(1<<(b-1)))-(1<<(b-1))
def hx(v):return f'{v&MASK:08x}'
class Reference:
    def __init__(self,image,io_read,io_write):
        assert len(image)<=32768
        self.rom=image+bytes(32768-len(image));self.ram=bytearray([0xa5]*32768)
        self.regs=[0]*32;self.pc=0;self.steps=0;self.stopped=False;self.stall=0;self.flush=0;self.last_load=0
        self.EX=[];self.WB=[];self.MEM=[];self.io_read=io_read;self.io_write=io_write
    def ordinary_read(self,address,size):
        if 0<=address and address+size<=32768:return int.from_bytes(self.rom[address:address+size],'little')
        assert 0x10000<=address and address+size<=0x18000,('unmapped read',hx(address))
        return int.from_bytes(self.ram[address-0x10000:address-0x10000+size],'little')
    def step(self):
        assert not self.stopped and self.steps<2000000 and self.pc%4==0 and 0<=self.pc<32768
        pc=self.pc;word=self.ordinary_read(pc,4)
        if word==0x00100073:self.stopped=True;return
        op=word&127;rd=(word>>7)&31;f3=(word>>12)&7;r1=(word>>15)&31;r2=(word>>20)&31;f7=word>>25
        a,b=self.regs[r1],self.regs[r2];value=None;next_pc=(pc+4)&MASK
        uses1=op in [0x13,0x33,3,0x23,0x63,0x67];uses2=op in [0x33,0x23,0x63]
        if self.last_load and ((uses1 and r1==self.last_load) or (uses2 and r2==self.last_load)):self.stall+=1
        self.last_load=rd if op==3 and rd else 0
        self.EX.append(hx(pc));self.steps+=1
        if op==0x37:value=word&0xfffff000
        elif op==0x17:value=pc+(word&0xfffff000)
        elif op==0x13:
            imm=sx(word>>20,12)
            if f3==0:value=a+imm
            elif f3==1:
                assert f7==0;value=a<<((word>>20)&31)
            elif f3==2:value=int(sx(a,32)<imm)
            elif f3==3:value=int(a<(imm&MASK))
            elif f3==4:value=a^(imm&MASK)
            elif f3==5:
                assert f7 in [0,32];value=a>>((word>>20)&31) if f7==0 else sx(a,32)>>((word>>20)&31)
            elif f3==6:value=a|(imm&MASK)
            elif f3==7:value=a&(imm&MASK)
        elif op==0x33:
            assert f7==0 or (f7==32 and f3 in [0,5])
            if f3==0:value=a+b if f7==0 else a-b
            elif f3==1:value=a<<(b&31)
            elif f3==2:value=int(sx(a,32)<sx(b,32))
            elif f3==3:value=int(a<b)
            elif f3==4:value=a^b
            elif f3==5:value=a>>(b&31) if f7==0 else sx(a,32)>>(b&31)
            elif f3==6:value=a|b
            elif f3==7:value=a&b
        elif op in [3,0x23]:
            imm=sx(word>>20,12) if op==3 else sx((word>>25)<<5|((word>>7)&31),12)
            address=(a+imm)&MASK;size={0:1,1:2,2:4,4:1,5:2}.get(f3)
            assert size and address%size==0
            io=(0x20000000<=address<=0x200000ff) or address in [0x20000100,0x20000104]
            if op==3:
                if io:
                    assert f3==2;raw=self.io_read(pc,address)&MASK;value=raw
                else:
                    raw=self.ordinary_read(address&~3,4);value=self.ordinary_read(address,size)
                    if f3 in [0,1]:value=sx(value,size*8)&MASK
                self.MEM.append(['READ',hx(pc),hx(address),hx(raw),hx(value)])
            else:
                assert f3 in [0,1,2]
                data=(b&((1<<(size*8))-1))<<((address&3)*8);mask=((1<<size)-1)<<(address&3)
                if io:
                    assert size==4;self.io_write(pc,address,data,mask)
                else:
                    assert 0x10000<=address and address+size<=0x18000
                    self.ram[address-0x10000:address-0x10000+size]=(b&((1<<(size*8))-1)).to_bytes(size,'little')
                self.MEM.append(['STORE',hx(pc),hx(address),hx(data),f'{mask:x}'])
        elif op==0x63:
            imm=sx((word>>31)<<12|((word>>7)&1)<<11|((word>>25)&63)<<5|((word>>8)&15)<<1,13)
            assert f3 in [0,1,4,5,6,7]
            take={0:a==b,1:a!=b,4:sx(a,32)<sx(b,32),5:sx(a,32)>=sx(b,32),6:a<b,7:a>=b}[f3]
            if take:next_pc=(pc+imm)&MASK;self.flush+=1
        elif op==0x6f:
            imm=sx((word>>31)<<20|((word>>12)&255)<<12|((word>>20)&1)<<11|((word>>21)&1023)<<1,21)
            value=pc+4;next_pc=(pc+imm)&MASK;self.flush+=1
        elif op==0x67:
            assert f3==0;value=pc+4;next_pc=((a+sx(word>>20,12))&MASK)&~1;self.flush+=1
        else:raise AssertionError(('unsupported program encoding',hx(pc),hx(word)))
        if value is not None and rd:self.regs[rd]=value&MASK;self.WB.append([str(rd),hx(value)])
        self.regs[0]=0;self.pc=next_pc

def selftest():
    import importlib.util
    h=Path(__file__).resolve().parent;p=h.parents[2]
    spec=importlib.util.spec_from_file_location('elf',p/'work/system/2026-10-23-c-boot-m1/check_c_boot.py')
    e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
    symbols=e.elf_symbols(h/'build/soc.elf');manual=json.loads((h/'manual-expectations.json').read_text())
    writes=[];state=dict(gpio=0,gin_reads=0,status_reads=0,last_ready=0)
    def io_read(pc,address):
        off=address&255
        if off==8:
            state['status_reads']+=1;v=int(state['status_reads']%2==0);state['last_ready']=v;return v
        if off==12:return state['gpio']
        if off==16:
            state['gin_reads']+=1;return 0x3c if state['gin_reads']<=2 else 0xc3
        raise AssertionError(('unexpected IO read',pc,address))
    def io_write(pc,address,data,mask):
        assert mask==15
        if address==0x2000000c:state['gpio']=data&255
        elif address==0x20000000:assert state['last_ready']==1;state['last_ready']=0
        else:raise AssertionError('unexpected IO write')
        writes.append((address,data&255))
    r=Reference((h/'build/soc.bin').read_bytes(),io_read,io_write)
    while not r.stopped:r.step()
    def word(symbol,index=0):
        address=symbols[symbol]+index*4;return int.from_bytes(r.ram[address-0x10000:address-0x10000+4],'little')
    assert [word('results',i) for i in range(12)]==manual['expected_results']
    assert word('signature')==manual['signature'] and r.regs[10]==0 and r.regs[2]==0x18000
    assert writes==[(0x2000000c,v) for v in manual['gpio_writes']]+[(0x20000000,v) for v in manual['tx_bytes']]
    out=dict(status='PASS',synthetic_environment=True,CPU_DUT_runs=0,SoC_runs=0,architectural_steps=r.steps,
        stop_pc=r.pc,GPIO_writes=3,TX_writes=12,signature=word('signature'),stack_restored=True,
        note='alternating abstract ready reads, synthetic GPIO values; NOT physical timing or frozen live-system expected trace')
    with (h/'software-reference-selftest.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out))
if __name__=='__main__':selftest()
