from native import *
from run_fast import frozen_check
import gzip,re,threading,struct
def replay(name,mutation=None):
 d=H/'runs'/name;idx=json.loads((d/'TRACE_INDEX.json').read_text());label=name+('-'+mutation if mutation else '')
 if (d/f'AUDIT-{mutation or "full"}.json').exists():raise RuntimeError('Audit attempt already recorded')
 if not mutation and json.loads((d/'RESULT.json').read_text())['status']!='PASS':raise RuntimeError('Case not accepted')
 log=H/'logs'/f'raw-replay-{label}.log';errors=[];counts=dict(bytes=0,chunks=0);start=time.monotonic()
 with log.open('xb')as out:
  argv=[H/'audit_raw.exe',d/'program.bin',d];j=job.OwnedJob(list(map(str,argv)),cwd=H,stdin=subprocess.PIPE,stdout=out,stderr=subprocess.STDOUT)
  def writer():
   try:
    first=True;last=None
    for row in idx['chunks']:
     p=d/'trace'/row['file']
     if p.resolve().parent!=(d/'trace').resolve()or not re.fullmatch(r'\d{6}\.bin\.gz',p.name):raise RuntimeError('Unsafe archive path')
     if sha(p)!=row['compressed_sha256']:raise RuntimeError('Compressed SHA mismatch')
     h=hashlib.sha256();n=0
     with gzip.open(p,'rb')as src:
      for block in iter(lambda:src.read(1048560),b''):
       h.update(block);n+=len(block);original=block
       if first:
        first=False
        if mutation=='wrong-first':v=bytearray(block);v[12]^=1;block=bytes(v)
        elif mutation=='missing-first':block=block[20:]
        elif mutation=='duplicate-first':block=block[:20]+block
        elif mutation=='swap-first-two':block=block[20:40]+block[:20]+block[40:]
       if mutation=='truncate-tail':
        if last is not None:j.p.stdin.write(last)
        last=block;block=b''
       if block:j.p.stdin.write(block)
       counts['bytes']+=len(original)
     if n!=row['raw_bytes']or h.hexdigest()!=row['raw_sha256']:raise RuntimeError('Raw SHA mismatch')
     counts['chunks']+=1
    if mutation=='truncate-tail'and last is not None:j.p.stdin.write(last[:-1])
    if mutation=='extra-event':j.p.stdin.write(struct.pack('<IIIII',1,0,31,1,0))
   except BrokenPipeError:errors.append('BrokenPipe: native verifier rejected input')
   except BaseException as e:errors.append(repr(e))
   finally:
    try:j.p.stdin.close()
    except BrokenPipeError:pass
  t=threading.Thread(target=writer,daemon=True);t.start();deadline=start+1800
  try:
   while j.p.poll()is None:
    if time.monotonic()>deadline:raise TimeoutError('Replay timeout')
    if log.stat().st_size>1048576:raise RuntimeError('Replay log limit')
    time.sleep(.1)
   t.join(5)
   if t.is_alive():raise RuntimeError('Replay writer did not terminate')
   rc=j.p.returncode;active=j.active();j.close()
  except BaseException:
   j.close();t.join(5);raise
 text=log.read_text();result=dict(name=name,mutation=mutation,rc=rc,errors=errors,seconds=time.monotonic()-start,counts=counts,remaining_before_close=active,log_sha256=sha(log))
 if mutation:
  result['pass_']=rc==3 and 'REJECT 'in text and not active
 else:
  model=json.loads(text);runtime=json.loads((d/'checker-final.json').read_text());result['model']=model
  result['pass_']=rc==0 and not errors and not active and model['status']=='MATCH'and all(model[k]==runtime[k]for k in ['records','instructions','wb','stores'])and counts['bytes']==idx['raw_bytes']
 save(d/f'AUDIT-{mutation or "full"}.json',result);print('AUDIT',label,result['pass_'],result['seconds'],flush=True)
 if not result['pass_']:raise RuntimeError('Replay audit failed')
 return result
if __name__=='__main__':
 frozen_check()
 if sys.argv[1]=='qualify':
  replay('terminal-qualification-performance')
  for m in ['wrong-first','missing-first','duplicate-first','swap-first-two','truncate-tail','extra-event']:replay('terminal-qualification-performance',m)
 else:
  pred=int(sys.argv[1])
  for mode in ['performance','validation']:replay(f'long-{mode}-p{pred}')
