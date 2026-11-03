"""Own primitive binding test runner. Never modifies licensed model or old work."""
from pathlib import Path
import sys,importlib.util,json,ctypes,subprocess,time,hashlib,difflib
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
M1=H.parent/'2026-10-23-memory-adapt-m1'
spec=importlib.util.spec_from_file_location('m1_helpers',M1/'run_stage.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
s.HERE=H # explicitly bind reviewed helper functions to NEW work directory
VENDOR=Path('D:/PDS/PDS_2022.2-SP6.4/arch/vendor/pango/verilog/simulation')
names=['P01','P02','P03T','P03N','P04','P05','cboot','performance','validation']
def save(p,o):s.save(p,o)
def read(p):return s.read(p)
def check_frozen():return s.frozen()
def prepare():
    for r in read(M1/'frozen.json')['files']:assert s.sha(r['path'])==r['sha256']
    for n in ['cpu.v','alu.v','control.v','regfile.v']:
        assert s.sha(H/'source'/n)==s.sha(H/'source-before'/n)==s.sha(M1/'source'/n)
    small=read(s.M0/'inputs/cases.json');tables=[];receipts=[]
    for i,name in enumerate(names+['selftest']):
        rom=[0]*8192;ram=[0xa5a5a5a5]*8192
        if i<6:
            image=s.M0/'inputs'/f'{name}.program.hex';data=s.M0/'inputs'/f'{name}.data.hex'
            data_words=[int(v,16) for v in data.read_text().split()];ram[:len(data_words)]=data_words
            rombytes,rambytes,rambase=1024,256,256
        elif i==6:image=s.CBOOT/'inputs/smoke.mem32.hex';rombytes,rambytes,rambase=16384,16384,65536
        elif i<9:image=s.CM/name/'image.hex';rombytes,rambytes,rambase=32768,32768,65536
        else:
            image=None;rombytes,rambytes,rambase=32768,32768,65536
            rom=[((0x31415927+j*0x10103)^(j<<19))&0xffffffff for j in range(8192)]
            ram=[((0xdeadbeef-j*0x30107)^(j<<17))&0xffffffff for j in range(8192)]
        if image:
            words=[int(v,16) for v in image.read_text().split()];rom[:len(words)]=words
        tables.append(dict(id=name,ROM=rom,RAM=ram,rombytes=rombytes,rambytes=rambytes,rambase=rambase))
        receipts.append(dict(id=name,image=None if image is None else str(image),image_sha=None if image is None else s.sha(image),
            physical_ROM_bytes=32768,physical_RAM_bytes=32768,visible_ROM_bytes=rombytes,visible_RAM_bytes=rambytes,RAM_base=rambase))
    with (H/'init_tables.svh').open('x',encoding='ascii') as f:
        f.write('// Generated immutable input constants, NOT vendor source.\n')
        for kind in ['ROM','RAM']:
            f.write(f'localparam [262143:0] {kind}_BITS =\n')
            for i,t in enumerate(tables):
                data=''.join(f'{w:08x}' for w in reversed(t[kind]))
                # Bound lexer token length without changing the 262144-bit value.
                chunks=[data[n:n+1024] for n in range(0,len(data),1024)]
                assert len(chunks)==64 and ''.join(chunks)==data
                f.write(f'CASE=={i} ? {{'+',\n'.join("4096'h"+c for c in chunks)+'} :\n')
            f.write("262144'd0;\n")
        for key,col in [('ROM_BYTES','rombytes'),('RAM_BYTES','rambytes'),('RAM_BASE','rambase')]:
            f.write(f'localparam integer {key} = '+''.join(f'CASE=={i}?{t[col]}:' for i,t in enumerate(tables))+'0;\n')
    # Independent host check: bank/lane/9-bit pack roundtrip, no DUT used.
    count=0
    for t in tables:
        for kind in ['ROM','RAM']:
            for b in range(8):
                for h in range(2):
                    physical=[]
                    for c in range(64):
                        packed=sum(((t[kind][b*1024+c*16+j//2]>>(h*16+(j%2)*8))&255)<<(9*j) for j in range(32))
                        physical.extend((packed>>(9*j))&511 for j in range(32))
                    for w in range(1024):
                        actual=physical[2*w]|physical[2*w+1]<<8
                        assert actual==(t[kind][b*1024+w]>>(16*h))&65535;count+=1
    save(H/'initialization-receipts.json',dict(cases=receipts,synthetic_roundtrip_checks=count,DUT_runs=0))
    targets=[]
    for i,name in enumerate(names+['selftest']):
        tb=H/('tb_full_memory.sv' if i==9 else 'tb_mem_adapt.sv');top='tb_full_memory' if i==9 else 'tb_mem_adapt'
        sources=[H/'memory_model.sv',tb,VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v']
        if i<9:sources+=[H/'source'/n for n in ['cpu.v','alu.v','control.v','regfile.v']]
        output=H/'compile'/(name+'.vvp')
        argv=[str(s.IVL),'-B',str(s.LIB),'-g2012','-Wall','-I',str(H),'-s',top]
        if i<9:argv+=['-Ptb_mem_adapt.CASE='+str(i)]
        argv+=['-o',str(output),*[str(p) for p in sources]]
        targets.append(dict(id=name,argv=argv,output=str(output),sources=[str(p) for p in sources]))
    targets=targets[-1:]+targets[:-1] # selftest compiles/runs first
    save(H/'compile-plan.json',dict(targets=targets,max_compiles=10,timeout_seconds=60,fail_fast=True,only_compile=True))
    files={Path(r['path']) for r in read(M1/'frozen.json')['files']}
    files.update(M1/p for p in ['summary.json','programs-result.json','small-result.json','wave-audit.json','SHA256SUMS.txt','run_stage.py'])
    files.update(p for p in H.rglob('*') if p.is_file())
    for t in targets:files.update(Path(p) for p in t['sources'])
    save(H/'frozen.json',dict(files=[dict(path=str(p),sha256=s.sha(p)) for p in sorted(files)]))
    print(json.dumps(dict(prepared=True,targets=len(targets),protected=len(files),synthetic_pack_checks=count)))
def compile_all():
    check_frozen();assert not ctypes.windll.shell32.IsUserAnAdmin()
    save(H/'compile-attempt.json',dict(maximum=10,only_compile=True))
    rows=[]
    for t in read(H/'compile-plan.json')['targets']:
        p=s.bounded(t['argv'],H,'compile-'+t['id'],60)
        ok=p['returncode']==0 and not p['timed_out'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if ok else 'FAIL',process=p,output=t['output'],sha256=s.sha(t['output']) if Path(t['output']).is_file() else None))
        if not ok:break
    save(H/'compile-result.json',dict(status='ALL_COMPILED_NOT_SIMULATED' if len(rows)==10 and all(r['status']=='PASS' for r in rows) else 'COMPILE_STOP',rows=rows,protected=check_frozen()))
    print(json.dumps([(r['id'],r['status']) for r in rows]))
def artifacts():
    check_frozen();c=read(H/'compile-result.json');assert c['status']=='ALL_COMPILED_NOT_SIMULATED'
    assert all(s.sha(r['output'])==r['sha256'] for r in c['rows'])
    return {r['id']:r['output'] for r in c['rows']}
def selftest():
    paths=artifacts();rows=[]
    for bad in [0,1,2,3]:
        d=H/'runs'/f'selftest-{bad}';d.mkdir()
        p=s.bounded([s.VVP,'-N','-M-','-M'+str(s.LIB),paths['selftest'],f'+BAD={bad}'],d,f'selftest-{bad}',30)
        stdout=s.text_log(p['stdout'])
        ok=(p['returncode']==0 and 'MAP_SELFTEST_PASS' in stdout) if bad==0 else (p['returncode']!=0 and 'MEMORY_PROTOCOL' in stdout and 'NEGATIVE_NOT_REJECTED' not in stdout)
        ok=ok and not p['timed_out']
        row=dict(id=bad,status='PASS' if ok else 'FAIL',expected='normal selftest' if bad==0 else 'explicit protocol rejection',process=p)
        save(d/'result.json',row);rows.append(row)
        if not ok:break
    save(H/'selftest-result.json',dict(status='PASS' if len(rows)==4 and all(r['status']=='PASS' for r in rows) else 'NOT_ACCEPTED',cases=rows,protected=check_frozen()))
    print(json.dumps([(r['id'],r['status']) for r in rows]))
def programs():
    assert read(H/'selftest-result.json')['status']=='PASS'
    paths=artifacts();rows=[]
    for name in names:
        r=s.generic(name,1,{'generic-1':paths[name]});rows.append(dict(id=name,**r))
        print(name+': '+r['status']+' '+str(r.get('errors')),flush=True)
        if r['status']!='PASS':break
    save(H/'programs-result.json',dict(status='PASS' if len(rows)==9 and all(r['status']=='PASS' for r in rows) else 'NOT_ACCEPTED',cases=rows,protected=check_frozen()))
if __name__=='__main__':
    action=sys.argv[1]
    {'prepare':prepare,'compile':compile_all,'selftest':selftest,'programs':programs,'verify':lambda:print(check_frozen())}[action]()
