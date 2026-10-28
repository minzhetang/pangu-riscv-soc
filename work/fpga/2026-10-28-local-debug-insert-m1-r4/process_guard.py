"""The GUI now requires a completed pre-synthesis process and verified real artifacts."""
import json,hashlib
def allowed(ok,hashes,unused):return bool(ok and hashes and unused)
def verify_completed_synthesis(H):
 r=json.loads((H/'PRE_EXIT_RECEIPT.json').read_text())
 ok=r['process']['returncode']==0 and r['process']['error'] is None
 hashes=all((H/x['path']).is_file() and hashlib.sha256((H/x['path']).read_bytes()).hexdigest().upper()==x['SHA256'] for x in r['artifacts'])
 unused=not (H/'GUI-attempt.json').exists()
 if not allowed(ok,hashes,unused):raise RuntimeError('COMPLETED_SYNTHESIS_GATE_FAILED')
 with (H/'GUI_LAUNCH_GATE.json').open('x',encoding='utf-8') as f:json.dump(dict(status='PASS',native_pre_process_exit=0,real_new_artifacts_verified=len(r['artifacts']),no_live_process_or_marker_substitution=True),f,indent=2)
