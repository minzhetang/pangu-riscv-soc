"""Small architectural oracle for trusted directed programs, not a complete ISA.

Reports every non-x0 register write and store in program order. No deduplication.
Reference PC is explanatory metadata; observed CPU lacks a retirement-PC port.
"""
from itertools import zip_longest
import re

MASK = 0xFFFFFFFF

def sx(n, bits):
    u = n & ((1 << bits) - 1)
    return u - ((1 << bits) if u & (1 << (bits-1)) else 0)

def reference(case):
    words = [int(i["word"],16) for i in case["instructions"]]
    regs, mem, wb, stores = [0]*32, [0]*64, [], []
    for address,value in case["initial_memory"].items(): mem[int(address)//4] = value
    byte_mem=bytearray(b''.join(value.to_bytes(4, 'little') for value in mem))
    loads=[]
    ram_events=[]
    bus_stores=[]
    pc = 0
    for _ in range(256):
        assert pc % 4 == 0 and 0 <= pc//4 < len(words), (case["id"],pc)
        w = words[pc//4]
        op, rd, f3, r1, r2, f7 = w&127,(w>>7)&31,(w>>12)&7,(w>>15)&31,(w>>20)&31,w>>25
        a,b,nxt,value = regs[r1],regs[r2],pc+4,None
        r4_reject = op == 0x33 and ((f3 in (1,2,3,4,6,7) and f7 != 0) or (f3 in (0,5) and f7 not in (0,32)))
        pattern_reject = (w & 0xFFFF) == 0 or w == 0xFFFFFFFF
        shifti_reject = op == 0x13 and ((f3 == 1 and f7 != 0) or (f3 == 5 and f7 not in (0,32)))
        if w in (0x00000073,0x00100073) or pattern_reject or r4_reject or shifti_reject:
            event=dict(pc=pc,kind=3 if pattern_reject or r4_reject or shifti_reject else (1 if w==0x73 else 2))
            assert event==case.get('expected_stop'), "Terminating event requires explicit EEI contract"
            assert regs==case['expected_regs'] and mem==case['expected_mem']
            trace=dict(writebacks=wb,stores=stores,stop_event=event)
            if 'manual_ordered_loads' in case: trace['loads']=loads
            if 'manual_bus_stores' in case: trace['bus_stores']=bus_stores
            if 'manual_ram_events' in case: trace['ram_events']=ram_events
            return trace
        if op == 0x13:
            imm = sx(w>>20,12)
            assert f3 in (0,1,2,3,4,5,6,7)
            if f3==0: value=a+imm
            elif f3==1:
                assert f7==0, "Unsupported SLLI high bits"
                value=a<<((w>>20)&31)
            elif f3==2: value=int(sx(a,32)<imm)
            elif f3==3: value=int((a&MASK)<(imm&MASK))
            elif f3==4: value=a^(imm&MASK)
            elif f3==5:
                assert f7 in (0,32), "Unsupported shift-I high bits"
                value=(a&MASK)>>((w>>20)&31) if f7==0 else sx(a,32)>>((w>>20)&31)
            elif f3==6: value=a|(imm&MASK)
            else: value=a&(imm&MASK)
        elif op == 0x0F:
            assert f3 == 0, "Not ordinary FENCE funct3"
            ram_events.append(dict(kind="F",pc=pc,word=f"{w:08x}",address="00000000",data="00000000",mask="0",after="00000000"))
        elif op == 0x37:
            value = (w & MASK) & 0xFFFFF000
        elif op == 0x17:
            value = (pc + sx(w >> 12, 20) * 4096) & MASK
        elif op == 0x33:
            if f3==0:
                assert f7 in (0,32)
                value = a+b if f7==0 else a-b
            elif f3==7:
                assert f7==0, "Unsupported AND funct7"
                value=a&b
            elif f3==6:
                assert f7==0, "Unsupported OR funct7"
                value=a|b
            elif f3==4:
                assert f7==0, "Unsupported XOR funct7"
                value=a^b
            elif f3==1:
                assert f7==0, "Unsupported SLL funct7"
                value=a<<(b&31)
            elif f3==2:
                assert f7==0, "Unsupported SLT funct7"
                value=int(sx(a,32)<sx(b,32))
            elif f3==3:
                assert f7==0, "Unsupported SLTU funct7"
                value=int((a&MASK)<(b&MASK))
            elif f3==5:
                assert f7 in (0,32)
                value=a>>(b&31) if f7==0 else sx(a,32)>>(b&31)
            else: raise AssertionError("Unsupported reference ALU op")
        elif op in (3,0x23):
            assert (op==3 and f3 in (0,1,2,4,5)) or (op==0x23 and f3 in (0,1,2))
            imm=sx(w>>20,12) if op==3 else sx(((w>>25)<<5)|((w>>7)&31),12)
            address=(a+imm)&MASK
            assert address<256
            if (op==3 and f3 in (1,5)) or (op==0x23 and f3==1): assert address%2==0
            elif not (op==3 and f3 in (0,4)) and not (op==0x23 and f3==0): assert address%4==0
            if op==3:
                raw=int.from_bytes(byte_mem[address&~3:(address&~3)+4], "little")
                if f3 in (1,5):
                    value=int.from_bytes(byte_mem[address:address+2], "little", signed=(f3==1))&MASK
                elif f3==0:
                    value=int.from_bytes(byte_mem[address:address+1], "little", signed=True)&MASK
                else:
                    value=byte_mem[address] if f3==4 else int.from_bytes(byte_mem[address:address+4], "little")
                loads.append(dict(pc=pc,rd=rd,funct3=f3,address=f"{address:08x}",raw=f"{raw:08x}",value=f"{value:08x}"))
                ram_events.append(dict(kind="R",pc=pc,word=f"{w:08x}",address=f"{address:08x}",data=f"{value:08x}",mask="0",after=f"{raw:08x}"))
            else:
                if f3==1:
                    byte_mem[address:address+2]=(b & 65535).to_bytes(2, "little")
                    lane=address % 4
                    mask=3 << lane
                    bus_value=(b & 65535) << (lane * 8)
                    base=address & ~3
                    mem[address//4]=int.from_bytes(byte_mem[base:base+4], "little")
                elif f3==0:
                    byte_mem[address]=b & 255
                    lane=address % 4
                    mask=1 << lane
                    bus_value=(b & 255) << (lane * 8)
                    base=address & ~3
                    mem[address//4]=int.from_bytes(byte_mem[base:base+4], "little")
                else:
                    mem[address//4]=b
                    byte_mem[address:address+4]=b.to_bytes(4, "little")
                    mask,bus_value=15,b
                stores.append(dict(pc=pc,address=f"{address:08x}",data=f"{bus_value:08x}"))
                bus_stores.append(dict(pc=pc,address=f"{address:08x}",data=f"{bus_value:08x}",mask=f"{mask:x}"))
                ram_events.append(dict(kind="W",pc=pc,word=f"{w:08x}",address=f"{address:08x}",data=f"{bus_value:08x}",mask=f"{mask:x}",after=f"{mem[address//4]:08x}"))
        elif op==0x63:
            assert f3 in (0,1,4,5,6,7)
            imm=sx(((w>>31)<<12)|(((w>>7)&1)<<11)|(((w>>25)&63)<<5)|(((w>>8)&15)<<1),13)
            taken=(a==b) if f3==0 else ((a!=b) if f3==1 else ((sx(a,32)<sx(b,32)) if f3==4 else ((sx(a,32)>=sx(b,32)) if f3==5 else (((a&MASK)<(b&MASK)) if f3==6 else ((a&MASK)>=(b&MASK))))))
            if taken: nxt=pc+imm
        elif op==0x6F:
            imm=sx(((w>>31)<<20)|(((w>>12)&255)<<12)|(((w>>20)&1)<<11)|(((w>>21)&1023)<<1),21)
            value,nxt=pc+4,pc+imm
        elif op==0x67:
            assert f3==0
            value,nxt=pc+4,((a+sx(w>>20,12))&MASK)&~1
        else: raise AssertionError("Unsupported reference opcode")
        if value is not None and rd!=0:
            regs[rd]=value&MASK
            wb.append(dict(pc=pc,rd=rd,data=f"{regs[rd]:08x}"))
        regs[0]=0
        if op==0x13 and rd==31 and regs[31]==90:
            assert regs==case["expected_regs"] and mem==case["expected_mem"], "Trace oracle disagrees with frozen final expectations"
            trace=dict(writebacks=wb,stores=stores)
            if 'manual_ordered_loads' in case: trace['loads']=loads
            if 'manual_bus_stores' in case: trace['bus_stores']=bus_stores
            if 'manual_ram_events' in case: trace['ram_events']=ram_events
            return trace
        pc=nxt
    raise AssertionError("Reference failed to finish")

def compare(log_text, expected, final_status):
    actual_wb=[dict(cycle=int(c),rd=int(r),data=v) for c,r,v in
               re.findall(r"^WB\|cycle=(\d+)\|rd=(\d+)\|data=([0-9a-fxz]+)$",log_text,re.M)]
    actual_stores=[dict(cycle=int(c),address=a,data=v) for c,a,v in
                   re.findall(r"^STORE\|cycle=(\d+)\|addr=([0-9a-fxz]+)\|data=([0-9a-fxz]+)$",log_text,re.M)]
    differences=[]
    for kind,exp,actual,keys in [("WB",expected["writebacks"],actual_wb,("rd","data")),
                                ("STORE",expected["stores"],actual_stores,("address","data"))]:
        for i,(e,a) in enumerate(zip_longest(exp,actual)):
            if e is None or a is None or any(e[k]!=a[k] for k in keys):
                differences.append(dict(kind=kind,index=i,expected=e,actual=a))
    unknown=[]
    # Old TB guard can miss an unknown destination. Inspect its raw TRACE too.
    for line in log_text.splitlines():
        if line.startswith("TRACE|"):
            fields=dict(p.split("=",1) for p in line.split("|")[1:] if "=" in p)
            if fields.get("wb_en") not in ("0","1") or (fields.get("wb_en")=="1" and
                any(x in fields.get(k,"") for k in ("wb_rd","wb_data") for x in ("x","z"))):
                unknown.append(line)
    status="PASS" if not differences and not unknown else "FAIL"
    strict="TIMEOUT" if final_status=="TIMEOUT" else ("PASS" if final_status=="PASS" and status=="PASS" else "FAIL")
    return dict(status=status,strict_status=strict,expected=expected,actual_writebacks=actual_wb,
                actual_stores=actual_stores,differences=differences,unknown_active_writeback=unknown)
