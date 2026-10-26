"""Explicit launch policy for assertion-based verification dependencies."""
from pathlib import Path
import sys,json,runpy
if sys.flags.optimize:
    sys.stderr.write('UNSUPPORTED_OPTIMIZED_PYTHON: verification assertions must remain enabled\n')
    raise SystemExit(2)
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
if len(sys.argv)!=2 or sys.argv[1] not in ['status','compile','capture','check']:
    sys.stderr.write('usage: python -B guarded_entry.py status|compile|capture|check\n');raise SystemExit(2)
operation=sys.argv[1]
if operation=='status':
    print(json.dumps(dict(status='ENTRY_POLICY_OK',optimization=sys.flags.optimize,compile_used=(H/'compile-attempt.json').exists(),DUT_used=(H/'DUT-attempt.json').exists(),note='Existing attempt markers prohibit repeating this stage')))
else:
    script={'compile':'compile_once.py','capture':'run_capture_once.py','check':'run_final_check.py'}[operation]
    sys.argv=[str(H/script)];runpy.run_path(str(H/script),run_name='__main__')
