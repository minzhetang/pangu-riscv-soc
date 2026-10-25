"""D139 bounded candidate: only CPU frontend and one SoC binding change."""
from pathlib import Path
import ast,ctypes,difflib,hashlib,importlib.util,json,re,shutil,sys,subprocess,time
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
B=P/'work/fpga/2026-10-25-board-coremark-m1';T=P/'work/system/2026-10-24-timed-coremark-m1'
OLD=P/'work/icarus/2026-10-21-cpu-shifti-reject';ADAPT=P/'work/system/2026-10-23-memory-adapt-m1';M=P/'work/fpga/2026-10-24-implementability-m0'
spec=importlib.util.spec_from_file_location('redirect_bounded',M/'stage.py');lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib);lib.H=H
read,save,sha,log,extract=lib.read,lib.save,lib.sha,lib.log,lib.extract
def bounded(argv,cwd,name,limit):
    folder=H/'logs'/name;folder.mkdir(exist_ok=False);start=time.monotonic();timed=cap=False;cleanup=None
    with (folder/'stdout.log').open('xb') as out,(folder/'stderr.log').open('xb') as err:
        proc=subprocess.Popen(list(map(str,argv)),cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        while proc.poll() is None:
            timed=time.monotonic()-start>limit
            cap=any((Path(cwd)/n).exists() and (Path(cwd)/n).stat().st_size>256*1024*1024 for n in ['trace.log','bus.log','wave.vcd','fetch.log'])
            cap=cap or any((folder/n).stat().st_size>8*1024*1024 for n in ['stdout.log','stderr.log'])
            if timed or cap:
                try:
                    q=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(proc.pid),'/T','/F'],capture_output=True,timeout=8)
                    cleanup=dict(native_rc=q.returncode,remaining_tree='NOT_INDEPENDENTLY_ENUMERATED_NO_SUCCESS_CLAIM')
                except Exception as e:cleanup=dict(error=repr(e),remaining_tree='UNKNOWN')
                break
            time.sleep(.02)
        try:rc=proc.wait(timeout=2)
        except subprocess.TimeoutExpired:rc=None
    result=dict(argv=list(map(str,argv)),cwd=str(cwd),returncode=rc,returncode_hex=None if rc is None else f'0x{rc&0xffffffff:08X}',
        timed_out=timed,cap=cap,trace_cap=cap,cleanup=cleanup,elapsed_seconds=round(time.monotonic()-start,6),timeout_seconds=limit,
        stdout=str(folder/'stdout.log'),stderr=str(folder/'stderr.log'))
    save(folder/'process.json',result);return result
def protect():
    rows=read(H/'protected-originals.json')['files']
    if (H/'frozen.json').exists():rows+=read(H/'frozen.json')['files']
    bad=[x['path'] for x in rows if sha(x['path'])!=x['sha256']];assert not bad,bad[:5]
    return len(rows)
def patch_cpu():
    f=H/'source/cpu.v';s=f.read_text(encoding='utf-8');original=s
    s=s.replace('parameter integer SYNC_MEMORY = 0','parameter integer SYNC_MEMORY = 0,\n    parameter integer RESOLVED_TARGET_FETCH = 0',1)
    s=s.replace('    wire stall_if, flush_if, flush_id;','''    wire stall_if, flush_if, flush_id;
    wire [31:0] redirect_target;
    wire redirect_request, redirect_fetch_hit;
    reg fetch_redirect_valid;
    reg [31:0] fetch_redirect_pc;''',1)
    s=s.replace('if (flush_if) if_valid<=0;','if (flush_if) if_valid<=redirect_fetch_hit;',1)
    assert s.count('    assign pc = pc_reg;')==1;s=s.replace('    assign pc = pc_reg;','',1)
    anchor='    // 缺省下一跳 PC\n'
    block='''    // Opt-in resolved-target fetch for the fixed one-edge synchronous ROM.
    // Request on the memory-sampling phase; consume only its matched response.
    assign redirect_target = id_jump ? jump_target : branch_target;
    assign redirect_request = (SYNC_MEMORY != 0) && (RESOLVED_TARGET_FETCH != 0)
        && rst_n && id_valid && !eei_hold && (branch_taken || id_jump)
        && (redirect_target[1:0] == 2'b00);
    assign pc = redirect_request ? redirect_target : pc_reg;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            fetch_redirect_valid <= 1'b0;
            fetch_redirect_pc <= 32'd0;
        end else if (!pipeline_advance) begin
            fetch_redirect_valid <= redirect_request;
            fetch_redirect_pc <= pc;
        end else begin
            fetch_redirect_valid <= 1'b0;
        end
    end
    // Unmapped/zero returns conservatively retain the previous redirect path.
    // This is not an ISA decoder or a new exception mechanism.
    assign redirect_fetch_hit = redirect_request && fetch_redirect_valid
        && (fetch_redirect_pc == redirect_target) && (inst != 32'd0);

'''
    assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
    a='assign pc_next = (flush_if) ? (id_jump ? jump_target : branch_target) : '
    assert s.count(a)==1;s=s.replace(a,'assign pc_next = (flush_if) ? (redirect_fetch_hit ? (fetch_redirect_pc + 32\'d4) : redirect_target) : ',1)
    a='''        end else if (pipeline_advance && (flush_if || eei_hold)) begin
            if_pc   <= 32'd0;
            if_inst <= 32'd0;'''
    b='''        end else if (pipeline_advance && eei_hold) begin
            if_pc   <= 32'd0;
            if_inst <= 32'd0;
        end else if (pipeline_advance && flush_if) begin
            if_pc   <= redirect_fetch_hit ? fetch_redirect_pc : 32'd0;
            if_inst <= redirect_fetch_hit ? inst : 32'd0;'''
    assert s.count(a)==1;s=s.replace(a,b,1)
    f.write_text(s,encoding='utf-8')
    (H/'CPU_DIFF.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='source-before/cpu.v',tofile='source/cpu.v')),encoding='utf-8')
    f=H/'source/soc_top.sv';old=f.read_text();assert old.count('cpu #(.SYNC_MEMORY(1))')==1
    new=old.replace('cpu #(.SYNC_MEMORY(1))','cpu #(.SYNC_MEMORY(1),.RESOLVED_TARGET_FETCH(1))')
    f.write_text(new,encoding='ascii');(H/'SOC_DIFF.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='source-before/soc_top.sv',tofile='source/soc_top.sv')),encoding='utf-8')
def prepare():
    for n in ['source','source-before','models','models-before','cases','runs','logs','compile','build','tests']:(H/n).mkdir(exist_ok=False)
    originals={x['path']:x for x in read(ADAPT/'frozen.json')['files']}
    originals.update({x['path']:x for x in read(B/'frozen.json')['files']})
    for r in read(B/'postflight.json')['source']:
        f=B/'source'/r['file'];assert sha(f)==r['sha256']
        for n in ['source','source-before']:shutil.copyfile(f,H/n/f.name)
        originals[str(f)]=dict(path=str(f),sha256=sha(f))
    for n in ['cpu_program_reference.py','peripheral_checker.py']:
        for dst in ['models','models-before']:shutil.copyfile(B/'models'/n,H/dst/n)
    for f in [*B.glob('*.py'),B/'tests/tb_board_coremark.sv',ADAPT/'run_stage.py',OLD/'compile-batch-plan.json']:
        originals[str(f)]=dict(path=str(f),sha256=sha(f))
    save(H/'protected-originals.json',dict(files=list(originals.values())))
    patch_cpu();protect()
    save(H/'APPROVAL.json',dict(date_beijing='2026-10-25',decision='D139',user_reply='批准 继续推进！',scope_SHA256=sha(H/'IMPLEMENTATION_SCOPE.md'),
        base_git='f28794776cf559d910d168954bd0209ae5e9233a',scope='independent CPU/SoC parameterized resolved-target fetch, bounded verification; PDS after benefit only',hardware='STOPPED'))
    sys.path.insert(0,str(H/'models'));from cpu_program_reference import Reference
    import plan_cases
    plans=[]
    for c in plan_cases.cases():
        d=H/'cases'/c['id'];d.mkdir();image=c.pop('image');data=bytearray(b'\xa5'*32768)
        for a,v in c['initial_data'].items():data[int(a):int(a)+4]=(v&0xffffffff).to_bytes(4,'little')
        (d/'program.bin').write_bytes(image)
        for fn,raw in [('imem.hex',image),('dmem.hex',data)]:
            with (d/fn).open('x',encoding='ascii') as f:f.write(''.join(f'{int.from_bytes(raw[i:i+4],"little"):08x}\n' for i in range(0,32768,4)))
        r=Reference(image,lambda *x:(_ for _ in ()).throw(AssertionError('unexpected IO')),lambda *x:(_ for _ in ()).throw(AssertionError('unexpected IO')));r.ram[:]=data;redirects=[]
        while r.pc!=c['stop_pc']:
            assert r.steps<1000 and not r.stopped
            pc=r.pc;word=int.from_bytes(r.rom[pc:pc+4],'little');f=r.flush;r.step()
            if r.flush!=f:
                target=r.pc;w=int.from_bytes(r.rom[target:target+4],'little') if target<32768 else 0
                redirects.append(dict(pc=pc,target=target,request=target%4==0,eligible=target%4==0 and w!=0,word=w))
        assert r.flush==c['expected_flush'] and r.stall==c['expected_stall'],(c['id'],r.flush,r.stall)
        assert all(r.regs[int(k)]==v for k,v in c['manual_registers'].items()),c['id']
        assert all(int.from_bytes(r.ram[int(k):int(k)+4],'little')==v for k,v in c['manual_memory'].items()),c['id']
        (d/'expected-ram.hex').write_text(''.join(f'{v:02x}\n' for v in r.ram),encoding='ascii')
        expected=dict(registers=r.regs,ram_SHA256=sha(d/'expected-ram.hex'),EX=r.EX,WB=r.WB,MEM=r.MEM,redirects=redirects)
        save(d/'expected.json',expected);save(d/'manual.json',c);plans.append(c)
    save(H/'manual-plan.json',dict(date_beijing='2026-10-25',before_DUT=True,cases=plans,programs=34,new_small_runs=67,
        stop='first design failure stops, no RTL/expectation expansion',timing='1ns/1ps, small10ns clock, fixed one-edge memory',formal_score=False))
    # Preserve the entire old regression function and frozen specialized checks.
    oldtext=(ADAPT/'run_stage.py').read_text(encoding='utf-8');tree=ast.parse(oldtext)
    functions='\n\n'.join(ast.get_source_segment(oldtext,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['text_log','regress'])
    head="from pathlib import Path\nimport json,re,hashlib\nfrom itertools import zip_longest\nimport stage_redirect as s\nHERE=s.H;OLD=s.OLD\nread,save,sha,bounded,extract=s.read,s.save,s.sha,s.bounded,s.extract\nVVP=s.lib.VVP;LIB=s.lib.LIB\nfrozen=s.protect\ndef artifacts():return s.artifacts('initial')\n"
    (H/'regression_bridge.py').write_text(head+functions+'\n',encoding='utf-8')
    targets=[]
    for g in read(OLD/'compile-batch-plan.json')['requests']:
        tb=Path(list(g['input_SHA256'])[-1]);out=H/'compile'/('regression-'+g['name']+'.vvp')
        argv=[lib.IVL,'-B',lib.LIB,'-g2012','-Wall','-s','tb_cpu_selfcheck_v1','-o',out,*[H/'source'/n for n in ['cpu.v','alu.v','control.v','regfile.v']],tb]
        targets.append(dict(id='regression-'+g['name'],argv=list(map(str,argv)),output=str(out),phase='initial'))
    for pf in [0,1]:
        out=H/'compile'/f'directed-{pf}.vvp';argv=[lib.IVL,'-B',lib.LIB,'-g2012','-Wall','-s','tb_redirect',f'-Ptb_redirect.PF={pf}','-o',out,*[H/'source'/n for n in ['cpu.v','alu.v','control.v','regfile.v']],H/'tb_redirect.sv']
        targets.append(dict(id=f'directed-{pf}',argv=list(map(str,argv)),output=str(out),phase='initial'))
    save(H/'initial-compile-plan.json',dict(maximum=16,timeout_seconds=120,fail_fast=True,only_compile=True,targets=targets))
    print('Manual/reference 34 cases frozen before DUT; source diff CPU/SoC only; 16 initial compile targets',flush=True)
def freeze():
    protect();files=[f for f in H.rglob('*') if f.is_file() and f.name!='protected-originals.json']
    save(H/'frozen.json',dict(files=[dict(path=str(f),sha256=sha(f)) for f in sorted(files)]));print('Frozen',protect())
def compiles(phase):
    protect();assert not ctypes.windll.shell32.IsUserAnAdmin()
    if phase=='core':assert read(H/'small-result.json')['status']==read(H/'regression-result.json')['status']=='PASS'
    plan=read(H/(phase+'-compile-plan.json'));rows=[]
    for t in plan['targets']:
        r=bounded(t['argv'],H,'compile-'+t['id'],120);ok=r['returncode']==0 and not r['timed_out'] and not r['cap'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if ok else 'FAIL',output=t['output'],sha256=sha(t['output']) if ok else None,process=r));print(t['id'],rows[-1]['status'],flush=True)
        if not ok:break
    save(H/(phase+'-compile-result.json'),dict(status='PASS' if len(rows)==plan['maximum'] and all(r['status']=='PASS' for r in rows) else 'STOPPED',rows=rows,protected=protect()))
def artifacts(phase):
    result=read(H/(phase+'-compile-result.json'));assert result['status']=='PASS'
    assert all(sha(x['output'])==x['sha256'] for x in result['rows']);return {x['id']:x['output'] for x in result['rows']}
def small():
    protect();paths=artifacts('initial');rows=[]
    import check_redirect
    for c in read(H/'manual-plan.json')['cases']:
        for pf in ([1] if c['reset_pending'] else [0,1]):
            tid=c['id']+f'-PF{pf}';d=H/'runs'/tid;d.mkdir()
            args=[lib.VVP,'-N','-M-','-M'+str(lib.LIB),paths[f'directed-{pf}'],'+IMAGE='+str(H/'cases'/c['id']/'imem.hex'),'+DATA='+str(H/'cases'/c['id']/'dmem.hex'),'+MAX_CYCLES=4000']
            if c['reset_pending']:args.append('+RESET_PENDING')
            r=bounded(args,d,'run-'+tid,30);save(d/'process.json',r);shutil.copyfile(r['stdout'],d/'stdout.log')
            try:
                assert r['returncode']==0 and not r['timed_out'] and not r['cap'],r
                result=check_redirect.check(c,pf,d);save(d/'check-result.json',result);assert result['status']=='PASS',result
            except Exception as e:
                save(H/'small-result.json',dict(status='STOPPED',case=tid,error=repr(e),completed=rows,protected=protect()));raise
            rows.append(dict(id=tid,status='PASS',process=r,check=result))
    save(H/'small-result.json',dict(status='PASS',cases=rows,new_DUT_runs=len(rows),protected=protect()));print('Directed',len(rows),'PASS')
def regress():
    protect();import regression_bridge;regression_bridge.regress()
if __name__=='__main__':
    {'prepare':prepare,'freeze':freeze,'compile-initial':lambda:compiles('initial'),'small':small,'regression':regress,'verify':lambda:print(protect())}[sys.argv[1]]()
