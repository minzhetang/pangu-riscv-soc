"""Mainline-owned runner: no incoming Python/VVP/PYC execution.
Fixed four compiles require a separate permission grant; ordinary DUT runs only
after frozen hash and native compile checks, unique outputs, bounded execution.
"""
from pathlib import Path
import sys,json,importlib.util,ctypes,re,shutil
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;STAGE=H.parent;P=STAGE.parents[2]
sys.path.insert(0,str(STAGE))
import build_prepare as b
import check_system
s=b.s;s.HERE=H
VENDOR=Path('D:/PDS/PDS_2022.2-SP6.4/arch/vendor/pango/verilog/simulation')
SRC=P/'队员成果接收/increment-20261024-0030'
ROOTS=[P/'队员成果接收'/n for n in ['stage-return-20261023-1345','increment-20261023-1740','increment-20261023-1930','increment-20261024-0030']]
def inherited(rel):
    for root in reversed(ROOTS):
        p=root/rel
        if p.exists():return p
    raise FileNotFoundError(rel)
def save(p,o):s.save(p,o)
def read(p):return s.read(p)
def frozen():
    files=read(H/'frozen.json')['files'];assert all(s.sha(r['path'])==r['sha256'] for r in files)
    return len(files)
def prepare():
    for r in read(STAGE/'preparation-frozen.json')['files']:assert s.sha(r['path'])==r['sha256']
    sources={n:STAGE/'source'/n for n in ['cpu.v','alu.v','control.v','regfile.v','memory_model.sv','soc_data_adapter.sv','soc_top.sv','init_tables.svh']}
    sources.update({'local_regif_txgpio_m1.v':SRC/'work/regif/txgpio-m1/src/local_regif_txgpio_m1.v',
        'uart_tx.v':inherited('work/peripherals/src/uart_tx.v'),
        'gpio_core.v':inherited('work/peripherals/gpio/src/gpio_core.v'),
        'tb_wrapper.sv':SRC/'work/regif/txgpio-m1/tb/tb_local_regif_txgpio_m1.sv',
        'tb_soc_txgpio_m1.sv':STAGE/'tests/tb_soc_txgpio_m1.sv'})
    for name,path in sources.items():
        dest=H/'source'/name;assert not dest.exists();shutil.copyfile(path,dest);assert s.sha(path)==s.sha(dest)
    save(H/'source-receipts.json',[dict(copy=name,original=str(path),sha256=s.sha(path)) for name,path in sources.items()])
    targets=[]
    for kind in ['wrapper','system']:
        for n in [16,234]:
            names=['local_regif_txgpio_m1.v','uart_tx.v','gpio_core.v']
            if kind=='wrapper':
                top='tb_local_regif_txgpio_m1';names+=['tb_wrapper.sv'];params=[f'-DCLKS_PER_BIT={n}','-DTB_MAX_CYCLES=300000']
                extra=[]
            else:
                top='tb_soc_txgpio_m1';names+=['cpu.v','alu.v','control.v','regfile.v','memory_model.sv','soc_data_adapter.sv','soc_top.sv','tb_soc_txgpio_m1.sv']
                params=[f'-Ptb_soc_txgpio_m1.N={n}',
                    '-DB_GPIO_ACCEPT_PATH=tb_soc_txgpio_m1.dut.peripherals.u_gpio.gpio_wr_en']
                extra=[VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v']
            tid=f'{kind}-N{n}';output=H/'compile'/(tid+'.vvp')
            argv=[s.IVL,'-B',s.LIB,'-g2012','-Wall','-I',H/'source','-s',top,*params,'-o',output,*[H/'source'/x for x in names],*extra]
            targets.append(dict(id=tid,argv=list(map(str,argv)),output=str(output)))
    save(H/'compile-plan.json',dict(maximum=4,timeout=60,fail_fast=True,only_compile=True,targets=targets))
    files={Path(r['path']) for r in read(STAGE/'preparation-frozen.json')['files']}
    files.update(p for p in SRC.rglob('*') if p.is_file())
    files.update(sources.values());files.update(p for p in H.rglob('*') if p.is_file())
    files.update([s.IVL,s.VVP,VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v'])
    files.update(STAGE/n for n in ['manual-expectations.json','peripheral_checker.py','cpu_program_reference.py','check_system.py','firmware-artifacts.json','build/soc.bin','build/soc.elf'])
    save(H/'frozen.json',dict(files=[dict(path=str(p),sha256=s.sha(p)) for p in sorted(files)]))
    print('Prepared four fixed compiles; actual GPIO CORE input enable reviewed/bound; CPU/B unmodified')
def compile_all():
    frozen();assert not ctypes.windll.shell32.IsUserAnAdmin();save(H/'compile-attempt.json',dict(maximum=4,non_admin=True))
    rows=[]
    for t in read(H/'compile-plan.json')['targets']:
        r=s.bounded(t['argv'],H,'compile-'+t['id'],60)
        ok=r['returncode']==0 and not r['timed_out'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if ok else 'FAIL',process=r,output=t['output'],sha256=s.sha(t['output']) if Path(t['output']).exists() else None))
        if not ok:break
    save(H/'compile-result.json',dict(status='ALL_COMPILED_NOT_SIMULATED' if len(rows)==4 and all(r['status']=='PASS' for r in rows) else 'STOPPED',rows=rows,protected=frozen()))
    print([(r['id'],r['status']) for r in rows])
def run():
    frozen();compiled=read(H/'compile-result.json');assert compiled['status']=='ALL_COMPILED_NOT_SIMULATED'
    assert all(s.sha(r['output'])==r['sha256'] for r in compiled['rows'])
    rows=[]
    for t in compiled['rows']:
        name=t['id'];kind,n=name.split('-N');n=int(n);d=H/'runs'/name;d.mkdir()
        args=['+WAVE_FILE=wave.vcd'] if kind=='wrapper' else ['+MAX_CYCLES=100000']
        r=s.bounded([s.VVP,'-N','-M-','-M'+str(s.LIB),t['output'],*args],d,'run-'+name,30)
        raw=s.text_log(r['stdout']);row=dict(id=name,process=r,status='FAIL')
        if r['returncode']==0 and not r['timed_out']:
            if kind=='wrapper':
                expected=[f'W{i:02d}' for i in range(1,11)] if n==16 else [f'W{i:02d}-N234' for i in [5,6,9]]
                actual=re.findall(r'^TEST_PASS (W\d\d(?:-N234)?)$',raw,re.M)
                counts=re.findall(r'REGIF_M1_SELFCHECK_PASS accepted_tx=(\d+) accepted_gpio=(\d+) rejected=(\d+) frames=(\d+)',raw)
                ok=actual==expected and counts==([('9','6','10','6')] if n==16 else [('9','0','1','6')]) and not any(x in raw for x in ['CHK_FAIL','TEST_FAIL','WATCHDOG_TIMEOUT'])
                row.update(status='PASS_LIMITED_ORIGINAL_TB' if ok else 'FAIL',expected_case_markers=expected,actual_case_markers=actual,
                    caveat='fresh original TB execution, NOT closure of counter/negative-checker gaps')
            else:
                shutil.copyfile(r['stdout'],d/'stdout.log');assert s.sha(r['stdout'])==s.sha(d/'stdout.log')
                try:check=check_system.check(d,n)
                except Exception as e:check=dict(status='CHECKER_ERROR',error=repr(e))
                save(d/'checker-result.json',check);row.update(status=check['status'],checker=check)
        save(d/'result.json',row);rows.append(row);print(name,row['status'],row.get('checker',{}).get('errors',row.get('checker',{}).get('error')),flush=True)
        if row['status'] not in ['PASS','PASS_LIMITED_ORIGINAL_TB']:break
    save(H/'result.json',dict(status='PASS_LIMITED_SYSTEM' if len(rows)==4 and all(r['status'] in ['PASS','PASS_LIMITED_ORIGINAL_TB'] for r in rows) else 'NOT_ACCEPTED',
        cases=rows,protected=frozen(),no_CPU_or_B_RTL_changes=True,hardware='STOP'))
if __name__=='__main__':{'prepare':prepare,'compile':compile_all,'run':run,'verify':lambda:print(frozen())}[sys.argv[1]]()
