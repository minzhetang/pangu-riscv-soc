from pathlib import Path
import sys,time,json,hashlib,shutil
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from stream_io import Archiver,open_stream,save
from stage_budget import deadline,check
from run_capture_once import spool_budget
import host_supervisor as hs
rows=[]
def reject(name,fn):
 try:fn()
 except (RuntimeError,AssertionError,ValueError,OSError,KeyError) as e:rows.append(dict(id=name,status='EXPECTED_REJECT',reason=str(e)[:200]));print(name,'REJECTED',flush=True)
 else:raise RuntimeError(name+' unexpectedly accepted')
if __name__=='__main__':
 end=deadline(900);d=H/'controls/container-scale';d.mkdir();(d/'spool').mkdir();a=Archiver(d,deadline=end)
 fmt='EDGE|{c}|00|00000000|0|00000000|0|00000000|0|1|00|1|00|0|0|0000000000000000|0000000000000001\n'
 count=0;total=0;bus_hash=hashlib.sha256();trace_hash=hashlib.sha256()
 for seq in range(180):
  check(end);raw=''.join(fmt.format(c=count+i+1) for i in range(32768)).encode('ascii');count+=32768;total+=len(raw);bus_hash.update(raw)
  (d/'spool'/f'bus-{seq:06d}.log').write_bytes(raw);a.consume(f'SEGMENT|bus|{seq}|32768|spool/bus-{seq:06d}.log')
 for seq in range(1025):
  check(end);raw=f'EX|{2+2*seq}|00000000\n'.encode('ascii');trace_hash.update(raw)
  (d/'spool'/f'trace-{seq:06d}.log').write_bytes(raw);a.consume(f'SEGMENT|trace|{seq}|1|spool/trace-{seq:06d}.log')
 a.consume(f'END_STREAM|bus|180|{count}');a.consume('END_STREAM|trace|1025|1025');a.finish();assert total>512*1024**2
 got=hashlib.sha256();n=0;size=0
 for n,line in enumerate(open_stream(d,'bus'),1):
  assert line==fmt.format(c=n);got.update(line.encode('ascii'));size+=len(line)
 assert n==count and size==total and got.digest()==bus_hash.digest()
 ntrace=0
 for ntrace,line in enumerate(open_stream(d,'trace'),1):assert line==f'EX|{2*ntrace}|00000000\n'
 assert ntrace==1025
 rows.append(dict(id='real-size-and-1025-segments',status='PASS',bus_actual_bytes=total,bus_actual_records=count,trace_actual_segments=1025,pointwise_every_line=True,not_CPU_or_new_DUT=True))
 # Small valid container for independent destructive copies; original large input stays immutable.
 small=H/'controls/small';small.mkdir();(small/'spool').mkdir();b=Archiver(small,deadline=end)
 for kind,raw in [('trace',b'EX|2|00000000\n'),('bus',fmt.format(c=1).encode('ascii'))]:
  (small/'spool'/f'{kind}-000000.log').write_bytes(raw);b.consume(f'SEGMENT|{kind}|0|1|spool/{kind}-000000.log');b.consume(f'END_STREAM|{kind}|1|1')
 b.finish()
 for name in ['bad-index','bad-payload','missing-segment']:
  bad=H/'controls'/name;shutil.copytree(small,bad);spec=json.loads((bad/'streams.json').read_text(encoding='utf-8'))
  for kind in spec:spec[kind]['path']=str(bad/'archive'/kind)
  (bad/'streams.json').write_text(json.dumps(spec),encoding='utf-8');p=bad/'archive/trace/stream-index.json' if name=='bad-index' else bad/'archive/trace/000000/block-000000.gz'
  if name=='missing-segment':p.rename(p.with_suffix('.retained'))
  else:
   data=bytearray(p.read_bytes());data[len(data)//2]^=1;p.write_bytes(data)
  reject(name,lambda:list(open_stream(bad,'trace')))
 for name,event in [('reordered','SEGMENT|trace|1|1|spool/trace-000001.log'),('missing-ready','END_STREAM|trace|1|1')]:
  bad=H/'controls'/name;bad.mkdir();(bad/'spool').mkdir();obj=Archiver(bad,deadline=end);reject(name,lambda:obj.consume(event))
 bad=H/'controls/duplicate';bad.mkdir();(bad/'spool').mkdir();obj=Archiver(bad,deadline=end);obj.consume('END_STREAM|trace|0|0');reject('duplicate END',lambda:obj.consume('END_STREAM|trace|0|0'));reject('missing terminal',lambda:obj.finish())
 bad=H/'controls/deadline';bad.mkdir();(bad/'spool').mkdir();obj=Archiver(bad,deadline=time.monotonic()-1);reject('absolute archive deadline',lambda:obj.consume('SEGMENT|trace|0|1|spool/trace-000000.log'))
 bad=H/'controls/spool';bad.mkdir();(bad/'spool').mkdir()
 with (bad/'spool/trace-000000.log').open('xb') as f:f.seek(32*1024**2);f.write(b'X')
 reject('spool cap',lambda:spool_budget(bad))
 bad=H/'controls/long-line';bad.mkdir();(bad/'raw.log').write_bytes(b'X'*256+b'\n');save(bad/'streams.json',dict(trace=dict(mode='raw',path=str(bad/'raw.log'),complete=True)));reject('oversized line',lambda:list(open_stream(bad,'trace')))
 real=hs.peak;hs.peak=lambda pid:None
 try:reject('unavailable memory fails closed',lambda:hs.bounded([sys.executable,'-B','-c','import time;time.sleep(2)'],H,'negative-no-memory',1))
 finally:hs.peak=real
 reject('parent deadline kills actual own child',lambda:hs.bounded([sys.executable,'-B','-c','import time;time.sleep(2)'],H,'negative-parent-deadline',.15))
 result=dict(status='PASS_HOST_ONLY',rows=rows,archive_timings=a.timings,not_CPU=True,new_DUT=0);save(H/'controls/container-results.json',result);print(json.dumps(dict(status=result['status'],actual_bytes=total,records=count,segments=1025,controls=len(rows))),flush=True)
