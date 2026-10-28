from pathlib import Path
import hashlib,json,ctypes,sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from stage_budget import check
from host_supervisor import bounded
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,o):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
check();assert not ctypes.windll.shell32.IsUserAnAdmin()
assert not (H/'logs').exists()
assert read(H/'PREPARATION_ERROR.json')['actual_vendor_invocations']==0
assert not (H/'NATIVE_START_01.json').exists()
assert all(sha(Path(x['path']))==x['SHA256'] for x in read(H/'PROTECTED_ORIGINALS.json')['files'])
assert all(sha(H/x['path'])==x['SHA256'] for x in read(H/'PROBE_FROZEN_INPUTS.json')['files'])
(H/'logs').mkdir()
argv=read(H/'PROBE_ATTEMPT.json')['argv']
save('NATIVE_START_01.json',dict(actual_Inserter_calls_reserved=1,max_Inserter=6,PDS_used=0,argv=argv,v2_resume_SHA256=sha(Path(__file__)),preparation_correction='PREPARATION_ERROR.json',hardware='STOPPED'))
try:
    result=bounded(argv,H/'ins-input','inserter-probe-01',60,cap=4*1024**3)
    log=(H/'logs/inserter-probe-01/stdout.log').read_text(encoding='utf-8',errors='replace')
    assert all(t in log for t in ['A_INS_PROBE_BEGIN','A_INS_NETS_BEGIN','A_INS_NETS_END','A_INS_PROBE_END']),'SCRIPT_OR_NETLIST_NOT_COMPLETED'
    assert all(sha(H/x['path'])==x['SHA256'] for x in read(H/'PROBE_FROZEN_INPUTS.json')['files'])
    assert all(sha(Path(x['path']))==x['SHA256'] for x in read(H/'PROTECTED_ORIGINALS.json')['files'])
    save('PROBE_RESULT_V2.json',dict(status='CLI_SCRIPT_COMPLETED_NETLIST_PARSE_PENDING',native_rc=result['returncode'],actual_Inserter_calls=1,PDS_used=0,hardware='STOPPED'))
    print('First actual Inserter probe exited; parse real net list next')
except Exception as e:
    save('PROBE_RESULT_V2.json',dict(status='FIRST_NATIVE_INTERFACE_OR_LOAD_FAILURE_STOPPED',error_type=type(e).__name__,error=str(e)[:250],actual_Inserter_calls=1,PDS_used=0,hardware='STOPPED',retry=False))
    print('First actual native/interface failure retained; no native retry or GUI fallback')
    raise
