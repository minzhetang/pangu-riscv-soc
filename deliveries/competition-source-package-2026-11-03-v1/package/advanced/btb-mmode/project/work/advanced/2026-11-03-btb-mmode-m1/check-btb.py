from execute import *
vvp=H/'btb-unit.vvp';d=H/'runs/btb-unit';d.mkdir(parents=True,exist_ok=False)
rc=run('compile-btb-unit',[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','btb_tb','-o',vvp,H/'source/btb.v',H/'btb_tb.sv'],H,35)
if rc:raise SystemExit(1)
rc=run('run-btb-unit',[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp],d,10)
log=(H/'logs/run-btb-unit.log').read_text()
result=dict(status='PASS' if rc==0 and 'BTB_MODULE_PASS checks=12' in log else 'FAIL',checks=12,scope='Re-run of inherited finite BTB unit test on current candidate source; not CPU or ISA acceptance')
(H/'BTB_UNIT_RESULT.json').write_text(json.dumps(result,indent=2));print(result)
