from pathlib import Path
import json,re,hashlib
from itertools import zip_longest
import stage_redirect as s
HERE=s.H;OLD=s.OLD
read,save,sha,bounded,extract=s.read,s.save,s.sha,s.bounded,s.extract
VVP=s.lib.VVP;LIB=s.lib.LIB
frozen=s.protect
def artifacts():return s.artifacts('initial')
def text_log(p):
    with Path(p).open('rb') as f:b=f.read(8*1024*1024+1)
    assert len(b)<=8*1024*1024,'stdout exceeds read cap'
    return b.decode('utf-8',errors='replace').replace('\r\n','\n')

def regress():
    assert read(HERE/'small-result.json')['status']=='PASS'
    paths=artifacts();plan=read(OLD/'validation-v2/plan.json');traces=read(OLD/'expected-traces.json')
    byid={c['id']:c for c in plan['cases']}
    compare=extract(OLD/'models/cpu_trace_oracle.py',{'compare'},{'re':re,'zip_longest':zip_longest})['compare']
    rows=[]
    for group in read(OLD/'compile-batch-plan.json')['requests']:
        for cid in group['case_ids']:
            case=byid[cid];directory=HERE/'runs/regression'/cid;directory.mkdir(parents=True,exist_ok=False)
            args=['+case='+cid,'+inputs='+(OLD/'cases'/cid).as_posix()]
            if 'expected_stop' in case:
                args+=['+stop_kind='+str((case['expected_stop'] or {}).get('kind',0)),'+stop_pc='+format((case['expected_stop'] or {}).get('pc',0),'x')]
                if case.get('reset_check'):args+=['+reset_check']
            proc=bounded([VVP,'-N','-M-','-M'+str(LIB),paths['regression-'+group['name']],*args],directory,'reg-'+cid,30)
            text=text_log(proc['stdout']);verdict=re.findall(r'^CASE_RESULT\|[^|]+\|(PASS|FAIL|TIMEOUT)$',text,re.M)
            check=compare(text,traces[cid],verdict[0] if len(verdict)==1 else 'FAIL')
            errors=[]
            if proc['returncode']!=0 or proc['timed_out'] or verdict!=['PASS'] or check['strict_status']!='PASS':errors.append('process/final/ordered trace')
            regs={int(i):v for i,v in re.findall(r'^REG\|(\d+)\|([0-9a-fxz]+)$',text,re.M)}
            mem={int(i):v for i,v in re.findall(r'^MEM\|(\d+)\|([0-9a-fxz]+)$',text,re.M)}
            if regs!={i:f'{v:08x}' for i,v in enumerate(case['expected_regs'])}:errors.append('RF')
            if mem!={i*4:f'{v:08x}' for i,v in enumerate(case['expected_mem'])}:errors.append('RAM')
            if 'PROTOCOL_ERROR|' in text:errors.append('protocol')
            ml=re.findall(r'^METRICS\|(.*)$',text,re.M);mt=dict(x.split('=',1) for x in ml[0].split('|')) if len(ml)==1 else {}
            metrics={}
            for key in ['stall','flush']:
                want=plan[key+'_expectations'].get(cid);actual=int(mt.get(key+'_cycles',-1))
                metrics[key]=dict(expected=want,actual=actual,status='NOT_SPECIFIED' if want is None else ('PASS' if want==actual else 'FAIL'))
                if want is not None and want!=actual:errors.append(key)
            # Frozen specialized load/bus/EEI/RAM events are checked too.
            for key,pattern,fields in [('loads',r'^READ\|cycle=(\d+)\|rd=(\d+)\|f3=(\d+)\|addr=([0-9a-f]{8})\|raw=([0-9a-f]{8})$',('rd','funct3','address','raw')),('bus_stores',r'^WSTORE\|cycle=(\d+)\|addr=([0-9a-f]{8})\|mask=([0-9a-f])\|data=([0-9a-f]{8})$',('address','mask','data'))]:
                if key in traces[cid]:
                    got=[dict(zip(fields,[int(v) if k in ('rd','funct3') else v for k,v in zip(fields,row[1:])])) for row in re.findall(pattern,text,re.M)]
                    want=[{k:r[k] for k in fields} for r in traces[cid][key]]
                    if got!=want:errors.append(key)
            if 'expected_stop' in case:
                got=[dict(kind=int(k),pc=int(p,16)) for k,p in re.findall(r'^STOP_EVENT\|cycle=\d+\|kind=(\d+)\|pc=([0-9a-f]{8})$',text,re.M)]
                if got!=([] if case['expected_stop'] is None else [case['expected_stop']]):errors.append('stop event')
            if 'manual_ram_events' in case:
                got=[dict(kind=k,pc=int(p,16),word=w,address=a,data=data,mask=m,after=after) for cy,k,p,w,a,data,m,after in re.findall(r'^RAM\|cycle=(\d+)\|kind=([RWF])\|pc=([0-9a-f]{8})\|word=([0-9a-f]{8})\|addr=([0-9a-f]{8})\|data=([0-9a-f]{8})\|mask=([0-9a-f])\|after=([0-9a-f]{8})$',text,re.M)]
                if got!=case['manual_ram_events']:errors.append('RAM events')
            row=dict(id=cid,status='PASS' if not errors else 'FAIL',errors=errors,checks=metrics,process=proc,
                wave=str(directory/'wave.vcd'),ordered_WB_count=len(check['actual_writebacks']),ordered_STORE_count=len(check['actual_stores']))
            rows.append(row);save(directory/'result.json',row)
            if len(rows)%100==0:print(f"Default compatibility {len(rows)}/763",flush=True)
            if errors:break
        if rows[-1]['status']!='PASS':break
    save(HERE/'regression-result.json',dict(status='PASS' if len(rows)==763 and all(r['status']=='PASS' for r in rows) else 'NOT_ACCEPTED',cases=rows,protected_files=frozen()))
    print(f"Default compatibility: {len(rows)} cases; last={rows[-1]['status']}",flush=True)
