from pathlib import Path
import sys,time,json,ctypes,importlib.util,subprocess
R=Path('D:/A_FPGA_Comp');H=Path(sys.argv[1])
if not __debug__ or sys.argv[2:]!=['--run'] or ctypes.windll.shell32.IsUserAnAdmin():raise RuntimeError('Explicit ordinary mode required')
def save(n,v):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
if (H/'ATTEMPT.json').exists():raise RuntimeError('Used stage')
sp=importlib.util.spec_from_file_location('owned_native',R/'work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py');J=importlib.util.module_from_spec(sp);sp.loader.exec_module(J)
save('ATTEMPT.json',dict(kind='KEY0_CAPTURE_ONLY',transport='WIN32_READFILE',decision='D299',program_calls=0,hardware_server_calls=0,started=time.time()))
j=None;err=None;cleanup=[];start=time.monotonic()
try:
    j=J.OwnedJob([sys.executable,'-X','utf8','-B',str(R/'work/quality/2026-11-02-sm2-resume-m3/native_serial_capture.py'),'--run',str(H)],cwd=H,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    while not (H/'SERIAL_ARMED.json').exists():
        if j.p.poll() is not None or time.monotonic()-start>15:raise RuntimeError('Native receiver not armed; inspect SERIAL_RESULT')
        time.sleep(.1)
    print('ARMED_NATIVE_WIN32_KEY0_CAPTURE',flush=True)
    j.p.wait(timeout=615)
except BaseException as e:err=type(e).__name__+': '+str(e)
finally:
    (H/'STOP_SERIAL').touch(exist_ok=True)
    if j:
        # Preserve root outcome, allow up to2s for owned child/conhost teardown.
        # If anything remains, original conservative forced-cleanup flags still apply.
        if j.p.poll() is not None:
            settle=time.monotonic()+2
            while j.active() and time.monotonic()<settle:time.sleep(.05)
        try:cleanup.append(dict(name='serial',**j.close()))
        except Exception as e:cleanup.append(dict(name='serial',job_empty=False,error=type(e).__name__))
    save('RESULT.json',dict(kind='KEY0_CAPTURE_ONLY',error=err,full_svf_configuration_dispatches=0,cleanup=cleanup,elapsed=time.monotonic()-start))
    print(json.dumps(dict(error=err,cleanup=cleanup)),flush=True)
