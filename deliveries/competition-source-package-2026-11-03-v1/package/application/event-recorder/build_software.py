"""Explicit standalone software-only build; never patches FPGA ROM or programs hardware.
This portable entry is new; the frozen binary was built by historical execute.py.
"""
from pathlib import Path
import argparse,subprocess,json,hashlib,time
def main():
 p=argparse.ArgumentParser();p.add_argument('--gcc-dir',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--dense',type=int,choices=[0,1],default=0);a=p.parse_args()
 root=Path(__file__).resolve().parent;out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
 tool=a.gcc_dir.resolve();commands=[]
 def run(name,args):
  start=time.monotonic();args=[str(x) for x in args]
  try:r=subprocess.run(args,cwd=root,capture_output=True,timeout=60);rc=r.returncode;raw=r.stdout+r.stderr
  except subprocess.TimeoutExpired as e:rc='TIMEOUT';raw=(e.stdout or b'')+(e.stderr or b'')
  except OSError as e:rc='TOOL_ERROR';raw=str(e).encode()
  (out/(name+'.log')).write_bytes(raw);commands.append(dict(argv=args,cwd=str(root),native_rc=rc,seconds=time.monotonic()-start,max_seconds=60))
  (out/'COMMANDS.json').write_text(json.dumps(commands,indent=2),encoding='utf8')
  if rc!=0:raise RuntimeError(f'{name}: {rc}; stop, keep evidence')
 run('gcc',[tool/'riscv-none-elf-gcc.exe','-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-msmall-data-limit=0','-mno-relax','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,-T,firmware/link.ld','-Wl,-Map,'+str(out/'program.map'),'-DSAMPLE_PERIOD=2700000','-DSAMPLE_COUNT=128','-DWAIT_SAMPLES=20',f'-DDENSE={a.dense}','-DAUDIT=0','-o',out/'program.elf','firmware/start.S','firmware/app.c'])
 run('objcopy',[tool/'riscv-none-elf-objcopy.exe','-O','binary',out/'program.elf',out/'program.bin'])
 data=(out/'program.bin').read_bytes()
 if len(data)>32768:raise RuntimeError('ROM capacity exceeded')
 padded=data+bytes(32768-len(data));(out/'program.hex').write_text(''.join(f'{int.from_bytes(padded[i:i+4],"little"):08x}\n' for i in range(0,32768,4)))
 profile='production1-r1' if a.dense else 'production0-r1';golden=root/'software'/profile/'program.bin'
 same=data==golden.read_bytes()
 (out/'RESULT.json').write_text(json.dumps(dict(status='BINARY_IDENTICAL' if same else 'BINARY_DIFFERENT_NOT_ACCEPTED',SHA256=hashlib.sha256(data).hexdigest().upper(),bytes=len(data),golden_profile=profile,identical=same,FPGA_ROM_updated=False,DUT_run=False),indent=2))
 if not same:raise RuntimeError('Stop: new binary differs from frozen version, no automatic ROM update')
 print('Software build matches frozen binary; no FPGA ROM update/DUT run')
if __name__=='__main__':main()
