"""Independent CONTRACT MODEL/checker, not B RTL and not a peripheral substitute.
Synthetic selftests prove checker behavior only. Future live observations must be
read from separately reviewed system monitor; no DUT data may set expected bytes.
"""
from dataclasses import dataclass,field
from pathlib import Path
import json,copy

@dataclass
class ContractModel:
    n:int
    ready:bool=False
    gpio_out:int=0
    sync1:int=0
    sync2:int=0
    active:object=None
    accepts:list=field(default_factory=list)
    gpio_accepts:list=field(default_factory=list)
    def step(self,cycle,reset_n,gpio_async,address=0,write=False,data=0,mask=0):
        assert self.n>=8 and all(isinstance(v,int) for v in [cycle,reset_n,gpio_async,address,data,mask])
        if not reset_n:
            self.ready=False;self.gpio_out=0;self.sync1=0;self.sync2=0;self.active=None
            return dict(read_pre=0,error_pre=0,tx_post=1,gpio_post=0,ready_post=0,sync_post=0)
        selected=0x20000000<=address<=0x200000ff;off=address&255
        read=0
        if selected and off%4==0:
            read={0:0,8:int(self.ready),12:self.gpio_out,16:self.sync2}.get(off,0)
        request=selected and write
        tx_accept=request and off==0 and mask==15 and self.ready
        gp_accept=request and off==12 and mask==15
        error=int(request and not(tx_accept or gp_accept))
        # Old ready decides acceptance, including the completion edge.
        if self.active is not None and cycle-self.active[0]>=10*self.n:
            self.active=None;self.ready=True
        elif self.active is None:self.ready=True
        if tx_accept:
            self.active=(cycle,data&255);self.ready=False;self.accepts.append((cycle,data&255))
        if gp_accept:
            self.gpio_out=data&255;self.gpio_accepts.append((cycle,data&255))
        self.sync2,self.sync1=self.sync1,gpio_async&255
        pin=1
        if self.active is not None:
            phase=(cycle-self.active[0])//self.n
            pin=0 if phase==0 else (((self.active[1]>>(phase-1))&1) if phase<=8 else 1)
        return dict(read_pre=read,error_pre=error,tx_post=pin,gpio_post=self.gpio_out,
            ready_post=int(self.ready),sync_post=self.sync2)

def decode_frames(samples,n):
    """Separate public-pin UART centre sampler, no reference-model state input."""
    assert n>=8 and all(x in (0,1) for x in samples)
    frames=[];i=1
    while i<len(samples):
        if samples[i-1]==1 and samples[i]==0:
            end=i+10*n
            assert end<=len(samples),'incomplete UART frame'
            assert samples[i+n//2]==0,'bad start'
            byte=sum(samples[i+(k+1)*n+n//2]<<k for k in range(8))
            assert samples[i+9*n+n//2]==1,'bad stop'
            frames.append((i,byte));i=end
        else:i+=1
    return frames

def require_equal(actual,expected):
    assert actual==expected,dict(actual=actual,expected=expected)

def selftest():
    checks=[]
    def check(label,ok):
        assert ok,label
        checks.append(label)
    for n in [8,16,234]:
        model=ContractModel(n);samples=[1];rows=[];expected=[]
        message=list(b'PG100 M1\r\nAA');accept_cycle=2;end=accept_cycle+len(message)*(10*n+1)+4
        schedule={accept_cycle+k*(10*n+1):b for k,b in enumerate(message)}
        for c in range(1,end):
            out=model.step(c,1,0x3c if c>=4 else 0,0x20000000,c in schedule,schedule.get(c,0),15 if c in schedule else 0)
            samples.append(out['tx_post']);rows.append(out)
        expected=list(schedule.items())
        check(f'N{n}:exact_public_pin_decode',decode_frames(samples,n)==expected)
        check(f'N{n}:accepted_all12_without_dedup',model.accepts==expected)
        check(f'N{n}:two_flipflop_timing',rows[3]['sync_post']==0 and rows[4]['sync_post']==0x3c)
        # Wrong data and an extra SAME byte must not pass merely by deduplication.
        wrong=samples.copy();p=expected[0][0]+n+n//2;wrong[p]^=1
        check(f'N{n}:wrong_byte_rejected',decode_frames(wrong,n)!=expected)
        extra=samples[:-4]+[1]+samples[expected[-1][0]:expected[-1][0]+10*n]+[1]*4
        check(f'N{n}:extra_duplicate_frame_rejected',decode_frames(extra,n)!=expected)
        bad_stop=samples.copy();bad_stop[expected[0][0]+9*n+n//2]=0
        try:decode_frames(bad_stop,n)
        except AssertionError:check(f'N{n}:bad_stop_rejected',True)
        else:raise AssertionError('bad stop accepted')
    m=ContractModel(8)
    first=m.step(1,1,0,0x20000000,True,0x41,15)
    check('release_first_edge_rejected',first['error_pre']==1 and m.accepts==[])
    m.step(2,1,0,0x20000000,True,0x41,15)
    for c in range(3,82):m.step(c,1,0)
    last=m.step(82,1,0,0x20000000,True,0x42,15)
    check('completion_old_ready_rejects',last['error_pre']==1 and last['ready_post']==1 and len(m.accepts)==1)
    m.step(83,1,0,0x20000000,True,0x42,15)
    check('next_edge_accepts',m.accepts[-1]==(83,0x42))
    m=ContractModel(16)
    for c,v in enumerate([0x5a,0x5a,0xa5],1):m.step(c,1,0,0x2000000c,True,v,15)
    check('GPIO_duplicate_transactions_preserved',m.gpio_accepts==[(1,0x5a),(2,0x5a),(3,0xa5)])
    m.step(4,1,0,0x2000000d,True,0xff,15)
    check('unaligned_GPIO_no_accept',len(m.gpio_accepts)==3 and m.gpio_out==0xa5)
    m.step(5,1,0,0x2000000c,True,0xff,1)
    check('partial_GPIO_no_accept',len(m.gpio_accepts)==3)
    good=[(1,0x5a),(2,0x5a),(3,0xa5)]
    for label,bad in [('missing',good[:1]+good[2:]),('extra',good+[good[-1]]),('wrong',[(1,0x5b)]+good[1:])]:
        try:require_equal(bad,good)
        except AssertionError:check('GPIO_'+label+'_rejected',True)
        else:raise AssertionError(label)
    return dict(status='PASS',synthetic_only=True,DUT_runs=0,checks=len(checks),items=checks,
        scope='contract model and separate serial decoder; NOT B module or full system validation')
if __name__=='__main__':
    result=selftest()
    with (Path(__file__).parent/'checker-selftest.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
