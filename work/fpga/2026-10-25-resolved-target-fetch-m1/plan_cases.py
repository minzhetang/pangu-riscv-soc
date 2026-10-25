"""Frozen small programs and hand checks before DUT; not compiler-generated code."""
MASK=0xffffffff
def I(rd,rs,imm,f=0,op=0x13):return ((imm&4095)<<20)|(rs<<15)|(f<<12)|(rd<<7)|op
def U(rd,upper):return (upper<<12)|(rd<<7)|0x37
def B(rs1,rs2,off,f):
    v=off&8191;return ((v>>12)<<31)|(((v>>5)&63)<<25)|(rs2<<20)|(rs1<<15)|(f<<12)|(((v>>1)&15)<<8)|(((v>>11)&1)<<7)|0x63
def J(rd,off):
    v=off&0x1fffff;return ((v>>20)<<31)|(((v>>1)&1023)<<21)|(((v>>11)&1)<<20)|(((v>>12)&255)<<12)|(rd<<7)|0x6f
def S(rs,base,off):return (((off&4095)>>5)<<25)|(rs<<20)|(base<<15)|(2<<12)|((off&31)<<7)|0x23
class Program:
    def __init__(self):self.words={};self.pc=0;self.labels={};self.fix=[]
    def emit(self,w):assert self.pc not in self.words;self.words[self.pc]=w&MASK;self.pc+=4
    def label(self,n):assert n not in self.labels;self.labels[n]=self.pc
    def at(self,a):self.pc=a
    def const(self,rd,v):
        v&=MASK;s=v if v<0x80000000 else v-(1<<32)
        if -2048<=s<=2047:self.emit(I(rd,0,s))
        else:self.emit(U(rd,((v+0x800)>>12)&0xfffff));self.emit(I(rd,rd,v&4095))
    def branch(self,a,b,f,target):self.fix.append((self.pc,'B',(a,b,f,target)));self.emit(0)
    def jump(self,rd,target):self.fix.append((self.pc,'J',(rd,target)));self.emit(0)
    def stop(self):self.label('stop');self.emit(0x00100073)
    def image(self):
        for pc,k,args in self.fix:
            if k=='B':a,b,f,t=args;self.words[pc]=B(a,b,self.labels[t]-pc,f)
            else:rd,t=args;self.words[pc]=J(rd,self.labels[t]-pc)
        data=bytearray(32768)
        for a,w in self.words.items():assert a%4==0 and a+4<=len(data);data[a:a+4]=w.to_bytes(4,'little')
        return bytes(data)
def cases():
    out=[]
    def add(cid,p,regs,mem,flush,stall=0,data=None,kind=2,stop=None,reset=False):
        image=p.image();sp=p.labels.get('stop') if stop is None else stop
        assert sp is not None
        out.append(dict(id=cid,image=image,manual_registers={str(k):v&MASK for k,v in regs.items()},manual_memory={str(k):v&MASK for k,v in mem.items()},
            expected_flush=flush,expected_stall=stall,initial_data=data or {},stop_kind=kind,stop_pc=sp,reset_pending=reset,
            instructions=[dict(pc=a,word=f'{w:08x}') for a,w in sorted(p.words.items())]))
    def select(cid,f,a,b,take,load=None,path=None):
        p=Program();p.const(20,0x10000);p.const(1,a);p.const(2,b)
        p.branch(1,2,f,'taken');p.emit(I(10,0,0x11));p.emit(S(10,20,0));p.jump(0,'stop')
        p.label('taken');p.emit(I(10,0,0x22));p.emit(S(10,20,0));p.stop()
        add(cid,p,{10:0x22 if take else 0x11},{0:0x22 if take else 0x11},1)
    for f,name,a,b in [(0,'beq',1,1),(1,'bne',1,2),(4,'blt',-1,0),(5,'bge',0,-1),(6,'bltu',0,-1),(7,'bgeu',-1,0)]:
        select(name+'-taken',f,a,b,True)
        aa,bb=(1,2) if f==0 else (1,1) if f==1 else (b,a)
        select(name+'-not-taken',f,aa,bb,False)
    p=Program();p.const(20,0x10000);p.const(1,3);p.const(10,0);p.label('loop');p.emit(I(10,10,1));p.emit(I(1,1,-1));p.branch(1,0,1,'loop');p.emit(S(10,20,0));p.stop();add('finite-backward-loop',p,{1:0,10:3},{0:3},2)
    p=Program();p.const(20,0x10000);p.branch(0,0,5,'next');p.label('next');p.emit(I(10,0,7));p.emit(S(10,20,0));p.stop();add('taken-PC-plus4',p,{10:7},{0:7},1)
    p=Program();p.const(20,0x10000);link=p.pc+4;p.jump(1,'target');p.emit(S(0,20,0));p.at(0x40);p.label('target');p.emit(I(10,1,1));p.emit(S(10,20,0));p.stop();add('jal-link-first-target',p,{1:link,10:link+1},{0:link+1},1)
    p=Program();p.const(20,0x10000);p.const(5,0x41);link=p.pc+4;p.emit(I(5,5,0,op=0x67));p.emit(S(0,20,0));p.at(0x40);p.emit(I(10,5,2));p.emit(S(10,20,0));p.stop();add('jalr-rd-equals-rs1-lowbit',p,{5:link,10:link+2},{0:link+2},1)
    p=Program();p.const(20,0x10000);p.emit(I(5,20,0,2,3));link=p.pc+4;p.emit(I(1,5,0,op=0x67));p.emit(S(0,20,4));p.at(0x40);p.emit(S(1,20,4));p.emit(I(10,1,0));p.stop();add('load-jalr',p,{1:link,10:link},{4:link},1,1,{0:0x40})
    for name,rs1,rs2,f,initial,take in [('both',5,5,0,42,True),('rs1',5,0,1,42,True),('rs2',0,5,5,1,False)]:
        p=Program();p.const(20,0x10000);p.emit(I(5,20,0,2,3));p.branch(rs1,rs2,f,'taken');p.emit(I(10,0,0x11));p.emit(S(10,20,4));p.jump(0,'stop');p.label('taken');p.emit(I(10,0,0x22));p.emit(S(10,20,4));p.stop();value=0x22 if take else 0x11;add('load-branch-'+name,p,{10:value},{4:value},1,1,{0:initial})
    for cid,latest in [('WB-ID-source',False),('newest-producer',True)]:
        p=Program();p.const(20,0x10000)
        if latest:p.const(5,1);p.const(5,-1)
        else:p.const(5,-1);p.const(6,1);p.const(7,2)
        p.branch(5,0,5,'taken');p.emit(I(10,0,0x11));p.emit(S(10,20,0));p.jump(0,'stop');p.label('taken');p.emit(I(10,0,0x22));p.emit(S(10,20,0));p.stop();add(cid,p,{5:-1,10:0x11},{0:0x11},1)
    for cid,a,b,wbid in [('EX-rs1',-1,0,False),('WB-rs2',0,1,False),('WB-ID-rs2',0,1,True)]:
        p=Program();p.const(20,0x10000);p.const(2,b)
        if wbid:p.const(6,1);p.const(7,2)
        else:p.const(1,a)
        p.branch(1 if not wbid else 0,2,5,'taken');p.emit(I(10,0,0x11));p.emit(S(10,20,0));p.jump(0,'stop');p.label('taken');p.emit(I(10,0,0x22));p.emit(S(10,20,0));p.stop();add(cid,p,{10:0x11},{0:0x11},1)
    p=Program();p.const(20,0x10000);p.const(10,0x33);p.emit(S(10,20,0));p.jump(0,'target');p.emit(S(0,20,0));p.at(0x40);p.label('target');p.emit(I(11,20,0,2,3));p.emit(I(12,11,1));p.emit(S(12,20,4));p.stop();add('older-store-target-load',p,{11:0x33,12:0x34},{0:0x33,4:0x34},1,1)
    p=Program();p.const(20,0x10000);link=p.pc+4;p.jump(1,'function');p.emit(I(10,1,2));p.emit(S(10,20,0));p.jump(0,'stop');p.at(0x40);p.label('function');p.jump(0,'inner');p.emit(S(0,20,0));p.label('inner');p.emit(I(0,1,0,op=0x67));p.stop();add('consecutive-jump-return',p,{1:link,10:link+2},{0:link+2},4)
    p=Program();p.const(20,0x10000);p.emit(I(0,20,0,2,3));p.branch(0,0,5,'target');p.emit(S(0,20,4));p.emit(0x00000073);p.emit(0x00100073);p.at(0x40);p.label('target');p.emit(I(10,0,0x22));p.emit(S(10,20,4));p.stop();add('load-x0-wrong-path-stops',p,{0:0,10:0x22},{4:0x22},1,0,{0:MASK})
    p=Program();p.const(20,0x10000);p.const(10,5);p.jump(0,'target');p.emit(S(0,20,0));p.at(0x1000);p.label('target');p.emit(I(0,0,0));p.emit(S(10,20,0));p.stop();add('cross-bank-target-legitimate-NOP',p,{10:5,0:0},{0:5},1)
    for cid,target in [('unmapped-target',0x8000),('misaligned-target',0x102),('mapped-zero-target',0x100)]:
        p=Program();p.const(20,0x10000);p.const(5,4);p.emit(S(5,20,0));p.const(6,target);p.emit(I(0,6,0,op=0x67));p.emit(0x00100073);add(cid,p,{5:4},{0:4},1,kind=3,stop=target)
    p=Program();p.const(20,0x10000);p.const(5,4);p.emit(S(5,20,0));p.jump(0,'target');p.emit(S(0,20,0));p.at(0x40);p.label('target');p.label('stop');p.emit(0x00000073);add('target-ECALL-drain',p,{5:4},{0:4},1,kind=1)
    p=Program();p.jump(0,'target');p.emit(0x00000073);p.at(0x20);p.label('target');p.const(20,0x10000);p.const(10,7);p.emit(S(10,20,0));p.stop();add('reset-between-request-apply',p,{10:7},{0:7},1,reset=True)
    assert len(out)==34 and len({x['id'] for x in out})==34
    return out
