"""A pipeline-specific negative controls, not B's generic QA matrix."""
from pathlib import Path
import sys,json,shutil,time,copy
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-25-coremark-iter2-m1'
from stream_io import Archiver,open_stream,save,LINE
import stream_io
import check_coremark as c
from stage_coremark import read
rows=[]
def rejected(label,fn):
    try:
        got=fn();ok=isinstance(got,dict) and got.get('status')=='FAIL'
        why=str(got.get('errors',[]))[:300] if isinstance(got,dict) else 'did not reject'
    except (AssertionError,ValueError,OSError,KeyError,UnicodeError) as exc:ok=True;why=type(exc).__name__+': '+str(exc)[:300]
    assert ok,label+' accepted'
    rows.append(dict(id=label,status='EXPECTED_REJECT',reason=why));print(label,'REJECTED',flush=True)

def archive_controls():
    d=H/'controls/archive-good';d.mkdir();(d/'spool').mkdir();arch=Archiver(d)
    chunks=[]
    with (B/'runs/performance-N234/trace.log').open('rb') as f:
        for _ in range(32769):chunks.append(f.readline())
    source=b''.join(chunks)
    for seq,raw in [(0,b''.join(chunks[:32768])),(1,chunks[-1])]:
        p=d/'spool'/f'trace-{seq:06d}.log';p.write_bytes(raw)
        arch.consume(f'SEGMENT|trace|{seq}|{32768 if seq==0 else 1}|spool/trace-{seq:06d}.log')
    with (B/'runs/performance-N234/bus.log').open('rb') as f:bus=f.readline()
    (d/'spool/bus-000000.log').write_bytes(bus);arch.consume('SEGMENT|bus|0|1|spool/bus-000000.log')
    arch.consume('END_STREAM|trace|2|32769');arch.consume('END_STREAM|bus|1|1');arch.finish()
    assert ''.join(open_stream(d,'trace')).encode('ascii')==source and ''.join(open_stream(d,'bus')).encode('ascii')==bus
    rows.append(dict(id='archive-positive-two-segments',status='PASS',records=32769,byte_for_byte=True,not_DUT=True))
    for label in ['index-damage','payload-damage']:
        bad=H/'controls'/label;shutil.copytree(d,bad)
        specs=read(bad/'streams.json')
        for k in specs:specs[k]['path']=str(bad/'archive'/k)
        (bad/'streams.json').write_text(json.dumps(specs),encoding='utf-8')
        q=bad/'archive/trace'/'stream-index.json' if label=='index-damage' else bad/'archive/trace/000000/block-000000.gz'
        data=bytearray(q.read_bytes());data[len(data)//2]^=1;q.write_bytes(data)
        rejected(label,lambda:list(open_stream(bad,'trace')))
    for label,line in [('missing-ready','END_STREAM|trace|1|32768'),('reordered-ready','SEGMENT|trace|1|1|spool/trace-000001.log'),('duplicate-end','END_STREAM|trace|0|0')]:
        bd=H/'controls'/label;bd.mkdir();(bd/'spool').mkdir();a=Archiver(bd)
        if label=='duplicate-end':a.consume(line)
        rejected(label,lambda:a.consume(line))
    bad=H/'controls/line-overflow';bad.mkdir();(bad/'raw.log').write_bytes(b'X'*256+b'\n')
    (bad/'streams.json').write_text(json.dumps(dict(trace=dict(mode='raw',path=str(bad/'raw.log'),complete=True))),encoding='utf-8')
    rejected('line-overflow',lambda:list(open_stream(bad,'trace')))

def functional_controls():
    d=H/'replays/performance-N234';base_open=c.open_stream
    tests=['missing-WB','extra-STORE','architectural-X','wrong-phase','wrong-timer']
    for label in tests:
        mutation=dict(done=False)
        def altered(directory,kind):
            touched=False;last_cycle=0
            for line in base_open(directory,kind):
                a=line.strip().split('|')
                if kind=='trace':last_cycle=int(a[1])
                if not touched:
                    hit=(kind=='trace' and a[0]=='WB' and label in ['missing-WB','architectural-X']) or (kind=='trace' and a[0]=='STORE' and a[3]=='00010800' and label=='wrong-phase') or (kind=='bus' and label=='wrong-timer')
                    if hit:
                        touched=True;mutation['done']=True
                        if label=='missing-WB':continue
                        if label=='architectural-X':a[3]='0000000x'
                        elif label=='wrong-phase':a[4]='00000001'
                        else:a[15]='0000000000000001'
                        line='|'.join(a)+'\n'
                yield line
            if kind=='trace' and label=='extra-STORE':
                mutation['done']=True;yield f'STORE|{last_cycle+1 if last_cycle%2==0 else last_cycle}|00000000|00010000|00000000|f\n'
        c.open_stream=altered
        try:rejected(label,lambda:c.check('performance-N234',d));assert mutation['done'],label+' not injected'
        finally:c.open_stream=base_open
    # Small copied result inputs, no historical raw log or expectations are edited.
    for label in ['wrong-stop','missing-serial','wrong-serial-time']:
        bd=H/'controls'/label;bd.mkdir()
        for n in ['streams.json','process.json','stdout.log','registers.hex','ram.hex','ram-output.txt','uart-pins.log']:shutil.copyfile(d/n,bd/n)
        if label=='wrong-stop':
            p=bd/'stdout.log';text=p.read_text(encoding='utf-8');assert 'STOP|2|' in text;p.write_text(text.replace('STOP|2|','STOP|1|'),encoding='utf-8')
        else:
            p=bd/'uart-pins.log';lines=p.read_text(encoding='ascii').splitlines(True);i=next(i for i,l in enumerate(lines) if int(l.split('|')[2])>0)
            if label=='missing-serial':lines.pop(i)
            else:
                a=lines[i].strip().split('|');a[1]=str(int(a[1])+1);lines[i]='|'.join(a)+'\n'
            p.write_text(''.join(lines),encoding='ascii')
        rejected(label,lambda:c.check('performance-N234',bd))

if __name__=='__main__':
    assert not sys.flags.optimize
    start=time.monotonic();archive_controls();functional_controls()
    save(H/'controls/negative-results.json',dict(status='PASS',rows=rows,host_seconds=time.monotonic()-start,new_DUT=0,mutations='new files or bounded actual-input iterator only; no expected values changed',not_B_generic_suite=True))
    print('Pipeline-specific controls passed',len(rows),flush=True)
