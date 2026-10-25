"""Fixed seven rebuilt final-stage peripheral tests, no received Python execution."""
from review import *
import subprocess,ctypes,time,shutil
W=P/'work/peripheral-review/2026-10-25-stage-final-v02'
TOOLS=P/'tools/iverilog-13.0-msys2-ucrt64/ucrt64';IVL=TOOLS/'bin/iverilog.exe';VVP=TOOLS/'bin/vvp.exe';LIB=TOOLS/'lib/ivl'
def prepare():
    W.mkdir(exist_ok=False)
    for n in ['source','tests','build','logs']:(W/n).mkdir()
    rels=['work/regif/txgpio-m1/src/local_regif_txgpio_m1.v','work/peripherals/src/uart_tx.v','work/peripherals/gpio/src/gpio_core.v','work/peripherals/rx/src/uart_rx.v','work/peripherals/rx/tb/rx_ledger_check.svh','work/peripherals/rx/tb/rx_public_capture.sv','work/peripherals/rx/tb/tb_uart_rx.sv','work/peripherals/rx/tb/tb_uart_rx_neg.sv','work/regif/txgpio-m1/tb/tb_local_regif_txgpio_m1.sv','work/regif/txgpio-m1/tb/regif_tx_public_monitor.sv','work/regif/txgpio-m1/tb/tb_regif_tx_capture_neg.sv']
    inputs=[]
    for rel in rels:
        p=resolve(rel);dst=W/'source'/p.name;shutil.copyfile(p,dst);assert sha(p)==sha(dst)
        assert not re.search(r'\$(?:system|fopen|readmem|fwrite|fscanf|popen)\b',dst.read_text(encoding='utf-8-sig'))
        inputs.append(dict(original=str(p),copy=str(dst),SHA256=sha(p)))
    obs=W/'tests/review_rx_dump.sv'
    obs.write_text('''`timescale 1ns/1ps
module review_rx_dump;
integer k;
final begin
 for(k=0;k<tb_uart_rx.rx_cap.count;k=k+1)
  $display("A_SHARED_RX seq=%0d type=%0d data=%02x edge=%0d",k,tb_uart_rx.rx_cap.etype[k],tb_uart_rx.rx_cap.edata[k],tb_uart_rx.rx_cap.eedge[k]);
end
endmodule
''',encoding='utf-8')
    targets=[]
    for ident,n,top,names,budget in [('wrap16',16,'tb_local_regif_txgpio_m1',['local_regif_txgpio_m1.v','uart_tx.v','gpio_core.v','regif_tx_public_monitor.sv','tb_local_regif_txgpio_m1.sv'],300000),('wrap234',234,'tb_local_regif_txgpio_m1',['local_regif_txgpio_m1.v','uart_tx.v','gpio_core.v','regif_tx_public_monitor.sv','tb_local_regif_txgpio_m1.sv'],300000),('rx8',8,'tb_uart_rx',['uart_rx.v','rx_public_capture.sv','tb_uart_rx.sv'],5045),('rx16',16,'tb_uart_rx',['uart_rx.v','rx_public_capture.sv','tb_uart_rx.sv'],11319),('rx234',234,'tb_uart_rx',['uart_rx.v','rx_public_capture.sv','tb_uart_rx.sv'],110967),('rxneg',16,'tb_uart_rx_neg',['uart_rx.v','rx_public_capture.sv','tb_uart_rx_neg.sv'],20000),('txcap',16,'tb_regif_tx_capture_neg',['regif_tx_public_monitor.sv','tb_regif_tx_capture_neg.sv'],20000)]:
        argv=[str(IVL),'-B',str(LIB),'-g2012','-Wall','-s',top,f'-DCLKS_PER_BIT={n}',f'-DTB_MAX_CYCLES={budget}','-I',str(W/'source'),'-o',str(W/'build'/(ident+'.vvp'))]
        if ident in ['rx8','rx16','rx234']:argv+=['-s','review_rx_dump']
        argv += [str(W/'source'/name) for name in names]
        if ident in ['rx8','rx16','rx234']:argv.append(str(obs))
        targets.append(dict(id=ident,N=n,argv=argv,output=str(W/'build'/(ident+'.vvp')),budget=budget))
    save(W/'plan.json',dict(targets=targets,inputs=inputs,observer=dict(path=str(obs),SHA256=sha(obs),signal_writes=False),compile_timeout_s=60,run_timeout_s=30,maximum_compiles=7,hardware=False,core_or_received_TB_changes=False))
    print('Prepared seven scoped source builds, zero compiler/DUT runs')
def protect():
    plan=read(W/'plan.json')
    for x in plan['inputs']:assert sha(x['original'])==sha(x['copy'])==x['SHA256']
    assert sha(plan['observer']['path'])==plan['observer']['SHA256']
    return plan
def bounded(argv,ident,limit):
    d=W/'logs'/ident;d.mkdir(exist_ok=False);start=time.monotonic();expired=False
    with (d/'stdout.log').open('xb') as out,(d/'stderr.log').open('xb') as err:
        proc=subprocess.Popen(list(map(str,argv)),cwd=W,stdin=subprocess.DEVNULL,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        try:rc=proc.wait(timeout=limit)
        except subprocess.TimeoutExpired:
            expired=True;proc.kill();rc=proc.wait(timeout=2)
    r=dict(argv=list(map(str,argv)),cwd=str(W),returncode=rc,hex=f'0x{rc&0xffffffff:08X}',timed_out=expired,timeout_s=limit,duration_s=round(time.monotonic()-start,6),stdout=str(d/'stdout.log'),stderr=str(d/'stderr.log'),log_truncated=False,cleanup='NOT_NEEDED' if not expired else 'PARENT_KILL_NOT_A_SUCCESS_OR_TREE_PROOF')
    save(d/'process.json',r);return r
def compile_batch():
    assert not ctypes.windll.shell32.IsUserAnAdmin();plan=protect();rows=[]
    for t in plan['targets']:
        r=bounded(t['argv'],'compile-'+t['id'],60);ok=r['returncode']==0 and not r['timed_out'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],process=r,ok=ok,VVP_SHA256=sha(t['output']) if ok else None));print(t['id'],r['hex'],flush=True)
        if not ok:break
    save(W/'compile.json',dict(rows=rows,all_compiled=len(rows)==7 and all(x['ok'] for x in rows),new_DUT=0));protect()
def run():
    plan=protect();compiled=read(W/'compile.json');assert compiled['all_compiled'];rows=[]
    for t,c in zip(plan['targets'],compiled['rows']):
        assert sha(t['output'])==c['VVP_SHA256']
        r=bounded([VVP,'-N','-M-','-M'+str(LIB),t['output'],'+WAVE_FILE='+(W/'build'/(t['id']+'.vcd')).as_posix()],'run-'+t['id'],30)
        rows.append(dict(id=t['id'],N=t['N'],process=r));print(t['id'],r['hex'],flush=True)
        if r['returncode'] or r['timed_out']:break
    save(W/'run.json',dict(rows=rows,new_DUT=len(rows),CPU_CoreMark_PDS_runs=0,hardware=False));protect()
if __name__=='__main__':dict(prepare=prepare,compile=compile_batch,run=run)[sys.argv[1]]()
