from pathlib import Path
import json,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
from host_supervisor import bounded
H=Path(__file__).resolve().parent
assert json.loads((H/'HELP-attempt.json').read_text())['queries']==4
assert not (H/'WAIT_QUERY-attempt.json').exists()
(H/'WAIT_QUERY-attempt.json').write_text(json.dumps(dict(queries=2,total_queries=6,maximum=6,scope='READONLY_TCL_CAPABILITY_CHECK_NO_DESIGN_BUILD',timeout_seconds=30)),encoding='utf-8')
r=bounded(['D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe','-file',str(H/'scripts/wait-query.tcl')],H/'pds','readonly-wait-query',30,cap=1024**3)
t=(H/'logs/readonly-wait-query/stdout.log').read_text(errors='replace')
assert 'A_HAS_INCR=incr' in t and 'A_BOUNDED_WAIT_COUNT=2' in t and 'A_R2_WAIT_QUERY_END' in t
(H/'WAIT_QUERY_RESULT.json').write_text(json.dumps(dict(status='PASS',native_rc=r['returncode'],queries_total=6,actual_bounded_while_after_incr=True,no_design_build=True,hardware='STOPPED'),indent=2)+'\n',encoding='utf-8')
