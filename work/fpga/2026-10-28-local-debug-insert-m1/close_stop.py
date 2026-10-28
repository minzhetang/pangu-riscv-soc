from pathlib import Path
import hashlib,json,sys,time
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
from stage_budget import check,CLOCK
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest().upper()
def save(n,o):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
check();process=read(H/'logs/inserter-probe-01/process.json')
assert process['error']=='UNEXPECTED_GUI_VISIBLE' and process['returncode']==1
assert read(H/'PROBE_RESULT_V2.json')['status']=='FIRST_NATIVE_INTERFACE_OR_LOAD_FAILURE_STOPPED'
assert not list(H.rglob('*.fic')) and not list(H.rglob('*.sbit'))
originals=read(H/'PROTECTED_ORIGINALS.json')['files'];frozen=read(H/'PROBE_FROZEN_INPUTS.json')['files']
assert all(sha(Path(r['path']))==r['SHA256'] for r in originals)
assert all(sha(H/r['path'])==r['SHA256'] for r in frozen)
receipt=read(P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1/SOURCE_RECEIPTS.json')
assert all(sha(H/'source'/r['name'])==sha(H/'source-before'/r['name'])==r['SHA256'] for r in receipt['functional_RTL'])
summary=dict(stage='A-LOCAL-DEBUG-INSERT-M1',date_client='2026-10-28',approval='D169',fact='F166',decision_result='D170',status='STOPPED_AT_GUI_BOUNDARY_NO_INSERTION',actual_Inserter_CLI=1,PDS_builds=0,new_C=0,new_DUT=0,GUI='Unexpected visible window detected, no GUI interaction performed',hardware='STOPPED',native_process=dict(argv=process['argv'],cwd=process['cwd'],returncode=process['returncode'],termination=process['termination'],error=process['error'],seconds=process['elapsed_seconds'],child_peak_bytes=process['peak_working_set_bytes'],parent_peak_bytes=process['parent_peak_working_set_bytes'],cleanup=process['failure_cleanup']),preparation_error=dict(kind='Missing logs parent before Popen',actual_vendor_calls=0,retained='PREPARATION_ERROR.json',old_counter_and_probe_classification='Historical reservation/error; superseded by preparation diagnostic and actual native receipt'),Tcl_markers_seen=[],netlist_load='NOT_PROVEN',new_FIC=False,debug_insertion='NOT_RUN',new_bitstream=False,debug_timing_resources='NOT_RUN',functional_RTL_changes=[],source13_unchanged=True,protected_originals=len(originals),frozen_probe_inputs=len(frozen),native_license_status='NO_UNAMBIGUOUS_CURRENT_SUCCESS_OR_EXPIRY_PARSED',last_PDS_license_prompt='2026-10-27: 7days; not updated by this result',window_cause='UNDETERMINED; do not infer license failure or unsupported batch syntax',process_followup=dict(CIM_attempt='ACCESS_DENIED',Get_Process_filtered_cdt_ins_count=0,Get_Process_check_scope='current matching Inserter root names, not an independent all-descendant snapshot'),next='Request one bounded local Inserter GUI inspection only; no build, no hardware, no external consultation',first_native_failure_stop=True)
save('SUMMARY.json',summary)
save('STATUS.json',dict(status=summary['status'],native_calls=1,PDS_used=0,hardware='STOPPED',GUI_permission_needed_for_inspection=True,retry=False))
(H/'COMMANDS.md').write_text('''# Actual software-only call and stop

D169 approved scope, ordinary nonadministrator external call separately reviewed. Fixed argv:

```text
D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe -batch D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1/scripts/probe.tcl
cwd: D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1/ins-input
timeout: 60 seconds; per-stream cap: 32MiB
```

First Python wrapper failed at creating a missing log parent before Popen (0 native calls). Original script, counter reservation, traceback route and frozen inputs remain; PREPARATION_ERROR corrects its interface-failure classification. The separate v2 wrapper created only the missing parent and made the first actual native call using identical argv/Tcl/ADF. Native result: guard stopped on UNEXPECTED_GUI_VISIBLE after1.718s, rc1. No Tcl marker completed, no FIC/bitstream/PDS build. Native raw logs local-only; no conclusive fresh license success/expiry is claimed.

No native retry or GUI interaction followed. Root process exited; taskkill rc255 and absent independent descendant enumeration remain explicit. A subsequent ordinary Get-Process filter found zero cdt_ins processes; CIM was denied, not represented as a successful snapshot. No device enumeration/JTAG or hardware commands.

Read SUMMARY, PREPARATION_ERROR, PROBE_RESULT/V2 and logs/inserter-probe-01/process.json. Do not rerun wrappers, reset the absolute stage clock/counters or treat unused build budget as permission to cross GUI boundary.
''',encoding='utf-8')
rows=[]
for p in sorted(H.rglob('*')):
    if p.is_file() and p.name not in ['SHA256SUMS.json','POSTFLIGHT.json']:
        assert not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400
        rows.append(dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,SHA256=sha(p)))
save('SHA256SUMS.json',dict(files=rows,scope='Local immutable evidence; vendor ADF/expanded initializer/firmware and native logs excluded from Git'))
check();elapsed=round(time.monotonic()-CLOCK['started_monotonic'],3)
save('POSTFLIGHT.json',dict(status='INPUT_PROTECTION_PASS_STAGE_STOPPED',protected_originals=len(originals),frozen_probe_inputs=len(frozen),functional_source13_unchanged=True,all_originals_and_frozen_unchanged=True,elapsed_seconds=elapsed,budget_seconds=3600,within_budget=elapsed<=3600,manifest_files=len(rows),manifest_SHA256=sha(H/'SHA256SUMS.json'),actual_Inserter=1,PDS=0,new_DUT=0,hardware='STOPPED'))
print(json.dumps(dict(status=summary['status'],actual_Inserter=1,PDS=0,protected=len(originals),elapsed=elapsed)))
