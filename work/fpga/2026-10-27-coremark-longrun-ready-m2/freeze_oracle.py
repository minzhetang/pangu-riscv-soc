from pathlib import Path
import json,sys
H=Path('work/fpga/2026-10-27-coremark-longrun-ready-m2').resolve();sys.path.insert(0,str(H))
from stage_coremark import read,save,sha
from stage_budget import check
from preserve import protect
check();protect()
p=H/'manual-plan.json';v=read(p);v['coremark']['performance8']=dict(v['coremark']['performance']);v['authorization_M2']='D160';p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
f=H/'frozen-case-plan.json';v=read(f);o=read(H/'oracles/performance8/expected.json');v['cases']['performance8-N234']=dict(phase_address=67584,expected_raw_ticks=o['raw_ticks'],expected_stamps=o['stamps'],expected_report_sha256=o['report_SHA256'],expected_UART_bytes=o['report_bytes'],oracle_SHA256=sha(H/'oracles/performance8/expected.json'),iterations=8,n=234);v['M2_limits']=dict(cycles=32000000,seconds=2400);f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
# Freeze immutable input artifacts before the one DUT; compile later pins all scripts too.
save(H/'oracle-freeze.json',dict(status='PREFROZEN_BEFORE_DUT',files=[dict(path=str(p.relative_to(H)),SHA256=sha(p)) for p in (H/'oracles/performance8').iterdir()],steps=o['steps'],cycles=o['expected_physical'],iterations=8,raw_ticks=o['raw_ticks'],new_DUT=0))
# -O guard is observed, not assumed; process must explicitly reject before tests.
import subprocess
r=subprocess.run([sys.executable,'-O','-B','-c','import stage_budget'],cwd=H,capture_output=True,timeout=10)
save(H/'controls/optimized-entry.json',dict(returncode=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),status='EXPECTED_REJECT' if r.returncode!=0 and b'optimized' in r.stderr.lower() else 'FAIL'));assert r.returncode!=0 and b'optimized' in r.stderr.lower()
print('Oracle and plans frozen before DUT; 555 originals protected; -O explicit reject')
