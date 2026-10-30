"""Offline by default. One conditional official-client read-only session, no program path."""
from pathlib import Path
import sys,json,time,hashlib,re,subprocess,threading,queue,os,ctypes
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2];BIN=Path('D:/PDS/PDS_2022.2-SP6.4/bin')
COMMANDS=('cfg_set_tcl_break -flag true','cfg_connect -ip 127.0.0.1 -port 65420','cfg_set_cable_property -index 0 -freq 1Mhz','cfg_scan_chain','cfg_read_device_property -mode 0 -device_index 0','cfg_read_device_property -mode 3 -device_index 0','cfg_disconnect')
def save(n,o):
 with (H/n).open('x',encoding='utf8') as f:json.dump(o,f,ensure_ascii=False,indent=2)
def status(lines):
 text='\n'.join(lines);m=re.findall(r'Status Register:\s*(0x[0-9a-fA-F]{1,8})\b',text);assert len(m)==1,'missing/duplicate status'
 v=int(m[0],16);binary=re.findall(r'The Status Register Code is\s*:\s*([01]{32})',text)
 if binary:assert len(binary)==1 and int(binary[0],2)==v,'hex/binary disagreement'
 return dict(raw=f'0x{v:08x}',flags={name:(v>>bit)&1 for name,bit in [('over_temp',27),('done',12),('done_i',13),('timeout',4),('rbcrc_err',3),('aut_err',2),('crc_err',1),('id_err',0)]})
def redact(s):
 if re.search(r'(?i)serial|\buid\b|host[_ ]?id|\bmac\b|机器码|序列|USB\\VID_|(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}',s):return '[private field withheld]'
 if re.search('cable',s,re.I) and not re.search(r'Executing\s*:\s*cfg_set_cable_property',s):return '[cable details withheld]'
 return s
def offline(result_name='OFFLINE_CHECK.json'):
 raw='0x081efca0';n=int(raw,16)
 assert status(['Status Register: '+raw+'.'])['flags']['over_temp']==1
 assert status(['Status Register: 0x001efca0.'])['flags']['over_temp']==0
 assert status(['The Status Register Code is :'+f'{n:032b}','Status Register: '+raw+'.'])['raw']==raw
 bad=[[],['Status Register: 0x081efca0.']*2,['Status Register: 0xzzzz.'],['The Status Register Code is :'+'0'*32,'Status Register: '+raw+'.']]
 for lines in bad:
  try:status(lines)
  except AssertionError:pass
  else:raise AssertionError('invalid status accepted')
 assert all('program' not in s and 'assign' not in s and 'reset' not in s for s in COMMANDS)
 receipt=dict(date='2026-10-30',status='OFFLINE_ONLY_READY_NOT_HARDWARE_RUN',commands=list(COMMANDS),positive=3,negative=4,hardware_executions=0,tool_files=[dict(name=n,bytes=(BIN/n).stat().st_size,SHA256=hashlib.sha256((BIN/n).read_bytes()).hexdigest().upper()) for n in ['cdt_cfg_shell.exe','cdt_js.exe','CH347DLLA64.DLL']],physical_gate_required=True,limit_seconds=45,repeat_scan=False)
 receipt['script_SHA256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper()
 save(result_name,receipt);print('Offline parser3 positive/4 negative PASS; tools only hashed; hardware0')
def no_competing_clients():
 # Process names only, no device query or private process arguments; fail on incomplete snapshot.
 import ctypes.wintypes as w
 k=ctypes.WinDLL('kernel32',use_last_error=True)
 class Entry(ctypes.Structure):
  _fields_=[('dwSize',w.DWORD),('cntUsage',w.DWORD),('pid',w.DWORD),('heap',ctypes.c_size_t),('module',w.DWORD),('threads',w.DWORD),('parent',w.DWORD),('priority',w.LONG),('flags',w.DWORD),('name',w.WCHAR*260)]
 k.CreateToolhelp32Snapshot.restype=w.HANDLE;k.CreateToolhelp32Snapshot.argtypes=[w.DWORD,w.DWORD]
 for n in ['Process32FirstW','Process32NextW']:
  f=getattr(k,n);f.argtypes=[w.HANDLE,ctypes.POINTER(Entry)];f.restype=w.BOOL
 k.CloseHandle.argtypes=[w.HANDLE]
 handle=k.CreateToolhelp32Snapshot(2,0);assert handle not in [None,ctypes.c_void_p(-1).value],'snapshot failure'
 try:
  e=Entry();e.dwSize=ctypes.sizeof(e);ok=k.Process32FirstW(handle,ctypes.byref(e));found=False
  while ok:
   found=found or e.name.lower() in ['cdt_cfg.exe','cdt_cfg_shell.exe','cdt_js.exe']
   ok=k.Process32NextW(handle,ctypes.byref(e))
  assert ctypes.get_last_error()==18,'incomplete process snapshot'
  assert not found,'existing configuration process, stop without killing it'
 finally:k.CloseHandle(handle)
def run():
 assert not ctypes.windll.shell32.IsUserAnAdmin(),'ordinary user only'
 proof=json.loads((H/'OFFLINE_CHECK-v3.json').read_text(encoding='utf8'))
 assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper()==proof['script_SHA256']
 for x in proof['tool_files']:assert hashlib.sha256((BIN/x['name']).read_bytes()).hexdigest().upper()==x['SHA256'],'tool changed'
 gate=json.loads((H/'PHYSICAL_GATE.json').read_text(encoding='utf8'))
 assert gate['state']=='READY_AFTER_APPROVED_STEP' and gate['user_reports_power_on'] and gate['connection_confirmed']
 assert 0<=time.time()-gate['power_on_epoch_estimate']<40,'insufficient power window; user must power off'
 save('ATTEMPT.json',dict(used=1,max=1,scope='D204 cold read-only only',time=time.time()))
 started=time.monotonic();end=min(started+45,started+54-(time.time()-gate['power_on_epoch_estimate'])) # reserve cleanup time
 server=None;client=None;logs=[];history=[];values=[];why=None;cq=queue.Queue();counts=[0];err=[]
 def pump(pipe):
  try:
   for line in iter(pipe.readline,b''):
    counts[0]+=len(line)
    if counts[0]>1024**2:err.append('LOG_CAP');return
    cq.put(line.decode('utf-8','replace').rstrip('\r\n'))
  finally:pipe.close()
 def cmd(s,seconds=5):
  assert s in COMMANDS;assert not err
  until=min(end,time.monotonic()+seconds);assert time.monotonic()<until,'session deadline'
  history.append(dict(command=s,elapsed=time.monotonic()-started))
  client.stdin.write((s+'\n').encode());client.stdin.flush();lines=[]
  good=re.compile(r'Executing\s*:\s*'+re.escape(s)+r'\s+successfully\.')
  while time.monotonic()<until:
   assert not err,err
   try:line=cq.get(timeout=min(.1,max(.001,until-time.monotonic())))
   except queue.Empty:continue
   lines.append(line);logs.append(redact(line))
   if good.search(line):return lines
   assert not re.search(r'(?i)\bfailed\b|\bfailure\b|\bunsuccessful\b|^\s*E:|^\s*Error\b|invalid command|cannot connect',line),'official command error'
  raise TimeoutError('read-only command timeout')
 try:
  # Host process/port conflict checks belong here only, after physical gate, not offline mode.
  no_competing_clients()
  import socket
  with socket.socket() as s:
   s.settimeout(.2);assert s.connect_ex(('127.0.0.1',65420))!=0,'existing server; stop, do not reuse'
  private=H/'private-server';private.mkdir()
  server=subprocess.Popen([BIN/'cdt_js.exe','-port','65420','-work_dir',private],cwd=H,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
  client=subprocess.Popen([BIN/'cdt_cfg_shell.exe'],cwd=H,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
  for pipe in [client.stdout,client.stderr]:threading.Thread(target=pump,args=(pipe,),daemon=True).start()
  cmd(COMMANDS[0]);cmd(COMMANDS[1]);cmd(COMMANDS[2]);scan=cmd(COMMANDS[3],8)
  assert [s.strip() for s in scan if re.fullmatch(r'PG[A-Z0-9]+|Unknown(?: Device)?',s.strip())]==['PG2L100H'],'unexpected chain'
  ident=cmd(COMMANDS[4]);ids=re.findall(r'The ID value is:\s*(0x[0-9a-fA-F]+)','\n'.join(ident));assert len(ids)==1 and int(ids[0],16)==0x00602899,'ID mismatch'
  for i in range(2):
   v=status(cmd(COMMANDS[5]));v['monotonic']=time.monotonic();values.append(v)
   if v['flags']['over_temp']:why='FLAG1_OBSERVED_NOT_TRUE_TEMPERATURE_PROOF';break
   if i==0:
    if time.monotonic()+10>=end:
     why='ONE_FLAG0_SAMPLE_TIME_BUDGET_NOT_SAFETY_CLEARANCE';break
    time.sleep(5)
  cmd(COMMANDS[6]);client.stdin.write(b'exit\n');client.stdin.flush();client.stdin.close();client.wait(timeout=max(.001,min(2,end-time.monotonic())))
  assert client.returncode==0,'client abnormal exit'
  if why is None:why='TWO_FLAG0_SAMPLES_NOT_SAFETY_CLEARANCE'
 except Exception as e:why='STOPPED_'+type(e).__name__;logs.append('Controller diagnostic: '+type(e).__name__)
 finally:
  cleanup=[]
  for name,p in [('client',client),('own_server',server)]:
   if p is not None:
    if p.poll() is None:p.terminate()
    try:p.wait(timeout=2)
    except subprocess.TimeoutExpired:p.kill();p.wait(timeout=1)
    cleanup.append(dict(name=name,rc=p.returncode,exited=p.poll() is not None))
  save('RESULT.json',dict(status=why,samples=values,commands=history,cleanup=cleanup,sanitized_output=logs,hardware_diagnostic=True,temperature_measured=False,hardware_safe=False,programmed=False,Flash=False,needs_user_power_off=True))
  print('READ_ONLY_SESSION_ENDED: disconnect 12V then downloader USB; no programming performed',flush=True)
if __name__=='__main__':
 assert len(sys.argv)==2 and sys.argv[1] in ['--offline-check','--offline-check-v2','--offline-check-v3','--run']
 if sys.argv[1]=='--run':run()
 else:offline('OFFLINE_CHECK-v3.json' if sys.argv[1]=='--offline-check-v3' else 'OFFLINE_CHECK-v2.json' if sys.argv[1]=='--offline-check-v2' else 'OFFLINE_CHECK.json')
