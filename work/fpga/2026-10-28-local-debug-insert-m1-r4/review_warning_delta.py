from pathlib import Path
import json,collections,re
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-27-board-coremark8-bitstream-m1'
new=[s for s in (H/'build/flow.log').read_text(errors='replace').splitlines() if s.startswith('W: Public-4008')]
old=[s for s in (B/'pds/flow.log').read_text(errors='replace').splitlines() if s.startswith('W: Public-4008')]
added=list((collections.Counter(new)-collections.Counter(old)).elements());removed=list((collections.Counter(old)-collections.Counter(new)).elements())
assert len(new)==49 and len(old)==14 and len(added)==37 and len(removed)==2
debug=[s for s in added if 'u_CORES/' in s];cpu=[s for s in added if 'soc/cpu_core/eei_stop_' in s]
assert len(debug)==34 and len(cpu)==3
record=dict(status='CLASSIFIED_NOT_AUTOMATICALLY_WAIVED',old_count=14,new_count=49,net_increase=35,exact_new_messages=37,exact_removed_messages=removed,debug_namespace_new=debug,cpu_named_new=cpu,normalization='Old eei_stop_valid bmsWIDEDFFCPE vs new scalar GTP_DFF_C; old kind[1:0] bus cleanup vs two scalar kind bits',does_not_prove_sampling_source_correct=True,remaining='If these probes are used as evidence, verify actual mapped stop/error drivers; ordered FIC and register inventory alone do not prove per-channel physical fanin.')
with (H/'DANGLING_REVIEW.json').open('x',encoding='utf-8') as f:json.dump(record,f,indent=2);f.write('\n')
w=json.loads((H/'WARNINGS_AUDIT.json').read_text())
triage=dict(status='OPEN_NO_CONSTRAINT_OR_RTL_CHANGE',Place2028=1,Route2036=3,source='Tool-inserted SCANCHAIN/TCK1/CAPTUREDR/drck clock paths; not new user FDC edits',physical_clock_warning_waived=False,native_timing_summary='All Constraints Met under declared clocks; not a physical JTAG/CDC validation',generated_dedicated_route_false_attribute_observed=True,generated_attribute_not_user_edit=True,next='Read-only investigate documented debug-clock routing and actual source connectivity before any implementation acceptance or hardware stage')
with (H/'CRITICAL_TRIAGE.json').open('x',encoding='utf-8') as f:json.dump(triage,f,indent=2);f.write('\n')
print('4 critical warnings open; Public4008 14->49, exact-new37/removed2 classified, not waived')
