"""Ordinary builds only. No simulator and no outside-sandbox execution."""
import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import time
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
UP=HERE/'upstream-direct/files'
OLD=ROOT/'work/system/2026-10-23-c-boot-m1'
GCC=ROOT/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
NAMES=['alu.v','control.v','cpu.v','regfile.v']
HASHES=['6393472BC3635DA83213E0E9883766D5076C37EA60319F32F1DE5C420F68065E',
        '23CDBDFDD45DD60D6C7D95A13CC51927999A640FE5E30CAF8D324FA91AA87067',
        '555CB51AC20FFC439B61BB29D4F4D9F4DC02C38B54A37291A79519CD413B8114',
        'AE36F070B994EEF41AF1636516D737EDA240C2A18AF83048ADC3E3E2391C8468']
FILES=['core_list_join.c','core_main.c','core_matrix.c','core_state.c','core_util.c','coremark.h']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(p,data): p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
def item(p): return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
def call(label,argv,cwd,limit=60):
    directory=cwd/label; directory.mkdir(exist_ok=False)
    save(directory/'request.json',{'argv':list(map(str,argv)),'cwd':str(cwd),'timeout_seconds':limit,'ordinary':True})
    start=time.monotonic()
    try:
        p=subprocess.run(list(map(str,argv)),cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=limit,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        result={'exit_code':p.returncode,'timed_out':False}; out,err=p.stdout,p.stderr
    except subprocess.TimeoutExpired as exc:
        result={'exit_code':None,'timed_out':True}; out,err=exc.stdout or b'',exc.stderr or b''
    (directory/'stdout.log').write_bytes(out); (directory/'stderr.log').write_bytes(err)
    result['elapsed_seconds']=round(time.monotonic()-start,6); save(directory/'process.json',result)
    assert result['exit_code']==0 and not result['timed_out'], (label,result)
    return out.decode('utf-8',errors='replace')

def prepare():
    assert not (HERE/'protected-before.json').exists(), 'Do not overwrite existing stage'
    # Diagnose the exact upstream stale-checksum issue without editing the source.
    archive=HERE/'upstream-direct/source.zip'
    prefix='coremark-1f483d5b8316753a742cbf5590caf5bd0a4e4777/'
    z=zipfile.ZipFile(archive)
    verified=[]
    for p in UP.rglob('*'):
        if p.is_file():
            assert p.read_bytes()==z.read(prefix+p.relative_to(UP).as_posix())
            verified.append(item(p))
    for line in (UP/'coremark.md5').read_text().splitlines():
        expected,name=line.split(); data=(UP/name).read_bytes()
        if name=='coremark.h':
            assert data.count(b'multithread specific')==1
            assert hashlib.md5(data.replace(b'multithread specific',b'ultithread specific')).hexdigest()==expected
        else: assert hashlib.md5(data).hexdigest()==expected
    save(HERE/'source-integrity-review.json',{
        'status':'FIXED_SOURCE_VERIFIED_UPSTREAM_MANIFEST_STALE_HEADER_COMMENT',
        'archive_sha256':sha(archive),'verified_local_vs_archive':verified,
        'all_12_archive_vs_official_raw_checks_completed_before_fetch_direct_MD5_assertion':True,
        'five_C_MD5':'MATCH','header_current_MD5':hashlib.md5((UP/'coremark.h').read_bytes()).hexdigest(),
        'header_expected_pre_comment_MD5':'8ca974c013b380dc7f0d6d1afb76eb2d',
        'official_change':'https://github.com/eembc/coremark/commit/1f483d5b8316753a742cbf5590caf5bd0a4e4777',
        'source_modified':False,'failed_fetch_receipts_preserved':True})
    protected=[OLD/'source'/n for n in NAMES]+[OLD/n for n in ['tb_c_boot.sv','memory_model.sv','check_c_boot.py','result-after-external.json','wave-review.json']]
    protected += list((OLD/'inputs').glob('*'))
    protected += [ROOT/'work/icarus/2026-10-21-cpu-shifti-reject/runs-v2/result.json',
                  ROOT/'work/icarus/2026-10-21-cpu-shifti-reject/validation-v2/plan.json']
    for directory in ['source','source-before']:
        (HERE/directory).mkdir(exist_ok=False)
        for name,h in zip(NAMES,HASHES):
            assert sha(OLD/'source'/name)==h
            shutil.copy2(OLD/'source'/name,HERE/directory/name)
            assert sha(HERE/directory/name)==h
    shutil.copy2(OLD/'inputs/start.S',HERE/'start.S')
    save(HERE/'protected-before.json',[item(p) for p in protected]+verified)
    save(HERE/'manual-plan.json',{
        'stage':'A-COREMARK-CORRECTNESS-M1','authorized':'2026-10-23 user continuation directly following explicit single-phase proposal',
        'created_before_DUT':datetime.datetime.now().astimezone().isoformat(),
        'upstream_commit':'1f483d5b8316753a742cbf5590caf5bd0a4e4777',
        'cases':{
            'performance':{'seeds':[0,0,102],'seedcrc':'e9f5','crclist':'e714','crcmatrix':'1fd7','crcstate':'8e3a'},
            'validation':{'seeds':[13333,13333,102],'seedcrc':'18f2','crclist':'e3c1','crcmatrix':'0747','crcstate':'8d84'}},
        'iterations':1,'total_data_size':2000,'all_algorithms':7,'CPU_modified':False,
        'initial_RF':'existing initial zeros','RAM_poison':'a5','clock':'1ns/1ps, period10ns verification-only',
        'ROM_capacity':32768,'RAM_base':65536,'RAM_capacity':32768,'stack_reserved':8192,
        'timing':'UNAVAILABLE; get_time=0, expected upstream duration error retained, NO official score',
        'acceptance':'three official CRCs + params + exact golden RF/RAM/WB/RW/EX streams, no dedup, X/bounds/stop guards',
        'limits':{'reference_steps':5000000,'cycles':10000000,'compile_seconds':60,'run_seconds':180},
        'excluded':'CPU changes, new ISA, production MMIO/timer/peripherals/BRAM, new software, hardware'})

def build():
    for case in ['performance','validation']:
        out=HERE/case; out.mkdir(exist_ok=False)
        flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie',
               '-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0',
               '-Wall','-Wextra','-Wno-unused-parameter','-Wno-unused-variable','-nostdlib','-nostartfiles',
               '-DTOTAL_DATA_SIZE=2000','-DITERATIONS=1',f'-D{case.upper()}_RUN=1',
               '-I'+str(HERE/'port'),'-I'+str(UP),'-Wl,--no-relax','-Wl,--build-id=none',
               '-Wl,-T,'+str(HERE/'coremark.ld'),'-Wl,-Map,'+str(out/'coremark.map')]
        args=[GCC/'riscv-none-elf-gcc.exe']+flags+['-o',out/'coremark.elf',HERE/'start.S']
        args += [UP/n for n in FILES if n.endswith('.c')]+[HERE/'port/core_portme.c','-lgcc']
        call('compile',args,out)
        call('readelf',[GCC/'riscv-none-elf-readelf.exe','-h','-A','-l','-sW',out/'coremark.elf'],out,20)
        call('objdump',[GCC/'riscv-none-elf-objdump.exe','-d','-M','no-aliases',out/'coremark.elf'],out,20)
        undefined=call('undefined',[GCC/'riscv-none-elf-nm.exe','-u',out/'coremark.elf'],out,20)
        assert not undefined.strip()
        call('objcopy',[GCC/'riscv-none-elf-objcopy.exe','-O','binary',out/'coremark.elf',out/'coremark.bin'],out,20)
        image=(out/'coremark.bin').read_bytes(); assert 0<len(image)<=32768
        padded=image+bytes((-len(image))%4)
        (out/'image.hex').write_text(''.join(f'{int.from_bytes(padded[i:i+4],"little"):08x}\n' for i in range(0,len(padded),4)),encoding='ascii')
        save(out/'image-receipt.json',{'bytes':len(image),'words':len(padded)//4,'bin_sha256':sha(out/'coremark.bin'),'ELF_sha256':sha(out/'coremark.elf')})
    verify()

def verify():
    records=json.loads((HERE/'protected-before.json').read_text(encoding='utf-8'))
    changed=[r['path'] for r in records if sha(Path(r['path']))!=r['sha256']]
    assert not changed,changed
    for name,h in zip(NAMES,HASHES):
        assert sha(HERE/'source'/name)==sha(HERE/'source-before'/name)==h
    save(HERE/'postflight.json',{'protected_count':len(records),'changed':changed,'CPU_group_matches':True})

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['prepare','build','verify'])
    globals()[p.parse_args().action]()
