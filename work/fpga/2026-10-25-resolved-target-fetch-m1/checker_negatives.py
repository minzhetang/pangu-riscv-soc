"""Tamper copies of actual small-run evidence; never change DUT input or expected."""
from pathlib import Path
import sys,shutil
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_redirect as s;import check_redirect_v2 as ck
def main():
    s.protect();root=H/'checker-negative';root.mkdir();plan=s.read(H/'manual-plan.json')['cases'];rows=[]
    for name in ['two_digit_control','wrong_RAM_byte','duplicate_WB','wrong_IFID_tag','missing_reset_cancel']:
        reset=name=='missing_reset_cancel';cid='reset-between-request-apply' if reset else 'beq-taken';case=next(c for c in plan if c['id']==cid);src=H/'runs'/(cid+'-PF1');d=root/name;d.mkdir()
        for f in ['stdout.log','trace.log','fetch.log','registers.hex','ram.hex']:shutil.copyfile(src/f,d/f)
        if name=='two_digit_control':
            p=d/'ram.hex';p.write_text(''.join(f'{int(v,16):02x}\n' for v in p.read_text().split()),encoding='ascii')
        elif name=='wrong_RAM_byte':
            p=d/'ram.hex';v=p.read_text().splitlines();v[0]=f'{int(v[0],16)^1:08x}';p.write_text('\n'.join(v)+'\n',encoding='ascii')
        elif name=='duplicate_WB':
            p=d/'trace.log';v=p.read_text().splitlines();i=next(i for i,l in enumerate(v) if l.startswith('WB|'));v.insert(i+1,v[i]);p.write_text('\n'.join(v)+'\n',encoding='ascii')
        elif name=='wrong_IFID_tag':
            p=d/'fetch.log';v=p.read_text().splitlines();i=next(i for i,l in enumerate(v) if l.startswith('APPLY|'));a=v[i].split('|');a[7]=f'{int(a[7],16)^4:08x}';v[i]='|'.join(a);p.write_text('\n'.join(v)+'\n',encoding='ascii')
        else:
            p=d/'fetch.log';p.write_text(''.join(l+'\n' for l in p.read_text().splitlines() if not l.startswith('RESET|')),encoding='ascii')
        try:result=ck.check(case,1,d);passed=result['status']=='PASS';detail=result.get('errors',[])
        except (AssertionError,ValueError) as e:passed=False;detail=repr(e)
        assert passed==(name=='two_digit_control'),name
        rows.append(dict(id=name,status='PASS_CONTROL' if passed else 'EXPECTED_REJECTION',detail=detail,new_DUT_runs=0))
    s.save(H/'checker-negative-result.json',dict(status='PASS',positive=1,negative=4,rows=rows,new_DUT_runs=0,protected=s.protect()));print('Byte-format control + 4 actual-evidence tamper probes PASS, 0 new DUT')
if __name__=='__main__':main()
