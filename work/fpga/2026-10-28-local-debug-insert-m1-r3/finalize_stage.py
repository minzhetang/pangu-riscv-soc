from pathlib import Path
import json,re,hashlib,runpy,sys,time
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-27-board-coremark8-bitstream-m1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
protected=json.loads((H/'PROTECTED_ORIGINALS.json').read_text())['files']
frozen=json.loads((H/'FROZEN_INPUTS.json').read_text())['files']
assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
assert all(sha(H/x['path'])==x['SHA256'] for x in frozen)
gui=json.loads((H/'GUI_RESULT.json').read_text());pds=json.loads((H/'logs/pds-flow-once/process.json').read_text())
assert gui['rc']==0 and gui['seconds']<600 and gui['root_exited'] and not gui['remaining_own_windows']
assert pds['returncode']==1 and not pds['timed_out'] and pds['error'] is None
assert not (H/'FIC_READY.json').exists() and not list((H/'pds').rglob('*.sbit'))
native=(H/'logs/pds-flow-once/stdout.log').read_text(errors='replace')
assert 'Executing : synthesize -ads -selected_syn_tool_opt 2 successfully.' in native and 'A_GUI_ABORT' in native
assert 'invalid command name "clock"' not in native
tools=runpy.run_path(str(B/'audit_build_v3.py'),run_name='AUDIT_IMPORT_ONLY')
old=tools['blocks']((B/'pds/synthesize/board_top_syn.vm').read_text());new=tools['blocks']((H/'pds/synthesize/board_top_syn.vm').read_text())
assert len(old)==len(new)==28 and set(old)==set(new)
pieces=0
for n,p in old.items():
 for key,value in p.items():
  if re.fullmatch(r'INIT_[0-9A-F]{2}',key):
   pieces+=1;assert tools['literal'](value)==tools['literal'](new[n][key])
assert pieces==1792
save('MEMORY_INIT_AUDIT.json',dict(status='PASS_SYNTHESIS_LAYER_ONLY',DRM18_blocks=28,INIT_pieces=1792,changed=0,no_final_bitstream_or_readback=True))
assert json.loads((H/'REFERENCE_BINDING_AUDIT.json').read_text())['complete_canonical_VM_equal']
glog=(H/'gui-stdout.log').read_text(errors='replace')
days=sorted(set(map(int,re.findall(r'will\s+(?:invalid|invaild)\s+in\s+(\d+)\s+days',native+'\n'+glog,flags=re.I))))
assert days==[6]
fic=H/'debug.fic';s=fic.read_text(encoding='utf-8-sig')
assert 'dataDepth=1024' in s and 'clockEdge=Rising' in s
assert not re.search(r'\.triggerChannel<',s)
mapping=json.loads((H/'MAPPING_GATE.json').read_text())
save('POSTFLIGHT.json',dict(protected_originals=len(protected),protected_unchanged=True,frozen_inputs=len(frozen),frozen_unchanged=True,GUI_launches=1,GUI_seconds=gui['seconds'],GUI_rc=0,PDS_build_attempts=1,PDS_seconds=pds['elapsed_seconds'],PDS_rc=1,additional_native_queries=0,new_DUT=0,new_bitstream=False,partial_FIC_SHA256=sha(fic),partial_FIC_bytes=fic.stat().st_size,FIC_connected_data_bits=0,stage_seconds=time.monotonic()-json.loads((H/'STAGE_CLOCK.json').read_text())['start_monotonic'],hardware='STOPPED'))
summary=dict(date_client='2026-10-28',fact='F170',approval='D177',decision='D178',stage='A-LOCAL-DEBUG-INSERT-M1-R3',status='STOP_REQUIRED_PROBE_MAPPING_INCOMPLETE',GUI='NORMAL_NATIVE_EXIT_AFTER_RELIABLE_REMINDER_AND_MAIN_UI',GUI_seconds=gui['seconds'],PDS='EXPLICIT_MAPPING_GATE_ABORT_THEN_SYNTHESIS_COMPLETED_RC1',PDS_seconds=pds['elapsed_seconds'],actual_reference_nets=4898,planned_bits=140,exact_name_matches=138,verified_direct_alias_bits=1,accounted_bits=139,unresolved=['soc/cpu_core/eei_hold'],connected_bits=0,partial_FIC_SHA256=sha(fic),reference_binding='NEW_R3_AND_REFERENCE_R2_COMPLETE_CANONICAL_VM_IDENTICAL',INIT_same=1792,new_bitstream=False,new_final_timing='NOT_RUN',license_actual_days=days,new_DUT=0,hardware='STOPPED',next='One additional nonfunctional eei_hold tag and split two PDS CLI boundaries; separate approval required, not implemented')
save('SUMMARY.json',summary)
save('SHA256SUMS.json',dict(scope='LOCAL_ONLY_FINAL_SNAPSHOT',files=[dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,SHA256=sha(p)) for p in sorted(H.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json']))
print(json.dumps(summary,ensure_ascii=False))
