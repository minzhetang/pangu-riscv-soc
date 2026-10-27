from pathlib import Path
import sys,time,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tool-copy/src'));import support
out=Path(sys.argv[sys.argv.index('--out')+1]);hold=bytearray(32*1024**2)
for i in range(0,len(hold),4096):hold[i]=1
# A fixed resource-only fixture: not a compare or CPU correctness result.
time.sleep(.8)
r=dict(kind='B_VERIFY_OFFLINE_WORKER',case_id='A-active-memory-guard',ABI=support.ABI,CPU_function_proven=False,new_DUT=0,status='MATCH',native_rc=0,fully_consumed=True,checked=8,expected_records=8,actual_records=8,mismatch_count=0,differences=[],neighbors=[],first_difference=None,worker_reported_peak_bytes=support.peak_working_set())
support.dump_json(out/'worker-result.json',r);print('RESOURCE_FIXTURE_END');raise SystemExit(0)
