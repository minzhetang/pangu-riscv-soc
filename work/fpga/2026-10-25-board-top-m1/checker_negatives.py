"""Corrupt isolated evidence copies only; no new DUT/tool executions."""
from pathlib import Path
import importlib.util,json,shutil,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H));import stage_board as s;import check_board as ck
names=['process.json','stdout.log','trace.log','bus.log','registers.hex','ram.hex']
src=H/'runs/board5-N234';before={n:s.sha(src/n) for n in names};out=H/'checker-negative';out.mkdir()
rows=[]
for case in ['control','wrong_WB','duplicate_WB','missing_GPIO_STORE','UART_pin_error','GPIO_mapping_error','x0_error','RAM_signature_error','process_failure']:
    root=out/case;d=root/'runs/board5-N234';d.mkdir(parents=True)
    for n in names:shutil.copyfile(src/n,d/n)
    for n in ['manual-plan.json','firmware-result.json']:shutil.copyfile(H/n,root/n)
    if case in ['wrong_WB','duplicate_WB','missing_GPIO_STORE']:
        p=d/'trace.log';lines=p.read_text().splitlines();i=next(i for i,l in enumerate(lines) if l.startswith('WB|'))
        if case=='wrong_WB':
            a=lines[i].split('|');a[-1]=f'{int(a[-1],16)^1:08x}';lines[i]='|'.join(a)
        elif case=='duplicate_WB':lines.insert(i+1,lines[i])
        else:
            j=next(i for i,l in enumerate(lines) if l.startswith('STORE|') and l.split('|')[3]=='2000000c');lines.pop(j)
        p.write_text('\n'.join(lines)+'\n',encoding='ascii')
    elif case in ['UART_pin_error','GPIO_mapping_error']:
        p=d/'bus.log';lines=p.read_text().splitlines()
        i=next(i for i,l in enumerate(lines) if l.split('|')[9]=='0') if case=='UART_pin_error' else 0
        a=lines[i].split('|')
        if case=='UART_pin_error':a[11]=str(int(a[11])^1)
        else:a[2]=f'{int(a[2],16)^1:02x}'
        lines[i]='|'.join(a);p.write_text('\n'.join(lines)+'\n',encoding='ascii')
    elif case=='x0_error':
        p=d/'registers.hex';lines=p.read_text().splitlines();assert lines[0]=='00000000';lines[0]='00000001';p.write_text('\n'.join(lines)+'\n',encoding='ascii')
    elif case=='RAM_signature_error':
        p=d/'ram.hex';lines=p.read_text().splitlines();addr=s.read(H/'firmware-result.json')['symbols']['signature']-0x10000
        lines[addr]=f'{int(lines[addr],16)^1:02x}';p.write_text('\n'.join(lines)+'\n',encoding='ascii')
    elif case=='process_failure':
        p=d/'process.json';r=s.read(p);r['returncode']=1;p.write_text(json.dumps(r),encoding='utf-8')
    ck.H=root
    try:
        result=ck.check('board5-N234');accepted=result['status']=='PASS';detail=result.get('errors',[])[:2]
    except AssertionError as error:accepted=False;detail=str(error)[:250]
    assert accepted==(case=='control'),(case,detail)
    rows.append(dict(case=case,status='CONTROL_PASS' if accepted else 'EXPECTED_REJECTION',detail=detail))
ck.H=H
assert before=={n:s.sha(src/n) for n in names}
s.save(H/'checker-negative-result.json',dict(status='PASS',rows=rows,control=1,negative=8,new_DUT_runs=0,original_evidence_unchanged=True,protected=s.protect()))
print('checker control + 8 corruption rejections passed; original evidence unchanged; 0 new DUT')
