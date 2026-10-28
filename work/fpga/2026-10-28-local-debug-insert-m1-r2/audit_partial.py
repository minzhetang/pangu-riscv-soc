from pathlib import Path
import hashlib,json,re,runpy,sys,time
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-27-board-coremark8-bitstream-m1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
protected=json.loads((H/'PROTECTED_ORIGINALS.json').read_text())['files']
assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
frozen=json.loads((H/'FROZEN_INPUTS.json').read_text())['files']
assert all(sha(H/x['path'])==x['SHA256'] for x in frozen)
proc=json.loads((H/'logs/pds-flow-once/process.json').read_text())
flow=(H/'logs/pds-flow-once/stdout.log').read_text(errors='replace')
assert proc['returncode']==1 and 'invalid command name "clock"' in flow
assert 'Executing : synthesize -ads -selected_syn_tool_opt 2 successfully.' in flow
assert not list((H/'pds').rglob('*.sbit'))
assert not (H/'debug.fic').exists() and not (H/'FIC_READY.json').exists()
assert not (H/'pds/devmap').exists()
funcs=runpy.run_path(str(B/'audit_build_v3.py'),run_name='READ_ONLY_AUDIT_IMPORT')
old=funcs['blocks']((B/'pds/synthesize/board_top_syn.vm').read_text())
new=funcs['blocks']((H/'pds/synthesize/board_top_syn.vm').read_text())
assert len(old)==len(new)==28
changes=[];pieces=0
for block,p in old.items():
 assert block in new
 for key,value in p.items():
  if not re.fullmatch(r'INIT_[0-9A-F]{2}',key):continue
  pieces+=1
  if funcs['literal'](new[block][key])!=funcs['literal'](value):changes.append(dict(block=block,parameter=key))
assert pieces==1792 and not changes
save('SYNTHESIS_MEMORY_AUDIT.json',dict(level='SYNTHESIS_NETLIST_ONLY_NOT_FINAL_BITSTREAM',DRM18_blocks=28,INIT_pieces_compared=pieces,changed=changes,original_final_bitstream_validation_not_replaced=True))
vm=(H/'pds/synthesize/board_top_syn.vm').read_text()
marks=[]
for line in vm.splitlines():
 if 'PAP_MARK_DEBUG' in line:marks.append(line.strip())
save('MARKER_OBSERVATIONS.json',dict(level='STATIC_NEW_SYNTHESIS_VM_NOT_INSERTER_MAPPING',actual_attribute_lines=marks,limitation='Some grouped/scalar declarations propagate tags; absence on a VM bus declaration does not alone prove source tag ineffective. No 140-bit native net mapping or connection completed.'))
gui=json.loads((H/'GUI_RESULT.json').read_text());helptext=(H/'logs/readonly-help/stdout.log').read_text(errors='replace')
assert 'A_HAS_CLOCK=\n' in helptext.replace('\r\n','\n') and 'A_HAS_AFTER=after' in helptext and 'Executing : add_fic -help successfully.' in helptext
save('READONLY_HELP_RESULT.json',dict(status='PASS',queries_used=4,query_limit=6,clock_available=False,after_available=True,vwait_available=True,add_fic_help_pass=True,version='2022.2-SP6.4 build146967',no_build=True))
save('POSTFLIGHT.json',dict(protected_originals=len(protected),protected_unchanged=True,frozen_execution_files=len(frozen),frozen_unchanged=True,GUI_launches=1,GUI_seconds=gui['seconds'],GUI_root_exited=gui['root_exited'],PDS_build_attempts=1,PDS_native_rc=1,PDS_build_seconds=proc['elapsed_seconds'],PDS_readonly_help_processes=1,help_queries=4,new_DUT=0,new_FIC=False,new_bitstream=False,INIT_synthesis_only_same=True,stage_seconds=time.monotonic()-json.loads((H/'STAGE_CLOCK.json').read_text())['start_monotonic'],hardware='STOPPED'))
days=[int(n) for n in re.findall(r'license will inva(?:l|il)d in (\d+) days',flow+'\n'+helptext,flags=re.I)]
save('SUMMARY.json',dict(date_client='2026-10-28',fact='F169',approval='D175',result_decision='D176',stage='A-LOCAL-DEBUG-INSERT-M1-R2',status='SYNTHESIS_ONLY_STOPPED_OWN_CONTROL_SCRIPTS',synthesis='PASS',native_PDS_error='invalid command name clock after synthesis',GUI_error=gui['error'],GUI_error_classification='A queued main-role action while only reminder existed; no control invocation',new_FIC=False,new_bitstream=False,new_timing='NOT_RUN',new_DUT=0,source_originals_unchanged=True,INIT_synthesis_pieces_equal=1792,license_days_actual=sorted(set(days)),hardware='STOPPED',limits='One GUI and one complete-build attempt used; do not rerun historical entries. Four of six readonly help queries used.',Git_sync='SYSTEM_REVIEW_REJECTED_BEFORE_EXECUTION_DESPITE_CURRENT_USER_APPROVAL'))
print(json.dumps(json.loads((H/'SUMMARY.json').read_text()),ensure_ascii=False))
