"""Fixed M0 preparation and bounded execution. No vendor program is installed/run."""
from pathlib import Path
import argparse, datetime, hashlib, json, subprocess, time

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
BASE = PROJECT / 'work/icarus/2026-10-21-cpu-shifti-reject/source'
TOOLS = PROJECT / 'tools/iverilog-13.0-msys2-ucrt64/ucrt64'
IVL = TOOLS / 'bin/iverilog.exe'
VVP = TOOLS / 'bin/vvp.exe'
LIB = TOOLS / 'lib/ivl'
VENDOR = Path('D:/PDS/PDS_2022.2-SP6.4/arch/vendor/pango/verilog/simulation')
RELEASE = PROJECT / 'deliveries/mainline-txgpio-approval-2026-10-23-v1'
CPU_HASH = {
    'cpu.v': '555CB51AC20FFC439B61BB29D4F4D9F4DC02C38B54A37291A79519CD413B8114',
    'control.v': '23CDBDFDD45DD60D6C7D95A13CC51927999A640FE5E30CAF8D324FA91AA87067',
    'alu.v': '6393472BC3635DA83213E0E9883766D5076C37EA60319F32F1DE5C420F68065E',
    'regfile.v': 'AE36F070B994EEF41AF1636516D737EDA240C2A18AF83048ADC3E3E2391C8468',
}

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest().upper()

def save(p, obj):
    # Generated evidence; refuse overwriting an existing artifact.
    with Path(p).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def i(rd, rs, imm, f=0, op=0x13): return ((imm & 4095)<<20)|(rs<<15)|(f<<12)|(rd<<7)|op
def s(rs2, rs1, off, f=2):
    return ((off & 0xfe0)<<20)|(rs2<<20)|(rs1<<15)|(f<<12)|((off & 31)<<7)|0x23
def b(rs1, rs2, off):
    return (((off>>12)&1)<<31)|(((off>>5)&63)<<25)|(rs2<<20)|(rs1<<15)|(((off>>1)&15)<<8)|(((off>>11)&1)<<7)|0x63
EBREAK = 0x00100073

def cases():
    branch = [i(1,0,256),i(2,1,0,2,3),b(2,0,12),i(3,0,7),s(3,1,4),EBREAK]
    return [
        dict(id='P01', words=[i(1,0,128),i(2,1,0,2,3),i(3,2,1),EBREAK],
             regs={1:128,2:0x12345678,3:0x12345679}, stores=[], stop=12, stall=1, flush=0),
        dict(id='P02', words=[i(1,0,256),i(2,0,85),s(2,1,0),s(2,1,0),i(3,1,0,2,3),
             i(4,3,1),i(5,0,-1),s(5,1,1,0),s(4,1,2,1),i(6,1,0,2,3),EBREAK],
             regs={1:256,2:85,3:85,4:86,5:0xffffffff,6:0x0056ff55},
             stores=[[256,85,15],[256,85,15],[257,0xff00,2],[258,0x00560000,12]],
             stop=40, stall=1, flush=0),
        dict(id='P03T',words=branch,init={0:0},regs={1:256},stores=[],stop=20,stall=1,flush=1),
        dict(id='P03N',words=branch,init={0:5},regs={1:256,2:5,3:7},stores=[[260,7,15]],stop=20,stall=1,flush=0),
        dict(id='P04',words=[i(1,0,1),b(1,1,12),s(1,0,260),i(7,0,99),i(8,0,42),s(8,0,264),EBREAK],
             regs={1:1,8:42},stores=[[264,42,15]],stop=24,stall=0,flush=1),
        dict(id='P05',words=[i(1,0,256),i(2,1,4,2,3),EBREAK,s(2,1,8)],init={1:0xdeadbeef},
             regs={1:256,2:0xdeadbeef},stores=[],stop=8,stall=0,flush=0),
    ]

def reference(c):
    """Independent sequential subset for these probes, not a full RV32I reference."""
    rom = [EBREAK]*256
    rom[:len(c['words'])] = c['words']
    rom[32] = 0x12345678
    ram = [0xa5a5a5a5]*64
    for idx,val in c.get('init',{}).items(): ram[idx] = val
    initial_ram = ram.copy()
    regs, wb, stores, loads = [0]*32, [], [], []
    pc = 0
    for _ in range(100):
        ins = rom[pc//4]
        if ins == EBREAK: break
        op,rd,f,r1,r2 = ins&127,(ins>>7)&31,(ins>>12)&7,(ins>>15)&31,(ins>>20)&31
        imm = ins>>20
        if imm&2048: imm -= 4096
        nxt, value = pc+4, None
        if op==0x13 and f==0: value = (regs[r1]+imm)&0xffffffff
        elif op==3 and f==2:
            a = (regs[r1]+imm)&0xffffffff
            assert a%4==0
            value = ram[(a-256)//4] if 256<=a<512 else rom[a//4]
            loads.append([a,value])
        elif op==0x23 and f in (0,1,2):
            off = ((ins>>25)<<5)|((ins>>7)&31)
            if off&2048: off -= 4096
            a = (regs[r1]+off)&0xffffffff
            assert 256<=a<512
            n = 1<<f
            assert a%n==0
            mask = ((1<<n)-1)<<(a%4)
            wd = ((regs[r2]&((1<<(n*8))-1))<<((a%4)*8))&0xffffffff
            stores.append([a,wd,mask])
            for lane in range(4):
                if mask&(1<<lane):
                    ram[(a-256)//4] = (ram[(a-256)//4]&~(255<<(lane*8))) | (wd&(255<<(lane*8)))
        elif op==0x63 and f==0:
            off = (((ins>>31)&1)<<12)|(((ins>>7)&1)<<11)|(((ins>>25)&63)<<5)|(((ins>>8)&15)<<1)
            if off&4096: off -= 8192
            if regs[r1]==regs[r2]: nxt=pc+off
        else: raise ValueError(f'unsupported probe word {ins:08x}')
        if value is not None and rd:
            regs[rd] = value
            wb.append([rd,value])
        pc=nxt
    else: raise AssertionError('reference timeout')
    manual = [0]*32
    for r,v in c['regs'].items(): manual[r]=v
    assert regs==manual, (c['id'],'manual RF mismatch')
    assert stores==c['stores'] and pc==c['stop'], (c['id'],'manual flow mismatch')
    return dict(regs=regs,ram=ram,wb=wb,stores=stores,loads=loads,stop_pc=pc,stop_kind=2,
                stall=c['stall'],flush=c['flush']),rom,initial_ram

def check_log(text, exp):
    actual = dict(regs={},ram={},wb=[],stores=[],loads=[],stop=[],stall=0,flush=0)
    issues=[]
    end=False; stop_cycle=None
    for line in text.splitlines():
        t=line.split()
        if not t: continue
        try:
            if t[0]=='WB':
                actual['wb'].append([int(t[2]),int(t[3],16)])
                if stop_cycle is not None: issues.append('WB after stop')
            elif t[0]=='STORE':
                actual['stores'].append([int(x,16) for x in t[2:5]])
                if stop_cycle is not None: issues.append('STORE after stop')
            elif t[0]=='LOAD': actual['loads'].append([int(x,16) for x in t[2:4]])
            elif t[0]=='REG': actual['regs'][int(t[1])]=int(t[2],16)
            elif t[0]=='RAM': actual['ram'][int(t[1])]=int(t[2],16)
            elif t[0]=='STOP':
                actual['stop'].append([int(t[2]),int(t[3],16)])
                stop_cycle=int(t[1])
            elif t[0]=='EDGE':
                actual['stall']+=int(t[7].split('=')[1])
                actual['flush']+=int(t[8].split('=')[1])
            elif t[0] in ('FETCH_MISMATCH','UNKNOWN_CONTROL','CYCLE_TIMEOUT'): issues.append(line)
            elif t[0]=='SIM_END': end=True; actual['cycles']=int(t[1]); actual['time_ps']=int(t[2].split('=')[1])
        except (ValueError,IndexError): issues.append('X/Z or malformed record: '+line)
    for key in ('wb','stores','loads','stall','flush'):
        if actual[key]!=exp[key]: issues.append(key+' mismatch')
    for key,n in [('regs',32),('ram',64)]:
        if actual[key]!={idx:exp[key][idx] for idx in range(n)}: issues.append(key+' mismatch')
    if actual['stop']!=[[exp['stop_kind'],exp['stop_pc']]]: issues.append('stop mismatch')
    if not end: issues.append('no bounded normal end')
    return dict(status='PASS' if not issues else ('TIMEOUT' if 'CYCLE_TIMEOUT' in issues else 'FAIL'),
                issues=issues,actual=actual)

def bounded(argv, cwd, name, seconds):
    out,err=ROOT/'logs'/f'{name}.stdout.log',ROOT/'logs'/f'{name}.stderr.log'
    start=time.monotonic(); timeout=False; cap=False
    with out.open('xb') as o,err.open('xb') as e:
        p=subprocess.Popen([str(a) for a in argv],cwd=cwd,stdout=o,stderr=e,stdin=subprocess.DEVNULL)
        while p.poll() is None:
            timeout=time.monotonic()-start>seconds
            cap=out.stat().st_size+err.stat().st_size>8*1024*1024
            if timeout or cap:
                # Only the process tree started here; no unrelated process names.
                cleanup=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(p.pid),'/T','/F'],
                    capture_output=True,timeout=8)
                save(ROOT/'logs'/f'{name}.cleanup.json',dict(rc=cleanup.returncode,
                    stdout=cleanup.stdout.decode(errors='replace'),stderr=cleanup.stderr.decode(errors='replace')))
                break
            time.sleep(.05)
        try: rc=p.wait(timeout=2)
        except subprocess.TimeoutExpired: rc=None
    result=dict(argv=[str(a) for a in argv],cwd=str(cwd),timeout_seconds=seconds,
                returncode=rc,returncode_hex=None if rc is None else f'0x{rc&0xffffffff:08X}',
                elapsed_seconds=round(time.monotonic()-start,6),timeout=timeout,log_cap=cap,
                stdout=str(out),stderr=str(err))
    save(ROOT/'logs'/f'{name}.command.json',result)
    return result

def bounded_text(p):
    with Path(p).open('rb') as f: data=f.read(8*1024*1024+1)
    if len(data)>8*1024*1024: raise ValueError('log exceeds cap')
    return data.decode('utf-8',errors='replace')

def prepare():
    for name,h in CPU_HASH.items():
        for directory in [BASE,ROOT/'source-before',ROOT/'source']:
            assert sha(directory/name)==h, str(directory/name)
    protected=read(PROJECT/'reports/progress/2026-10-23-quality-evolution-evidence/protected-before.json')['files']
    for item in protected: assert sha(item['path'])==item['sha256']
    data=[]
    for c in cases():
        exp,rom,ram=reference(c)
        stem=ROOT/'inputs'/c['id']
        for suffix,words in [('program.hex',rom),('data.hex',ram)]:
            with Path(str(stem)+'.'+suffix).open('x',encoding='ascii') as f:
                f.write(''.join(f'{w:08x}\n' for w in words))
        save(Path(str(stem)+'.expected.json'),exp)
        data.append(dict(id=c['id'],words=[f'{x:08x}' for x in c['words']],expected=exp))
    save(ROOT/'inputs/cases.json',data)
    targets=[dict(id='drm',top='tb_drm',sources=[str(ROOT/'tb_drm.sv'),str(VENDOR/'GTP_DRM18K_E1.v'),str(VENDOR/'GTP_GRS.v')]),
             dict(id='cpu',top='tb_cpu_timing',sources=[str(ROOT/'tb_cpu_timing.sv')]+[str(ROOT/'source'/n) for n in CPU_HASH])]
    for t in targets:
        t['output']=str(ROOT/(t['id']+'.vvp'))
        t['argv']=[str(IVL),'-B',str(LIB),'-g2012','-Wall','-s',t['top'],'-o',t['output']]+t['sources']
    save(ROOT/'commands.json',dict(compiler_timeout=60,run_timeout=30,cycle_limit=2000,targets=targets))
    paths=[Path(x['path']) for x in protected]+[BASE/n for n in CPU_HASH]
    paths += [p for d in ['source','source-before','inputs'] for p in (ROOT/d).iterdir() if p.is_file()]
    paths += [ROOT/p for p in ['PLAN.md','run.py','tb_drm.sv','tb_cpu_timing.sv','commands.json']]
    paths += [IVL,VVP,VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v',
              Path('D:/PDS/PDS_2022.2-SP6.4/ip/module_ip/ipm2l_flex_ram/ipm2l_flex_ram_eval/ipm2l_spram/rtl/ipm2l_spram_v1_8.v.xml')]
    frozen=[dict(path=str(p),sha256=sha(p)) for p in sorted(set(paths))]
    save(ROOT/'frozen-inputs.json',dict(date=datetime.datetime.now().astimezone().isoformat(),files=frozen))
    # Contract release is a new approval overlay, never edit the historical contract.
    h=sha(RELEASE/'TXGPIO_REGIF_CONTRACT.md')
    q=sha(RELEASE/'QUALITY_EVOLUTION_ADDENDUM.md')
    assert h=='F0E31602D008459B3E95901C0F533BC7FF4153F6B5A93859780EA8D2AD64E988'
    assert q=='80DEBA901A0917E730CD14D98A08933274337588A1E2A31AFBAB6D91D700F476'
    save(RELEASE/'APPROVAL.json',dict(decision='D115',date_beijing=datetime.datetime.now().astimezone().isoformat(),
         task='B-REGIF-TXGPIO-M1',contract='LOCAL-REGIF-TXGPIO-M1/1.0.0',contract_sha256=h,
         quality_sha256=q,implementation='APPROVED_TO_START_ON_RECEIPT',relay='NOT_SENT',receipt='NOT_CONFIRMED',
         A_scope='A-MEM-TIMING-M0_ONLY',full_SoC='NOT_APPROVED',hardware='STOP'))
    with (RELEASE/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
        for p in sorted(RELEASE.iterdir()):
            if p.name!='SHA256SUMS.txt': f.write(f'{sha(p)}  {p.name}\n')
    # Checker negative tests are synthetic, explicitly not DUT runs.
    exp=data[0]['expected']
    def synth(e):
        rows=['EDGE 1 5 pc=0 inst=0 addr=0 rd=0 stall=1 flush=0 stop=0']
        rows += [f'WB 2 {r} {v:08x}' for r,v in e['wb']]
        rows += [f'LOAD 1 {a:08x} {v:08x}' for a,v in e['loads']]
        rows += [f'REG {r} {v:08x}' for r,v in enumerate(e['regs'])]
        rows += [f'RAM {r} {v:08x}' for r,v in enumerate(e['ram'])]
        rows += ['STOP 9 2 0000000c','SIM_END 17 time_ps=171000']
        return '\n'.join(rows)
    good=synth(exp)
    checks=[check_log(good,exp)['status']=='PASS',
            check_log(good.replace('STOP 9','WB 8 3 12345679\nSTOP 9'),exp)['status']=='FAIL',
            check_log(good.replace('12345678','12345670'),exp)['status']=='FAIL',
            check_log(good+'\nSTORE 18 00000100 00000001 f',exp)['status']=='FAIL',
            check_log(good.replace('stall=1','stall=0'),exp)['status']=='FAIL']
    assert all(checks),checks
    save(ROOT/'checker-selftest.json',dict(status='PASS',checks=checks,synthetic=True,DUT_runs=0))
    print(json.dumps(dict(prepared=True,targets=2,cases=len(data),modes=4,frozen=len(frozen),checker_selftests=5),ensure_ascii=False))

def verify():
    records=read(ROOT/'frozen-inputs.json')['files']
    bad=[x['path'] for x in records if sha(x['path'])!=x['sha256']]
    assert not bad,bad
    return dict(checked=len(records),changed=bad)

def run():
    if (ROOT/'results.json').exists(): raise RuntimeError('already executed; preserve outputs')
    verify()
    results=dict(scope='A-MEM-TIMING-M0',status='RUNNING',compiles=[],drm='NOT_RUN',cpu=[],
                 note='same CPU; behavioral latency probes are not physical memory mapping')
    for target in read(ROOT/'commands.json')['targets']:
        rec=bounded(target['argv'],ROOT,'compile-'+target['id'],60)
        results['compiles'].append(rec)
        if rec['returncode']!=0 or rec['timeout'] or rec['log_cap']:
            results['status']='TOOL_ERROR'
            results['stop_reason']='first compiler failure; no further compiler or partial VVP execution'
            results['unexecuted_targets']=[t['id'] for t in read(ROOT/'commands.json')['targets'] if t['id']!=target['id']]
            break
        assert Path(target['output']).stat().st_size>0
        if target['id']=='drm':
            d=ROOT/'runs/drm'; d.mkdir()
            rr=bounded([VVP,'-N','-M-','-M'+str(LIB),target['output']],d,'run-drm',30)
            text=bounded_text(rr['stdout'])
            results['drm']=dict(process=rr,status='PASS' if rr['returncode']==0 and 'DRM_PASS checks=13' in text and (d/'wave.vcd').stat().st_size>0 else 'FAIL')
            # Failed model check is not silently replaced with a behavioral PASS.
            if results['drm']['status']!='PASS':
                results['status']='MODEL_CHECK_FAILED'; break
        else:
            for c in read(ROOT/'inputs/cases.json'):
                for f,dmode in [(0,0),(1,0),(0,1),(1,1)]:
                    name=f"{c['id']}-i{f}-d{dmode}"; d=ROOT/'runs'/name; d.mkdir()
                    rr=bounded([VVP,'-N','-M-','-M'+str(LIB),target['output'],
                        '+PROGRAM='+str(ROOT/'inputs'/f"{c['id']}.program.hex"),
                        '+DATA='+str(ROOT/'inputs'/f"{c['id']}.data.hex"),f'+IF_SYNC={f}',f'+DATA_SYNC={dmode}'],d,'run-'+name,30)
                    checked=check_log(bounded_text(rr['stdout']),c['expected'])
                    if rr['timeout']: checked['status']='TIMEOUT'
                    elif rr['returncode']!=0: checked['status']='TOOL_ERROR'
                    checked.update(id=c['id'],if_sync=f,data_sync=dmode,process=rr,wave=str(d/'wave.vcd'))
                    if not (d/'wave.vcd').is_file(): checked['status']='FAIL'; checked['issues'].append('no new VCD')
                    results['cpu'].append(checked)
            results['status']='CHARACTERIZATION_COMPLETED'
    results['postflight']=verify()
    results['date_beijing']=datetime.datetime.now().astimezone().isoformat()
    save(ROOT/'results.json',results)
    print(json.dumps(dict(status=results['status'],compiles=len(results['compiles']),drm=results['drm'],cpu_runs=len(results['cpu'])),ensure_ascii=False))

if __name__=='__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(); parser.add_argument('action',choices=['prepare','run','verify'])
    args=parser.parse_args()
    if args.action=='prepare': prepare()
    elif args.action=='run': run()
    else: print(json.dumps(verify()))
