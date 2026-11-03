"""Freeze before DUT; one ordinary compile; runs only verified successful VVP."""
import argparse
import copy
import ctypes
import datetime
import hashlib
import json
import subprocess
import time
from pathlib import Path
from reference_coremark import Streams,check_ram_output
from prepare_and_build import HERE,ROOT,sha,save,item,verify

TOOLS=ROOT/'tools/iverilog-13.0-msys2-ucrt64/ucrt64'

def compare(case,directory):
    expected=json.loads((HERE/case/'expected.json').read_text())
    streams=Streams(); unknown=[]
    with (directory/'trace.log').open(encoding='ascii') as source:
        for index,line in enumerate(source):
            f=line.strip().split('|')
            assert f[0] in ('EX','WB','READ','STORE'),('invalid trace',index,line)
            if any('x' in v.lower() or 'z' in v.lower() for v in f[1:]): unknown.append(index)
            streams.add(f[0],*f[1:])
    regs=[int(v,16) for v in (directory/'registers.hex').read_text().split()]
    ram=[int(v,16) for v in (directory/'ram.hex').read_text().split()]
    text=(directory/'run/stdout.log').read_text()
    diff=[]
    for name,actual,exp in [('RF',regs,expected['registers']),('RAM',ram,expected['ram'])]:
        if actual!=exp:
            first=next((i for i,(a,b) in enumerate(zip(actual,exp)) if a!=b),None)
            diff.append({'kind':name,'first_index':first,'actual_length':len(actual),'expected_length':len(exp)})
    if streams.result()!=expected['streams']: diff.append({'kind':'ORDERED_STREAMS','actual':streams.result(),'expected':expected['streams']})
    lines=[x for x in text.splitlines() if x.startswith('METRICS|')]
    metrics=dict(x.split('=') for x in lines[0].split('|')[1:]) if len(lines)==1 else {}
    for key,val in [('stall',expected['stall']),('flush',expected['flush']),('holds',4),('cycles',expected['expected_normal_end_cycles'])]:
        if int(metrics.get(key,-1))!=val: diff.append({'kind':key,'actual':metrics.get(key),'expected':val})
    if 'STOP|2|00000068' not in text or 'SIMULATION_ENDED_NOT_FUNCTIONAL_PASS' not in text:
        diff.append({'kind':'STOP_OR_END_MARKER'})
    if 'FATAL' in text or unknown: diff.append({'kind':'FATAL_OR_UNKNOWN','unknown_trace_lines':unknown[:8]})
    try:
        output=check_ram_output(ram,expected['symbols'],case)
        (directory/'ram-output.txt').write_text(output,encoding='ascii')
    except Exception as exc: diff.append({'kind':'CRC_OR_PORT_OUTPUT','error':repr(exc)})
    return {'status':'PASS' if not diff else 'FAIL','differences':diff,'actual_streams':streams.result(),
            'metrics':metrics,'RAM_bytes_compared':len(ram),'registers_compared':len(regs),
            'unknown_trace_events':len(unknown),'retirement_PC':False,'unified_WB_STORE_commit':False,
            'score':'NOT_MEASURED_TIMER_UNAVAILABLE_SHORT_CRC_RUN'}

def frozen_verify():
    verify()
    records=json.loads((HERE/'frozen-before-DUT.json').read_text())
    changed=[r['path'] for r in records if sha(Path(r['path']))!=r['sha256']]
    assert not changed,changed
    return len(records)

def freeze():
    assert not (HERE/'frozen-before-DUT.json').exists()
    files=list((HERE/'source').glob('*.v'))+[HERE/n for n in ['memory_model.sv','tb_coremark.sv','reference_coremark.py','check_and_run.py',
             'manual-plan.json','coremark.ld','start.S','prepare_and_build.py','source-integrity-review.json']]
    files+=list((HERE/'port').glob('*'))
    for case in ['performance','validation']:
        files += [HERE/case/n for n in ['coremark.elf','coremark.bin','image.hex','expected.json','expected-output.txt']]
    # Checker negative tests do not involve DUT or modify any frozen data.
    a=Streams(); a.add('WB','1','00000001'); before=a.result(); a.add('WB','1','00000001')
    duplicates_rejected=a.result()!=before
    b=Streams(); b.add('STORE','00000004','00010000','00000001','f')
    c=Streams(); c.add('STORE','00000004','00010000','00000002','f')
    store_mutation_rejected=b.result()!=c.result()
    expected=json.loads((HERE/'performance/expected.json').read_text())
    bad=copy.deepcopy(expected['ram']); p=expected['symbols']['ram_log']-0x10000
    output=bytes(bad[p:p+4096]); offset=output.index(b'e714'); bad[p+offset]=ord('f')
    try: check_ram_output(bad,expected['symbols'],'performance'); crc_mutation_rejected=False
    except AssertionError: crc_mutation_rejected=True
    tests={'duplicate_WB_rejected':duplicates_rejected,'STORE_value_mutation_rejected':store_mutation_rejected,
           'known_CRC_output_mutation_rejected':crc_mutation_rejected}
    assert all(tests.values())
    save(HERE/'checker-selftest.json',tests)
    save(HERE/'frozen-before-DUT.json',[item(p) for p in files])
    save(HERE/'stage-status.json',{'stage':'PREPARED_GOLDEN_FROZEN','DUT':'NOT_RUN','new_CPU_changes':0})

def compile_once(external=False):
    frozen_verify()
    directory=HERE/('compile-external-01' if external else 'compile-ordinary-01')
    directory.mkdir(exist_ok=False)
    argv=[str(TOOLS/'bin/iverilog.exe'),'-B',str(TOOLS/'lib/ivl'),'-g2012','-Wall','-s','tb_coremark','-o',str(directory/'coremark.vvp')]
    argv += [str(HERE/'source'/n) for n in ['alu.v','control.v','regfile.v','cpu.v']]
    argv += [str(HERE/n) for n in ['memory_model.sv','tb_coremark.sv']]
    request={'argv':argv,'cwd':str(HERE),'timeout_seconds':60,'external':external,
             'compiler_SHA256':sha(TOOLS/'bin/iverilog.exe'),'inputs':[item(Path(n)) for n in argv[-6:]]}
    if external:
        admin=bool(ctypes.windll.shell32.IsUserAnAdmin())
        assert not admin,'Nonadmin only'; request['IsUserAnAdmin']=admin
    save(directory/'request.json',request)
    start=time.monotonic()
    try:
        p=subprocess.run(argv,cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        out,err=p.stdout,p.stderr; result={'exit_code':p.returncode,'timed_out':False}
    except subprocess.TimeoutExpired as exc:
        out,err=exc.stdout or b'',exc.stderr or b''; result={'exit_code':None,'timed_out':True}
    (directory/'stdout.log').write_bytes(out); (directory/'stderr.log').write_bytes(err)
    result['elapsed_seconds']=round(time.monotonic()-start,6)
    result['VVP']=item(directory/'coremark.vvp') if (directory/'coremark.vvp').exists() else None
    save(directory/'process.json',result)
    good=result['exit_code']==0 and not result['timed_out'] and result['VVP'] is not None
    save(HERE/'stage-status.json',{'stage':'COMPILED' if good else 'COMPILE_TOOL_ERROR','compile_directory':str(directory),
                                 'compile':result,'DUT':'NOT_RUN','new_CPU_changes':0})
    frozen_verify(); print(json.dumps(result,indent=2))

def run():
    frozen_verify()
    status=json.loads((HERE/'stage-status.json').read_text())
    assert status['stage']=='COMPILED', 'Never run residual failed VVP'
    compile_dir=Path(status['compile_directory']); record=json.loads((compile_dir/'process.json').read_text())
    vvp=compile_dir/'coremark.vvp'; assert record['exit_code']==0 and sha(vvp)==record['VVP']['sha256']
    results={}
    for case in ['performance','validation']:
        directory=HERE/case/'dut-run-01'; directory.mkdir(exist_ok=False)
        run_dir=directory/'run'; run_dir.mkdir()
        words=json.loads((HERE/case/'image-receipt.json').read_text())['words']
        # Short relative image path avoids truncation of fixed-width Verilog strings.
        argv=[str(TOOLS/'bin/vvp.exe'),'-N','-M-','-M'+str(TOOLS/'lib/ivl'),str(vvp),'+IMAGE=../image.hex',f'+WORDS={words}']
        save(run_dir/'request.json',{'argv':argv,'cwd':str(directory),'timeout_seconds':180,'cycle_limit':10000000,
                                    'VVP_sha256':sha(vvp),'vvp_SHA256':sha(TOOLS/'bin/vvp.exe'),'ordinary':True})
        start=time.monotonic()
        try:
            p=subprocess.run(argv,cwd=directory,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180,
                             creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            out,err=p.stdout,p.stderr; proc={'exit_code':p.returncode,'timed_out':False}
        except subprocess.TimeoutExpired as exc:
            out,err=exc.stdout or b'',exc.stderr or b''; proc={'exit_code':None,'timed_out':True}
        (run_dir/'stdout.log').write_bytes(out); (run_dir/'stderr.log').write_bytes(err)
        proc['elapsed_seconds']=round(time.monotonic()-start,6); save(run_dir/'process.json',proc)
        verdict={'status':'TIMEOUT' if proc['timed_out'] else 'TOOL_OR_SIMULATION_FAILURE'}
        if proc['exit_code']==0 and not proc['timed_out']:
            verdict=compare(case,directory)
        verdict['process']=proc; save(directory/'result.json',verdict); results[case]=verdict
        if verdict['status']!='PASS': break
    frozen_verify()
    save(HERE/'result.json',{'stage':'A-COREMARK-CORRECTNESS-M1','cases':results,'CPU_modified':False,'hardware_operations':0,
                           'status':'PASS' if len(results)==2 and all(x['status']=='PASS' for x in results.values()) else 'NOT_ACCEPTED',
                           'score':'NOT_MEASURED','frozen_files_verified':frozen_verify()})
    print(json.dumps(json.loads((HERE/'result.json').read_text()),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['freeze','compile','compile-external','run'])
    a=p.parse_args().action
    {'freeze':freeze,'compile':lambda:compile_once(False),'compile-external':lambda:compile_once(True),'run':run}[a]()
