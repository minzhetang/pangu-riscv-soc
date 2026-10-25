from pathlib import Path
import json,re,sys,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'models'))
import stage_board as s
from cpu_program_reference import Reference
from peripheral_checker import ContractModel,decode_frames
def data_row(line):
    a=line.strip().split('|');assert len(a)==17 and a[0]=='EDGE'
    assert not any(re.search('[xz]',v,re.I) for v in a[1:]),'unknown public/timer data'
    decimal={1,4,8,9,11,13,14}
    return [int(v,10 if i in decimal else 16) for i,v in enumerate(a[1:],1)]

def counter_pre(c,address):
    assert c>=1
    return ((c-1)>>(32 if address==0x20000104 else 0))&0xffffffff

def check(tid):
    d=H/'runs'/tid;name,ns=tid.split('-N');n=int(ns);k=s.read(H/'manual-plan.json')['cases'][tid]['key_pattern'];errors=[]
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
                cycle=len(samples);out=model.step(cycle,1,k)
                eq('omitted UART sample must be high',out['tx_post'],1);samples.append(1)
            eq('GPIO frozen input',gin,k)
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
    io_reads=[];io_writes=[];timer_reads=[];phases=[];phase_init_pcs=[];timer_stores=[];counts={k:0 for k in ['EX','WB','READ','STORE']}
    art=s.read(H/'firmware-result.json');image=Path(art['program_bin']).read_bytes();symbols=art['symbols']
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
                if kind=='STORE' and addr==symbols.get('timing_phase',-1):
                    value=int(a[4],16);phases.append((c,value))
                    if value==0:phase_init_pcs.append(pc)
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
    plan=s.read(H/'manual-plan.json')['cases'][tid]
    eq('hand results',[word('results',i*4) for i in range(8)],plan['results'])
    eq('hand signature',word('signature'),plan['signature'])
    eq('GPIO every accepted write',[v for c,v in gpio],plan['GPIO_writes'])
    expected_bytes=plan['UART_bytes'];detail=dict(key_pattern=k)
    eq('public UART all bytes no dedup',[b for c,b in frames],expected_bytes)
    if frames:eq('last serial complete before end',frames[-1][0]+10*n<metrics['physical']-32,True)
    return dict(status='PASS' if not errors else 'FAIL',errors=errors,metrics=metrics,trace_counts=counts,
        streams={k:dict(count=len(x),sha256=x.digest.hexdigest().upper()) for k,x in [('EX',ref.EX),('WB',ref.WB),('MEM',ref.MEM)]},
        timer_reads=timer_reads,GPIO_actual= gpio,UART_frames=len(frames),detail=detail,
        limitations=['finite inputs; no true retirement PC or unified WB-STORE commit','short simulation not valid CoreMark score','no hardware evidence'])
