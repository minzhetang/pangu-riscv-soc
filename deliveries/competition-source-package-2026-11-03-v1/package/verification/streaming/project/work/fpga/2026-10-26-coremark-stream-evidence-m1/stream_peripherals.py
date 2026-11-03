"""No per-clock UART sample list. Sparse idle advance is restricted to GPIO0."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'models'))
from peripheral_checker import ContractModel
from audit_uart import decode,expected_changes

class SparseModel:
    def __init__(self,n):
        self.model=ContractModel(n);self.cycle=0;self.last_pin=1;self.skipped=0;self.stepped=0
    def gap(self,end):
        m=self.model
        assert end>=self.cycle and m.sync1==m.sync2==0,'only frozen GPIO0 may skip'
        while self.cycle<end and (m.active is not None or not m.ready):
            self.cycle+=1;out=m.step(self.cycle,1,0);self.stepped+=1
            assert out['tx_post']==1 and self.last_pin==1,'omitted UART must be high'
            self.last_pin=out['tx_post']
        if self.cycle<end:
            assert m.active is None and m.ready and self.last_pin==1
            self.skipped+=end-self.cycle;self.cycle=end
    def step(self,c,gin,addr,write,data,mask):
        assert gin==0 and c==self.cycle+1
        out=self.model.step(c,1,gin,addr,write,data,mask);self.cycle=c;self.last_pin=out['tx_post'];self.stepped+=1
        return out

def public_frames(d,n,last_cycle):
    changes=[];last_time=-1;last_bit=1;releases=reset_rows=0;epoch=None;rows=0;first_active=None
    p=Path(d)/'uart-pins.log'
    assert p.stat().st_size<=8*1024*1024
    with p.open(encoding='ascii') as f:
        for line in f:
            assert len(line)<=256 and line.endswith('\n')
            a=line.strip().split('|');assert len(a)==6 and a[0]=='PIN' and all(v in ['0','1'] for v in a[3:])
            t,c,clk,rst,bit=map(int,a[1:]);assert t>last_time;last_time=t;rows+=1
            if not rst:
                assert c==0 and bit==1;last_bit=1;reset_rows+=1;continue
            if c==0:
                releases+=1;assert bit==1 and clk==1;first_active=t-1+37037;continue
            assert clk==1 and bit!=last_bit and 1<=c<=last_cycle and first_active is not None
            candidate=t-(c-1)*37037
            if epoch is None:epoch=candidate
            assert epoch==candidate==first_active+1,'pin timestamp vs cycle'
            changes.append((c,bit));last_bit=bit
    assert releases==1 and reset_rows>=1
    frames=decode(changes,n,last_cycle)
    return frames,changes,dict(records=rows,transitions=len(changes),samples_list_allocated=False)

def selftest():
    items=[]
    for n in [8,16,234]:
        # Schedules exercise release, active, completion-old-ready and next-edge acceptance.
        schedule={1:(0x20000000,True,0x41,15),2:(0x20000000,True,0x41,15),2+10*n:(0x20000000,True,0x42,15),3+10*n:(0x20000000,True,0x42,15)}
        sparse=SparseModel(n);old=ContractModel(n);last=3+20*n+100
        for c in range(1,last+1):
            req=schedule.get(c,(0,False,0,0));expected=old.step(c,1,0,*req)
            must=c in schedule or expected['tx_post']==0 or sparse.last_pin==0 or c==last
            if must:
                sparse.gap(c-1);got=sparse.step(c,0,*req);assert got==expected,(n,c,got,expected)
                for attr in ['ready','gpio_out','sync1','sync2','active','accepts','gpio_accepts']:assert getattr(sparse.model,attr)==getattr(old,attr),(n,c,attr)
        assert sparse.model.accepts==[(2,0x41),(3+10*n,0x42)]
        items.append(dict(N=n,status='PASS',stepped=sparse.stepped,skipped=sparse.skipped,full_clock_reference=last))
        bad=SparseModel(n);bad.step(1,0,0,False,0,0);bad.step(2,0,0x20000000,True,0,15)
        try:bad.gap(3)
        except AssertionError:items.append(dict(N=n,negative='active low omitted',status='EXPECTED_REJECT'))
        else:raise AssertionError('active gap accepted')
    return dict(status='PASS',items=items,new_DUT=0)
