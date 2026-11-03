"""Faithful baseline copies and explicit stage receipts, not tool execution."""
from pathlib import Path
import json,hashlib,shutil,sys,difflib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
OLD=P/'work/system/2026-10-24-soc-txgpio-m1/integration-0030-v1'
CM=P/'work/system/2026-10-23-coremark-correctness-m1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def copy(a,b):
    b.parent.mkdir(parents=True,exist_ok=True);assert not b.exists();shutil.copyfile(a,b);assert sha(a)==sha(b)
def main():
    assert read(OLD/'summary.json')['status']=='FINITE_SOFTWARE_SYSTEM_ACCEPTED_NOT_HARDWARE_OR_FINAL_PACKAGE'
    receipts=read(OLD/'source-receipts.json');protected={}
    for x in receipts:
        src=OLD/'source'/x['copy'];assert sha(src)==x['sha256']==sha(x['original'])
        protected[str(src)]=sha(src);protected[x['original']]=x['sha256']
        copy(src,H/'source-before'/x['copy'])
        if x['copy'] not in ['soc_top.sv','soc_data_adapter.sv','init_tables.svh','tb_soc_txgpio_m1.sv','tb_wrapper.sv']:
            copy(src,H/'source'/x['copy'])
    for n in ['start.S','link.ld']:copy(OLD.parent/'firmware'/n,H/'firmware'/n)
    for n in ['cpu_program_reference.py','peripheral_checker.py']:
        copy(OLD.parent/n,H/'models-before'/n)
        if n=='peripheral_checker.py':copy(OLD.parent/n,H/n)
    copy(CM/'port/core_portme.c',H/'port-before/core_portme.c');copy(CM/'port/core_portme.h',H/'port-before/core_portme.h')
    copy(CM/'port/core_portme.h',H/'port/core_portme.h')
    for p in (CM/'upstream-direct/files').glob('*.c'):copy(p,H/'upstream'/p.name)
    copy(CM/'upstream-direct/files/coremark.h',H/'upstream/coremark.h')
    for p in (H/'upstream').iterdir():protected[str(CM/'upstream-direct/files'/p.name)]=sha(p)
    for folder in ['build','logs','compile','cases','runs']: (H/folder).mkdir()
    protected[str(OLD/'summary.json')]=sha(OLD/'summary.json')
    protected[str(OLD.parent/'build/soc.bin')]=sha(OLD.parent/'build/soc.bin')
    protected[str(OLD.parent/'build/soc.elf')]=sha(OLD.parent/'build/soc.elf')
    for p in (H/'port-before').iterdir():protected[str(CM/'port'/p.name)]=sha(p)
    save(H/'protected-originals.json',dict(files=[dict(path=p,sha256=s) for p,s in sorted(protected.items())]))
    save(H/'manual-plan.json',dict(authorization='D123',date='2026-10-24',before_DUT=True,
      baseline=dict(N=[16,234],expected='identical F134 full RF/RAM/ordered events/stall/flush'),
      smoke=dict(N=16,checksum=528,signature=0x54494d31,UART=list(b'TIM1\r\n'),main_return=0,
        timestamps='four strictly increasing actual LOAD low-word sample times',delta='exact independent physical-edge differences',stall_flush='independent instruction oracle, not historical counter'),
      coremark=dict(N=16,iterations=1,total_data_size=2000,frequency_setting_hz=27000000,formal_score=False,
        performance=dict(seedcrc=0xe9f5,crclist=0xe714,crcmatrix=0x1fd7,crcstate=0x8e3a),
        validation=dict(seedcrc=0x18f2,crclist=0xe3c1,crcmatrix=0x0747,crcstate=0x8d84),
        output='all RAM report bytes after computation, including <10s validity failure'),
      budgets=dict(compile_seconds=90,small_run_seconds=45,coremark_run_seconds=240,physical_cycles=10000000,
        trace_bytes=256*1024*1024,bus_bytes=128*1024*1024,wave_bytes=128*1024*1024,stdout_read_bytes=8*1024*1024),
      hardware='STOP'))
    print('Protected originals; copied whole F134 group, fixed official algorithms, original port/TB/model; plan frozen before DUT.')
if __name__=='__main__':main()
