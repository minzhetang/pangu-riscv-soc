from pathlib import Path
import sys,json,time,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from stage_coremark import read,save,sha,elf_symbols,initial_word
from reference_schedule import Scheduled
from stage_budget import check
case=next(x for x in read(H/'FROZEN_PLAN.json')['cases'] if x['id']==sys.argv[1]);tid=case['id'];d=H/'oracles'/tid;d.mkdir(exist_ok=False)
elf=H/'build'/tid/'program.elf';symbols=elf_symbols(elf);image=elf.with_suffix('.bin').read_bytes()
assert initial_word(elf,symbols['seed4_volatile'])==case['iterations']
assert initial_word(elf,symbols['seed3_volatile'])==0x66
expected_seed=0 if case['seed']=='performance' else 0x3415
seed_address=symbols['seed1_volatile']
if symbols['__bss_start']<=seed_address and seed_address+4<=symbols['__bss_end']:
    assert expected_seed==0  # declaration only; do not prezero Reference RAM
else:
    assert initial_word(elf,seed_address)==expected_seed
assert symbols['__bss_end']<=0x16000 and symbols['__stack_top']==0x18000
start=time.monotonic();s=Scheduled(image);r=s.run();check();assert r.steps<=(5000000 if case['iterations']==2 else 250000000)
def word(n,size=4):
 a=symbols[n]-0x10000;return int.from_bytes(r.ram[a:a+size],'little')
assert word('seed1_volatile')==expected_seed and word('seed2_volatile')==expected_seed
n=word('ram_log_count');assert n<4096;a=symbols['ram_log']-0x10000;report=bytes(r.ram[a:a+n]);text=report.decode('ascii')
for field,expected in zip(['seedcrc','[0]crclist','[0]crcmatrix','[0]crcstate'],case['standard_CRC']):assert re.findall(re.escape(field)+r'\s*:\s*0x([0-9a-f]{4})',text)==[f'{expected:04x}'],field
assert re.findall(r'^Iterations\s*:\s*(\d+)\s*$',text,re.M)==[str(case['iterations'])]
for name in ['port_error','ram_log_overflow','timer_error','timing_unavailable']:assert word(name)==0,name
for name in ['timer_start_calls','timer_stop_calls','port_finished']:assert word(name)==1,name
delta=word('elapsed_ticks',8);assert 0<delta<=0xffffffff
assert ('Must execute for at least 10 secs' in text)==case['expected_short_error']
assert ('Errors detected' in text)==case['expected_short_error']
assert ('Correct operation validated.' in text)==(not case['expected_short_error'])
assert 'MEASUREMENT CANDIDATE; TARGET EVIDENCE REQUIRED' in text and r.regs[10]==0 and word('timing_phase')==4
assert (delta<270000000)==case['expected_short_error']
(d/'expected-report.txt').write_bytes(report);(d/'expected-ram.bin').write_bytes(r.ram);(d/'expected-registers.hex').write_text(''.join(f'{v:08x}\n' for v in r.regs),encoding='ascii')
save(d/'expected.json',dict(status='REFERENCE_ONLY_NOT_DUT',id=tid,iterations=case['iterations'],steps=r.steps,raw_ticks=delta,stamps=[word(n,8) for n in ['empty_start','empty_end','start_ticks','end_ticks']],physical=2*(r.steps+2*r.flush+r.stall+19)+1,stall=r.stall,flush=r.flush,streams={k:getattr(r,k).summary() for k in ['EX','WB','MEM']},symbols=symbols,io_reads=s.io_reads,io_writes=s.io_writes,timer_reads=s.timer_reads,crcfinal=re.findall(r'^\[0\]crcfinal\s*:\s*0x([0-9a-f]{4})',text,re.M)[0],bin_SHA256=sha(elf.with_suffix('.bin')),elapsed_seconds=time.monotonic()-start,hardware_valid=False,formal_score_valid=False))
print(tid,'REFERENCE_ONLY',r.steps,delta,flush=True)
