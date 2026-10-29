from stage_coremark import *
import sys,time,re
from stage_budget import check
R=H.parent/"2026-10-25-coremark-iter2-m1"
sys.path.insert(0,str(H/"models"))
from cpu_program_reference import Reference
class Digest:
    def __init__(self,owner,kind):self.owner=owner;self.kind=kind;self.count=0;self.h=hashlib.sha256()
    def append(self,value):
        if self.kind=='EX':
            r=self.owner.ref
            # Before steps++ and before this instruction's redirect; current
            # load-use stall has already been accounted by the independent ISA.
            self.owner.ex_cycle=6+2*r.steps+2*r.stall+4*r.flush
        self.count+=1;self.h.update((json.dumps(value,separators=(',',':'))+'\n').encode())
    def __len__(self):return self.count
    def summary(self):return dict(count=self.count,sha256=self.h.hexdigest().upper())
class Scheduled:
    def __init__(self,image):
        self.ex_cycle=0;self.uart_last=None;self.gpio=0;self.io_reads=[];self.io_writes=[];self.timer_reads=[];self.start=time.monotonic()
        self.ref=Reference(image,self.read,self.write)
        for kind in ['EX','WB','MEM']:setattr(self.ref,kind,Digest(self,kind))
    def ready(self,c):return int(self.uart_last is None or c>self.uart_last+2340)
    def read(self,pc,address):
        c=self.ex_cycle+2
        if address in [0x20000100,0x20000104]:
            value=((c-1)>>(32 if address==0x20000104 else 0))&0xffffffff
            self.timer_reads.append(dict(pc=pc,address=address,cycle=c,expected=value,actual=value))
        elif address==0x20000008:value=self.ready(c)
        elif address==0x2000000c:value=self.gpio
        elif address in [0x20000000,0x20000010]:value=0
        else:raise AssertionError(('unmodelled IO read',hex(address)))
        self.io_reads.append([pc,address,c,value]);return value
    def write(self,pc,address,data,mask):
        c=self.ex_cycle+1;assert mask==15
        if address==0x20000000:assert self.ready(c);self.uart_last=c
        elif address==0x2000000c:self.gpio=data&255
        else:raise AssertionError(('unexpected IO write',hex(address)))
        self.io_writes.append([pc,address,c,data,mask])
    def run(self):
        while not self.ref.stopped:
            assert self.ref.steps<250000000
            if self.ref.steps%1024==0:assert time.monotonic()-self.start<1200
            self.ref.step()
        return self.ref
