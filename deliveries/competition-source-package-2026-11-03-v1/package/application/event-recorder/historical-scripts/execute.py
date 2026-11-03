from pathlib import Path
import subprocess,json,time,sys,hashlib,os
H=Path(__file__).resolve().parent;R=H.parents[2];T=R/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin';I=R/'tools/iverilog-13.0-msys2-ucrt64/ucrt64'
def save(p,x):p.write_text(json.dumps(x,indent=2),encoding='utf8')
def run(name,args,cwd=H,limit=40):
 log=H/'logs'/f'{name}.log';record=H/'logs'/f'{name}.json'
 if log.exists() or record.exists():raise RuntimeError('Refuse to overwrite execution '+name)
 a=list(map(str,args));start=time.monotonic()
 try:
  env=dict(os.environ)
  if name.startswith('run-'):env['IVERILOG_DUMPER']='none'
  p=subprocess.run(a,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=limit);rc=p.returncode;out=p.stdout
 except subprocess.TimeoutExpired as e:rc='TIMEOUT';out=e.stdout or b''
 except OSError as e:rc='TOOL_ERROR';out=str(e).encode()
 log.write_bytes(out);save(record,dict(argv=a,cwd=str(cwd),rc=rc,seconds=time.monotonic()-start,timeout_seconds=limit))
 if rc:raise RuntimeError((name,rc))
 return out.decode(errors='replace')
def compile_sw(name,period,count,wait,dense):
 d=H/'build'/name;d.mkdir(exist_ok=False)
 defs=[f'-DSAMPLE_PERIOD={period}',f'-DSAMPLE_COUNT={count}',f'-DWAIT_SAMPLES={wait}',f'-DDENSE={dense}','-DAUDIT=0']
 run('gcc-'+name,[T/'riscv-none-elf-gcc.exe','-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-msmall-data-limit=0','-mno-relax','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,-T,firmware/link.ld','-Wl,-Map,'+str(d/'program.map'),*defs,'-o',d/'program.elf','firmware/start.S','firmware/app.c'])
 run('objcopy-'+name,[T/'riscv-none-elf-objcopy.exe','-O','binary',d/'program.elf',d/'program.bin'])
 nm=run('nm-'+name,[T/'riscv-none-elf-nm.exe','-S',d/'program.elf']);(d/'symbols.txt').write_text(nm)
 run('disassemble-'+name,[T/'riscv-none-elf-objdump.exe','-d',d/'program.elf'])
 sy={}
 for line in nm.splitlines():
  v=line.split()
  if len(v)==4:sy[v[3]]=(int(v[0],16),int(v[1],16))
 assert 'samples' not in sy and ('raw' in sy)==bool(dense)
 b=(d/'program.bin').read_bytes();assert len(b)<32768;b+=bytes(32768-len(b))
 (d/'program.hex').write_text(''.join(f'{int.from_bytes(b[i:i+4],"little"):08x}\n' for i in range(0,len(b),4)))
 save(d/'BUILD.json',dict(period=period,count=count,wait=wait,dense=dense,bin_bytes=(d/'program.bin').stat().st_size,symbols=sy,sha256=hashlib.sha256((d/'program.bin').read_bytes()).hexdigest().upper()))
 return d
def compile_rtl(name='rtl'):
 src=[p for p in sorted((H/'source').glob('*')) if p.suffix in ['.v','.sv'] and p.name not in ['memory_model.sv','board_top.sv','board_reset_sync.sv']]
 run('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-s','tb','-o',H/(name+'.vvp'),*src,H/'memory_sim.sv',H/'tb.sv'])
def simulate(name,build,inputs,repeat=2,limit=45,maxcycles=2500000):
 d=H/'runs'/name;d.mkdir(exist_ok=False);cfg=json.loads((build/'BUILD.json').read_text())
 assert len(inputs)==cfg['count'];(d/'input.hex').write_text(''.join(f'{v:02x}\n' for v in inputs+[0]*(128-len(inputs))))
 (d/'program.hex').write_bytes((build/'program.hex').read_bytes())
 save(d/'INPUTS.json',dict(build=build.name,config=cfg,inputs=inputs,repeat=repeat))
 run('run-'+name,[I/'bin/vvp.exe','-M',I/'lib/ivl',H/'external-diagnostic-1.vvp',f'+PERIOD={cfg["period"]}',f'+COUNT={cfg["count"]}',f'+REPEATS={repeat}',f'+MAX_CYCLES={maxcycles}'],d,limit)
 return d
if __name__=='__main__':
 # The plan is frozen by prepare_plan.py before any DUT invocation.
 plan=json.loads((H/'FROZEN_PLAN.json').read_text())
 if sys.argv[1:] == ['slow']:
  d=compile_sw('slow-witness',2700000,2,20,0)
  simulate('slow-witness',d,[1,1],repeat=1,limit=210,maxcycles=5600000)
 elif sys.argv[1:] == ['fast']:
  for mode in [0,1]:
   d=compile_sw('fast'+str(mode),12000,32,6,mode)
   for name,c in plan['cases'].items():simulate(name+'-mode'+str(mode),d,c['input'])
 elif sys.argv[1:] == ['production']:
  for mode in [0,1]:compile_sw('production'+str(mode),2700000,128,20,mode)
 elif sys.argv[1:] == ['rtl']:compile_rtl()
 else:raise SystemExit('Use rtl / fast / slow / production; outputs are immutable, use unique directory for retries')
