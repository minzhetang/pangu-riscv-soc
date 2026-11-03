"""Frozen inputs, bounded compile-only permission batch, ordinary simulations."""
from pathlib import Path
import argparse,ast,ctypes,datetime,difflib,hashlib,json,re,subprocess,sys,time
from collections import Counter
from itertools import zip_longest
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
OLD=PROJECT/'work/icarus/2026-10-21-cpu-shifti-reject'
M0=PROJECT/'work/system/2026-10-23-memory-timing-m0'
CBOOT=PROJECT/'work/system/2026-10-23-c-boot-m1'
CM=PROJECT/'work/system/2026-10-23-coremark-correctness-m1'
TOOLS=PROJECT/'tools/iverilog-13.0-msys2-ucrt64/ucrt64'
IVL=TOOLS/'bin/iverilog.exe';VVP=TOOLS/'bin/vvp.exe';LIB=TOOLS/'lib/ivl'

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,obj):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest().upper()
def stamp():return datetime.datetime.now().astimezone().isoformat()
def extract(p,names,ns):
    tree=ast.parse(p.read_text(encoding='utf-8-sig'))
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    assert len(nodes)==len(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
    return ns

def frozen():
    rows=read(HERE/'frozen.json')['files']
    bad=[r['path'] for r in rows if sha(r['path'])!=r['sha256']]
    assert not bad,bad[:10]
    return len(rows)

def bounded(argv,cwd,name,limit):
    folder=HERE/'logs'/name;folder.mkdir(exist_ok=False)
    start=time.monotonic();timed=False;oversize=False
    with (folder/'stdout.log').open('xb') as out,(folder/'stderr.log').open('xb') as err:
        p=subprocess.Popen([str(a) for a in argv],cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                           creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        while p.poll() is None:
            timed=time.monotonic()-start>limit
            trace=Path(cwd)/'trace.log'
            oversize=trace.exists() and trace.stat().st_size>256*1024*1024
            if timed or oversize:
                cleanup=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(p.pid),'/T','/F'],
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=8)
                save(folder/'cleanup.json',dict(returncode=cleanup.returncode,remaining_state='NOT_INDEPENDENTLY_ENUMERATED'))
                break
            time.sleep(.02)
        try:rc=p.wait(timeout=2)
        except subprocess.TimeoutExpired:rc=None
    rec=dict(argv=[str(a) for a in argv],cwd=str(cwd),returncode=rc,returncode_hex=None if rc is None else f'0x{rc&0xffffffff:08X}',
        timed_out=timed,trace_cap=oversize,elapsed_seconds=round(time.monotonic()-start,6),timeout_seconds=limit,
        stdout=str(folder/'stdout.log'),stderr=str(folder/'stderr.log'))
    save(folder/'process.json',rec)
    return rec
def text_log(p):
    with Path(p).open('rb') as f:b=f.read(8*1024*1024+1)
    assert len(b)<=8*1024*1024,'stdout exceeds read cap'
    return b.decode('utf-8',errors='replace').replace('\r\n','\n')

def prepare():
    original=read(M0/'frozen-inputs.json')['files']
    for r in original:assert sha(r['path'])==r['sha256']
    for name in ['cpu.v','alu.v','control.v','regfile.v']:
        assert sha(HERE/'source-before'/name)==sha(OLD/'source'/name)
        if name!='cpu.v':assert sha(HERE/'source'/name)==sha(OLD/'source'/name)
    with (HERE/'cpu.diff').open('x',encoding='utf-8') as f:
        f.writelines(difflib.unified_diff((HERE/'source-before/cpu.v').read_text(encoding='utf-8').splitlines(True),
            (HERE/'source/cpu.v').read_text(encoding='utf-8').splitlines(True),fromfile='source-before/cpu.v',tofile='source/cpu.v'))
    groups=read(OLD/'compile-batch-plan.json')['requests']
    plan=read(OLD/'validation-v2/plan.json')
    assert len(plan['cases'])==763 and len({c for g in groups for c in g['case_ids']})==763
    targets=[]
    for sync in [0,1]:
        targets.append(dict(id=f'generic-{sync}',top='tb_mem_adapt',parameters=[f'-Ptb_mem_adapt.SYNC={sync}'],
            sources=[HERE/'source'/n for n in ['cpu.v','alu.v','control.v','regfile.v']]+[HERE/'memory_model.sv',HERE/'tb_mem_adapt.sv']))
    for g in groups:
        targets.append(dict(id='regression-'+g['name'],top='tb_cpu_selfcheck_v1',parameters=[],
            sources=[HERE/'source'/n for n in ['cpu.v','alu.v','control.v','regfile.v']]+[Path(list(g['input_SHA256'])[-1])],cases=g['case_ids']))
    for t in targets:
        t['sources']=[str(p) for p in t['sources']];t['output']=str(HERE/'compile'/(t['id']+'.vvp'))
        t['argv']=[str(IVL),'-B',str(LIB),'-g2012','-Wall','-s',t['top'],*t['parameters'],'-o',t['output'],*t['sources']]
    save(HERE/'compile-plan.json',dict(scope='compile only, no vvp',targets=targets,max_compiles=16,each_timeout_seconds=60,fail_fast=True))
    files={Path(r['path']) for r in original}
    files.update(p for p in (HERE/'source').glob('*.v'));files.update((HERE/'source-before').glob('*.v'))
    files.update(HERE/n for n in ['PLAN.md','memory_model.sv','tb_mem_adapt.sv','run_stage.py','cpu.diff','compile-plan.json'])
    files.update(M0/'inputs'/p.name for p in (M0/'inputs').iterdir() if p.is_file())
    files.update(OLD/n for n in ['validation-v2/plan.json','expected-traces.json','runs-v2/result.json','models/cpu_trace_oracle.py'])
    for t in targets:files.update(Path(p) for p in t['sources'])
    for c in plan['cases']:
        files.update(OLD/'cases'/c['id']/name for name in ['imem.hex','dmem.hex','expected-regs.hex','expected-mem.hex'])
    files.update(CBOOT/n for n in ['expected.json','check_c_boot.py','inputs/smoke.mem32.hex','inputs/smoke.elf','inputs/smoke.bin','result-after-external.json'])
    files.update(CM/n for n in ['reference_coremark.py','manual-plan.json','result.json','handoff-result.json'])
    for case in ['performance','validation']:
        files.update(CM/case/n for n in ['image.hex','image-receipt.json','expected.json','coremark.bin','coremark.elf'])
    files.update([IVL,VVP])
    save(HERE/'frozen.json',dict(started='2026-10-23',frozen_at=stamp(),files=[dict(path=str(p),sha256=sha(p)) for p in sorted(files)]))
    # Synthetic validation of no-dedup stream digest: never a CPU result.
    oracle=extract(CM/'reference_coremark.py',{'Streams'},{'hashlib':hashlib,'collections':__import__('collections')})
    s=oracle['Streams']();s.add('WB','1','00000001');a=s.result();s.add('WB','1','00000001')
    assert s.result()!=a
    save(HERE/'checker-selftest.json',dict(synthetic=True,DUT_runs=0,duplicate_WB_changes_digest=True))
    print(json.dumps(dict(prepared=True,targets=len(targets),protected_files=len(files),RTL_files_changed=['source/cpu.v'])))

def compile_batch():
    frozen();assert not ctypes.windll.shell32.IsUserAnAdmin(),'non-admin only'
    save(HERE/'compile-attempt.json',dict(date_beijing=stamp(),maximum=16,simulations=0))
    result=dict(status='RUNNING',rows=[])
    for t in read(HERE/'compile-plan.json')['targets']:
        r=bounded(t['argv'],HERE,'compile-'+t['id'],60)
        good=r['returncode']==0 and not r['timed_out'] and not r['trace_cap'] and Path(t['output']).is_file()
        r.update(id=t['id'],output=t['output'],status='PASS' if good else 'FAIL',sha256=sha(t['output']) if Path(t['output']).is_file() else None)
        result['rows'].append(r)
        if not good:result['status']='STOPPED_COMPILE_ERROR';break
    else:result['status']='ALL_COMPILED_NOT_SIMULATED'
    result['protected_files']=frozen();save(HERE/'compile-result.json',result)
    print(json.dumps(dict(status=result['status'],targets=len(result['rows'])),ensure_ascii=False))

def artifacts():
    frozen();r=read(HERE/'compile-result.json');assert r['status']=='ALL_COMPILED_NOT_SIMULATED'
    assert all(sha(x['output'])==x['sha256'] for x in r['rows'])
    return {x['id']:x['output'] for x in r['rows']}

def trace_result(directory):
    streams=extract(CM/'reference_coremark.py',{'Streams'},{'hashlib':hashlib,'collections':__import__('collections')})['Streams']()
    records={'EX':[],'WB':[],'READ':[],'STORE':[]};n=0;unknown=[]
    small=(directory/'trace.log').stat().st_size<1_000_000
    with (directory/'trace.log').open(encoding='ascii') as f:
        for row in f:
            fields=row.strip().split('|');kind=fields[0]
            assert kind in records,fields
            if any('x' in v.lower() or 'z' in v.lower() for v in fields[1:]):unknown.append(n)
            streams.add(kind,*fields[1:]);n+=1
            if small:records[kind].append(fields[1:])
    return streams.result(),records,unknown

def generic(case,sync,paths):
    name=f'{case}-sync{sync}';directory=HERE/'runs'/name;directory.mkdir(exist_ok=False)
    if case.startswith('P'):
        exp=next(x['expected'] for x in read(M0/'inputs/cases.json') if x['id']==case)
        args=['+IMAGE='+str(M0/'inputs'/f'{case}.program.hex'),'+WORDS=256','+ROM_BYTES=1024','+RAM_BYTES=256','+RAM_BASE=256',
            '+RAM_IMAGE='+str(M0/'inputs'/f'{case}.data.hex'),'+MAX_CYCLES=4000']
        timeout=30
    elif case=='cboot':
        exp=read(CBOOT/'expected.json');args=['+IMAGE='+str(CBOOT/'inputs/smoke.mem32.hex'),'+WORDS=144',
            '+ROM_BYTES=16384','+RAM_BYTES=16384','+RAM_BASE=65536','+MAX_CYCLES=100000'];timeout=30
    else:
        exp=read(CM/case/'expected.json');words=read(CM/case/'image-receipt.json')['words']
        args=['+IMAGE='+str(CM/case/'image.hex'),f'+WORDS={words}','+ROM_BYTES=32768','+RAM_BYTES=32768','+RAM_BASE=65536',
              '+MAX_CYCLES='+str(exp['expected_normal_end_cycles']*2+128)];timeout=180
    proc=bounded([VVP,'-N','-M-','-M'+str(LIB),paths[f'generic-{sync}'],*args],directory,'run-'+name,timeout)
    errors=[]
    if proc['returncode']!=0 or proc['timed_out'] or proc['trace_cap']:
        result=dict(status='TIMEOUT' if proc['timed_out'] else 'TOOL_OR_SIM_ERROR',process=proc)
        save(directory/'result.json',result);return result
    stdout=text_log(proc['stdout']);stream,records,unknown=trace_result(directory)
    regs=[int(s,16) for s in (directory/'registers.hex').read_text().split()]
    ram=[int(s,16) for s in (directory/'ram.hex').read_text().split()]
    lines=[x for x in stdout.splitlines() if x.startswith('METRICS|')]
    mt={k:int(v) for k,v in (x.split('=') for x in lines[0].split('|')[1:])} if len(lines)==1 else {}
    if unknown or 'FATAL' in stdout or not mt:errors.append('unknown/fatal/missing metrics')
    if not re.search(r'^STOP\|2\|'+('000000'+format(exp['stop_pc'],'02x') if case.startswith('P') else '00000068')+r'$',stdout,re.M):errors.append('stop kind/PC')
    if case.startswith('P'):
        expected_ram=list(b''.join(x.to_bytes(4,'little') for x in exp['ram']))
        if regs!=exp['regs']:errors.append('RF')
        if ram!=expected_ram:errors.append('RAM')
        if [[int(r),int(v,16)] for r,v in records['WB']]!=exp['wb']:errors.append('ordered WB')
        if [[int(a,16),int(v,16),int(m,16)] for pc,a,v,m in records['STORE']]!=exp['stores']:errors.append('ordered STORE')
        if [[int(a,16),int(v,16)] for pc,a,v,load in records['READ']]!=exp['loads']:errors.append('ordered LOAD')
        expected_stall,expected_flush=exp['stall'],exp['flush']
    elif case=='cboot':
        if regs!=exp['registers']:errors.append('RF')
        if ram!=exp['ram']:errors.append('RAM')
        if records['WB']!=exp['writebacks']:errors.append('ordered WB')
        mem=[]
        for row in (directory/'trace.log').read_text(encoding='ascii').splitlines():
            t=row.split('|')
            if t[0] in ('READ','STORE'):mem.append(t)
        if mem!=exp['memory_events']:errors.append('ordered memory')
        if [r[0] for r in records['EX']]!=exp['execution_PC_not_retirement']:errors.append('EX PC')
        expected_stall,expected_flush=exp['stall_model_expected'],exp['flush_model_expected']
    else:
        if regs!=exp['registers']:errors.append('RF')
        if ram!=exp['ram']:errors.append('RAM')
        if stream!=exp['streams']:errors.append('ordered stream digests')
        crc=extract(CM/'reference_coremark.py',{'check_ram_output'},{'HERE':CM,'json':json})['check_ram_output']
        try:output=crc(ram,exp['symbols'],case)
        except Exception as e:errors.append('CRC/output '+repr(e));output=''
        with (directory/'ram-output.txt').open('x',encoding='ascii') as f:f.write(output)
        expected_stall,expected_flush=exp['stall'],exp['flush']
        if mt.get('advances')!=exp['expected_normal_end_cycles']:errors.append('logical advance count')
    if mt.get('stall')!=expected_stall or mt.get('flush')!=expected_flush:errors.append('logical stall/flush')
    if mt.get('physical')!=mt.get('advances',0)+mt.get('memory_holds',0):errors.append('physical accounting')
    if sync and mt.get('physical')!=2*mt.get('advances',0)+1:errors.append('two-phase physical clock accounting')
    if not sync and mt.get('memory_holds')!=0:errors.append('default unexpected memory hold')
    if 'SIMULATION_ENDED_NOT_FUNCTIONAL_PASS' not in stdout:errors.append('no normal end')
    result=dict(status='PASS' if not errors else 'FAIL',errors=errors,metrics=mt,actual_streams=stream,process=proc,
        registers_checked=len(regs),RAM_bytes_checked=len(ram),wave=str(directory/'wave.vcd'),unknown_events=len(unknown),
        scope='fixed behavioral memory; no physical mapping or CoreMark score',default_mode=not sync)
    save(directory/'result.json',result);return result

def run_small():
    paths=artifacts();result=[]
    for sync in [0,1]:
        for c in read(M0/'inputs/cases.json'):
            r=generic(c['id'],sync,paths);result.append(dict(id=c['id'],sync=sync,**r))
            if r['status']!='PASS':break
        if result[-1]['status']!='PASS':break
    save(HERE/'small-result.json',dict(cases=result,status='PASS' if len(result)==12 and all(r['status']=='PASS' for r in result) else 'NOT_ACCEPTED',protected_files=frozen()))
    print(json.dumps(dict(cases=[dict(id=r['id'],sync=r['sync'],status=r['status'],errors=r.get('errors'),metrics=r.get('metrics')) for r in result]),ensure_ascii=False))

def run_programs():
    assert read(HERE/'small-result.json')['status']=='PASS'
    paths=artifacts();rows=[]
    for case in ['cboot','performance','validation']:
        for sync in [0,1]:
            r=generic(case,sync,paths);rows.append(dict(id=case,sync=sync,**r))
            print(f"{case} sync={sync}: {r['status']}",flush=True)
            if r['status']!='PASS':break
        if rows[-1]['status']!='PASS':break
    save(HERE/'programs-result.json',dict(status='PASS' if len(rows)==6 and all(r['status']=='PASS' for r in rows) else 'NOT_ACCEPTED',cases=rows,protected_files=frozen()))

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

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','compile','small','programs','regression','verify'])
    a=p.parse_args().action
    {'prepare':prepare,'compile':compile_batch,'small':run_small,'programs':run_programs,'regression':regress,
     'verify':lambda:print(frozen())}[a]()
