"""Mutate NEW derived observation fixtures only, never original logs or expected.
No DUT execution. Exercises live checker on real positive trace and targeted
missing/extra/wrong observations. Native process acceptance is separate.
"""
from pathlib import Path
import sys,json,shutil
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent))
import check_system
import build_prepare as b
s=b.s
base=H/'runs/system-N16'
original={n:s.sha(base/n) for n in ['bus.log','trace.log','registers.hex','ram.hex','stdout.log']}
def run(name,mutate=None):
    d=H/'checker-fixtures'/name;d.mkdir(parents=True)
    for n in original:shutil.copyfile(base/n,d/n)
    if mutate:mutate(d)
    try:
        got=check_system.check(d,16);status=got['status'];detail=got.get('errors',[])[:4]
    except AssertionError as e:status='REJECTED_INPUT_VALIDATION';detail=[str(e)]
    passed=status=='PASS' if mutate is None else status in ['FAIL','REJECTED_INPUT_VALIDATION']
    return dict(id=name,selftest_status='PASS' if passed else 'FAIL',actual_checker_status=status,
        expected='PASS' if mutate is None else 'REJECT',detail=detail,DUT_runs=0)
def trace_edit(predicate,action):
    def edit(d):
        rows=(d/'trace.log').read_text(encoding='ascii').splitlines();i=next(i for i,r in enumerate(rows) if predicate(r))
        action(rows,i);(d/'trace.log').write_text('\n'.join(rows)+'\n',encoding='ascii')
    return edit
def bus_edit(predicate,field,value):
    def edit(d):
        rows=(d/'bus.log').read_text(encoding='ascii').splitlines();i=next(i for i,r in enumerate(rows) if predicate(r.split('|')))
        a=rows[i].split('|');a[field]=value(a[field]);rows[i]='|'.join(a)
        (d/'bus.log').write_text('\n'.join(rows)+'\n',encoding='ascii')
    return edit
rows=[run('correct_control'),
    run('extra_duplicate_WB',trace_edit(lambda r:r.startswith('WB|'),lambda a,i:a.insert(i,a[i]))),
    run('missing_STORE',trace_edit(lambda r:r.startswith('STORE|'),lambda a,i:a.pop(i))),
    run('wrong_WB',trace_edit(lambda r:r.startswith('WB|'),lambda a,i:a.__setitem__(i,a[i][:-1]+('1' if a[i][-1]!='1' else '2')))),
    run('wrong_UART_pin',bus_edit(lambda a:int(a[1])>1000,11,lambda x:'1' if x=='0' else '0')),
    run('extra_GPIO_accept',bus_edit(lambda a:a[13]=='0' and int(a[1])>100,13,lambda x:'1')),
    run('wrong_MMIO_read',bus_edit(lambda a:int(a[3],16)==0x20000008,7,lambda x:'00000002')),
    run('unknown_pin',bus_edit(lambda a:int(a[1])>100,11,lambda x:'x'))]
assert all(s.sha(base/n)==v for n,v in original.items())
out=dict(status='PASS' if all(r['selftest_status']=='PASS' for r in rows) else 'FAIL',cases=rows,
    source_original_SHA_unchanged=original,new_DUT_runs=0,scope='mainline live checker, derived corrupted evidence only')
s.save(H/'checker-negative-result.json',out)
print(json.dumps(dict(status=out['status'],cases=[(r['id'],r['actual_checker_status'],r['selftest_status']) for r in rows])))
