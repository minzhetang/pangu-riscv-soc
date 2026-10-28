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
check()
assert not ctypes.windll.shell32.IsUserAnAdmin()
assert all(sha(Path(x['path']))==x['SHA256'] for x in read(H/'PROTECTED_ORIGINALS.json')['files'])
c=read(H/'COUNTERS.json');assert not c['first_failure'] and c['Inserter_CLI_used']==0 and c['PDS_used']==0
inputs=[H/'scripts/probe.tcl',H/'ins-input/board_top_syn.adf',H/'host_supervisor.py',H/'stage_budget.py',Path(__file__)]
save('PROBE_FROZEN_INPUTS.json',dict(files=[dict(path=str(p.relative_to(H)),SHA256=sha(p)) for p in inputs]))
c['Inserter_CLI_used']=1;(H/'COUNTERS.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
argv=['D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe','-batch',str(H/'scripts/probe.tcl')]
save('PROBE_ATTEMPT.json',dict(argv=argv,cwd=str(H/'ins-input'),seconds=60,GUI_expected=False,only_new_process_visible_window_guard=True,hardware='STOPPED'))
try:
    result=bounded(argv,H/'ins-input','inserter-probe-01',60,cap=4*1024**3)
    log=(H/'logs/inserter-probe-01/stdout.log').read_text(encoding='utf-8',errors='replace')
    assert all(t in log for t in ['A_INS_PROBE_BEGIN','A_INS_NETS_BEGIN','A_INS_NETS_END','A_INS_PROBE_END']),'SCRIPT_OR_NETLIST_NOT_COMPLETED'
    assert all(sha(H/x['path'])==x['SHA256'] for x in read(H/'PROBE_FROZEN_INPUTS.json')['files'])
    assert all(sha(Path(x['path']))==x['SHA256'] for x in read(H/'PROTECTED_ORIGINALS.json')['files'])
    save('PROBE_RESULT.json',dict(status='CLI_SCRIPT_COMPLETED_NETLIST_PARSE_PENDING',native_rc=result['returncode'],native_calls_used=1,hardware='STOPPED'))
    print('Inserter probe exited; parse actual network list next')
except Exception as e:
    c['first_failure']=True;(H/'COUNTERS.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
    save('PROBE_RESULT.json',dict(status='FIRST_INTERFACE_OR_LOAD_FAILURE_STOPPED',error_type=type(e).__name__,error=str(e)[:250],native_calls_used=1,PDS_used=0,hardware='STOPPED',retry=False))
    print('First interface/load failure retained; no retry or GUI fallback')
    raise
