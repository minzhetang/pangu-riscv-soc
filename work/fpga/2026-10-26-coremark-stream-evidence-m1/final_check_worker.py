"""Post-exit functional check; never launches a simulator or compiler."""
from pathlib import Path
import sys,json,time,hashlib
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-25-coremark-iter2-m1'
from stream_io import open_stream,save
from stage_coremark import read,sha
from compile_once import protect
import check_coremark,audit_uart,audit_wave
if __name__=='__main__':
    assert not sys.flags.optimize
    d=H/'runs/performance-N234';start=time.monotonic()
    capture=read(d/'capture-result.json');assert capture['status']=='ARCHIVE_CAPTURE_COMPLETE_NOT_FUNCTIONAL_PASS'
    for x in read(H/'frozen-live-inputs.json')['files']:assert sha(x['path'])==x['SHA256'],x['path']
    result=check_coremark.check('performance-N234');save(d/'check-result.json',result)
    old=read(B/'runs/performance-N234/check-result.json')
    assert result['status']=='PASS' and json.loads(json.dumps({k:v for k,v in result.items() if k!='streaming'}))==old
    uart=audit_uart.audit('performance-N234');save(d/'uart-audit.json',uart)
    wave=audit_wave.audit('performance-N234');save(d/'wave-audit.json',wave)
    exact=[]
    for kind in ['trace','bus']:
        total=count=0;digest=hashlib.sha256()
        with (B/'runs/performance-N234'/(kind+'.log')).open('rb') as f:
            for line in open_stream(d,kind):
                actual=line.encode('ascii');assert actual==f.readline(),(kind,count)
                digest.update(actual);total+=len(actual);count+=1
            assert f.read(1)==b''
        exact.append(dict(kind=kind,status='BYTE_FOR_BYTE_EQUAL',records=count,raw_bytes=total,SHA256=digest.hexdigest().upper(),not_digest_only=True))
    for name in ['registers.hex','ram.hex','uart-pins.log','ram-output.txt']:
        assert (d/name).read_bytes()==(B/'runs/performance-N234'/name).read_bytes();exact.append(dict(file=name,status='BYTE_FOR_BYTE_EQUAL',bytes=(d/name).stat().st_size,SHA256=sha(d/name)))
    save(d/'strict-equality-result.json',dict(status='PASS',old_functional_summary_identical=True,evidence=exact,UART=uart,wave=wave,host_seconds=time.monotonic()-start,source_protected=protect(),no_new_DUT_in_this_checker=True,hardware='STOPPED',formal_score=False))
    print(json.dumps(dict(status='NEW_CAPTURE_FULL_FUNCTIONAL_AND_OLD_BYTE_EQUALITY_PASS',raw_ticks=result['detail']['raw_ticks'],frames=result['UART_frames'],physical=result['metrics']['physical'],host_seconds=time.monotonic()-start),ensure_ascii=False))
