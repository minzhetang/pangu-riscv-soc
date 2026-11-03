"""Finite RV32I C-image oracle/scoreboard. No DUT execution and no CPU edits.

Existing architectural operations are adapted to this ROM/RAM map. This is not
an ISA certification model. WB and memory streams remain separate; EX PC is
observed execution-stage PC, not a retirement interface.
"""
import copy
import json
import re
import struct
from itertools import zip_longest
from pathlib import Path

MASK = 0xffffffff
HERE = Path(__file__).resolve().parent

def sx(v, bits):
    v &= (1 << bits)-1
    return v - (1 << bits) if v & (1 << (bits-1)) else v

def hx(v):
    return f"{v & MASK:08x}"

def elf_symbols(path):
    raw = path.read_bytes()
    assert raw[:7] == b"\x7fELF\x01\x01\x01", "ELF32 little-endian required"
    h = struct.unpack_from("<HHIIIIIHHHHHH", raw, 16)
    assert h[1] == 243 and h[3] == 0 and h[6] == 0
    sections = [struct.unpack_from("<10I", raw, h[5]+i*h[10]) for i in range(h[11])]
    symbols = {}
    for section in sections:
        if section[1] != 2:
            continue
        string_section = sections[section[6]]
        strings = raw[string_section[4]:string_section[4]+string_section[5]]
        for offset in range(section[4], section[4]+section[5], section[9]):
            name, value, size, info, other, index = struct.unpack_from("<IIIBBH",raw,offset)
            text = strings[name:].split(b"\0",1)[0].decode("utf-8")
            if text:
                symbols[text] = value
    return symbols

def reference():
    image = (HERE/"inputs/smoke.bin").read_bytes()
    symbols = elf_symbols(HERE/"inputs/smoke.elf")
    rom = image + bytes(0x4000-len(image))
    ram = bytearray([0xa5]*0x4000)
    regs = [0]*32  # Explicit limitation: existing RF initial-zero state.
    wb, events, execution, writes = [], [], [], []
    pc, stalls, flushes, previous_load = 0, 0, 0, None
    visited = set()

    def read(address, size):
        if 0 <= address and address+size <= 0x4000:
            return int.from_bytes(rom[address:address+size],"little")
        assert 0x10000 <= address and address+size <= 0x14000, ("unmapped read",hx(address))
        return int.from_bytes(ram[address-0x10000:address-0x10000+size],"little")

    for step in range(20000):
        assert pc % 4 == 0 and 0 <= pc < 568, ("unexpected executed PC",hx(pc))
        word = read(pc,4)
        if word == 0x00100073:
            assert pc == 0x68
            break
        visited.add(pc)
        op, rd, f3, r1, r2, f7 = word&127,(word>>7)&31,(word>>12)&7,(word>>15)&31,(word>>20)&31,word>>25
        a, b, next_pc, value = regs[r1], regs[r2], (pc+4)&MASK, None
        uses1 = op in (0x13,0x33,3,0x23,0x63,0x67)
        uses2 = op in (0x33,0x23,0x63)
        if previous_load and ((uses1 and r1==previous_load) or (uses2 and r2==previous_load)):
            stalls += 1
        previous_load = rd if op==3 and rd else None
        execution.append(hx(pc))
        if op == 0x37:
            value = word & 0xfffff000
        elif op == 0x17:
            value = pc + (word & 0xfffff000)
        elif op == 0x13:
            imm = sx(word>>20,12)
            if f3==0: value = a+imm
            elif f3==1:
                assert f7==0
                value=a<<((word>>20)&31)
            elif f3==2: value=int(sx(a,32)<imm)
            elif f3==3: value=int(a<(imm&MASK))
            elif f3==4: value=a^(imm&MASK)
            elif f3==5:
                assert f7 in (0,32)
                value=a>>((word>>20)&31) if f7==0 else sx(a,32)>>((word>>20)&31)
            elif f3==6: value=a|(imm&MASK)
            elif f3==7: value=a&(imm&MASK)
        elif op == 0x33:
            assert f7==0 or (f7==32 and f3 in (0,5))
            if f3==0: value=a+b if f7==0 else a-b
            elif f3==1: value=a<<(b&31)
            elif f3==2: value=int(sx(a,32)<sx(b,32))
            elif f3==3: value=int(a<b)
            elif f3==4: value=a^b
            elif f3==5: value=a>>(b&31) if f7==0 else sx(a,32)>>(b&31)
            elif f3==6: value=a|b
            elif f3==7: value=a&b
        elif op in (3,0x23):
            imm=sx(word>>20,12) if op==3 else sx(((word>>25)<<5)|((word>>7)&31),12)
            address=(a+imm)&MASK
            size={0:1,1:2,2:4,4:1,5:2}.get(f3)
            assert size is not None and address%size==0
            if op==3:
                raw=read(address&~3,4)
                value=read(address,size)
                if f3 in (0,1): value=sx(value,size*8)&MASK
                events.append(["READ",hx(pc),hx(address),hx(raw),hx(value)])
            else:
                assert f3 in (0,1,2) and 0x10000 <= address and address+size <= 0x14000
                mask=((1<<size)-1)<<(address&3)
                data=(b&((1<<(8*size))-1))<<((address&3)*8)
                ram[address-0x10000:address-0x10000+size]=(b&((1<<(8*size))-1)).to_bytes(size,"little")
                event=["STORE",hx(pc),hx(address),hx(data),f"{mask:x}"]
                events.append(event)
                writes.append(event)
        elif op == 0x63:
            imm=sx(((word>>31)<<12)|(((word>>7)&1)<<11)|(((word>>25)&63)<<5)|(((word>>8)&15)<<1),13)
            assert f3 in (0,1,4,5,6,7)
            taken={0:a==b,1:a!=b,4:sx(a,32)<sx(b,32),5:sx(a,32)>=sx(b,32),6:a<b,7:a>=b}[f3]
            if taken:
                next_pc=(pc+imm)&MASK
                flushes+=1
        elif op == 0x6f:
            imm=sx(((word>>31)<<20)|(((word>>12)&255)<<12)|(((word>>20)&1)<<11)|(((word>>21)&1023)<<1),21)
            value,next_pc=pc+4,(pc+imm)&MASK
            flushes+=1
        elif op == 0x67:
            assert f3==0
            value,next_pc=pc+4,((a+sx(word>>20,12))&MASK)&~1
            flushes+=1
        else:
            raise AssertionError(("not in frozen program ISA",hx(pc),hx(word)))
        if value is not None and rd:
            regs[rd]=value&MASK
            wb.append([str(rd),hx(value)])
        regs[0]=0
        pc=next_pc
    else:
        raise AssertionError("REFERENCE_TIMEOUT")
    result_values=[read(symbols["results"]+4*i,4) for i in range(4)]
    assert result_values == [119752999,12727,48,1234664], result_values
    assert read(symbols["signature"],4)==0x50524f42 and regs[10]==0
    assert regs[2]==symbols["__stack_top"] and regs[3]==symbols["__global_pointer$"]
    assert all(symbols[n] in visited for n in ("main","__mulsi3","__udivsi3","__umodsi3"))
    # All data/BSS startup writes must occur before the first main instruction.
    startup = [e for e in writes if int(e[1],16)<symbols["main"]]
    assert [e[2] for e in startup[:2]]==["00010000","00010004"]
    cleared=[int(e[2],16) for e in startup[2:] if e[3]=="00000000" and e[4]=="f"]
    assert cleared==list(range(symbols["__bss_start"],symbols["__bss_end"],4))
    return {"symbols":symbols,"registers":regs,"ram":list(ram),"writebacks":wb,
            "memory_events":events,"execution_PC_not_retirement":execution,
            "stall_model_expected":stalls,"flush_model_expected":flushes,
            "hand_results":result_values,"signature":"50524f42","stop_pc":"00000068",
            "stop_kind":2,"architectural_instructions_including_ebreak":len(execution)+1,
            "startup_stores":startup}

def compare(text, expected, registers, ram):
    writebacks=[]; events=[]; execution=[]; stops=[]; metrics=None; unknown=[]
    for line in text.splitlines():
        f=line.split("|")
        if f[0]=="WB": writebacks.append(f[2:])
        elif f[0] in ("READ","STORE"): events.append([f[0]]+f[2:])
        elif f[0]=="EX": execution.append(f[2])
        elif f[0]=="STOP": stops.append(f[2:])
        elif f[0]=="METRICS": metrics=dict(x.split("=",1) for x in f[1:])
        if f[0] in ("WB","READ","STORE","EX","STOP") and any(re.search("[xz]",x,re.I) for x in f[2:]):
            unknown.append(line)
    differences=[]
    for label, exp, actual in [("WB",expected["writebacks"],writebacks),
            ("MEMORY_R_W_ORDER",expected["memory_events"],events),
            ("EX_PC_NOT_RETIREMENT",expected["execution_PC_not_retirement"],execution),
            ("REGISTERS",expected["registers"],registers),("RAM_BYTES",expected["ram"],ram)]:
        for i,(a,b) in enumerate(zip_longest(exp,actual)):
            if a!=b: differences.append({"kind":label,"index":i,"expected":a,"actual":b})
    if stops != [["2",expected["stop_pc"]]]:
        differences.append({"kind":"STOP","actual":stops})
    if not metrics:
        differences.append({"kind":"MISSING_METRICS"})
    else:
        for key,exp in [("stall",expected["stall_model_expected"]),("flush",expected["flush_model_expected"]),("stop_hold_edges",4)]:
            if int(metrics[key])!=exp:
                differences.append({"kind":key,"expected":exp,"actual":metrics[key]})
    if "SIMULATION_ENDED_NOT_YET_FUNCTIONAL_PASS" not in text:
        differences.append({"kind":"NO_NORMAL_END_MARKER"})
    return {"status":"PASS" if not differences and not unknown else "FAIL",
            "differences":differences,"unknown_active_events":unknown,"metrics":metrics,
            "observed_WB":len(writebacks),"observed_memory_events":len(events),
            "observed_EX_instructions":len(execution),"separate_WB_and_memory_order":True,
            "no_retirement_PC_interface":True}

def checker_selftest(expected):
    rows=[]
    for i,p in enumerate(expected["execution_PC_not_retirement"]): rows.append(f"EX|{i+1}|{p}")
    for i,w in enumerate(expected["writebacks"]): rows.append(f"WB|{i+1}|"+"|".join(w))
    for i,e in enumerate(expected["memory_events"]): rows.append(e[0]+f"|{i+1}|"+"|".join(e[1:]))
    rows += ["STOP|1|2|00000068",
             f"METRICS|cycles=1|stall={expected['stall_model_expected']}|flush={expected['flush_model_expected']}|stop_hold_edges=4|time_ns=0",
             "SIMULATION_ENDED_NOT_YET_FUNCTIONAL_PASS"]
    text="\n".join(rows)
    assert compare(text,expected,expected["registers"],expected["ram"])["status"]=="PASS"
    checks={}
    bad=copy.deepcopy(expected["ram"]); bad[expected["symbols"]["signature"]-0x10000]^=1
    checks["bad_signature_rejected"]=compare(text,expected,expected["registers"],bad)["status"]=="FAIL"
    duplicate=next(s for s in rows if s.startswith("WB|"))
    checks["duplicate_WB_rejected"]=compare(text+"\n"+duplicate,expected,expected["registers"],expected["ram"])["status"]=="FAIL"
    missing_rows=list(rows)
    missing_rows.remove(next(s for s in missing_rows if s.startswith("STORE|")))
    missing="\n".join(missing_rows)
    checks["missing_STORE_rejected"]=compare(missing,expected,expected["registers"],expected["ram"])["status"]=="FAIL"
    checks["unknown_WB_rejected"]=compare(text+"\nWB|1|1|xxxxxxxx",expected,expected["registers"],expected["ram"])["status"]=="FAIL"
    assert all(checks.values()), checks
    return checks
