"""Reproduce A's three finite guard probes; host-only, no production source edits."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--tool-root',required=True);ap.add_argument('--input-root',required=True);ap.add_argument('--work',required=True);ap.add_argument('--manifest-sha',default='5F06E6D6BCC3034D7EA1753BAE1168613519D45318881AD43B85E6F63371C8ED');a=ap.parse_args()
 tool=Path(a.tool_root).resolve(strict=True);inp=Path(a.input_root).resolve(strict=True);work=Path(a.work).resolve();assert not work.exists() and inp.is_dir()
 for root in [tool,inp,HERE]:assert work!=root and root not in work.parents,'work must be outside protected input/tool/response'
 assert sha(tool/'SHA256SUMS.txt')==a.manifest_sha.upper()
 for p in tool.rglob('*'):
  assert not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400,'links unsupported'
 for line in (tool/'SHA256SUMS.txt').read_text(encoding='utf-8-sig').splitlines():
  value,name=line.split('  ',1);rel=Path(name);assert not rel.is_absolute() and '..' not in rel.parts and ':' not in name;assert sha(tool/name)==value
 work.mkdir();shutil.copytree(tool,work/'tool-copy');(work/'fixtures').mkdir();(work/'outputs').mkdir();(work/'logs').mkdir()
 shutil.copyfile(HERE/'probes/resource_probe.py',work/'resource_probe.py');shutil.copyfile(HERE/'probes/memory_hold.py',work/'fixtures/memory_hold.py')
 rows=[]
 for mode in ['active-memory-guard','main-deadline']:
  r=subprocess.run([sys.executable,'-B',work/'resource_probe.py',mode,inp],capture_output=True,timeout=10)
  (work/'logs'/(mode+'-driver.stdout.log')).write_bytes(r.stdout);(work/'logs'/(mode+'-driver.stderr.log')).write_bytes(r.stderr);assert r.returncode==0,'probe infrastructure failed; retain logs'
  value=json.loads((work/'logs'/(mode+'.json')).read_text(encoding='utf-8-sig'));rows.append({k:v for k,v in value.items() if k!='observations'})
 case=json.loads((work/'tool-copy/tests/cases/C0-default.json').read_text(encoding='utf-8-sig'));case['id']='A-log-sink';case['limits']={'max_log_bytes_each':4096};cp=work/'log-case.json';cp.write_text(json.dumps(case),encoding='utf-8');out=work/'outputs/log-sink';peak=0;start=time.monotonic()
 with (work/'logs/log-driver.stdout.log').open('xb') as stdout,(work/'logs/log-driver.stderr.log').open('xb') as stderr:
  p=subprocess.Popen([sys.executable,'-B',work/'tool-copy/RUN.py','--case-file',cp,'--input-root',inp,'--out',out,'--fixture-worker','log_flood'],stdout=stdout,stderr=stderr)
  while p.poll() is None:
   q=out/'worker.stdout.log'
   if q.exists():peak=max(peak,q.stat().st_size)
   if time.monotonic()-start>10:p.kill();p.wait(2);raise RuntimeError('probe deadline')
   time.sleep(.001)
  rc=p.wait(2)
 rows.append(dict(id='log-sink',status='PASS' if rc==5 and peak<=4096 else 'FAIL',native_rc=rc,max_observed_file_bytes=peak,limit=4096))
 (work/'A_GUARD_RESULTS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(rows,ensure_ascii=False));return 0 if all(x['status']=='PASS' for x in rows) else 1
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');raise SystemExit(main())
