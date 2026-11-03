from pathlib import Path
import sys, subprocess, json, time, hashlib, importlib.util
H=Path(__file__).resolve().parent; R=H.parents[2]
spec=importlib.util.spec_from_file_location('owned',R/'work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
I=R/'tools/iverilog-13.0-msys2-ucrt64/ucrt64'; jobs=json.loads((H/'COMMANDS.json').read_text()) if (H/'COMMANDS.json').exists() else []
def run(name,args,cwd,limit):
 identities={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for a in args if (p:=Path(a)).is_file() and p.suffix in ['.v','.sv','.vvp']}
 program=Path(cwd)/'program.hex'
 if program.exists():identities[str(program)]=hashlib.sha256(program.read_bytes()).hexdigest()
 t=time.monotonic(); j=m.OwnedJob(list(map(str,args)),cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 try:
  out,_=j.p.communicate(timeout=limit);rc=j.p.returncode
 except subprocess.TimeoutExpired:
  j.close();out,_=j.p.communicate(timeout=3);rc='TIMEOUT'
 finally:
  if j.job:
   deadline=time.monotonic()+2
   while j.active() and time.monotonic()<deadline:time.sleep(.02)
   active=j.active();j.close()
  else:active=[]
 (H/'logs'/f'{name}.log').write_bytes(out)
 jobs.append(dict(name=name,argv=list(map(str,args)),cwd=str(cwd),rc=rc,seconds=time.monotonic()-t,remaining_before_close=active,input_sha256=identities))
 (H/'COMMANDS.json').write_text(json.dumps(jobs,indent=2))
 print(name,rc,flush=True)
 return rc
if __name__=='__main__':
 for version in ['source-before','source']:
  rc=run('compile-'+version,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb','-o',H/(version+'.vvp'),*sorted((H/version).glob('*.v')),H/'tb.sv'],H,35)
  if rc:sys.exit(1)
