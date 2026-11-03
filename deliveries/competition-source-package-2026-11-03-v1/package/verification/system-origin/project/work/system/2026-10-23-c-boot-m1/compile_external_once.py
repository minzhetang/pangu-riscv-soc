"""Exactly one user-approved non-admin external compilation; never simulates."""
import ctypes
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding="utf-8")
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from run_c_boot import verify, now

def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf-8")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def main():
    count=verify()
    request=json.loads((HERE/"next-compile-request.json").read_text(encoding="utf-8"))
    assert not ctypes.windll.shell32.IsUserAnAdmin(), "Administrator execution forbidden"
    assert request["timeout_seconds"]==60
    argv=request["argv"]
    assert sha(Path(argv[0]))==request["compiler_SHA256"]
    for item in request["input_SHA256"]:
        assert sha(Path(item["path"]))==item["sha256"]
    out=HERE/"external-compile-01"
    assert Path(argv[argv.index("-o")+1])==out/"c_boot.vvp"
    out.mkdir(exist_ok=False)
    actual={**request,"status":"USER_AUTHORIZED_SINGLE_EXTERNAL_COMPILE_STARTED",
            "authorized_on":"2026-10-23","started_at_beijing":now(),
            "IsUserAnAdmin":False,"protected_and_frozen_verified":count,
            "no_simulation_installation_or_hardware":True}
    save(out/"request.json",actual)
    start=time.monotonic()
    proc=subprocess.Popen(argv,cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          creationflags=subprocess.CREATE_NO_WINDOW)
    timed_out=False
    try:
        stdout,stderr=proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        timed_out=True
        # Kill only this freshly created compiler process tree, if necessary.
        cleanup=subprocess.run(["taskkill.exe","/PID",str(proc.pid),"/T","/F"],
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        save(out/"timeout-cleanup.json",{"exit_code":cleanup.returncode,
                                        "scope":"own newly created compiler PID tree only"})
        proc.kill()
        stdout,stderr=proc.communicate(timeout=5)
    (out/"stdout.log").write_bytes(stdout); (out/"stderr.log").write_bytes(stderr)
    result={"exit_code":proc.returncode,"timed_out":timed_out,
            "elapsed_wall_seconds":round(time.monotonic()-start,6),"IsUserAnAdmin":False,
            "single_compile_permission_consumed":True,"completed_at_beijing":now(),
            "simulation_calls":0,"verified_records_after":verify()}
    image=out/"c_boot.vvp"
    if image.is_file(): result["output"]={"path":str(image),"bytes":image.stat().st_size,"sha256":sha(image)}
    result["status"]="COMPILE_PASS_NOT_PROGRAM_PASS" if proc.returncode==0 and not timed_out and image.is_file() and image.stat().st_size>0 else "COMPILE_FAILED_DO_NOT_RUN_OUTPUT"
    save(out/"result.json",result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"]!="COMPILE_PASS_NOT_PROGRAM_PASS": sys.exit(1)

if __name__=="__main__": main()
