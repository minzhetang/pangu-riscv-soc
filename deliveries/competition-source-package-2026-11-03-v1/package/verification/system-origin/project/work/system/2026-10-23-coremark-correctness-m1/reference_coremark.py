"""Independent finite ISA interpreter; stream digests preserve every ordered event.

Not ISA certification. WB and memory order are separate, no retirement interface.
Uses the compiled binary, never DUT outputs, and validates upstream known CRCs.
"""
import collections
import hashlib
import importlib.util
import json
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'2026-10-23-c-boot-m1/check_c_boot.py'
spec=importlib.util.spec_from_file_location('frozen_m1_elf_parser',OLD)
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
elf_symbols=module.elf_symbols
MASK=0xffffffff
def sx(v,n): return ((v&((1<<n)-1))^(1<<(n-1)))-(1<<(n-1))
def hx(v): return f'{v&MASK:08x}'

class Streams:
    def __init__(self):
        self.hashes={n:hashlib.sha256() for n in ['EX','WB','MEM']}
        self.counts=collections.Counter()
    def add(self,kind,*values):
        channel='MEM' if kind in ('READ','STORE') else kind
        line='|'.join([kind]+list(values))+'\n'
        self.hashes[channel].update(line.encode('ascii')); self.counts[kind]+=1
    def result(self): return {'counts':dict(self.counts),'SHA256':{n:h.hexdigest().upper() for n,h in self.hashes.items()}}

def check_ram_output(ram,symbols,case):
    def word(name):
        p=symbols[name]-0x10000; return int.from_bytes(bytes(ram[p:p+4]),'little')
    p=symbols['ram_log']-0x10000
    count=word('ram_log_count')
    assert count<4096 and word('ram_log_overflow')==0 and word('port_error')==0
    assert word('port_finished')==1 and word('timing_unavailable')==1
    assert word('timer_start_calls')==word('timer_stop_calls')==1
    text=bytes(ram[p:p+count]).decode('ascii')
    expected=json.loads((HERE/'manual-plan.json').read_text())['cases'][case]
    import re
    for key in ['seedcrc','crclist','crcmatrix','crcstate']:
        values=re.findall(r'(?m)^(?:\[0\])?'+key+r'\s*: 0x([0-9a-f]{4})$',text)
        assert values==[expected[key]], (case,key,values,expected[key])
    assert not re.search(r'ERROR! (list|matrix|state) crc',text)
    assert 'Must execute for at least 10 secs' in text
    assert 'Correct operation validated' not in text and 'CoreMark 1.0 :' not in text
    assert 'Iterations       : 1' in text and 'CoreMark Size    : 666' in text
    return text

def reference(case):
    start=time.monotonic(); out=HERE/case
    assert not (out/'expected.json').exists(), 'Never overwrite frozen expected results'
    image=(out/'coremark.bin').read_bytes()
    symbols=elf_symbols(out/'coremark.elf')
    rom=image+bytes(32768-len(image)); ram=bytearray([0xa5]*32768); regs=[0]*32
    streams=Streams(); pc=0; stalls=flushes=0; previous_load=None; min_sp=0x18000
    opcodes=collections.Counter(); first_main_step=None; startup_stores=0
    def read(address,size):
        assert address%size==0
        if 0<=address and address+size<=32768: return int.from_bytes(rom[address:address+size],'little')
        assert 0x10000<=address and address+size<=0x18000,('READ_BOUNDS',hx(pc),hx(address))
        return int.from_bytes(ram[address-0x10000:address-0x10000+size],'little')
    for step in range(5000000):
        if step%100000==0: assert time.monotonic()-start<120,'REFERENCE wall limit'
        assert pc%4==0 and 0<=pc<symbols['__data_load'],('EX_PC',hx(pc))
        word=read(pc,4)
        if word==0x00100073:
            assert pc==0x68; break
        if pc==symbols['main'] and first_main_step is None: first_main_step=step
        op,rd,f3,r1,r2,f7=word&127,(word>>7)&31,(word>>12)&7,(word>>15)&31,(word>>20)&31,word>>25
        a,b,next_pc,value=regs[r1],regs[r2],(pc+4)&MASK,None
        uses1=op in (0x13,0x33,3,0x23,0x63,0x67); uses2=op in (0x33,0x23,0x63)
        if previous_load and ((uses1 and r1==previous_load) or (uses2 and r2==previous_load)): stalls+=1
        previous_load=rd if op==3 and rd else None
        streams.add('EX',hx(pc)); opcodes[hx(op)]+=1
        if op==0x37: value=word&0xfffff000
        elif op==0x17: value=pc+(word&0xfffff000)
        elif op==0x13:
            imm=sx(word>>20,12)
            if f3==0: value=a+imm
            elif f3==1:
                assert f7==0; value=a<<((word>>20)&31)
            elif f3==2: value=int(sx(a,32)<imm)
            elif f3==3: value=int(a<(imm&MASK))
            elif f3==4: value=a^(imm&MASK)
            elif f3==5:
                assert f7 in (0,32); value=(a>>((word>>20)&31)) if f7==0 else (sx(a,32)>>((word>>20)&31))
            elif f3==6: value=a|(imm&MASK)
            elif f3==7: value=a&(imm&MASK)
        elif op==0x33:
            assert f7==0 or (f7==32 and f3 in (0,5))
            if f3==0: value=a+b if f7==0 else a-b
            elif f3==1: value=a<<(b&31)
            elif f3==2: value=int(sx(a,32)<sx(b,32))
            elif f3==3: value=int(a<b)
            elif f3==4: value=a^b
            elif f3==5: value=(a>>(b&31)) if f7==0 else (sx(a,32)>>(b&31))
            elif f3==6: value=a|b
            elif f3==7: value=a&b
        elif op in (3,0x23):
            imm=sx(word>>20,12) if op==3 else sx(((word>>25)<<5)|((word>>7)&31),12)
            address=(a+imm)&MASK; size={0:1,1:2,2:4,4:1,5:2}.get(f3)
            assert size is not None and address%size==0
            if op==3:
                raw=read(address&~3,4); value=read(address,size)
                if f3 in (0,1): value=sx(value,size*8)&MASK
                streams.add('READ',hx(pc),hx(address),hx(raw),hx(value))
            else:
                assert f3 in (0,1,2) and 0x10000<=address and address+size<=0x18000
                mask=((1<<size)-1)<<(address&3); data=(b&((1<<(8*size))-1))<<((address&3)*8)
                ram[address-0x10000:address-0x10000+size]=(b&((1<<(8*size))-1)).to_bytes(size,'little')
                streams.add('STORE',hx(pc),hx(address),hx(data),f'{mask:x}')
                if first_main_step is None: startup_stores+=1
        elif op==0x63:
            imm=sx(((word>>31)<<12)|(((word>>7)&1)<<11)|(((word>>25)&63)<<5)|(((word>>8)&15)<<1),13)
            assert f3 in (0,1,4,5,6,7)
            taken={0:a==b,1:a!=b,4:sx(a,32)<sx(b,32),5:sx(a,32)>=sx(b,32),6:a<b,7:a>=b}[f3]
            if taken: next_pc=(pc+imm)&MASK; flushes+=1
        elif op==0x6f:
            imm=sx(((word>>31)<<20)|(((word>>12)&255)<<12)|(((word>>20)&1)<<11)|(((word>>21)&1023)<<1),21)
            value,next_pc=pc+4,(pc+imm)&MASK; flushes+=1
        elif op==0x67:
            assert f3==0
            value,next_pc=pc+4,((a+sx(word>>20,12))&MASK)&~1; flushes+=1
        else: raise AssertionError(('UNSUPPORTED_IN_FIXED_IMAGE',hx(pc),hx(word)))
        if value is not None and rd:
            regs[rd]=value&MASK; streams.add('WB',str(rd),hx(value))
            if rd==2: min_sp=min(min_sp,regs[2]); assert regs[2]>=symbols['__bss_end']+256,'stack collided with data'
        regs[0]=0; pc=next_pc
    else: raise AssertionError('REFERENCE instruction limit')
    assert regs[2]==symbols['__stack_top'] and regs[3]==symbols['__global_pointer$'] and regs[10]==0
    text=check_ram_output(ram,symbols,case)
    assert startup_stores==(symbols['__data_end']-symbols['__data_start']+symbols['__bss_end']-symbols['__bss_start'])//4
    result={'type':'PRE_DUT_GOLDEN_NOT_CPU_PASS','case':case,'symbols':symbols,'registers':regs,'ram':list(ram),
            'streams':streams.result(),'stall':stalls,'flush':flushes,'stop_pc':'00000068','stop_kind':2,
            'architectural_instructions_including_ebreak':step+1,'opcodes':dict(opcodes),'min_stack_pointer':hx(min_sp),
            'reference_seconds':round(time.monotonic()-start,6),'startup_store_count':startup_stores,
            'expected_normal_end_cycles':streams.counts['EX']+2*flushes+stalls+7,
            'ROM_image_bytes':len(image),'RAM_static_end':hx(symbols['__bss_end']),
            'timing':'UNAVAILABLE_NOT_A_SCORE','output':text}
    (out/'expected.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out/'expected-output.txt').write_text(text,encoding='ascii')
    print(json.dumps({k:v for k,v in result.items() if k not in ('symbols','registers','ram','output')},indent=2))
    return result

if __name__=='__main__':
    for case in ['performance','validation']: reference(case)
