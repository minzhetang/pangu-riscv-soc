from pathlib import Path
import json,sys,time,hashlib,difflib,platform
P=Path('D:/A_FPGA_Comp');H=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2';M=H.parent/'2026-10-26-coremark-stream-evidence-m1';R=H.parent/'2026-10-25-coremark-iter2-m1';D=H/'runs/performance8-N234'
sys.path.insert(0,str(H));sys.dont_write_bytecode=True
from stage_coremark import read,save,sha
from preserve import protect
from stage_budget import check as budget_check
if __name__=='__main__':
 budget_check();protected=protect();result=read(D/'check-result.json');func=read(D/'functional-result.json');assert result['status']=='PASS';assert func['status'].startswith('PASS_')
 live=read(H/'frozen-inputs.json')['files'];assert all(sha(H/x['path'])==x['SHA256'] for x in live)
 for name in ['performance','validation']:assert read(H/'replays'/(name+'-N234')/'replay-result.json')['status']=='PASS_OLD_REPLAY_NOT_NEW_DUT'
 assert read(H/'controls/container-results.json')['status']=='PASS_HOST_ONLY'
 processes={p.parent.name:read(p) for p in sorted((H/'logs').glob('*/process.json'))}
 run=processes['run-performance8-N234'];final=processes['final-functional-performance8'];comp=processes['compile-performance8'];arc=read(D/'archive-receipt.json');cap=read(D/'capture-result.json');oracle=read(H/'oracles/performance8/expected.json')
 assert read(H/'C-build-attempt.json')['used']==read(H/'compile-attempt.json')['used']==read(H/'DUT-attempt.json')['used']==1
 raw=sum(v['raw_bytes'] for v in arc['per_stream'].values());archive=sum(p.stat().st_size for p in (D/'archive').rglob('*') if p.is_file());assert archive<=4*1024**3 and not list((D/'spool').iterdir())
 warnings=(H/'logs/compile-performance8/stderr.log').read_text(encoding='utf-8-sig');oldwarn=(M/'logs/compile-performance-N234/stderr.log').read_text(encoding='utf-8-sig');normalize=lambda s:s.replace(str(H),'<STAGE>').replace(str(M),'<STAGE>').replace('performance8-N234','performance-N234');warnsame=normalize(warnings)==normalize(oldwarn)
 (H/'compiler-warnings.txt').write_text(warnings,encoding='utf-8')
 receipt=dict(protected_original_files=protected,frozen_execution_files=len(live),functional_RTL=[],unchanged_C_inputs=[],reference_budget_only=True,peripheral_model_unchanged=True,codec_unchanged=True)
 for p in sorted((H/'source').iterdir()):
  if p.is_file():receipt['functional_RTL'].append(dict(name=p.name,SHA256=sha(p),baseline_SHA256=sha(M/'source'/p.name),unchanged=sha(p)==sha(M/'source'/p.name)))
 for folder in ['port','upstream','firmware']:
  for p in sorted((H/folder).iterdir()):
   if p.is_file():receipt['unchanged_C_inputs'].append(dict(path=str(p.relative_to(H)),SHA256=sha(p),baseline_SHA256=sha(R/folder/p.name)))
 assert len(receipt['functional_RTL'])==13 and all(x['unchanged'] for x in receipt['functional_RTL'])
 save(H/'SOURCE_RECEIPTS.json',receipt)
 diff=[]
 for p in sorted((H/'before').iterdir()):
  q=H/p.name
  if p.is_file() and q.is_file() and p.suffix in ['.py','.sv']:
   diff+=difflib.unified_diff(p.read_text(encoding='utf-8-sig').splitlines(True),q.read_text(encoding='utf-8-sig').splitlines(True),fromfile='before/'+p.name,tofile=p.name)
 for p in sorted((H/'models-before').iterdir()):
  q=H/'models'/p.name
  if p.is_file() and q.is_file():diff+=difflib.unified_diff(p.read_text(encoding='utf-8-sig').splitlines(True),q.read_text(encoding='utf-8-sig').splitlines(True),fromfile='models-before/'+p.name,tofile='models/'+p.name)
 p=H/'before/tb_board_coremark.sv';q=H/'tests/tb_board_coremark.sv'
 diff+=difflib.unified_diff(p.read_text().splitlines(True),q.read_text().splitlines(True),fromfile='before/tb_board_coremark.sv',tofile='tests/tb_board_coremark.sv')
 (H/'EXACT_DIFF.patch').write_text(''.join(diff),encoding='utf-8')
 elapsed=time.monotonic()-read(H/'STAGE_CLOCK.json')['started_monotonic'];assert elapsed<=7200
 summary=dict(stage='A-COREMARK-LONGRUN-READY-M2',date_client='2026-10-27',approval='D160',decision_result='D161',status='PASS_FINITE_8_ITERATIONS_NOT_FORMAL_LONGRUN',C_builds=1,RTL_compiles=1,new_DUT=1,metrics=result['metrics'],raw_ticks=result['detail']['raw_ticks'],crcfinal=result['frozen_comparison']['crcfinal'],UART_bytes=result['UART_frames'],streams=arc['per_stream'],raw_bytes=raw,raw_records=sum(x['records'] for x in arc['per_stream'].values()),segments=sum(x['segments'] for x in arc['per_stream'].values()),archive_bytes_including_metadata=archive,archive_timings=arc['timings'],spool_peak_bytes=cap['supervisor']['peak_spool'],parent_archive_peak_bytes=cap['supervisor']['peak_parent'],DUT_host_seconds=run['elapsed_seconds'],DUT_cpu=run['child_cpu'],archive_parent_cpu_before=run['parent_cpu_before'],archive_parent_cpu_after=run['parent_cpu_after'],check_host_seconds=final['elapsed_seconds'],check_peak_bytes=final['peak_working_set_bytes'],reference_host_seconds=processes['oracle-performance8']['elapsed_seconds'],reference_steps=oracle['steps'],reference_peak_bytes=processes['oracle-performance8']['peak_working_set_bytes'],compile_host_seconds=comp['elapsed_seconds'],compile_warning_groups=warnings.count('warning:'),warnings_identical_normalized=warnsame,host_container=read(H/'controls/container-results.json'),stage_elapsed_before_documentation_seconds=elapsed,stage_limit_seconds=7200,limits=dict(raw_per_stream=16*1024**3,records_per_stream=500000000,segments_per_stream=16384,index_per_stream=16*1024**2,archive_total=4*1024**3,spool=32*1024**2,working_set=512*1024**2,VCD=256*1024**2),protected=protected,frozen_inputs=len(live),RTL13_unchanged=True,reference_semantics_unchanged=True,hardware='STOPPED',PDS=0,B_R1_receipt='UNKNOWN',limitations=['Finite performance seed8 only; validation seed is old2 replay, not new DUT','No >4GiB actual I/O validation, no160 run or permission','No formal FPGA CoreMark score, real clock or ILA evidence','No real retirement PC or unified WB/STORE sequence; fixed input/initial state','Direct child and parent memory only; native compiler internal descendant peaks not separately measured','Timing observations across different runs are not controlled CPU or simulator speedup evidence','Container controls are host-only, not CPU verification','Compatibility raw/F153 readers are not independently stressed to every maximum'])
 summary['extra_guards']=read(H/'controls/extra-guards.json');summary['optimized_entry']=read(H/'controls/optimized-entry.json')['status'];summary['tools']=dict(iverilog='13.0 MSYS2 UCRT64 portable',vvp='13.0',GNU='xPack15.2.0-1 RV32I/ILP32',Python=sys.version.split()[0]);save(H/'SUMMARY.json',summary);save(H/'STATUS.json',dict(status=summary['status'],compile_used=1,DUT_used=1,C_build_used=1,hardware='STOPPED',followup_longrun='NOT_AUTHORIZED'))
 save(H/'COMMANDS-exact-local.json',dict(processes=processes,Python=sys.version))
 def scrub(o):
  if isinstance(o,str) and ('C:\\Users\\' in o or 'C:/Users/' in o):return '<EXISTING_PYTHON>'
  if isinstance(o,dict):return {k:scrub(v) for k,v in o.items()}
  if isinstance(o,list):return [scrub(v) for v in o]
  return o
 (H/'COMMANDS.md').write_text('# M2 actual commands and native results\n\nD160 scope, one GNU build plus auxiliary commands, one separately approved external-route Icarus compile, one ordinary vvp DUT. Nonadministrator. JSON argv entries are arguments, not shell expressions. Exact local Python path stays in COMMANDS-exact-local.json, excluded from Git.\n\n'+''.join('## '+name+'\n\n```json\n'+json.dumps(scrub(r),ensure_ascii=False,indent=2)+'\n```\n\n' for name,r in processes.items())+'Preparation failure replay-performance is retained: missing build-result metadata before the build completed, no CPU/DUT run or failed functional comparison. After dependency readiness replay-ready-* passed. No C/RTL/DUT retry. The extra callback deadline guard rejected correctly but its first auxiliary wrapper used a lowercase error token; original wrapper/fixture retained and independently qualified with the exact uppercase error. Negative controls intentionally reject.\n',encoding='utf-8')
 (H/'REPRODUCE.md').write_text('''# M2 reproduction boundary

Read SUMMARY.json, TEST_PLAN.json, APPROVAL.json, COMMANDS.md, SOURCE_RECEIPTS.json and EXACT_DIFF.patch first. All attempts are single-use. Do not rerun preparation/build/compile/capture scripts in this completed directory or remove markers. A new DUT reproduction needs a new independent copy and separately scoped approval; no160 or hardware authorization is implied.

stage_budget.py rejects optimized Python at import; all public workers reach that guard through the adapter/supervisor. Keep -B and ordinary execution. Stage clock is absolute and must not be silently reset. The old guarded_entry.py is an inherited M1 boundary and is not an M2 production launch command. Existing vendor GTP models remain external to this repository. The local full evidence contains wave.vcd, ELF/bin/init, archive payloads and original logs; Git deliberately excludes these plus tools and overlimit fixtures. A Git clone alone is not the complete local raw-evidence collection.

Host-scale and two old replays are not new CPU runs. Only performance8-N234 is the one new DUT. Its independently frozen reference predates compile/DUT. No change to13 functional RTL, official algorithms/port/start/link or ISA semantics. Model changes only budget5M to25M; frozen_checks uses the per-case iteration/cycle requirement. Remaining raw/F153 compatibility reader maxima are not fully stressed; CLOSED-SEGMENTS is the new tested path.
''',encoding='utf-8')
 print(json.dumps({k:summary[k] for k in ['status','DUT_host_seconds','check_host_seconds','raw_bytes','archive_bytes_including_metadata','segments','protected','frozen_inputs']},ensure_ascii=False))
