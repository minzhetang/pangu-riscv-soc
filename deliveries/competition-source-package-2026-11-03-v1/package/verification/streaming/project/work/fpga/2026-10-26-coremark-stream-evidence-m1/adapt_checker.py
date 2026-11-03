from pathlib import Path
import difflib,json
H=Path('D:/A_FPGA_Comp/work/fpga/2026-10-26-coremark-stream-evidence-m1')
p=H/'check_coremark.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace('from peripheral_checker import ContractModel,decode_frames','from stream_io import open_stream\nfrom stream_peripherals import SparseModel,public_frames\nfrom audit_uart import expected_changes')
s=s.replace('def check(tid):\n    d=H/\'runs\'/tid;',"def check(tid,directory=None):\n    d=Path(directory) if directory is not None else H/'runs'/tid;")
s=s.replace('model=ContractModel(n);samples=[1];read_at={};bus={};gpio=[];prev=0;max_bus=0','sparse=SparseModel(n);model=sparse.model;last_pin=1;read_at={};bus={};gpio=[];prev=0;max_bus=0')
s=s.replace("with (d/'bus.log').open(encoding='ascii') as f:","with __import__('contextlib').closing(open_stream(d,'bus')) as f:")
a='''            while len(samples)<c:
                cycle=len(samples);out=model.step(cycle,1,0)
                eq('omitted UART sample must be high',out['tx_post'],1);samples.append(1)'''
assert a in s;s=s.replace(a,"            sparse.gap(c-1);last_pin=sparse.last_pin")
s=s.replace("samples[-1]","last_pin").replace('out=model.step(c,1,gin,addr,bool(write),data,mask)','out=sparse.step(c,gin,addr,bool(write),data,mask)').replace('samples.append(post_tx)','last_pin=post_tx')
s=s.replace("frames=decode_frames(samples,n);eq('all public starts vs independently accepted events',frames,model.accepts)","frames,changes,pin_detail=public_frames(d,n,metrics['physical']);eq('all public starts vs independently accepted events',frames,model.accepts)\n    eq('every actual UART transition',changes,expected_changes([c for c,b in model.accepts],[b for c,b in model.accepts],n))")
s=s.replace("with (d/'trace.log').open(encoding='ascii') as f:","with __import__('contextlib').closing(open_stream(d,'trace')) as f:")
s=s.replace("    cursor=0\n", "    bus.clear();read_at.clear()\n    cursor=0\n",1)
s=s.replace("self.f=(d/'trace.log').open(encoding='ascii')","self.f=open_stream(d,'trace')")
s=s.replace('actual=frozen_checks.from_actual(name,answer)','actual=frozen_checks.from_actual(name,answer,d)')
s=s.replace("    return answer\n","    answer['streaming']=dict(pin=pin_detail,idle_cycles_skipped=sparse.skipped,model_steps=sparse.stepped,no_per_clock_samples=True)\n    return answer\n")
assert ';samples=' not in s and 'samples.append' not in s
p.write_text(s,encoding='utf-8',newline='\n')
p=H/'frozen_checks.py';s=p.read_text(encoding='utf-8-sig').replace('def from_actual(name,result):', 'def from_actual(name,result,directory=None):').replace("d=H/'runs'/(name+'-N234');report=", "d=Path(directory) if directory is not None else H/'runs'/(name+'-N234');report=");p.write_text(s,encoding='utf-8',newline='\n')
# Audit input only: same independent original semantics, flexible run directory/stream iterators.
for n in ['audit_uart.py','audit_wave.py']:
    p=H/n;s=p.read_text(encoding='utf-8-sig')
    if n=='audit_uart.py':
        s=s.replace('def audit(tid,path=None):','def audit(tid,path=None,directory=None):').replace("d=H/'runs'/tid;p=", "d=Path(directory) if directory is not None else H/'runs'/tid;p=")
        s=s.replace("with (d/'trace.log').open(encoding='ascii') as f:","with __import__('contextlib').closing(__import__('stream_io').open_stream(d,'trace')) as f:")
    p.write_text(s,encoding='utf-8',newline='\n')
for n in ['check_coremark.py','frozen_checks.py','audit_uart.py','audit_wave.py']:
    before=(H/'before'/n).read_text(encoding='utf-8-sig');after=(H/n).read_text(encoding='utf-8-sig');(H/(n+'.patch')).write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before/'+n,tofile=n)),encoding='utf-8')
print('Checker input/UART-only adapters created; ISA model and 13 RTL unchanged; no DUT run')

