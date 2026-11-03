from native import *
import gzip,re,struct,shutil
I=R/'tools/iverilog-13.0-msys2-ucrt64/ucrt64'
class Pump:
 def __init__(self,d):self.d=d;self.index=[];self.raw=0;self.compressed=0
 def __call__(self):
  files=sorted((self.d/'trace').glob('*.bin'))
  pending=sum(p.stat().st_size for p in (self.d/'trace').glob('*.bin*'))
  if pending>96*1024**2:raise RuntimeError('TRACE_BACKLOG_LIMIT')
  for p in files:
   if not re.fullmatch(r'\d{6}\.bin',p.name)or p.resolve().parent!=(self.d/'trace').resolve():raise RuntimeError('trace path')
   size=p.stat().st_size
   if size%20 or size>10*1024**2:raise RuntimeError('chunk size')
   target=p.with_suffix('.bin.gz');tmp=target.with_suffix('.gz.part');digest=hashlib.sha256()
   with p.open('rb')as inp,gzip.open(tmp,'wb',compresslevel=1)as out:
    for b in iter(lambda:inp.read(1048576),b''):digest.update(b);out.write(b)
   check=hashlib.sha256();n=0
   with gzip.open(tmp,'rb')as inp:
    for b in iter(lambda:inp.read(1048576),b''):check.update(b);n+=len(b)
   if n!=size or digest.digest()!=check.digest():raise RuntimeError('gzip roundtrip mismatch')
   tmp.rename(target);self.raw+=size;self.compressed+=target.stat().st_size
   self.index.append(dict(file=target.name,raw_bytes=size,records=size//20,raw_sha256=digest.hexdigest(),compressed_bytes=target.stat().st_size,compressed_sha256=sha(target)))
   # Only this newly generated exact path, after a full byte-for-byte roundtrip check.
   p.unlink()
   if self.raw>8*1024**3 or self.compressed>4*1024**3:raise RuntimeError('TRACE_LIMIT')
  for fn,cap in [('state.txt',1048576),('window.vcd',64*1024**2),('uart.txt',16384)]:
   p=self.d/fn
   if p.exists()and p.stat().st_size>cap:raise RuntimeError('FILE_LIMIT '+fn)
def frozen_check():
 plan=json.loads((H/'plans/FROZEN-v2.json').read_text())
 for rel,digest in plan['sha256'].items():
  if sha(H/rel)!=digest:raise RuntimeError('Frozen input changed '+rel)
 return plan
def compile_tb(name,pred,mutate=0):
 native('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb',f'-Ptb.PRED={pred}',f'-Ptb.MUTATE={mutate}','-o',H/(name+'.vvp'),*sorted((H/'source').glob('*.v')),H/'tb.sv'],limit=60)
def run_case(name,mode,it,pred,mutate=0):
 plan=frozen_check();d=H/'runs'/name;d.mkdir(exist_ok=False);(d/'trace').mkdir()
 source=H/'build'/f'{mode}-{it}'
 for fn in ['program.hex','program.bin']:shutil.copyfile(source/fn,d/fn)
 symbols=json.loads((source/'symbols.json').read_text());pump=Pump(d)
 limit=240 if it==1 else plan['budget']['case_seconds']
 status='NOT_RUN';error=None;command=None
 try:
  command=native(name,[I/'bin/vvp.exe','-M',H,'-M',I/'lib/ivl','-m','checker',H/(f'control-{mutate}.vvp'if mutate else f'pred{pred}.vvp'),f'+PHASE={symbols["timing_phase"]:x}'],cwd=d,limit=limit,housekeeping=pump)
  if mutate:
   if not(d/'checker-failure.txt').exists()or(d/'checker-final.json').exists():raise RuntimeError('Negative control accepted/incomplete')
   message=(d/'checker-failure.txt').read_text()
   expected='timer clock equation'if mutate==5 else 'X/Z task argument'if mutate==6 else 'event mismatch'
   if expected not in message:raise RuntimeError('Negative control failed for wrong reason: '+message)
   status='REJECTED_AS_EXPECTED'
  else:
   cks=json.loads((d/'checker-final.json').read_text())
   if cks['status']!='MATCH'or cks['raw_bytes']!=pump.raw or cks['records']!=sum(x['records']for x in pump.index):raise RuntimeError('Incomplete trace/checker')
   state=(d/'state.txt').read_text().splitlines();ram={int(s.split()[1]):int(s.split()[2],16)for s in state if s.startswith('MEM ')}
   ports=dict(port_error=0,ram_log_overflow=0,timer_error=0,port_finished=1,timer_start_calls=1,timer_stop_calls=1,timing_phase=4,seed4_volatile=it,seed3_volatile=0x66,seed5_volatile=0,seed1_volatile=0 if mode=='performance'else 0x3415,seed2_volatile=0 if mode=='performance'else 0x3415)
   if not all(ram[symbols[n]//4]==v for n,v in ports.items()):raise RuntimeError('Port/seed errors')
   if ram[0x17ff8//4]!=0 or ram[0x17ffc//4]!=0x600d600d:raise RuntimeError('Return/done')
   def u64(n):a=symbols[n]//4;return ram[a]|ram[a+1]<<32
   delta=u64('elapsed_ticks');end=next(s for s in state if s.startswith('END ')).split();cy=list(map(int,end[1:]));phase=cy[2]-cy[1]
   if phase-delta!=4 or delta!=u64('end_ticks')-u64('start_ticks'):raise RuntimeError('Timer/phase mismatch')
   timer=[s.split()for s in(d/'timer-reads.txt').read_text().splitlines()]
   if len(timer)!=12 or not all(int(v,16)==(int(edge)-2 if int(addr,16)==0x20000100 else 0)for _,edge,addr,v in timer):raise RuntimeError('Independent clock check')
   text=(d/'uart.txt').read_text();reference=(d/'reference-uart.txt').read_text()
   oracle=next(x for x in json.loads((H/'HOST_CRC_ORACLE.json').read_text())if x['mode']==mode and x['iterations']==it)
   for n,expected in zip(['crclist','crcmatrix','crcstate','crcfinal'],oracle['crcs']+[oracle['final_crc']]):
    if re.search(n+r'\s*:\s*0x([0-9a-f]+)',text)[1]!=expected:raise RuntimeError('Independent algorithm CRC '+n)
   if text!=reference or f'Iterations       : {it}\n'not in text:raise RuntimeError('UART/iteration')
   if it!=1 and(delta<270000000 or 'ERROR'in text or 'Errors detected'in text or 'Correct operation validated.'not in text):raise RuntimeError('Long-run duration/correctness')
   if it==1 and 'ERROR! Must execute for at least 10 secs'not in text:raise RuntimeError('Short qualification classification')
   status='PASS';save(d/'MEASUREMENT.json',dict(mode=mode,iterations=it,pred=pred,entries=32,clock_hz=27000000,mtime_ticks=delta,target_seconds=delta/27000000,phase_cycles=phase,full_cycles=cy[0],correctness=ports,oracle=oracle,formal_hardware_score=False,checker=cks,host_seconds=command['seconds']))
 except BaseException as e:error=repr(e);status='FAIL'
 finally:
  save(d/'TRACE_INDEX.json',dict(format='Little-endian uint32 records: tag,edge,a,b,c; tag1 WB(rd,data,0),tag2 STORE(address,data,mask),tag3 TIMER(address,data,0)',chunks=pump.index,raw_bytes=pump.raw,compressed_bytes=pump.compressed))
  save(d/'RESULT.json',dict(name=name,status=status,error=error,mode=mode,iterations=it,pred=pred,mutation=mutate,raw_bytes=pump.raw,compressed_bytes=pump.compressed,native=command))
 print(name,status,error,flush=True)
 if status not in ['PASS','REJECTED_AS_EXPECTED']:raise RuntimeError('Stop on failed case '+name)
 frozen_check()
 return json.loads((d/'RESULT.json').read_text())
if __name__=='__main__':
 if sys.argv[1]=='compile':
  for p in [0,1]:compile_tb(f'pred{p}',p)
  for m in range(1,7):compile_tb(f'control-{m}',1,m)
 elif sys.argv[1]=='qualify':
  for m in range(1,7):run_case(f'q2-control-{m}','performance',1,1,m)
  run_case('q2-performance','performance',1,1)
  run_case('q2-validation','validation',1,1)
 elif sys.argv[1]=='long':
  run_case('long-performance-p1','performance',192,1)
  run_case('long-validation-p1','validation',192,1)
 elif sys.argv[1]=='off':
  run_case('long-performance-p0','performance',192,0)
  run_case('long-validation-p0','validation',192,0)
