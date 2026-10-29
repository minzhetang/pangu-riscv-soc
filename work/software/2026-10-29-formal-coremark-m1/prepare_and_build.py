from pathlib import Path
import sys,json,hashlib,shutil,time,difflib
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2];S=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
scope=P/'deliveries/mainline-formal-coremark-software-scope-2026-10-29-v1';status=json.loads((scope/'SCOPE_STATUS.json').read_text());assert sha(scope/'IMPLEMENTATION_SCOPE.md')==status['scope_SHA256']
start=time.monotonic();save('STAGE_CLOCK.json',dict(start=start,deadline_monotonic=start+7200));save('APPROVAL.json',dict(date='2026-10-29',decision='D194',user_approved=True,scope_SHA256=status['scope_SHA256'],hardware='STOPPED'))
protected=[]
for folder in ['source','models','port','firmware','upstream','tests']:
 shutil.copytree(S/folder,H/folder)
 for p in (S/folder).rglob('*'):
  if p.is_file():protected.append(dict(path=str(p),SHA256=sha(p)))
 if folder in ['source','models','port']:shutil.copytree(S/folder,H/(folder+'-before'))
save('PROTECTED_INPUTS.json',protected)
for name in ['stage_budget.py','host_supervisor.py']:shutil.copy2(S/name,H/name)
(H/'logs').mkdir();(H/'build').mkdir()
save('FROZEN_PLAN.json',dict(before_new_C_builds=True,cases=[dict(id=seed+str(n),seed=seed,iterations=n,standard_CRC={'performance':[0xe9f5,0xe714,0x1fd7,0x8e3a],'validation':[0x18f2,0xe3c1,0x0747,0x8d84]}[seed],DUT=n==2,expected_short_error=n==2,hardware_valid=False) for n in [2,256] for seed in ['performance','validation']],source_constraints='13RTL/official6/start/link unchanged; port metadata/time constant only'))
p=H/'port/core_portme.h';s=p.read_text();s=s.replace('#include <stddef.h>','#include <stddef.h>\n#include "build_identity.h"').replace('#define COMPILER_FLAGS "RV32I/ILP32 -O2; full flags in build request"','#define COMPILER_FLAGS FLAGS_STR').replace('STATIC RAM; timed simulation, NO VALID SCORE','Code in on-chip ROM; data in static on-chip RAM; clock ratio 1:1');p.write_text(s,encoding='utf-8',newline='\n')
p=H/'port/core_portme.c';s=p.read_text().replace('return ticks/27000000u;','return ticks/COREMARK_CLOCK_HZ;').replace('ee_printf("Timer Hz set    : 27000000; SIM ONLY, NO VALID SCORE\\n");','ee_printf("Timer Hz set    : %u; MEASUREMENT CANDIDATE; TARGET EVIDENCE REQUIRED\\n",COREMARK_CLOCK_HZ);');p.write_text(s,encoding='utf-8',newline='\n')
diff=''
for n in ['core_portme.c','core_portme.h']:diff+=''.join(difflib.unified_diff((H/'port-before'/n).read_text().splitlines(True),(H/'port'/n).read_text().splitlines(True),fromfile='port-before/'+n,tofile='port/'+n))
(H/'PORT_DIFF.patch').write_text(diff,encoding='utf-8')
from host_supervisor import bounded
tools=P/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
results=[]
try:
 for case in json.loads((H/'FROZEN_PLAN.json').read_text())['cases']:
  tid=case['id'];d=H/'build'/tid;d.mkdir()
  flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie','-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0','-Wall','-Wextra','-Werror','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none','-Wl,-T,firmware/link.ld','-Wl,-Map,build/'+tid+'/program.map','-Ifirmware','-Iport','-Iupstream','-Ibuild/'+tid,'-DTOTAL_DATA_SIZE=2000','-DITERATIONS='+str(case['iterations']),'-D'+case['seed'].upper()+'_RUN=1']
  (d/'build_identity.h').write_text('#define COREMARK_CLOCK_HZ 27000000u\n#define FLAGS_STR '+json.dumps(' '.join(flags))+'\n',encoding='ascii')
  inputs=['firmware/start.S']+[p.relative_to(H).as_posix() for p in sorted((H/'upstream').glob('*.c'))]+['port/core_portme.c']
  jobs=[('gcc',[tools/'riscv-none-elf-gcc.exe',*flags,'-o','build/'+tid+'/program.elf',*inputs,'-lgcc']),('objcopy',[tools/'riscv-none-elf-objcopy.exe','-O','binary','build/'+tid+'/program.elf','build/'+tid+'/program.bin']),('objdump',[tools/'riscv-none-elf-objdump.exe','-d','-M','no-aliases','build/'+tid+'/program.elf']),('readelf',[tools/'riscv-none-elf-readelf.exe','-h','-A','-l','-sW','build/'+tid+'/program.elf']),('nm',[tools/'riscv-none-elf-nm.exe','-u','build/'+tid+'/program.elf'])]
  save('build/'+tid+'/FROZEN_BUILD.json',dict(case=case,flags=flags,jobs=[dict(name=n,argv=list(map(str,args))) for n,args in jobs],inputs=[dict(path=str(p.relative_to(H)),SHA256=sha(p)) for p in [*(H/x for x in inputs),H/'port/core_portme.h',H/'firmware/link.ld',d/'build_identity.h']]))
  rec=[bounded(args,H,'build-'+tid+'-'+n,60 if n=='gcc' else 20) for n,args in jobs]
  assert not Path(rec[-1]['stdout']).read_text().strip()
  b=(d/'program.bin').read_bytes();assert len(b)<=32768 and len(b)%4==0
  results.append(dict(id=tid,bytes=len(b),bin_SHA256=sha(d/'program.bin'),ELF_SHA256=sha(d/'program.elf'),commands=rec,status='BUILD_ONLY_NOT_EXECUTED'))
  save('build/'+tid+'/RESULT.json',results[-1]);print(tid,'BUILD_ONLY',len(b),flush=True)
 save('BUILD_RESULTS.json',results)
except Exception as exc:
 save('BUILD_ERROR.json',dict(error=str(exc),completed=results));raise
finally:
 assert all(sha(Path(r['path']))==r['SHA256'] for r in protected)
 save('BUILD_POSTFLIGHT.json',dict(protected_inputs=len(protected),unchanged=True,hardware='STOPPED'))
