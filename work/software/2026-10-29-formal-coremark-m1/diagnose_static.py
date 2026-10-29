from pathlib import Path
import sys,json,hashlib,struct,difflib,re
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
# Parse ELF symbols/file-backed data only. No instruction interpreter imported.
from stage_coremark import elf_symbols,initial_word,sha,read,save
rows=[]
for case in read(H/'FROZEN_PLAN.json')['cases']:
 d=H/'build'/case['id'];p=d/'program.elf';s=elf_symbols(p);seed=[]
 for n,expected in [('seed1_volatile',0 if case['seed']=='performance' else 0x3415),('seed2_volatile',0 if case['seed']=='performance' else 0x3415),('seed3_volatile',0x66),('seed4_volatile',case['iterations'])]:
  address=s[n];bss=s['__bss_start']<=address and address+4<=s['__bss_end']
  v=0 if bss else initial_word(p,address);assert v==expected
  seed.append(dict(symbol=n,address=address,ELF_region='BSS_ZERO_REQUIRED_FROM_CRT_NOT_FILE_BYTES' if bss else 'FILE_BACKED',declared_initial=v,requires_actual_startup_validation=bss))
 assert s['__bss_end']<=s['__stack_bottom'] and s['__stack_top']==0x18000
 r=read(d/'RESULT.json');text=Path(r['commands'][2]['stdout']).read_text(encoding='utf-8-sig')
 ops=re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+([a-z0-9.]+)',text,re.M)
 allowed=set('lui auipc jal jalr beq bne blt bge bltu bgeu lb lh lw lbu lhu sb sh sw add sub sll slt sltu xor srl sra or and addi slti sltiu xori ori andi slli srli srai ebreak'.split());assert ops and all(x[2] in allowed for x in ops)
 rows.append(dict(id=case['id'],seed_location_check=seed,decoded_instructions=len(ops),all_decoded_OPs_base_I=True,bin_SHA256=r['bin_SHA256'],ELF_SHA256=r['ELF_SHA256'],executed=False))
original=read(H/'PROTECTED_INPUTS.json');assert all(sha(Path(x['path']))==x['SHA256'] for x in original)
save('STATIC_ELF_DIAGNOSIS.json',dict(rows=rows,status='STATIC_ONLY_NO_PROGRAM_RUN',cause='initial_word accepts only file-backed bytes; zero seeds are in BSS. Existing CRT must really clear RAM A5 in subsequent reference/DUT, not prezeroed by testbench',original_inputs_unchanged=len(original)))
p=H/'reference_worker.py';s=p.read_text();old="assert initial_word(elf,symbols['seed1_volatile'])==(0 if case['seed']=='performance' else 0x3415)";assert old in s
new="""expected_seed=0 if case['seed']=='performance' else 0x3415
seed_address=symbols['seed1_volatile']
if symbols['__bss_start']<=seed_address and seed_address+4<=symbols['__bss_end']:
    assert expected_seed==0  # declaration only; do not prezero Reference RAM
else:
    assert initial_word(elf,seed_address)==expected_seed"""
candidate=s.replace(old,new).replace("n=word('ram_log_count');", "assert word('seed1_volatile')==expected_seed and word('seed2_volatile')==expected_seed\nn=word('ram_log_count');")
(H/'reference_worker-r1-PENDING.py').write_text(candidate,encoding='utf-8')
(H/'REFERENCE_FIX_PENDING.patch').write_text(''.join(difflib.unified_diff(s.splitlines(True),candidate.splitlines(True),fromfile='reference_worker.py',tofile='reference_worker-r1-PENDING.py')),encoding='utf-8')
save('STAGE_RESULT.json',dict(date='2026-10-29',status='PARTIAL_BUILD_PASS_REFERENCE_PREFLIGHT_ERROR_STOPPED',approval='D194',C_builds=4,C_builds_pass=4,native_GNU_commands=20,reference_worker_invocations=1,actual_reference_steps=0,completed_oracles=0,RTL_compiles=0,new_DUT=0,PDS=0,hardware='STOPPED',cause='A precheck assumed zero seed file-backed; ELF puts it in BSS',pending='one replacement reference invocation approval and remaining already scoped work; no rebuild required',originals_unchanged=True))
print('Static ELF diagnosis4 PASS; source originals unchanged; replacement worker prepared NOT RUN')
