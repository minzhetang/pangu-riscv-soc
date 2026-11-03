"""Ordinary-user single run, only of the newly successful external-compile image."""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding="utf-8")
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from run_c_boot import verify, sha, item, save, now, TOOLS
from check_c_boot import compare

def main():
    count=verify()
    receipt=json.loads((HERE/"external-compile-01/result.json").read_text(encoding="utf-8"))
    assert receipt["exit_code"]==0 and not receipt["timed_out"] and receipt["IsUserAnAdmin"] is False
    assert receipt["status"]=="COMPILE_PASS_NOT_PROGRAM_PASS"
    image=HERE/"external-compile-01/c_boot.vvp"
    assert str(image)==receipt["output"]["path"] and sha(image)==receipt["output"]["sha256"]
    out=HERE/"ordinary-run-01"
    out.mkdir(exist_ok=False)
    (out/"inputs").mkdir(); (out/"runs").mkdir()
    shutil.copy2(HERE/"inputs/smoke.mem32.hex",out/"inputs/smoke.mem32.hex")
    assert sha(out/"inputs/smoke.mem32.hex")==sha(HERE/"inputs/smoke.mem32.hex")
    argv=[str(TOOLS/"bin/vvp.exe"),"-N","-M-","-M"+str(TOOLS/"lib/ivl"),str(image)]
    save(out/"request.json",{"argv":argv,"cwd":str(out),"timeout_seconds":30,
         "ordinary_user":True,"requested_at_beijing":now(),"verified_records":count,
         "VVP":item(image),"frozen_expectations":item(HERE/"expected.json"),
         "runner":item(Path(__file__))})
    start=time.monotonic()
    try:
        proc=subprocess.run(argv,cwd=out,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                            timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
        stdout,stderr=proc.stdout,proc.stderr
        process={"exit_code":proc.returncode,"timed_out":False}
    except subprocess.TimeoutExpired as e:
        stdout,stderr=e.stdout or b"",e.stderr or b""
        process={"exit_code":None,"timed_out":True}
    process["elapsed_wall_seconds"]=round(time.monotonic()-start,6)
    (out/"stdout.log").write_bytes(stdout); (out/"stderr.log").write_bytes(stderr)
    save(out/"process.json",process)
    result={"stage":"A-CBOOT-M1","compile_receipt":"external-compile-01/result.json",
            "process":process,"CPU_C_execution":"TIMEOUT" if process["timed_out"] else "FAIL",
            "CPU_RTL_changed":False,"protected_records_after":verify(),"hardware_calls":0}
    if process["exit_code"]==0 and not process["timed_out"]:
        expected=json.loads((HERE/"expected.json").read_text(encoding="utf-8"))
        try:
            regs=[int(v,16) for v in (out/"runs/registers.hex").read_text().split()]
            ram=[int(v,16) for v in (out/"runs/ram.hex").read_text().split()]
            verdict=compare(stdout.decode("utf-8",errors="replace"),expected,regs,ram)
            result["CPU_C_execution"]=verdict["status"]
            result["checks"]=verdict
            address=expected["symbols"]["results"]-0x10000
            result["actual_C_results"]=[int.from_bytes(bytes(ram[address+i*4:address+i*4+4]),"little") for i in range(4)]
            address=expected["symbols"]["signature"]-0x10000
            result["actual_signature"]=f"{int.from_bytes(bytes(ram[address:address+4]),'little'):08x}"
            result["actual_main_return_a0"]=regs[10]
        except (OSError,ValueError) as e:
            result["state_or_unknown_error"]=str(e)
    wave=out/"runs/wave.vcd"
    if wave.is_file(): result["wave"]=item(wave)
    save(HERE/"result-after-external.json",result)
    display={**result}
    if "checks" in display:
        display["checks"]={**display["checks"],"differences":display["checks"]["differences"][:8]}
    print(json.dumps(display,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
