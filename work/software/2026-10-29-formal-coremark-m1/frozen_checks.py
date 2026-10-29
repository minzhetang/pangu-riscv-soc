"""Actual summary vs pre-DUT frozen oracle; shared path for negative controls."""
from pathlib import Path
import json,re,hashlib,copy
H=Path(__file__).resolve().parent
def validate(actual,frozen):
    errors=[]
    def eq(k,a,b):
        if a!=b:errors.append(dict(kind=k,actual=a,expected=b))
    eq('iterations',actual['iterations'],frozen['iterations'])
    eq('crcfinal',actual['crcfinal'],frozen['crcfinal'])
    for k in ['raw_ticks','stamps','streams','physical','ram_SHA256','regs','report_SHA256','timer_reads']:
        expected=frozen['expected_physical'] if k=='physical' else frozen['RAM_SHA256'] if k=='ram_SHA256' else frozen[k]
        eq(k,actual[k],expected)
    eq('phase order',actual['phases'],[0,1,2,3,4])
    eq('budget',0<actual['physical']<=(32000000 if frozen['iterations']==8 else 8000000),True)
    eq('no timer/port error',actual['no_errors'],True)
    return errors
def freeze_for(name):
    d=H/'oracles-recovery'/name
    o=json.loads((d/'expected.json').read_text(encoding='utf-8-sig'));o['regs']=[int(x,16) for x in (d/'expected-registers.hex').read_text().split()]
    o['expected_physical']=o['physical'];o['RAM_SHA256']=hashlib.sha256((d/'expected-ram.bin').read_bytes()).hexdigest().upper();o['report_SHA256']=hashlib.sha256((d/'expected-report.txt').read_bytes()).hexdigest().upper()
    return o
def from_actual(name,result,directory=None):
    d=Path(directory) if directory is not None else H/'runs'/(name+'-N234');report=(d/'ram-output.txt').read_bytes();text=report.decode('ascii')
    return dict(iterations=int(re.findall(r'^Iterations\s*:\s*(\d+)\s*$',text,re.M)[0]),crcfinal=re.findall(r'^\[0\]crcfinal\s*:\s*0x([0-9a-f]{4})\s*$',text,re.M)[0],raw_ticks=result['detail']['raw_ticks'],stamps=result['detail']['stamps'],streams=result['streams'],physical=result['metrics']['physical'],ram_SHA256=hashlib.sha256(bytes(int(x,16) for x in (d/'ram.hex').read_text().split())).hexdigest().upper(),regs=[int(x,16) for x in (d/'registers.hex').read_text().split()],report_SHA256=hashlib.sha256(report).hexdigest().upper(),timer_reads=result['timer_reads'],phases=[p for c,p in result['detail']['phases']],no_errors=not result['errors'])
def selftest():
    f=freeze_for('performance');good=dict(iterations=2,crcfinal=f['crcfinal'],raw_ticks=f['raw_ticks'],stamps=f['stamps'],streams=f['streams'],physical=f['expected_physical'],ram_SHA256=f['RAM_SHA256'],regs=f['regs'],report_SHA256=f['report_SHA256'],timer_reads=f['timer_reads'],phases=[0,1,2,3,4],no_errors=True)
    assert not validate(good,f);rows=[dict(id='control',status='PASS')]
    for label,fn in [('iterations1',lambda o:o.update(iterations=1)),('crcfinal',lambda o:o.update(crcfinal='0000')),('missing_WB',lambda o:o['streams']['WB'].update(count=o['streams']['WB']['count']-1)),('extra_MEM',lambda o:o['streams']['MEM'].update(count=o['streams']['MEM']['count']+1)),('raw_timing',lambda o:o.update(raw_ticks=o['raw_ticks']+1)),('phase_missing_BSS',lambda o:o.update(phases=[1,2,3,4])),('budget_over',lambda o:o.update(physical=8000001))]:
        o=copy.deepcopy(good);fn(o);errs=validate(o,f);assert errs;rows.append(dict(id=label,status='EXPECTED_REJECT',errors=errs))
    return dict(status='PASS',control_and_negatives=rows,new_DUT=0,shared_actual_checker_path=True)
