"""Prepare/freeze, compile once ordinarily, then run once with fixed timeouts."""
import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from check_c_boot import reference, checker_selftest, compare

sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding="utf-8")
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE=ROOT/"work/icarus/2026-10-21-cpu-shifti-reject"
SOFTWARE=ROOT/"work/toolchain-readiness/2026-10-22-xpack-rv32i"
TOOLS=ROOT/"tools/iverilog-13.0-msys2-ucrt64/ucrt64"
CPU_HASH={
    "cpu.v":"555CB51AC20FFC439B61BB29D4F4D9F4DC02C38B54A37291A79519CD413B8114",
    "control.v":"23CDBDFDD45DD60D6C7D95A13CC51927999A640FE5E30CAF8D324FA91AA87067",
    "alu.v":"6393472BC3635DA83213E0E9883766D5076C37EA60319F32F1DE5C420F68065E",
    "regfile.v":"AE36F070B994EEF41AF1636516D737EDA240C2A18AF83048ADC3E3E2391C8468"}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf-8")
def now(): return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def item(p): return {"path":str(p),"sha256":sha(p),"bytes":p.stat().st_size}

def prepare():
    assert not (HERE/"plan.json").exists(), "Never overwrite frozen plan"
    protected=[]
    for n,h in CPU_HASH.items():
        assert sha(BASE/"source"/n)==h, (n,"baseline mismatch")
        protected.append(BASE/"source"/n)
    protected += list((BASE/"models").glob("*.py"))
    protected += list(BASE.glob("tb*.sv"))
    protected += [BASE/"runs-v2/result.json",BASE/"validation-v2/plan.json",
                  SOFTWARE/"summary.json",SOFTWARE/"artifact-checks.json"]
    for d in ["source","models-before","inputs"]: (HERE/d).mkdir(exist_ok=False)
    for n in CPU_HASH: shutil.copy2(BASE/"source"/n,HERE/"source"/n)
    for p in (BASE/"models").glob("*.py"): shutil.copy2(p,HERE/"models-before"/p.name)
    for n in ["smoke.c","start.S","smoke.ld","manual-expectations.json","COMMANDS.md"]:
        p=SOFTWARE/n
        shutil.copy2(p,HERE/"inputs"/n); protected.append(p)
    for n in ["smoke.elf","smoke.bin","smoke.mem32.hex","smoke.bytes.hex"]:
        p=SOFTWARE/"runs-ordinary"/n
        shutil.copy2(p,HERE/"inputs"/n); protected.append(p)
    shutil.copy2(SOFTWARE/"runs-ordinary/objdump/stdout.log",HERE/"inputs/objdump.log")
    protected.append(SOFTWARE/"runs-ordinary/objdump/stdout.log")
    protected += [ROOT/"deliveries/mainline-rx-approval-2026-10-22-v1/RX_CORE_CONTRACT.md"]
    for n,h in {"bin/iverilog.exe":"25E1BA02E72F58D9D484BC5457D69A6B179D22D86BDF5BA5D6F9F0D4FE620BBF",
                "bin/vvp.exe":"F0775603E1F1BCF1B2DEA16DFF963A4B7D71B7B33D5BBE23D2B01FF5B2304E09"}.items():
        assert sha(TOOLS/n)==h
        protected.append(TOOLS/n)
    save(HERE/"protected-before.json",[item(p) for p in protected])
    manual={"authorization":"User approved A-CBOOT-M1 after D105 review, 2026-10-23",
            "hand_results":[119752999,12727,48,1234664],"signature":"50524f42",
            "proof":"1234567*97=119752999; 97*12727+48=1234567; sum=1234664",
            "startup":"copy 8 ROM bytes to .data, clear 20 BSS bytes from A5 poison; SP/GP per ELF",
            "stop":{"kind":2,"pc":"00000068","main_return":0},
            "initial_conditions":"all RAM bytes A5, existing RF initial-zero, 4 reset clocks",
            "scope":"unchanged CPU, zero-wait verification memory only; no MMIO/BRAM/ISA/hardware",
            "stall_flush":"model-derived from frozen executed instruction sequence, independently of DUT; not hand-counted",
            "created_before_reference":now()}
    save(HERE/"manual-plan.json",manual)
    expected=reference()
    save(HERE/"expected.json",expected)
    save(HERE/"checker-selftest.json",checker_selftest(expected))
    frozen=list((HERE/"source").glob("*.v"))+list((HERE/"models-before").glob("*.py"))+list((HERE/"inputs").glob("*"))
    frozen += [HERE/n for n in ["tb_c_boot.sv","memory_model.sv","check_c_boot.py","run_c_boot.py","manual-plan.json","expected.json"]]
    plan={"stage":"A-CBOOT-M1","approved_scope":manual["scope"],"frozen_before_DUT":now(),
          "input_files":[item(p) for p in frozen],"cycle_limit":100000,"compile_timeout_seconds":60,
          "run_timeout_seconds":30,"time_unit":"new TB 1ns/1ps, 10ns clock; not FPGA Fmax",
          "expected_arch_instructions":expected["architectural_instructions_including_ebreak"],
          "expected_WB":len(expected["writebacks"]),"expected_memory_events":len(expected["memory_events"]),
          "expected_stall":expected["stall_model_expected"],"expected_flush":expected["flush_model_expected"]}
    save(HERE/"plan.json",plan)
    save(HERE/"status.json",{"stage":"PREPARED","CPU_execution":"NOT_RUN","created":now()})
    print(json.dumps({k:v for k,v in plan.items() if k!="input_files"},ensure_ascii=False,indent=2))

def verify():
    records=json.loads((HERE/"plan.json").read_text(encoding="utf-8"))["input_files"]
    records+=json.loads((HERE/"protected-before.json").read_text(encoding="utf-8"))
    changed=[r["path"] for r in records if sha(Path(r["path"]))!=r["sha256"]]
    assert not changed, changed
    return len(records)

def call(label, argv, limit):
    save(HERE/f"runs/{label}-request.json",{"argv":argv,"cwd":str(HERE),"timeout_seconds":limit,
                                          "ordinary_user":True,"requested_at":now()})
    start=time.monotonic()
    try:
        proc=subprocess.run(argv,cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                            timeout=limit,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
        output,errors=proc.stdout,proc.stderr
        result={"exit_code":proc.returncode,"timed_out":False}
    except subprocess.TimeoutExpired as e:
        output,errors=e.stdout or b"",e.stderr or b""
        result={"exit_code":None,"timed_out":True}
    except OSError as e:
        output,errors=b"",str(e).encode("utf-8")
        result={"exit_code":None,"timed_out":False,"startup_error":str(e)}
    result["elapsed_wall_seconds"]=round(time.monotonic()-start,6)
    (HERE/f"runs/{label}-stdout.log").write_bytes(output)
    (HERE/f"runs/{label}-stderr.log").write_bytes(errors)
    save(HERE/f"runs/{label}-process.json",result)
    return result

def execute():
    verify()
    (HERE/"runs").mkdir(exist_ok=False)
    cmd=[str(TOOLS/"bin/iverilog.exe"),"-B",str(TOOLS/"lib/ivl"),"-g2012","-Wall","-s","tb_c_boot",
         "-o",str(HERE/"runs/c_boot.vvp")]
    cmd += [str(HERE/"source"/n) for n in ["alu.v","control.v","regfile.v","cpu.v"]]
    cmd += [str(HERE/"memory_model.sv"),str(HERE/"tb_c_boot.sv")]
    result=call("compile",cmd,60)
    if result["exit_code"]!=0 or result["timed_out"] or not (HERE/"runs/c_boot.vvp").is_file():
        save(HERE/"status.json",{"stage":"COMPILE_TOOL_ERROR","compile":result,"CPU_execution":"NOT_RUN",
                                 "reason":"Stop; no blind retry or stale VVP execution. New external permission required if indicated."})
        print(json.dumps(json.loads((HERE/"status.json").read_text(encoding="utf-8")),indent=2)); return
    run_and_check()

def run_and_check():
    # Internal ordinary-success path only. A failed compile's partial VVP is unsafe.
    verify()
    compile_record=json.loads((HERE/"runs/compile-process.json").read_text(encoding="utf-8"))
    assert compile_record["exit_code"]==0 and not compile_record["timed_out"], "Never run a partial failed-compile VVP"
    assert not (HERE/"runs/run-request.json").exists(), "Do not overwrite an existing attempt"
    vvp=HERE/"runs/c_boot.vvp"
    save(HERE/"runs/vvp-input.json",item(vvp))
    proc=call("run",[str(TOOLS/"bin/vvp.exe"),"-N","-M-","-M"+str(TOOLS/"lib/ivl"),str(vvp)],30)
    result={"stage":"EXECUTED","process":proc,"compile":json.loads((HERE/"runs/compile-process.json").read_text(encoding="utf-8")),
            "CPU_execution":"TIMEOUT" if proc["timed_out"] else "FAIL","baseline_unmodified_files":verify()}
    if proc["exit_code"]==0 and not proc["timed_out"]:
        text=(HERE/"runs/run-stdout.log").read_text(encoding="utf-8",errors="replace")
        regs=[int(v,16) for v in (HERE/"runs/registers.hex").read_text().split()]
        ram=[int(v,16) for v in (HERE/"runs/ram.hex").read_text().split()]
        verdict=compare(text,json.loads((HERE/"expected.json").read_text(encoding="utf-8")),regs,ram)
        save(HERE/"runs/check-results.json",verdict)
        result["CPU_execution"]=verdict["status"]
        result["checks"]=verdict
    result["new_hardware_operations"]=0
    result["CPU_RTL_changed"]=False
    save(HERE/"status.json",result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("action",choices=["prepare","execute"])
    action=parser.parse_args().action
    {"prepare":prepare,"execute":execute}[action]()
