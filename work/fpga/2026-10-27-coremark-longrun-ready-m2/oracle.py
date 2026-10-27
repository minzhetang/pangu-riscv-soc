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
            assert self.ref.steps<25000000
            if self.ref.steps%1024==0:assert time.monotonic()-self.start<900
            self.ref.step()
        return self.ref
def run(case):
    baseline=False;name=case;assert name=='performance8';expected_iterations=8
    image=(B if baseline else H)/'build'/name/'program.bin';elf=image.with_suffix('.elf')
    symbols=elf_symbols(elf);assert initial_word(elf,symbols['seed4_volatile'])==expected_iterations
    s=Scheduled(image.read_bytes());r=s.run();d=H/'oracles'/case;d.mkdir(exist_ok=False)
    def word(sym,off=0,size=4):
        a=symbols[sym]-0x10000+off;return int.from_bytes(r.ram[a:a+size],'little')
    length=word('ram_log_count');a=symbols['ram_log']-0x10000;report=bytes(r.ram[a:a+length]);text=report.decode('ascii')
    assert re.findall(r'^Iterations\s*:\s*(\d+)\s*$',text,re.M)==[str(expected_iterations)]
    assert 'Must execute for at least 10 secs' in text and 'SIM ONLY, NO VALID SCORE' in text
    for sym in ['port_error','ram_log_overflow','timer_error','timing_unavailable']:assert word(sym)==0
    for sym in ['timer_start_calls','timer_stop_calls','port_finished']:assert word(sym)==1
    assert r.regs[10]==0 and r.regs[2]==0x18000 and word('timing_phase')==4
    stamps=[word(n,0,8) for n in ['empty_start','empty_end','start_ticks','end_ticks']];delta=word('elapsed_ticks',0,8);assert delta==stamps[3]-stamps[2] and 0<delta<270000000
    assert [t['actual'] for t in s.timer_reads if t['address']==0x20000100]==stamps
    phase3_addr=symbols['timing_phase'];phase_writes=[]
    # RAM phase stores are in the independent MEM digest; final phase checked
    # now and actual per-store phase sequence remains a separate live check.
    (d/'expected-ram.bin').write_bytes(bytes(r.ram));(d/'expected-registers.hex').write_text(''.join(f'{v:08x}\n' for v in r.regs),encoding='ascii');(d/'expected-report.txt').write_bytes(report)
    final_crc=re.findall(r'^\[0\]crcfinal\s*:\s*0x([0-9a-f]{4})\s*$',text,re.M);assert len(final_crc)==1
    result=dict(status='PREFROZEN_REFERENCE_ONLY',case=case,baseline_replay=baseline,iterations=expected_iterations,image_SHA256=sha(image),ELF_SHA256=sha(elf),steps=r.steps,stop_pc=r.pc,stall=r.stall,flush=r.flush,streams={k:getattr(r,k).summary() for k in ['EX','WB','MEM']},timer_reads=s.timer_reads,io_reads=s.io_reads,io_writes=s.io_writes,stamps=stamps,raw_ticks=delta,expected_physical=2*(r.steps+2*r.flush+r.stall+19)+1,report_bytes=length,report_SHA256=sha(d/'expected-report.txt'),RAM_SHA256=sha(d/'expected-ram.bin'),RF_SHA256=sha(d/'expected-registers.hex'),crcfinal=final_crc[0],host_seconds=round(time.monotonic()-s.start,6),native_DUT_runs=0,limited_schedule='F143 SYNC_MEMORY1: EX6 then2 physical ticks, load-use+2, redirect+4, READ EX+2 and STORE EX+1; independently calibrated on two old F143 traces/states',hardware=False)
    if baseline:
        old=B/'runs'/(name+'-N234');check=read(old/'check-result.json')
        assert result['streams']==check['streams']
        assert result['raw_ticks']==check['detail']['raw_ticks'] and result['stamps']==check['detail']['stamps']
        assert result['expected_physical']==check['metrics']['physical']
        assert result['timer_reads']==check['timer_reads']
        assert report==(old/'ram-output.txt').read_bytes()
        actual_ram=bytes(int(v,16) for v in (old/'ram.hex').read_text().split());assert actual_ram==bytes(r.ram)
        actual_rf=[int(v,16) for v in (old/'registers.hex').read_text().split()];assert actual_rf==r.regs
        result['calibration']='PASS_OLD_TRACE_DIGEST_ALL_STATE_TIME_REPORT_NO_NEW_DUT'
    else:
        old=read(R/'oracles'/'performance'/'expected.json');result['calibration_source_SHA256']=sha(R/'oracles'/'performance'/'expected.json')
    save(d/'expected.json',result)
    print(json.dumps({k:result[k] for k in ['case','steps','raw_ticks','expected_physical','report_bytes','crcfinal','host_seconds','native_DUT_runs']}),flush=True)
if __name__=="__main__":check();run("performance8");check()
