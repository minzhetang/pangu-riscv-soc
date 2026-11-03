"""Prepare immutable directed cases, then bounded Icarus runs. No functional RTL edits.

prepare and run are separate, so the plan/expectations can be reviewed before execution.
All generated input files are plain data; no RISC-V compiler or package installation.
"""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

ROOT = Path(r"D:\A_FPGA_Comp")
BASE = ROOT / "work/icarus/2026-10-19-cpu-sb-tbfix"
TOOLS = ROOT / "tools/iverilog-13.0-msys2-ucrt64/ucrt64"
NAMES = ["alu.v", "control.v", "regfile.v", "cpu.v", "tb_cpu.v"]
EXPECTED_HASH = dict(zip(NAMES, [
    "6393472BC3635DA83213E0E9883766D5076C37EA60319F32F1DE5C420F68065E",
    "23CDBDFDD45DD60D6C7D95A13CC51927999A640FE5E30CAF8D324FA91AA87067",
    "AE36F070B994EEF41AF1636516D737EDA240C2A18AF83048ADC3E3E2391C8468",
    "43BE7479D041F950CFA6222D07337EB0155E1AC63CF3A22D881774A521C620A6",
    "17AFD2B4CFBAF9E4D6183D4C44CA4F8717357D2725DE61E9D90AB1096180B9E5",
]))
TOOL_HASH = {
    "bin/iverilog.exe": "25E1BA02E72F58D9D484BC5457D69A6B179D22D86BDF5BA5D6F9F0D4FE620BBF",
    "bin/vvp.exe": "F0775603E1F1BCF1B2DEA16DFF963A4B7D71B7B33D5BBE23D2B01FF5B2304E09",
    "lib/ivl/ivl.exe": "75B5B4569796B4CD85C74E9B4836699A70159279C3BAE20268A8578558686643",
    "lib/ivl/ivlpp.exe": "D41181DF44C4C6A6AD07E5F91A34F7624EC081150C5B08E007133AFDB7FAD3C8",
}
NOP = 0x13
MASK = 0xFFFFFFFF

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()

def save_json(p, obj):
    Path(p).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def manifest(directory):
    return [{"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)}
            for p in sorted(directory.rglob("*")) if p.is_file()]

def verify_manifest(entries):
    for e in entries:
        assert Path(e["path"]).is_file() and sha(e["path"]) == e["sha256"], e["path"]

def sext(n, bits):
    return (n & ((1 << bits) - 1)) - ((1 << bits) if n & (1 << (bits - 1)) else 0)

def itype(rd, rs1, imm, f3=0, op=0x13):
    assert -2048 <= imm <= 2047
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op

def rtype(rd, rs1, rs2, f3, f7=0):
    return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | 0x33

def store(rs2, rs1, imm):
    u = imm & 0xFFF
    return ((u >> 5) << 25) | (rs2 << 20) | (rs1 << 15) | (2 << 12) | ((u & 31) << 7) | 0x23

def branch(rs1, rs2, off, f3):
    assert off % 2 == 0 and -4096 <= off <= 4094
    u = off & 0x1FFF
    return ((u >> 12) << 31) | (((u >> 5) & 63) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (((u >> 1) & 15) << 8) | (((u >> 11) & 1) << 7) | 0x63

def jal(rd, off):
    assert off % 2 == 0 and -(1 << 20) <= off < (1 << 20)
    u = off & 0x1FFFFF
    return ((u >> 20) << 31) | (((u >> 1) & 1023) << 21) | (((u >> 11) & 1) << 20) | (((u >> 12) & 255) << 12) | (rd << 7) | 0x6F

def golden(program, initial, stop_event=None):
    """Independent sequential subset interpreter: verify manual expectations/encoding.

    This is an input/oracle consistency check, NOT an implementation of DUT timing.
    Only instructions in the frozen plan are supported; other encodings reject.
    """
    regs = [0] * 32
    mem = [0] * 64
    for addr, value in initial.items():
        mem[addr // 4] = value
    pc = 0
    for step in range(256):
        assert pc % 4 == 0 and 0 <= pc // 4 < len(program), (pc, step)
        w = program[pc // 4][0]
        op, rd, f3, r1, r2, f7 = w & 127, (w >> 7) & 31, (w >> 12) & 7, (w >> 15) & 31, (w >> 20) & 31, w >> 25
        a, b, next_pc, value = regs[r1], regs[r2], pc + 4, None
        r4_reject = op == 0x33 and ((f3 in (1, 2, 3, 4, 6, 7) and f7 != 0) or (f3 in (0, 5) and f7 not in (0, 32)))
        pattern_reject = (w & 0xFFFF) == 0 or w == 0xFFFFFFFF
        shifti_reject = op == 0x13 and ((f3 == 1 and f7 != 0) or (f3 == 5 and f7 not in (0, 32)))
        if w in (0x00000073, 0x00100073) or pattern_reject or r4_reject or shifti_reject:
            assert stop_event is not None, "Terminating event requires explicit EEI contract"
            assert stop_event == dict(pc=pc,kind=3 if pattern_reject or r4_reject or shifti_reject else (1 if w == 0x73 else 2))
            return regs, mem, step + 1
        if op == 0x13:
            imm = sext(w >> 20, 12)
            assert f3 in (0, 1, 2, 3, 4, 5, 6, 7)
            if f3 == 0: value = a + imm
            elif f3 == 1:
                assert f7 == 0, "Unsupported SLLI high bits"
                value = a << ((w >> 20) & 31)
            elif f3 == 2: value = int(sext(a, 32) < imm)
            elif f3 == 3: value = int((a & MASK) < (imm & MASK))
            elif f3 == 4: value = a ^ (imm & MASK)
            elif f3 == 5:
                assert f7 in (0, 32), "Unsupported shift-I high bits"
                value = (a & MASK) >> ((w >> 20) & 31) if f7 == 0 else sext(a, 32) >> ((w >> 20) & 31)
            elif f3 == 6: value = a | (imm & MASK)
            else: value = a & (imm & MASK)
        elif op == 0x0F:
            # RAM-FENCE-0.1: stronger ordinary-RAM barrier; no register result.
            # fm/pred/succ/rs1/rd ignored, FENCE.I is explicitly not included.
            assert f3 == 0, "Not ordinary FENCE funct3"
        elif op == 0x37:
            value = w & 0xFFFFF000
        elif op == 0x17:
            value = (pc + (w & 0xFFFFF000)) & MASK
        elif op == 0x33:
            if f3 == 0:
                assert f7 in (0, 32)
                value = a + b if f7 == 0 else a - b
            elif f3 == 7:
                assert f7 == 0, "Unsupported AND funct7"
                value = a & b
            elif f3 == 6:
                assert f7 == 0, "Unsupported OR funct7"
                value = a | b
            elif f3 == 4:
                assert f7 == 0, "Unsupported XOR funct7"
                value = a ^ b
            elif f3 == 1:
                assert f7 == 0, "Unsupported SLL funct7"
                value = a << (b & 31)
            elif f3 == 2:
                assert f7 == 0, "Unsupported SLT funct7"
                value = int(sext(a, 32) < sext(b, 32))
            elif f3 == 3:
                assert f7 == 0, "Unsupported SLTU funct7"
                value = int((a & MASK) < (b & MASK))
            elif f3 == 5:
                assert f7 in (0, 32)
                value = a >> (b & 31) if f7 == 0 else sext(a, 32) >> (b & 31)
            else: raise AssertionError("Unsupported reference ALU op")
        elif op in (3, 0x23):
            assert (op == 3 and f3 in (0, 1, 2, 4, 5)) or (op == 0x23 and f3 in (0, 1, 2))
            imm = sext(w >> 20, 12) if op == 3 else sext(((w >> 25) << 5) | ((w >> 7) & 31), 12)
            addr = (a + imm) & MASK
            assert addr < 256
            if op == 3 and f3 in (1, 5):
                assert addr % 2 == 0
                half = (mem[addr // 4] >> (8 * (addr % 4))) & 65535
                value = sext(half, 16) if f3 == 1 else half
            elif op == 3 and f3 in (0, 4):
                byte = (mem[addr // 4] >> (8 * (addr % 4))) & 255
                value = sext(byte, 8) if f3 == 0 else byte
            elif op == 0x23 and f3 == 1:
                assert addr % 2 == 0
                shift = 8 * (addr % 4)
                half_mask = 65535 << shift
                mem[addr // 4] = (mem[addr // 4] & (MASK ^ half_mask)) | ((b & 65535) << shift)
            elif op == 0x23 and f3 == 0:
                shift = 8 * (addr % 4)
                byte_mask = 255 << shift
                mem[addr // 4] = (mem[addr // 4] & (MASK ^ byte_mask)) | ((b & 255) << shift)
            else:
                assert addr % 4 == 0
                if op == 3: value = mem[addr // 4]
                else: mem[addr // 4] = b
        elif op == 0x63:
            assert f3 in (0, 1, 4, 5, 6, 7)
            imm = sext(((w >> 31) << 12) | (((w >> 7) & 1) << 11) | (((w >> 25) & 63) << 5) | (((w >> 8) & 15) << 1), 13)
            taken = (a == b) if f3 == 0 else ((a != b) if f3 == 1 else ((sext(a, 32) < sext(b, 32)) if f3 == 4 else ((sext(a, 32) >= sext(b, 32)) if f3 == 5 else (((a & MASK) < (b & MASK)) if f3 == 6 else ((a & MASK) >= (b & MASK))))))
            if taken: next_pc = pc + imm
        elif op == 0x6F:
            imm = sext(((w >> 31) << 20) | (((w >> 12) & 255) << 12) | (((w >> 20) & 1) << 11) | (((w >> 21) & 1023) << 1), 21)
            value, next_pc = pc + 4, pc + imm
        elif op == 0x67:
            assert f3 == 0
            value, next_pc = pc + 4, ((a + sext(w >> 20, 12)) & MASK) & ~1
        else: raise AssertionError(f"Unsupported reference opcode {op:x}")
        if value is not None and rd != 0: regs[rd] = value & MASK
        regs[0] = 0
        if rd == 31 and op == 0x13 and regs[31] == 90:
            return regs, mem, step + 1
        pc = next_pc
    raise AssertionError("Reference did not reach marker")

def cases():
    out = []
    def add(name, purpose, category, p, regs, initial=None, changed_mem=None):
        initial = initial or {}
        p = p + [(itype(31, 0, 90), "addi x31,x0,90 ; completion")]
        er = [0] * 32
        for r, v in {**regs, 31: 90}.items(): er[r] = v & MASK
        em = [0] * 64
        for addr, v in {**initial, **(changed_mem or {})}.items(): em[addr // 4] = v & MASK
        gr, gm, steps = golden(p, initial)
        assert er == gr and em == gm, f"Manual expectations/reference disagree: {name}"
        out.append(dict(id=name, purpose=purpose, category=category, initial_memory=initial,
                        expected_regs=er, expected_mem=em, reference_steps=steps,
                        instructions=[dict(pc=i * 4, word=f"{w:08x}", asm=s) for i, (w, s) in enumerate(p)]))
    nops = [(NOP, "nop ; ISOLATION ONLY")] * 4
    add("T01_addi_x0", "Independent ADDI, negative immediate and x0 write rejection", "basic-no-dependency",
        [(itype(0, 0, 123), "addi x0,x0,123"), (itype(1, 0, 7), "addi x1,x0,7"),
         (itype(2, 0, -3), "addi x2,x0,-3"), (itype(3, 0, 0), "addi x3,x0,0")], {1:7, 2:-3})
    p = [(itype(1,0,10),"addi x1,x0,10"), (itype(2,0,5),"addi x2,x0,5"),
         (itype(3,0,-16),"addi x3,x0,-16"), (itype(4,0,2),"addi x4,x0,2")] + nops
    for rd, r1, r2, f3, f7, asm in [
        (10,1,2,0,0,"add x10,x1,x2"), (11,1,2,0,32,"sub x11,x1,x2"),
        (12,1,2,7,0,"and x12,x1,x2"), (13,1,2,6,0,"or x13,x1,x2"),
        (14,1,2,4,0,"xor x14,x1,x2"), (15,1,4,1,0,"sll x15,x1,x4"),
        (16,3,4,5,0,"srl x16,x3,x4"), (17,3,4,5,32,"sra x17,x3,x4")]:
        p.append((rtype(rd,r1,r2,f3,f7),asm))
    p.append((itype(18,2,16,6),"ori x18,x2,16"))
    add("T02_alu_isolated", "ALU/ORI with four NOP setup isolation; NOT forwarding coverage", "NOP-isolated",
        p, {1:10,2:5,3:-16,4:2,10:15,11:5,13:15,14:15,15:40,16:0x3FFFFFFC,17:-4,18:21})
    add("T03_memory_isolated", "LW then isolated SW and reload; initial data is external memory only", "NOP-isolated",
        [(itype(5,0,0,2,3),"lw x5,0(x0)")] + nops + [(store(5,0,4),"sw x5,4(x0)")] + nops +
        [(itype(6,0,4,2,3),"lw x6,4(x0)")] + nops,
        {5:0x12345678,6:0x12345678}, {0:0x12345678}, {4:0x12345678})
    for name, f3, second, taken in [("T04_beq_taken",0,5,True), ("T05_beq_not_taken",0,6,False),
                                     ("T06_bne_taken",1,6,True), ("T07_bne_not_taken",1,5,False)]:
        mnemonic = "beq" if f3 == 0 else "bne"
        add(name, f"Isolated {mnemonic}, taken={taken}; squash/fallthrough and target", "NOP-isolated-control",
            [(itype(1,0,5),"addi x1,x0,5"),(itype(2,0,second),f"addi x2,x0,{second}")] + nops +
            [(branch(1,2,8,f3),f"{mnemonic} x1,x2,+8"), (itype(10,0,1),"addi x10,x0,1 ; fallthrough-only"),
             (itype(11,0,2),"addi x11,x0,2 ; branch target")],
            {1:5,2:second,10:0 if taken else 1,11:2})
    add("T08_raw_adjacent", "Adjacent ALU producer/consumer, no NOP; requires correct RAW handling", "hazard-diagnostic",
        [(itype(1,0,7),"addi x1,x0,7"),(itype(2,1,3),"addi x2,x1,3")], {1:7,2:10})
    add("T09_store_raw_adjacent", "Adjacent producer to store-data consumer, no NOP", "hazard-diagnostic",
        [(itype(3,0,85),"addi x3,x0,85"),(store(3,0,0),"sw x3,0(x0)")], {3:85}, changed_mem={0:85})
    add("T10_load_use_adjacent", "Adjacent LW/ADDI dependency, no NOP", "hazard-diagnostic",
        [(itype(1,0,0,2,3),"lw x1,0(x0)"),(itype(2,1,1),"addi x2,x1,1")], {1:6,2:7}, {0:6})
    add("T11_load_use_same_rd", "Pointer-chasing LW with same destination/source, no NOP; bounded progress test", "hazard-diagnostic",
        [(itype(1,0,0,2,3),"lw x1,0(x0)"),(itype(1,1,0,2,3),"lw x1,0(x1)")], {1:42}, {0:4,4:42})
    add("T12_jal", "JAL target, PC+4 link and wrong-path side effects; no isolation padding", "incomplete-control-diagnostic",
        [(jal(1,16),"jal x1,+16"),(itype(2,0,4),"addi x2,x0,4 ; wrong path"),
         (itype(2,0,8),"addi x2,x0,8 ; wrong path"),(itype(2,0,12),"addi x2,x0,12 ; wrong path"),
         (itype(3,0,7),"addi x3,x0,7 ; target")], {1:4,3:7})
    add("T13_jalr", "JALR with isolated base; PC+4 link, target and wrong-path effects", "NOP-isolated-incomplete-control",
        [(itype(1,0,32),"addi x1,x0,32")] + nops +
        [(itype(5,1,0,0,0x67),"jalr x5,0(x1) ; PC=20, link=24"),
         (itype(2,0,4),"addi x2,x0,4 ; wrong path"),(itype(2,0,8),"addi x2,x0,8 ; wrong path"),
         (itype(3,0,7),"addi x3,x0,7 ; target PC=32")], {1:32,3:7,5:24})
    return out

def write_hex(path, words):
    path.write_text("".join(f"{w & MASK:08x}\n" for w in words), encoding="ascii")

def prepare(dest):
    assert not dest.exists(), "Fresh directory required; no overwrite"
    before = manifest(ROOT / "集创赛/RTL代码文件") + manifest(BASE)
    for n in NAMES: assert sha(BASE / "source" / n) == EXPECTED_HASH[n], n
    for n, h in TOOL_HASH.items(): assert sha(TOOLS / n) == h, n
    cs = cases()  # Reject inconsistent program/manual expectations before creating files.
    dest.mkdir(parents=True)
    (dest / "source").mkdir()
    for n in NAMES:
        shutil.copyfile(BASE / "source" / n, dest / "source" / n)
        assert sha(dest / "source" / n) == EXPECTED_HASH[n]
    shutil.copyfile(Path(__file__).with_name("tb_cpu_selfcheck_v1.sv"), dest / "tb_cpu_selfcheck_v1.sv")
    for c in cs:
        d = dest / "cases" / c["id"]
        d.mkdir(parents=True)
        words = [int(i["word"],16) for i in c["instructions"]]
        write_hex(d / "imem.hex", words + [NOP] * (256 - len(words)))
        initial = [0] * 64
        for addr, v in c["initial_memory"].items(): initial[addr // 4] = v
        write_hex(d / "dmem.hex", initial)
        write_hex(d / "expected-regs.hex", c["expected_regs"])
        write_hex(d / "expected-mem.hex", c["expected_mem"])
        (d / "program.lst").write_text("\n".join(f"{i['pc']:04x}: {i['word']}  {i['asm']}" for i in c["instructions"]) + "\n", encoding="utf-8")
    save_json(dest / "plan.json", {"version":1,"cases":cs,"cycle_limit":64,"time_unit":"1ns/1ps","clock_period_ns":10,
        "marker":"real WB of x31=90, then four drain cycles", "no_functional_rtl_changes":True,
        "expected_state":"all 32 registers and all 64 data words; case inequality catches X/Z",
        "reference_note":"Manual expectations cross-checked by sequential subset interpreter; no external compiler"})
    plan = ["# CPU self-check v1 — frozen before execution", "", "Date: 2026-10-16. No RTL edits. Separate vvp process per case.",
            "", "Static inspection: explicit decode exists for ADD/SUB/AND/OR/XOR/SLL/SRL/SRA/ADDI/ORI/LW/SW/BEQ/BNE; this is not functional proof.",
            "JAL/JALR have decode but incomplete-looking target/link paths; test as diagnostics, not assumed supported.",
            "SLT/SLTU, other immediate arithmetic, other branch comparisons, byte/halfword memory, LUI/AUIPC/CSR/traps are incomplete/absent and not tested.",
            "No forwarding mux is present; RAW/load-use correctness is a static concern pending execution.", "",
            "Four NOPs are conservative setup isolation only, not a statement that hazards work or that four are minimally necessary.",
            "External imem/dmem initialized via readmemh. DUT internals observed read-only; no force or final-state preloading.",
            "Reset 1→0 at1ns, release20ns off the rising edge; checks after NBA (#1). Max64 active cycles; compile60s/run30s wall limits.",
            "Expected registers initially zero because regfile's own initial block; not written by TB. imem padding is NOP only after explicit test/marker.",
            "A missing WB marker is TIMEOUT with final mismatches reported; an observed marker alone cannot PASS.", "",
            "| Case | Category | Purpose |", "|---|---|---|"]
    for c in cs: plan.append(f"| {c['id']} | {c['category']} | {c['purpose']} |")
    for c in cs:
        plan += ["", f"## {c['id']}", "", f"Initial memory (byte address): {c['initial_memory'] or 'all zero'}.",
                 "Expected nonzero registers: " + ", ".join(f"x{i}=0x{v:08x}" for i,v in enumerate(c["expected_regs"]) if v) + ". All others zero.",
                 "Expected nonzero memory: " + (", ".join(f"[{i*4}]=0x{v:08x}" for i,v in enumerate(c["expected_mem"]) if v) or "none") + ". All others zero.",
                 "```text"] + [f"{i['pc']:04x}: {i['word']}  {i['asm']}" for i in c["instructions"]] + ["```"]
    (dest / "PLAN.md").write_text("\n".join(plan) + "\n", encoding="utf-8")
    verify_manifest(before)
    save_json(dest / "input-manifest.json", {"protected":before, "inputs":manifest(dest),
        "runner":str(Path(__file__).resolve()),"runner_sha256":sha(__file__),
        "process_wrapper":str(Path(__file__).with_name("Invoke-CpuSelfcheckProcess.ps1")),
        "process_wrapper_sha256":sha(Path(__file__).with_name("Invoke-CpuSelfcheckProcess.ps1")),
        "tool_hashes":[{"path":str(TOOLS/n),"sha256":h} for n,h in TOOL_HASH.items()]})
    print(f"PREPARED {len(cs)} frozen cases; NOT EXECUTED; {dest}")

def execute(dest):
    frozen = json.loads((dest / "input-manifest.json").read_text(encoding="utf-8"))
    verify_manifest(frozen["protected"] + frozen["inputs"] + frozen["tool_hashes"])
    assert sha(__file__) == frozen["runner_sha256"], "Runner changed after freeze"
    assert sha(frozen["process_wrapper"]) == frozen["process_wrapper_sha256"], "Process wrapper changed after freeze"
    assert not (dest / "result.json").exists() and not (dest / "runs").exists(), "Existing evidence, no overwrite"
    assert os.environ.get("IVERILOG_DUMPER", "vcd").lower() == "vcd", "Plain VCD only; no env modification"
    plan = json.loads((dest / "plan.json").read_text(encoding="utf-8"))
    state = {"date":"2026-10-16","tool":"Icarus/vvp 13.0 (MSYS2)","commands":[],"cases":[],
             "compile_passed":False,"protected_unchanged":False,"inputs_unchanged":False,
             "rtl_modified":False,"hardware_operated":False,"modelsim_executed":False,"path_modified":False,
             "full_cpu_correctness_verified":False,"error":None}
    old_path = os.environ.get("PATH")
    runs = dest / "runs"
    runs.mkdir()
    def persist(): save_json(dest / "result.json", state)
    def call(label, exe, args, cwd, limit):
        log = cwd / (label + ".log")
        rec = dict(label=label, executable=str(exe), arguments=[str(a) for a in args], cwd=str(cwd),
                   timeout_seconds=limit, timed_out=False, exit_code=None, log=str(log))
        state["commands"].append(rec)
        started = time.perf_counter()
        # .NET wrapper ensures an owned child tree is killed on wall-clock timeout.
        request = cwd / (label + "-request.json")
        response = cwd / (label + "-process.json")
        save_json(request, {"executable":str(exe),"arguments":[str(a) for a in args],"cwd":str(cwd),
                           "timeout_seconds":limit,"log":str(log),"response":str(response)})
        ps = ROOT / "scripts/verification/Invoke-CpuSelfcheckProcess.ps1"
        shell = shutil.which("pwsh")
        assert shell, "Existing PowerShell 7 required; no install allowed"
        outer = subprocess.run([shell,"-NoLogo","-NoProfile","-File",str(ps),"-Request",str(request)],
                               capture_output=True, text=True, timeout=limit+15,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        if outer.returncode != 0 or not response.exists():
            raise RuntimeError(f"Process wrapper failed: {outer.stdout}\n{outer.stderr}")
        native = json.loads(response.read_text(encoding="utf-8"))
        rec.update(native)
        rec["wrapper_elapsed_wall_seconds"] = round(time.perf_counter()-started,4)
        persist()
        return rec, log.read_text(encoding="utf-8")
    try:
        for label, exe in [("iverilog-version",TOOLS/"bin/iverilog.exe"),("vvp-version",TOOLS/"bin/vvp.exe")]:
            rec, text = call(label,exe,["-V"],runs,15)
            assert rec["exit_code"] == 0 and not rec["timed_out"] and "13.0 (stable)" in text
        vvp = runs / "cpu-selfcheck.vvp"
        sources = [dest/"source"/n for n in NAMES[:4]] + [dest/"tb_cpu_selfcheck_v1.sv"]
        rec, text = call("compile",TOOLS/"bin/iverilog.exe",["-B",TOOLS/"lib/ivl","-g2012","-Wall","-s","tb_cpu_selfcheck_v1","-o",vvp,*sources],runs,60)
        state["compile_diagnostics"] = [s for s in text.splitlines() if re.search(r"warning|error|sorry",s,re.I)]
        if rec["exit_code"] != 0 or rec["timed_out"] or not vvp.is_file():
            raise RuntimeError("Compilation/elaboration failed; stop, no RTL changes")
        state["compile_passed"] = True
        state["vvp"] = {"path":str(vvp),"bytes":vvp.stat().st_size,"sha256":sha(vvp)}
        for c in plan["cases"]:
            cwd = runs / c["id"]
            cwd.mkdir()
            rec, text = call("run",TOOLS/"bin/vvp.exe",["-N","-M-","-M"+str(TOOLS/"lib/ivl"),vvp,
                                 "+case="+c["id"],"+inputs="+(dest/"cases"/c["id"]).as_posix()],cwd,30)
            marker = re.findall(r"^CASE_RESULT\|([^|]+)\|(PASS|FAIL|TIMEOUT)$",text,re.M)
            if rec["timed_out"]: status = "PROCESS_TIMEOUT"
            elif len(marker) != 1 or marker[0][0] != c["id"]:
                status = "RUN_ERROR"
            else: status = marker[0][1]
            wave = cwd / "wave.vcd"
            wave_info = None
            if wave.is_file():
                wt = wave.read_text(encoding="ascii")
                ticks = re.findall(r"^#(\d+)$", wt, re.M)
                ts = re.search(r"\$timescale\s+(.*?)\s+\$end",wt,re.S)
                wave_info = dict(path=str(wave),bytes=wave.stat().st_size,sha256=sha(wave),
                                 time_precision=ts.group(1).strip() if ts else None,
                                 last_timestamp=int(ticks[-1]) if ticks else None, timestamps=len(ticks))
            metrics = re.findall(r"^METRICS\|(.*)$",text,re.M)
            actual_regs = {int(i):v for i,v in re.findall(r"^REG\|(\d+)\|([0-9a-fxz]+)$",text,re.M)}
            actual_mem = {int(i):v for i,v in re.findall(r"^MEM\|(\d+)\|([0-9a-fxz]+)$",text,re.M)}
            mismatches = re.findall(r"^MISMATCH\|(.*)$",text,re.M)
            row = dict(id=c["id"],status=status,process_exit=rec["exit_code"],wall_seconds=rec["elapsed_wall_seconds"],
                       metrics=metrics, mismatches=mismatches,protocol_errors=re.findall(r"^PROTOCOL_ERROR\|(.*)$",text,re.M),
                       actual_regs=actual_regs,actual_mem=actual_mem,wave=wave_info,log=rec["log"])
            if status in ("PASS","FAIL","TIMEOUT"):
                assert wave_info and wave_info["timestamps"] > 3 and wave_info["last_timestamp"] > 0, "Missing fresh advancing waveform"
                assert len(actual_regs) == 32 and len(actual_mem) == 64 and len(metrics) == 1, "Incomplete comparisons"
                independent_mismatch = any(actual_regs[i] != f"{v:08x}" for i,v in enumerate(c["expected_regs"])) or any(actual_mem[i*4] != f"{v:08x}" for i,v in enumerate(c["expected_mem"]))
                if status == "PASS":
                    assert not independent_mismatch and not mismatches and not row["protocol_errors"] and rec["exit_code"] == 0
                else: assert rec["exit_code"] != 0
            state["cases"].append(row)
            persist()
            print(f"{c['id']}: {status}; mismatches={len(mismatches)}; {row['metrics']}")
            if status in ("PROCESS_TIMEOUT","RUN_ERROR"):
                raise RuntimeError("Tool/testbench runtime anomaly; preserve and stop")
        state["counts"] = {s:sum(c["status"]==s for c in state["cases"]) for s in ("PASS","FAIL","TIMEOUT")}
        state["baseline_completed"] = True
    except Exception as exc:
        state["error"] = str(exc)
        raise
    finally:
        verify_manifest(frozen["protected"])
        state["protected_unchanged"] = True
        verify_manifest(frozen["inputs"] + frozen["tool_hashes"])
        state["inputs_unchanged"] = True
        state["path_modified"] = os.environ.get("PATH") != old_path
        state["artifacts"] = manifest(runs)
        persist()
    print("BASELINE_COMPLETE; NO_FUNCTIONAL_RTL_CHANGE; NO_HARDWARE; STOP")

if __name__ == "__main__":
    raise SystemExit("Reference-only copy; use cpu_sh.py, not legacy runner.")
    p = argparse.ArgumentParser()
    p.add_argument("phase",choices=["prepare","run"])
    p.add_argument("--directory",default=str(ROOT/"work/icarus/2026-10-16-cpu-selfcheck-v1"))
    a = p.parse_args()
    directory = Path(a.directory).resolve()
    assert directory.is_relative_to(ROOT/"work/icarus"), "Out of scope directory"
    assert not ctypes.windll.shell32.IsUserAnAdmin(), "Refusing Windows administrator context"
    if a.phase == "prepare": prepare(directory)
    else: execute(directory)
