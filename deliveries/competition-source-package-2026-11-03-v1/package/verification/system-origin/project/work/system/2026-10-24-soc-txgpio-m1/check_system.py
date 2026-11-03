"""Candidate live checker; not live-tested until B integration.
Expected MMIO read values come from the independent clocked CONTRACT MODEL.
Observed READ timestamps qualify the environmental sampling point; DUT returned
read DATA is never fed into the reference to create expected values.
"""
from pathlib import Path
import json,re,sys
from itertools import zip_longest
sys.dont_write_bytecode=True
from peripheral_checker import ContractModel,decode_frames,require_equal
from cpu_program_reference import Reference
H=Path(__file__).resolve().parent
def check(directory,n):
    assert n in [16,234]
    directory=Path(directory);manual=json.loads((H/'manual-expectations.json').read_text())
    errors=[]
    def eq(label,actual,expected):
        if actual!=expected and len(errors)<64:
            if isinstance(actual,list) and isinstance(expected,list):
                i,a,b=next((i,a,b) for i,(a,b) in enumerate(zip_longest(actual,expected)) if a!=b)
                errors.append(dict(kind=label,index=i,actual=str(a)[:500],expected=str(b)[:500],actual_count=len(actual),expected_count=len(expected)))
            else:errors.append(dict(kind=label,actual=str(actual)[:500],expected=str(expected)[:500]))
    model=ContractModel(n);pin_before=1;gpio_before=0;samples=[1];reads={};bus_by_cycle={};gpio_actual=[]
    with (directory/'bus.log').open(encoding='ascii') as f:
        for expected_cycle,line in enumerate(f,1):
            a=line.strip().split('|');assert len(a)==15 and a[0]=='EDGE'
            assert not any(re.search('[xz]',s,re.I) for s in a[1:]),'unknown bus values'
            decimal=[1,4,8,9,11,13,14]
            vals={i:int(a[i],10 if i in decimal else 16) for i in range(1,15)}
            c,gin,addr,write,data,mask,rd,err,pre_tx,pre_gpio,post_tx,post_gpio,accept,stop=[vals[i] for i in range(1,15)]
            assert c==expected_cycle
            eq('external GPIO frozen schedule',gin,0 if c<16 else (0x3c if c<4096 else 0xc3))
            eq('UART pre-edge',pre_tx,pin_before);eq('GPIO pre-edge',pre_gpio,gpio_before)
            out=model.step(c,1,gin,addr,bool(write),data,mask)
            eq('MMIO read independent pre-edge',rd,out['read_pre']);eq('MMIO error independent pre-edge',err,out['error_pre'])
            eq('normal program must not reject writes',err,0)
            eq('UART post-edge',post_tx,out['tx_post']);eq('GPIO post-edge',post_gpio,out['gpio_post'])
            expected_accept=int(write and addr==0x2000000c and mask==15)
            eq('actual reviewed GPIO enable',accept,expected_accept)
            if accept:gpio_actual.append((c,data&255))
            pin_before=out['tx_post'];gpio_before=out['gpio_post'];samples.append(post_tx)
            reads[c]=out['read_pre'];bus_by_cycle[c]=dict(address=addr,write=write,data=data,mask=mask,stopped=stop)
    decoded=decode_frames(samples,n)
    eq('public pin frame bytes (no dedup)',[b for c,b in decoded],manual['tx_bytes'])
    eq('public starts vs independently accepted events',decoded,model.accepts)
    eq('GPIO accepted values (incl duplicate)',[v for c,v in model.gpio_accepts],manual['gpio_writes'])
    eq('actual GPIO enable stream',gpio_actual,model.gpio_accepts)
    EX=[];WB=[];MEM=[];io_reads=[]
    with (directory/'trace.log').open(encoding='ascii') as f:
        last_cycle=0
        for line in f:
            a=line.strip().split('|');kind=a[0];assert kind in ['EX','WB','READ','STORE']
            assert not any(re.search('[xz]',s,re.I) for s in a[1:]),'unknown CPU event'
            c=int(a[1]);assert c>=last_cycle and c in bus_by_cycle;last_cycle=c
            if kind=='EX':assert c%2==0;EX.append(a[2])
            elif kind=='WB':assert c%2==0;WB.append(a[2:])
            else:
                assert c%2==(1 if kind=='STORE' else 0)
                pc,addr=int(a[2],16),int(a[3],16)
                eq('trace/bus address',addr,bus_by_cycle[c]['address'])
                if kind=='READ' and 0x20000000<=addr<=0x200000ff:io_reads.append((pc,addr,reads[c]))
                if kind=='STORE':
                    eq('STORE bus write enable',bus_by_cycle[c]['write'],1)
                    eq('STORE bus data',int(a[4],16),bus_by_cycle[c]['data'])
                    eq('STORE bus mask',int(a[5],16),bus_by_cycle[c]['mask'])
                MEM.append([kind]+a[2:])
    cursor=0
    def reference_io_read(pc,addr):
        nonlocal cursor
        assert cursor<len(io_reads),'missing IO sample time'
        ep,ea,value=io_reads[cursor];cursor+=1
        assert (pc,addr)==(ep,ea),'oracle PC/address does not match independently qualified IO read'
        return value
    io_writes=[]
    def reference_io_write(pc,addr,data,mask):io_writes.append((addr,data,mask))
    ref=Reference((H/'build/soc.bin').read_bytes(),reference_io_read,reference_io_write)
    while not ref.stopped:ref.step()
    eq('all observed IO sampling points consumed',cursor,len(io_reads))
    eq('ordered EX PC (not retirement)',EX,ref.EX);eq('every ordered WB',WB,ref.WB);eq('ordered READ/STORE',MEM,ref.MEM)
    actual_regs=[int(x,16) for x in (directory/'registers.hex').read_text().split()]
    actual_ram=[int(x,16) for x in (directory/'ram.hex').read_text().split()]
    eq('full RF',actual_regs,ref.regs);eq('full32K RAM',actual_ram,list(ref.ram))
    import build_prepare as b
    symbols=b.elf.elf_symbols(H/'build/soc.elf')
    def ram_word(name,i=0):
        a=symbols[name]-0x10000+i*4;return int.from_bytes(bytes(actual_ram[a:a+4]),'little')
    eq('manual results',[ram_word('results',i) for i in range(12)],manual['expected_results'])
    eq('manual signature',ram_word('signature'),manual['signature']);eq('ABI main return',actual_regs[10],0)
    eq('stack restored',actual_regs[2],0x18000)
    # Must read original file-backed stdout, not a PASS substring handed by caller.
    log=(directory/'stdout.log').read_text(encoding='utf-8',errors='replace')
    mt=re.findall(r'^METRICS\|(.*)$',log,re.M);assert len(mt)==1
    metrics={k:int(v) for k,v in (s.split('=') for s in mt[0].split('|'))}
    eq('stall logical',metrics['stall'],ref.stall);eq('flush logical',metrics['flush'],ref.flush)
    eq('tail physical clocks',metrics['tail'],32)
    # Fixed F130 pipeline +32physical tail: old +7 with8tail becomes +19.
    expected_advances=len(ref.EX)+2*ref.flush+ref.stall+19
    eq('fixed phase logical progression',metrics['advances'],expected_advances)
    eq('two-phase physical progression',metrics['physical'],2*expected_advances+1)
    eq('all bus cycles',len(bus_by_cycle),metrics['physical'])
    eq('normal end marker','SYSTEM_ENDED_NOT_FUNCTIONAL_PASS' in log,True)
    eq('stop kind/PC',re.findall(r'^STOP\|(\d+)\|([0-9a-f]{8})$',log,re.M),[('2',f'{ref.pc:08x}')])
    eq('no FATAL','FATAL' in log,False)
    return dict(status='PASS' if not errors else 'FAIL',errors=errors,metrics=metrics,reference_stall=ref.stall,reference_flush=ref.flush,
        WB_events=len(WB),MEM_events=len(MEM),EX_PC_events=len(EX),public_UART_frames=decoded,GPIO_actual_events=gpio_actual,
        independent_MMIO_reads=len(io_reads),limitations=['not real retirement PC or unified WB-STORE commit order',
            'fixed memory and initial RF state; no hardware evidence'])
if __name__=='__main__':
    result=check(Path(sys.argv[1]),int(sys.argv[2]))
    with (Path(sys.argv[1])/'checker-result.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
