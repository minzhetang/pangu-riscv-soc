from pathlib import Path
import json,hashlib,ctypes,importlib.util,subprocess,time,threading,queue,re
H=Path(__file__).resolve().parent;R=H.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,x):
 with (H/('pred32-'+n)).open('x',encoding='utf8') as f:json.dump(x,f,indent=2)
def require(v,s):
 if not v:raise RuntimeError(s)
require(not ctypes.windll.shell32.IsUserAnAdmin(),'Ordinary user only')
require(not (H/'pred32-ATTEMPT.json').exists(),'One invocation only; preserve original attempt')
require(not (H/'pred32/generate_bitstream').exists(),'No old bitstream directory')
for x in json.loads((H/'PROTECTED_INPUTS.json').read_text()):require(sha(R/x['path'])==x['sha256'],'Protected input changed')
exe=Path('D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe')
require(sha(exe)=='631FFD8F14D6246872873C72025CBC2734C9F8C388075B7AFB0B042F3A684E6F','PDS tool identity changed')
inputs=[p for p in (H/'pred32/source').iterdir() if p.is_file()]+[H/'pred32'/n for n in ['flow.tcl','board_pins.fdc','clock_27mhz.fdc','closure_io.fdc']]
frozen=[{'path':p.relative_to(H).as_posix(),'sha256':sha(p)} for p in inputs];save('FROZEN_INPUTS.json',frozen)
spec=importlib.util.spec_from_file_location('owned',R/'work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py');J=importlib.util.module_from_spec(spec);spec.loader.exec_module(J)
args=[str(exe),'-file',str(H/'pred32/flow.tcl')];epoch=time.time();start=time.monotonic()
save('ATTEMPT.json',dict(date='2026-11-03',argv=args,cwd=str(H/'pred32'),deadline_seconds=1800,started_epoch=epoch,hardware_calls=0,administrator=False))
job=None;error=None;license_issue=False;license_days=[]
def sanitize(s):
 if re.search(r'(?i)host.?id|machine|hostname|host name|local address|\bUID\b|serial number|license|\.lic\b',s):return '[private licensing/host field omitted]'
 return s
try:
 job=J.OwnedJob(args,cwd=H/'pred32',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 q=queue.Queue(maxsize=8192)
 def pump():
  total=0
  for raw in iter(job.p.stdout.readline,b''):
   total+=len(raw)
   if total>16*1024*1024:q.put('LOG_LIMIT');break
   q.put(raw.decode('utf8','replace').rstrip())
  job.p.stdout.close()
 t=threading.Thread(target=pump,daemon=True);t.start()
 with (H/'pred32-native-sanitized.log').open('x',encoding='utf8') as f:
  while job.p.poll() is None or t.is_alive() or not q.empty():
   require(time.monotonic()-start<1800,'PDS build deadline')
   try:line=q.get(timeout=.1)
   except queue.Empty:continue
   require(line!='LOG_LIMIT','Log limit')
   days=re.search(r'(?i)(?:expire\w*|remaining).*?(\d+)\s*days?',line)
   if days:license_days.append(int(days[1]))
   fail=bool(re.search(r'(?i)(?:no valid license|license.*(?:has expired|is expired|not found|checkout failed)|cannot.*license)',line))
   license_issue|=fail;f.write(sanitize(line)+'\n');f.flush();require(not fail,'PDS licensing failure: no configuration attempted')
 job.p.wait(timeout=2);require(job.p.returncode==0,'PDS native nonzero')
 end=time.monotonic()+10
 while job.active() and time.monotonic()<end:time.sleep(.1)
except BaseException as e:error=type(e).__name__+': '+str(e)
finally:
 cleanup=job.close() if job else None
 # Native tool writes its own logs; sanitize only newly generated logs, not original evidence.
 sanitized_files=[]
 for p in (H/'pred32').rglob('*'):
  if p.is_file() and p.suffix.lower() in ['.log','.rpt','.snr','.rtr','.ccr','.prr']:
   text=p.read_text(encoding='utf8',errors='replace');lines=text.splitlines()
   if any(sanitize(l)!=l for l in lines):p.write_text('\n'.join(sanitize(l) for l in lines)+'\n',encoding='utf8');sanitized_files.append(p.relative_to(H).as_posix())
 artifacts=[]
 for p in (H/'pred32/generate_bitstream').glob('*.sbit'):
  artifacts.append(dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,sha256=sha(p),fresh=p.stat().st_mtime>=epoch-2))
 result=dict(error=error,elapsed_seconds=time.monotonic()-start,cleanup=cleanup,inputs_unchanged=all(sha(H/x['path'])==x['sha256'] for x in frozen),artifacts=artifacts,license_issue=license_issue,license_remaining_days_actual_prompts=license_days,sanitized_native_log_files=sanitized_files,audit_pending=True,hardware_calls=0)
 save('BUILD_EXIT.json',result);print(json.dumps(result),flush=True)
