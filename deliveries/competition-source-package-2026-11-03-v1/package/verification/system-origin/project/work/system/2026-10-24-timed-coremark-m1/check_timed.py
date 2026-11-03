"""Independent physical-time oracle + streaming, no-dedup architecture check."""
from pathlib import Path
import json,re,sys,hashlib
sys.dont_write_bytecode=True
import run_stage as s
from cpu_program_reference import Reference
from peripheral_checker import ContractModel,decode_frames
H=Path(__file__).resolve().parent
def data_row(line):
    a=line.strip().split('|');assert len(a)==17 and a[0]=='EDGE'
    assert not any(re.search('[xz]',v,re.I) for v in a[1:]),'unknown public/timer data'
    decimal={1,4,8,9,11,13,14}
    return [int(v,10 if i in decimal else 16) for i,v in enumerate(a[1:],1)]
def counter_pre(c,address):
    assert c>=1
    return ((c-1)>>(32 if address==0x20000104 else 0))&0xffffffff
def check(tid):
    d=H/'runs'/tid;name,ns=tid.split('-N');n=int(ns);errors=[]
    def eq(label,a,b):
        if a!=b and len(errors)<32:errors.append(dict(kind=label,actual=str(a)[:300],expected=str(b)[:300]))
    r=s.read(d/'process.json');assert r['returncode']==0 and not r['timed_out'] and not r['cap']
    text=s.log(d/'stdout.log');m=re.findall(r'^METRICS\|(.*)$',text,re.M);assert len(m)==1
    metrics={k:int(v) for k,v in (x.split('=') for x in m[0].split('|'))}
    model=ContractModel(n);samples=[1];read_at={};bus={};gpio=[];prev=0;max_bus=0
    with (d/'bus.log').open(encoding='ascii') as f:
        for line in f:
            c,gin,addr,write,data,mask,rd,err,pre_tx,pre_gpio,post_tx,post_gpio,accept,stop,pre_t,post_t=data_row(line)
            assert prev<c<=metrics['physical'];prev=c;max_bus=c
            while len(samples)<c:
                cycle=len(samples);out=model.step(cycle,1,0 if cycle<16 else 0x3c if cycle<4096 else 0xc3)
                eq('omitted UART sample must be high',out['tx_post'],1);samples.append(1)
            eq('GPIO frozen input',gin,0 if c<16 else 0x3c if c<4096 else 0xc3)
            eq('pre tick physical clock',pre_t,c-1);eq('post tick physical clock',post_t,c)
            eq('UART pre-edge',pre_tx,samples[-1]);eq('GPIO pre-edge',pre_gpio,model.gpio_out)
            out=model.step(c,1,gin,addr,bool(write),data,mask)
            if addr in [0x20000100,0x20000104]:expected=counter_pre(c,addr)
            elif 0x20000000<=addr<=0x200000ff:expected=out['read_pre']
            else:expected=None
            if expected is not None:eq('independent MMIO read pre-edge',rd,expected)
            eq('independent write error',err,out['error_pre']);eq('normal software no reject',err,0)
            eq('UART post-edge',post_tx,out['tx_post']);eq('GPIO post-edge',post_gpio,out['gpio_post'])
            ea=int(write and addr==0x2000000c and mask==15);eq('actual GPIO core accept',accept,ea)
            if accept:gpio.append((c,data&255))
            samples.append(post_tx)
            if 0x20000000<=addr<=0x20000107:bus[c]=dict(addr=addr,write=write,data=data,mask=mask,expected=expected)
            if expected is not None:read_at[c]=expected
    eq('bus captured through tail',max_bus,metrics['physical'])
    frames=decode_frames(samples,n);eq('all public starts vs independently accepted events',frames,model.accepts)
    io_reads=[];io_writes=[];timer_reads=[];phases=[];timer_stores=[];counts={k:0 for k in ['EX','WB','READ','STORE']}
    art=None if name=='baseline' else next(x for x in s.read(H/'build-result.json')['artifacts'] if x['id']==name)
    if name=='baseline':image=(s.OLD.parent/'build/soc.bin').read_bytes();symbols=s.read(s.OLD.parent/'firmware-artifacts.json')['symbols']
    else:image=(H/'build'/name/'program.bin').read_bytes();symbols=art['symbols']
    with (d/'trace.log').open(encoding='ascii') as f:
        last=0
        for line in f:
            a=line.strip().split('|');kind=a[0];assert kind in counts
            assert not any(re.search('[xz]',v,re.I) for v in a[1:]),'unknown architectural event'
            c=int(a[1]);assert last<=c<=metrics['physical'];last=c;counts[kind]+=1
            if kind in ['EX','WB']:assert c%2==0
            else:
                assert c%2==(1 if kind=='STORE' else 0)
                pc,addr=int(a[2],16),int(a[3],16)
                if 0x20000000<=addr<=0x20000107:
                    assert c in bus and bus[c]['addr']==addr
                    if kind=='READ':
                        io_reads.append((pc,addr,read_at[c],c))
                        if addr in [0x20000100,0x20000104]:timer_reads.append(dict(pc=pc,address=addr,cycle=c,expected=counter_pre(c,addr),actual=int(a[4],16)))
                    else:
                        eq('actual IO write asserted',bus[c]['write'],1);eq('actual IO write data',int(a[4],16),bus[c]['data']);eq('actual IO mask',int(a[5],16),bus[c]['mask'])
                        io_writes.append((c,addr,int(a[4],16),int(a[5],16)))
                        if addr>=0x20000100:timer_stores.append(c)
                if kind=='STORE' and addr==symbols.get('timing_phase',-1):phases.append((c,int(a[4],16)))
    cursor=0
    def io_read(pc,addr):
        nonlocal cursor
        assert cursor<len(io_reads),'oracle requested missing MMIO read'
        p,a,value,c=io_reads[cursor];cursor+=1;assert (pc,addr)==(p,a),'oracle PC/address differs from sample'
        return value
    ref=Reference(image,io_read,lambda *args:None)
    class Stream:
        def __init__(self,kind):self.f=(d/'trace.log').open(encoding='ascii');self.kind=kind;self.count=0;self.digest=hashlib.sha256()
        def append(self,expected):
            for line in self.f:
                a=line.strip().split('|');k=a[0]
                if (self.kind=='MEM' and k in ['READ','STORE']) or k==self.kind:
                    actual=([k]+a[2:]) if self.kind=='MEM' else a[2] if k=='EX' else a[2:]
                    if actual!=expected and len(errors)<32:errors.append(dict(kind='ordered '+self.kind,index=self.count,actual=actual,expected=expected))
                    self.count+=1;self.digest.update((json.dumps(actual,separators=(',',':'))+'\n').encode());return
            raise AssertionError('missing '+self.kind+' event')
        def finish(self):
            for line in self.f:
                k=line.split('|',1)[0]
                assert not ((self.kind=='MEM' and k in ['READ','STORE']) or k==self.kind),'extra '+self.kind+' event'
            self.f.close()
        def __len__(self):return self.count
    ref.EX=Stream('EX');ref.WB=Stream('WB');ref.MEM=Stream('MEM')
    while not ref.stopped:ref.step()
    for x in [ref.EX,ref.WB,ref.MEM]:x.finish()
    eq('all MMIO samples consumed',cursor,len(io_reads))
    actual_regs=[int(v,16) for v in (d/'registers.hex').read_text().split()]
    actual_ram=bytes(int(v,16) for v in (d/'ram.hex').read_text().split())
    eq('all RF',actual_regs,ref.regs);eq('all32K RAM',actual_ram,bytes(ref.ram));eq('main return',actual_regs[10],0);eq('restored stack',actual_regs[2],0x18000)
    eq('stall independent',metrics['stall'],ref.stall);eq('flush independent',metrics['flush'],ref.flush)
    eq('tail',metrics['tail'],32);expected_adv=len(ref.EX)+2*ref.flush+ref.stall+19
    eq('logical progression',metrics['advances'],expected_adv);eq('physical progression',metrics['physical'],2*expected_adv+1)
    eq('normal stop',re.findall(r'^STOP\|(\d+)\|([0-9a-f]{8})$',text,re.M),[('2',f'{ref.pc:08x}')]);eq('no FATAL','FATAL' in text,False)
    eq('no writes to read-only timer',timer_stores,[])
    def word(sym,offset=0,size=4):
        a=symbols[sym]-0x10000+offset;return int.from_bytes(ref.ram[a:a+size],'little')
    detail={}
    lows=[x for x in timer_reads if x['address']==0x20000100]
    if name=='baseline':
        manual=s.read(s.OLD.parent/'manual-expectations.json');eq('original manual results',[word('results',i*4) for i in range(12)],manual['expected_results'])
        eq('signature',word('signature'),manual['signature']);expected_bytes=manual['tx_bytes'];eq('original GPIO accepts',[v for c,v in gpio],manual['gpio_writes'])
        old=s.read(s.OLD/'runs'/tid.replace('baseline','system')/'checker-result.json')
        eq('old physical/stall/flush',metrics,old['metrics'])
        for filename in ['registers.hex','ram.hex']:eq('original '+filename+' unchanged result',s.sha(d/filename),s.sha(s.OLD/'runs'/tid.replace('baseline','system')/filename))
    elif name=='smoke':
        eq('manual checksum',word('checksum'),528);eq('manual signature',word('signature'),0x54494d31)
        stamps=[word('stamps',8*i,8) for i in range(4)];deltas=[word('deltas',8*i,8) for i in range(2)]
        eq('four low read samples',len(lows),4);eq('stamps independently sampled',stamps,[x['cycle']-1 for x in lows])
        eq('exact deltas',deltas,[stamps[1]-stamps[0],stamps[3]-stamps[2]])
        eq('monotonic',all(a<b for a,b in zip(stamps,stamps[1:])),True);eq('work larger than empty window',deltas[1]>deltas[0],True)
        expected_bytes=list(b'TIM1\r\n');detail=dict(stamps=stamps,deltas=deltas)
    else:
        plan=s.read(H/'manual-plan.json')['coremark'][name]
        a=symbols['ram_log']-0x10000;length=word('ram_log_count');assert length<4096
        report=bytes(ref.ram[a:a+length]);expected_bytes=list(report);report_text=report.decode('ascii')
        for field in ['seedcrc','crclist','crcmatrix','crcstate']:
            label='[0]'+field if field!='seedcrc' else field
            mm=re.findall(re.escape(label)+r'\s*:\s*0x([0-9a-f]{4})',report_text)
            eq('official '+field,mm,[f'{plan[field]:04x}'])
        for sym in ['port_error','ram_log_overflow','timer_error','timing_unavailable']:eq(sym,word(sym),0)
        for sym in ['timer_start_calls','timer_stop_calls','port_finished']:eq(sym,word(sym),1)
        eq('timing phase finished',word('timing_phase'),4);eq('phase order',[p for c,p in phases],[1,2,3,4])
        eq('four low read samples',len(lows),4)
        stamps=[word(x,0,8) for x in ['empty_start','empty_end','start_ticks','end_ticks']]
        eq('all raw timestamps',stamps,[x['cycle']-1 for x in lows]);delta=word('elapsed_ticks',0,8)
        eq('elapsed ticks independent difference',delta,stamps[3]-stamps[2]);eq('positive nonoverflow',0<delta<=0xffffffff,True)
        eq('short run validity warning retained','Must execute for at least 10 secs' in report_text,True)
        eq('no IO writes inside algorithm timer',[(c,a) for c,a,v,m in io_writes if stamps[2]<c<=stamps[3]+1],[])
        eq('UART entirely after phase3',all(c>phases[2][0] for c,a,v,m in io_writes if a==0x20000000),True)
        detail=dict(stamps=stamps,empty_window=stamps[1]-stamps[0],raw_ticks=delta,frequency_setting_hz=27000000,
            simulated_seconds_at_setting=delta/27000000,formal_score_valid=False,phases=phases,report_bytes=length)
        (d/'ram-output.txt').write_bytes(report)
    eq('public UART all bytes no dedup',[b for c,b in frames],expected_bytes)
    if frames:eq('last serial complete before end',frames[-1][0]+10*n<metrics['physical']-32,True)
    return dict(status='PASS' if not errors else 'FAIL',errors=errors,metrics=metrics,trace_counts=counts,
        streams={k:dict(count=len(x),sha256=x.digest.hexdigest().upper()) for k,x in [('EX',ref.EX),('WB',ref.WB),('MEM',ref.MEM)]},
        timer_reads=timer_reads,GPIO_actual= gpio,UART_frames=len(frames),detail=detail,
        limitations=['finite inputs; no true retirement PC or unified WB-STORE commit','short simulation not valid CoreMark score','no hardware evidence'])
if __name__=='__main__':
    result=check(sys.argv[1]);s.save(H/'runs'/sys.argv[1]/'check-result.json',result);print(json.dumps(result))
