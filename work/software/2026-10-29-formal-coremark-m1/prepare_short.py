from pathlib import Path
import sys,shutil,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2];S=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2'
from stage_coremark import read,save,sha,table
from stage_budget import check
check()
for n in ['block_codec.py','stream_io.py','stream_peripherals.py','audit_uart.py','audit_wave.py','check_coremark.py']:
 shutil.copy2(S/n,H/n)
s=(H/'check_coremark.py').read_text();s=s.replace("H/'oracles'/name", "H/'oracles-recovery'/name")
(H/'check_coremark.py').write_text(s,encoding='utf8')
s=(H/'audit_uart.py').read_text().replace("H/'oracles'/tid", "H/'oracles-recovery'/tid")
(H/'audit_uart.py').write_text(s,encoding='utf8')
s=(S/'frozen_checks.py').read_text().replace("d=H/'oracles'/name", "d=H/'oracles-recovery'/name")
s=s.replace("    return o\n", "    o['expected_physical']=o['physical'];o['RAM_SHA256']=hashlib.sha256((d/'expected-ram.bin').read_bytes()).hexdigest().upper();o['report_SHA256']=hashlib.sha256((d/'expected-report.txt').read_bytes()).hexdigest().upper()\n    return o\n")
(H/'frozen_checks.py').write_text(s,encoding='utf8')
s=(S/'tests/tb_board_coremark.sv').read_text();assert s.count('32000000')==3;s=s.replace('32000000','12000000')
(H/'tests/tb_board_coremark.sv').write_text(s,encoding='utf8')
(H/'cases').mkdir();(H/'compile').mkdir();(H/'runs').mkdir()
frozen={};artifacts=[];manual={};jobs=[]
template=read(S/'compile-plan.json')['targets'][0]['argv']
for tid in ['performance2','validation2']:
 o=read(H/'oracles-recovery'/tid/'expected.json');d=H/'cases'/tid/'source';shutil.copytree(H/'source',d)
 for p in sorted(d.glob('init_tables*')):p.rename(p.with_name('before-'+p.name))
 table((H/'build'/tid/'program.bin').read_bytes(),d/'init_tables.svh')
 frozen[tid+'-N234']=dict(phase_address=o['symbols']['timing_phase'],expected_raw_ticks=o['raw_ticks'],expected_stamps=o['stamps'],expected_report_sha256=sha(H/'oracles-recovery'/tid/'expected-report.txt'),expected_UART_bytes=(H/'oracles-recovery'/tid/'expected-report.txt').stat().st_size,iterations=2,n=234)
 artifacts.append(dict(id=tid,symbols=o['symbols']))
 c=next(c for c in read(H/'FROZEN_PLAN.json')['cases'] if c['id']==tid)
 manual[tid]=dict(zip(['seedcrc','crclist','crcmatrix','crcstate'],c['standard_CRC']))
 argv=[]
 for a in template:
  a=a.replace(str(S/'cases/performance8-N234/source'),str(d)).replace(str(S/'tests'),str(H/'tests')).replace(str(S/'compile/performance8-N234.vvp'),str(H/'compile'/(tid+'.vvp')))
  a=a.replace('-Ptb_board_coremark.PHASE_ADDR=67584','-Ptb_board_coremark.PHASE_ADDR='+str(o['symbols']['timing_phase']))
  argv.append(a)
 jobs.append(dict(id=tid,argv=argv))
save(H/'frozen-case-plan.json',dict(cases=frozen))
save(H/'build-result.json',dict(artifacts=artifacts));save(H/'manual-plan.json',dict(coremark=manual));save(H/'SHORT_COMPILE_PLAN.json',dict(targets=jobs))
save(H/'SHORT_FROZEN_INPUTS.json',dict(files=[dict(path=str(p.relative_to(H)),SHA256=sha(p)) for root in ['source','models','tests','cases','oracles-recovery'] for p in (H/root).rglob('*') if p.is_file()]))
print('Short plans frozen before compile; RTL unchanged except case INIT; TB only maximum cycles changed')
