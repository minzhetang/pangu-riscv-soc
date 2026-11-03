"""Offline byte-by-byte report parsing; never opens hardware or runs DUT."""
from pathlib import Path
import argparse,json,sys
sys.dont_write_bytecode=True
from check_report import check
P=Path(__file__).resolve().parents[1]
def main():
 a=argparse.ArgumentParser();a.add_argument('--output',required=True,type=Path);args=a.parse_args()
 d=args.output.resolve();d.mkdir(parents=True,exist_ok=False)
 cases=[('board/M4','idle',True),('board/M4/capture-normal','normal',False),('board/M4/capture-normal-r2','normal',True),('board/M4/capture-order','order',False),('board/M4/capture-order-r2','order',True),('board/M4/capture-timeout','timeout',False)]
 if (P/'evidence/board/M5/capture-timeout/uart-raw.bin').exists():
  # Replay preserves the recorded acceptance classification; it never changes
  # the frozen scenario's semantic expectations in check_report.check().
  cases.append(('board/M5/capture-timeout','timeout',False))
 if (P/'evidence/board/M5/capture-timeout-r2/uart-raw.bin').exists():
  cases.append(('board/M5/capture-timeout-r2','timeout',True))
 if (P/'evidence/board/M5/uart-raw.bin').exists():cases.append(('board/M5','idle',True))
 rows=[]
 for rel,case,expected in cases:
  h=P/'evidence'/rel;result=None
  try:result=check((h/'uart-raw.bin').read_bytes(),case,json.loads((h/'SERIAL_RESULT.json').read_text()));actual=True
  except Exception as e:result=dict(error=type(e).__name__+': '+str(e));actual=False
  rows.append(dict(source=rel,scenario=case,expected_checker_accept=expected,checker_accept=actual,expectation_matched=actual==expected,detail=result))
 ok=all(r['expectation_matched'] for r in rows)
 (d/'RESULT.json').write_text(json.dumps(dict(status='PASS_OFFLINE_REPLAY' if ok else 'FAIL',new_DUT_runs=0,rows=rows),ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(dict(status='PASS_OFFLINE_REPLAY' if ok else 'FAIL',records=len(rows),new_DUT_runs=0)));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
