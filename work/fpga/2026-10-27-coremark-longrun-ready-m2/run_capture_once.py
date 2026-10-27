from pathlib import Path
import sys,json,time,os,stat,re,shutil
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from stage_coremark import read,sha
from stage_budget import check,deadline,measured_peak
from stream_io import Archiver,save,require
from host_supervisor import bounded
from preserve import protect

def spool_budget(run):
 total=0
 for p in (Path(run)/'spool').iterdir():
  try:st=p.lstat()
  except FileNotFoundError:continue # only this run's concurrently verified/unlinked spool
  require(stat.S_ISREG(st.st_mode) and not getattr(st,'st_file_attributes',0)&0x400 and re.fullmatch(r'(trace|bus)-[0-9]{6}\.log',p.name),'UNKNOWN_SPOOL_FILE_OR_LINK')
  total+=st.st_size
 require(total<=32*1024**2,'UNARCHIVED_SPOOL_CAP');return total
if __name__=='__main__':
 check();protect()
 for x in read(H/'frozen-inputs.json')['files']:assert sha(H/x['path'])==x['SHA256']
 comp=read(H/'compile-result.json');assert comp['status']=='COMPILED_NOT_FUNCTIONAL_PASS';row=comp;assert sha(row['output'])==row['SHA256']
 save(H/'DUT-attempt.json',dict(maximum=1,used=1,decision='D160',iterations=8,max_cycles=32000000,max_host_seconds=2400))
 run=H/'runs/performance8-N234';run.mkdir();(run/'spool').mkdir();end=deadline(2400)
 state=dict(offset=0,pending=b'',peak_spool=0,peak_parent=0,ready_events=0,parse_lines=0)
 def probe():
  check(end);state['peak_spool']=max(state['peak_spool'],spool_budget(run));own=measured_peak();state['peak_parent']=max(state['peak_parent'],own);require(own<=512*1024**2,'PARENT_MEMORY_CAP')
  for name,cap in [('wave.vcd',256*1024**2),('uart-pins.log',8*1024**2)]:
   p=run/name
   if p.exists():require(p.stat().st_size<=cap,name+'_CAP')
 arch=Archiver(run,deadline=end,poll=probe)
 def collect(logdir,exitcode):
  probe();p=logdir/'stdout.log'
  if not p.exists():return
  with p.open('rb') as f:f.seek(state['offset']);data=f.read(8*1024**2+1)
  state['offset']+=len(data);state['pending']+=data;require(len(state['pending'])<=8*1024**2,'STDOUT_PENDING_CAP')
  parts=state['pending'].split(b'\n');state['pending']=parts.pop()
  for line in parts:
   check(end);state['parse_lines']+=1;text=line.rstrip(b'\r').decode('utf-8-sig')
   if text.startswith(('SEGMENT|','END_STREAM|')):arch.consume(text);state['ready_events']+=text.startswith('SEGMENT|')
  probe()
  if exitcode is not None:require(not state['pending'],'TRUNCATED_STDOUT')
 lib=H.parents[2]/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/lib/ivl';vvp=lib.parents[1]/'bin/vvp.exe'
 r=bounded([vvp,'-N','-M-','-M'+str(lib),row['output'],'+MAX_CYCLES=32000000'],run,'run-performance8-N234',max(.001,end-time.monotonic()),while_running=collect,resource_probe=probe)
 specs=arch.finish();save(run/'process.json',r);shutil.copyfile(r['stdout'],run/'stdout.log');save(run/'capture-result.json',dict(status='ARCHIVE_CAPTURE_COMPLETE_NOT_FUNCTIONAL_PASS',process=r,streams=specs,supervisor={k:v for k,v in state.items() if k!='pending'},timings=arch.timings,source_protected=protect(),new_DUT=1))
 print(json.dumps(dict(status='NEW_8_ITER_DUT_CAPTURE_COMPLETE',host_seconds=r['elapsed_seconds'],spool_peak=state['peak_spool'],segments=state['ready_events'],timings=arch.timings),ensure_ascii=False))
