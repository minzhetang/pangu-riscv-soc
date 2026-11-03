"""Corrupt derived evidence only; no new DUT runs and no expectation changes."""
from pathlib import Path
import json,shutil,sys
sys.dont_write_bytecode=True
import run_stage as s
import check_timed as ck
H=Path(__file__).resolve().parent
def main():
    source=H/'runs/smoke-N16';assert s.read(source/'check-result.json')['status']=='PASS'
    inputs=['trace.log','bus.log','ram.hex','registers.hex','stdout.log','process.json']
    before={n:s.sha(source/n) for n in inputs};results=[]
    for name in ['control','post_edge_tick_alias','frozen_counter','wrong_high_word','wrong_LOAD_result','duplicate_WB','missing_STORE','extra_GPIO_accept','unknown_pin']:
        root=H/'checker-negatives'/name;d=root/'runs/smoke-N16';d.mkdir(parents=True)
        shutil.copyfile(H/'build-result.json',root/'build-result.json');(root/'build/smoke').mkdir(parents=True)
        shutil.copyfile(H/'build/smoke/program.bin',root/'build/smoke/program.bin')
        for n in inputs:shutil.copyfile(source/n,d/n)
        if name in ['post_edge_tick_alias','frozen_counter','wrong_high_word','extra_GPIO_accept','unknown_pin']:
            p=d/'bus.log';lines=p.read_text().splitlines()
            for i,line in enumerate(lines):
                a=line.split('|');addr=int(a[3],16)
                if name=='extra_GPIO_accept':a[13]='1'
                elif name=='unknown_pin':a[11]='x'
                elif name=='frozen_counter' and int(a[15],16)>0:a[15]='0000000000000000'
                elif name=='post_edge_tick_alias' and addr==0x20000100:a[7]=f'{int(a[1]):08x}'
                elif name=='wrong_high_word' and addr==0x20000104:a[7]=f'{int(a[1])-1:08x}'
                else:continue
                lines[i]='|'.join(a);break
            else:raise AssertionError('negative mutation not applied')
            p.write_text('\n'.join(lines)+'\n')
        elif name in ['duplicate_WB','missing_STORE','wrong_LOAD_result']:
            p=d/'trace.log';lines=p.read_text().splitlines()
            for i,line in enumerate(lines):
                a=line.split('|')
                if name=='duplicate_WB' and a[0]=='WB':lines.insert(i,line);break
                if name=='missing_STORE' and a[0]=='STORE':del lines[i];break
                if name=='wrong_LOAD_result' and a[0]=='READ' and a[3]=='20000100':
                    a[4]=a[5]=f'{(int(a[4],16)+1)&0xffffffff:08x}';lines[i]='|'.join(a);break
            else:raise AssertionError('negative mutation not applied')
            p.write_text('\n'.join(lines)+'\n')
        ck.H=root
        try:r=ck.check('smoke-N16');actual=r['status'];detail=r['errors'][:1]
        except (AssertionError,ValueError,KeyError) as e:actual='REJECTED_INPUT_VALIDATION';detail=[str(e)]
        finally:ck.H=H
        ok=actual=='PASS' if name=='control' else actual!='PASS'
        results.append(dict(id=name,status='PASS' if ok else 'FAIL',actual_checker_status=actual,detail=detail,DUT_runs=0))
    assert all(s.sha(source/n)==v for n,v in before.items())
    result=dict(status='PASS' if all(x['status']=='PASS' for x in results) else 'FAIL',cases=results,original_SHA_unchanged=before,new_DUT_runs=0)
    s.save(H/'checker-negative-result.json',result);print(json.dumps(result))
if __name__=='__main__':main()
