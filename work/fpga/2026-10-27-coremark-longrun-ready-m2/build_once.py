"""Single ITERATIONS=8 GNU build; all commands are pinned and fail-stop."""
from pathlib import Path
import sys,struct,json,ast
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2];R=H.parent/'2026-10-25-coremark-iter2-m1'
from stage_coremark import read,sha,save,elf_symbols,initial_word,table
from stage_budget import check
from host_supervisor import bounded
if __name__=='__main__':
 check();d=H/'build/performance8';d.mkdir(exist_ok=False);save(H/'C-build-attempt.json',dict(used=1,maximum=1,iterations=8,decision='D160'))
 tool=P/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin';installed={Path(x['path']):x['sha256'] for x in read(P/'work/toolchain-readiness/2026-10-22-xpack-rv32i/installed-files.json')}
 for n in ['gcc','objcopy','objdump','readelf','nm']:assert sha(tool/f'riscv-none-elf-{n}.exe')==installed[tool/f'riscv-none-elf-{n}.exe']
 fw=H/'firmware';flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie','-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0','-Wall','-Wextra','-Werror','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none','-Wl,-T,'+str(fw/'link.ld'),'-Wl,-Map,'+str(d/'program.map'),'-I'+str(fw),'-I'+str(H/'port'),'-I'+str(H/'upstream'),'-DTOTAL_DATA_SIZE=2000','-DITERATIONS=8','-DPERFORMANCE_RUN=1']
 jobs=[('compile',[tool/'riscv-none-elf-gcc.exe',*flags,'-o',d/'program.elf',fw/'start.S',*sorted((H/'upstream').glob('*.c')),H/'port/core_portme.c','-lgcc']),('objcopy',[tool/'riscv-none-elf-objcopy.exe','-O','binary',d/'program.elf',d/'program.bin']),('objdump',[tool/'riscv-none-elf-objdump.exe','-d','-M','no-aliases',d/'program.elf']),('readelf',[tool/'riscv-none-elf-readelf.exe','-h','-A','-l','-sW',d/'program.elf']),('nm',[tool/'riscv-none-elf-nm.exe','-u',d/'program.elf'])]
 records=[]
 for name,args in jobs:records.append(bounded(args,d,'build-'+name,60 if name=='compile' else 20))
 assert not Path(records[-1]['stdout']).read_text().strip()
 symbols=elf_symbols(d/'program.elf');image=(d/'program.bin').read_bytes();assert initial_word(d/'program.elf',symbols['seed4_volatile'])==8 and len(image)<=32768 and len(image)%4==0
 assert symbols['__bss_end']<=0x16000 and symbols['__stack_top']==0x18000
 old=(R/'build/performance/program.bin').read_bytes();assert len(old)==len(image)
 diffs=[dict(offset=i,before=a,after=b) for i,(a,b) in enumerate(zip(old,image)) if a!=b];assert len(diffs)==1 and diffs[0]['before']==2 and diffs[0]['after']==8
 data=Path(records[2]['stdout']).read_text(encoding='utf-8-sig');decoded=__import__('re').findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+([a-z0-9.]+)',data,__import__('re').M)
 allowed={'lui','auipc','jal','jalr','beq','bne','blt','bge','bltu','bgeu','lb','lh','lw','lbu','lhu','sb','sh','sw','add','sub','sll','slt','sltu','xor','srl','sra','or','and','addi','slti','sltiu','xori','ori','andi','slli','srli','srai','ebreak'}
 assert decoded and all(x[2] in allowed for x in decoded)
 # Replace only the candidate's old initialization copy, retain it in before.
 init=H/'cases/performance8-N234/source/init_tables.svh'
 if init.exists():
  (H/'before/init_tables-iter2.svh').write_bytes(init.read_bytes());init.rename(init.with_name('init_tables-iter2.svh'));table(image,init)
 base=read(H/'BASE_BUILD_RESULT.json');base['artifacts'].append(dict(id='performance8',bytes=len(image),symbols=symbols,bin_sha=sha(d/'program.bin'),ELF_sha=sha(d/'program.elf'),ELF_seed4=8,commands=records))
 save(H/'build-result.json',base);save(H/'IMAGE_DIFF.json',dict(status='ONLY_PARAMETER_WORD_BYTE_CHANGED',diffs=diffs,new_image_SHA256=sha(d/'program.bin'),old_image_SHA256=sha(R/'build/performance/program.bin')))
 print('One GNU build and auxiliary checks passed; actual ELF seed4=8; image differs by one byte; no DUT')
