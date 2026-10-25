"""Native VCD request/response/IFID audit, strict pre/post separation, 0 DUT."""
from pathlib import Path
import json,re,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_redirect as s
def snapshots(path):
    scope=[];names={};values={};time=0;started=False;header=True;recording=True
    with path.open(encoding='ascii') as f:
        for line in f:
            a=line.split()
            if not a:continue
            if header:
                if a[0]=='$scope':scope.append(a[2])
                elif a[0]=='$upscope':scope.pop()
                elif a[0]=='$var':names.setdefault(a[3],[]).append('.'.join(scope+[a[4]]))
                elif a[0]=='$enddefinitions':header=False
                continue
            if a[0].startswith('#'):
                if started:yield time,dict(values),recording
                time=int(a[0][1:]);started=True
            elif a[0]=='$dumpoff':recording=False
            elif a[0]=='$dumpon':recording=True
            elif a[0][0] in 'bB' and len(a)==2:
                for n in names.get(a[1],[]):values[n]=a[0][1:]
            elif a[0][0] in '01xz':
                for n in names.get(a[0][1:],[]):values[n]=a[0][0]
    if started:yield time,dict(values),recording
def audit(tid,core=False):
    d=H/'runs'/tid
    if core:
        root='tb_board_coremark';checked=s.read(d/'check-result.json');name=tid.split('-')[0];image=(H/'build'/name/'program.bin').read_bytes()
        names=dict(cycle='cycle',req='pref_req',redir='pref_redir',hit='pref_hit',target='pref_target',pc='pref_pc',idpc='pref_id_pc',valid='monitor_pref_valid',tag='monitor_pref_tag',inst='monitor_inst',regpc='monitor_pc_reg',ifvalid='monitor_if_valid',ifpc='monitor_if_pc',ifinst='monitor_if_inst',idvalid='monitor_id_valid')
    else:
        root='tb_redirect';cid=tid.rsplit('-PF',1)[0];checked=s.read(d/('check-result-v2.json' if tid=='beq-taken-PF0' else 'check-result.json'));image=(H/'cases'/cid/'program.bin').read_bytes()
        names=dict(cycle='physical',req='pre_request',redir='pre_redirect',hit='pre_hit',target='pre_target',pc='pre_pc',idpc='pre_id_pc',valid='dut.fetch_redirect_valid',tag='dut.fetch_redirect_pc',inst='inst',regpc='dut.pc_reg',ifvalid='dut.if_valid',ifpc='dut.if_pc',ifinst='dut.if_inst',idvalid='dut.id_valid')
    assert checked['status']=='PASS';names={k:root+'.'+v for k,v in names.items()}
    def word(a):return int.from_bytes(image[a:a+4],'little') if a<32768 else 0
    def value(v,n):assert n in v and not re.search('[xz]',v[n],re.I),(tid,n);return int(v[n],2)
    seen=set();epoch=0;last_rst=0;sample=apply=reset_checks=off=0;classes=set();matched=[]
    for time,v,recording in snapshots(d/'wave.vcd'):
        if not recording:off+=1;continue
        if root+'.rst_n' not in v or re.search('[xz]',v[root+'.rst_n'],re.I):continue
        rst=value(v,root+'.rst_n')
        if not rst:
            if last_rst==1:epoch+=1
            if time>0:
                assert value(v,names['valid'])==0;reset_checks+=1
            last_rst=0;continue
        last_rst=1
        if value(v,root+'.clk')!=1:continue
        c=value(v,names['cycle'])
        if c<1:continue
        if core and value(v,root+'.pref_settled_cycle')!=c:continue
        req=value(v,names['req']);redir=value(v,names['redir']);hit=value(v,names['hit'])
        if c%2==1 and req and (epoch,c,'S') not in seen:
            seen.add((epoch,c,'S'));sample+=1;target=value(v,names['pc']);pc=value(v,names['idpc']);payload=word(target)
            assert value(v,names['valid'])==1 and value(v,names['tag'])==target and value(v,names['inst'])==payload
            op=word(pc)&127;classes.add({0x63:'B'+str((word(pc)>>12)&7),0x6f:'JAL',0x67:'JALR'}.get(op,'INVALID'))
            if len(matched)<8:matched.append(dict(kind='SAMPLE',cycle=c,pc=f'{pc:08x}',target=f'{target:08x}',time_ps=time,epoch=epoch))
        if c%2==0 and redir and (epoch,c,'A') not in seen:
            seen.add((epoch,c,'A'));apply+=1;target=value(v,names['target']);pc=value(v,names['idpc'])
            assert value(v,names['valid'])==0 and value(v,names['idvalid'])==0
            assert value(v,names['regpc'])==((target+4)&0xffffffff if hit else target)
            assert value(v,names['ifvalid'])==hit and value(v,names['ifpc'])==(target if hit else 0) and value(v,names['ifinst'])==(word(target) if hit else 0)
            if len(matched)<8:matched.append(dict(kind='APPLY',cycle=c,pc=f'{pc:08x}',target=f'{target:08x}',hit=hit,time_ps=time,epoch=epoch))
    if core:assert sample>0 and apply>0 and off>0 and classes=={'B0','B1','B4','B5','B6','B7','JAL','JALR'},(tid,classes)
    else:
        assert sample==checked['fetch']['requests'] and apply==checked['fetch']['applies'],(tid,sample,apply,checked['fetch'])
        if 'reset-between' in tid:assert epoch==1 and reset_checks>0 and sample==2
    return dict(id=tid,status='PASS_NATIVE_VCD_ONLY',samples_checked=sample,applies_checked=apply,request_classes=sorted(classes),reset_checks=reset_checks,reset_epochs=epoch,
        VCD_SHA256=s.sha(d/'wave.vcd'),bytes=(d/'wave.vcd').stat().st_size,explicit_off_groups=off,examples=matched,
        core_windowed=core,full_algorithm_wave=False if core else 'FULL_FINITE_DIRECTED_RUN',hardware_ILA=False,new_DUT_runs=0)
def small():
    r=s.read(H/'small-result-v2.json');assert r['status']=='PASS';rows=[audit(x['id']) for x in r['cases']]
    s.save(H/'small-wave-audit.json',dict(status='PASS',rows=rows,new_DUT_runs=0,protected=s.protect()));print('67 directed native VCDs request/tag/apply/reset PASS')
def core():
    assert s.read(H/'core-result.json')['status']=='PASS';rows=[audit(x['id'],True) for x in s.read(H/'core-result.json')['rows']]
    s.save(H/'prefetch-wave-audit.json',dict(status='PASS',rows=rows,new_DUT_runs=0,protected=s.protect()));print('Two core native-window prefetch audits PASS, not full algorithm/ILA')
if __name__=='__main__':{'small':small,'core':core}[sys.argv[1]]()
