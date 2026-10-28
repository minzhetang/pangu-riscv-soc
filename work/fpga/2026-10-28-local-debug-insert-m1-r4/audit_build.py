from pathlib import Path
import json,hashlib,re,collections,runpy,sys,time
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-27-board-coremark8-bitstream-m1';PD=H/'build'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
text=lambda p:p.read_text(encoding='utf-8-sig',errors='replace').replace('\r\n','\n')
def save(n,o):
 if (H/n).exists():
  assert json.loads((H/n).read_text())==o,'Existing checkpoint differs: '+n
  return
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
receipt=json.loads((H/'BUILD_EXIT_RECEIPT.json').read_text());proc=receipt['process']
assert proc['returncode']==0 and proc['error'] is None and not proc['timed_out']
artifact=receipt['artifacts'][0];ap=H/artifact['path'];assert sha(ap)==artifact['SHA256'] and ap.stat().st_size==artifact['bytes']
assert receipt['started_epoch']-2<=ap.stat().st_mtime<=receipt['ended_epoch']+2
flow=text(PD/'flow.log');stdout=text(H/'logs/build-once/stdout.log')
stages={
 'compile':'Action compile: Real time elapsed' in flow and not (PD/'compile/error_info.txt').read_bytes(),
 'synthesis':'has been successfully synthesized' in flow,
 'map':'has been successfully mapped' in flow,
 'pnr':'has been placed and routed successfully' in flow,
 'timing':'Report timing is finished successfully' in flow,
 'bitstream':'Generating Programming File done.' in flow and 'gen_bit_stream -scbv {High Voltage} successfully.' in stdout,
 'actual_debug_core_compile':(PD/'device_map/ins_ads.log').is_file() and 'ips_dbc_debug_core_v1_4.vp' in text(PD/'device_map/ins_ads.log')
}
assert all(stages.values()) and not re.search(r'^E:',flow,re.M),stages
# Compare the complete pre and build syntheses before insertion, not just names/selected cells.
def canonical(phase):
 s=text(H/phase/'synthesize/board_top_syn.vm').replace((H/phase).as_posix(),'[PHASE_ROOT]')
 return re.sub(r'(?m)^// Generated (.*?) at .*$',r'// Generated \1 [DATE_OMITTED]',s)
pre=canonical('pre');build=canonical('build');assert pre==build
save('SYNTHESIS_IDENTITY.json',dict(status='PASS_COMPLETE_NORMALIZED_VM_EQUAL',pre_SHA256=hashlib.sha256(pre.encode()).hexdigest().upper(),build_SHA256=hashlib.sha256(build.encode()).hexdigest().upper(),normalization=['exact pre/build phase root paths','generated date line'],not_postmap_formal_equivalence=True))
funcs=runpy.run_path(str(B/'audit_build_v3.py'),run_name='AUDIT_FUNCTION_IMPORT_ONLY')
old=funcs['blocks'](text(B/'pds/synthesize/board_top_syn.vm'));new=funcs['blocks'](text(PD/'synthesize/board_top_syn.vm'))
assert set(new)==set(old) and len(new)==28;pieces=0
rom=funcs['init_data'](PD/'source/init_tables.svh','ROM');ram=funcs['init_data'](PD/'source/init_tables.svh','RAM')
assert len(rom)==len(ram)==32768 and set(ram)=={0xa5}
assert rom[:15912]==(H/'firmware/program.bin').read_bytes() and not any(rom[15912:])
for name,p in new.items():
 m=re.fullmatch(r'\\bank\[(\d+)\]\.halfword\[(\d+)\]\.(rom|ram)_block',name);assert m,name
 bank,half=int(m[1]),int(m[2]);raw=rom if m[3]=='rom' else ram
 keys=[k for k in p if re.fullmatch(r'INIT_[0-9A-F]{2}',k)];assert len(keys)==64
 for key in keys:
  value=funcs['literal'](p[key]);assert value==funcs['literal'](old[name][key])
  assert value==funcs['expected_piece'](raw,bank,half,int(key[-2:],16));pieces+=1
assert pieces==1792
save('MEMORY_INIT_AUDIT.json',dict(status='PASS_1792_FUNCTIONAL_SYNTHESIS_INIT_SAME_AND_RAW_BYTES_MATCH',blocks=28,pieces=pieces,changed=0,ROM_bytes=len(rom),RAM_bytes=len(ram),RAM_fill='A5',program_bytes=15912,program_SHA256=sha(H/'firmware/program.bin'),ROM_SHA256=hashlib.sha256(rom).hexdigest().upper(),RAM_SHA256=hashlib.sha256(ram).hexdigest().upper(),level='SYNTHESIS_INIT_NO_PROPRIETARY_BITSTREAM_DECODE_OR_HARDWARE_READBACK'))
# All named observation registers reached the post-route inventory. Inventory is not connectivity export.
pnr=text(PD/'place_route/board_top_pnr.netlist')
actual_d1=set(map(int,re.findall(r'^u_CORES/u_debug_core_0/trig0_d1\[(\d+)\]/',pnr,re.M)))
assert actual_d1==set(range(140))
drm=[(n,t) for n,t in re.findall(r'^([^;\n]+);(gopDRM\w*)$',pnr,re.M)]
assert len(drm)==32
debug_drm=[(n,t) for n,t in drm if n.startswith('u_CORES/')];assert len(debug_drm)==4 and all(t=='gopDRM' for n,t in debug_drm)
functional_drm=[(n,t) for n,t in drm if not n.startswith('u_CORES/')];assert len(functional_drm)==28 and all(t=='gopDRM18K' for n,t in functional_drm)
save('INSERTION_AUDIT.json',dict(status='PASS_FIC_140_ORDER_AND_NATIVE_INSERTION_WITH_LIMITS',FIC_SHA256=sha(H/'debug.fic'),FIC_channels=140,postroute_data_stage_indices=sorted(actual_d1),functional_DRM18=28,debug_DRM36=4,total_DRM18_equivalent=36,physical_memory_cells=32,core_instance='u_CORES/u_debug_core_0',independent_all_channel_postroute_wiring_decode=False,limits='Saved ordered FIC plus native insertion compile and complete 140 stage inventory; not independent bitstream route decode or physical capture'))
rtr=text(PD/'report_timing/board_top.rtr');assert all(x in rtr for x in ['PG2L100H','FBG676','146967','Design Summary : All Constraints Met.'])
timing={};allrows=[]
for kind,corner,body in re.findall(r'(Setup|Hold|Recovery|Removal) Summary\((Slow|Fast) Corner\):(.*?)(?=\n\w|\Z)',rtr,re.S):
 for launch,capture,slack,tns,failing,endpoints in re.findall(r'^\s*(\S+)\s+(\S+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(\d+)\s+(\d+)\s*$',body,re.M):
  row=dict(type=kind.lower(),corner=corner.lower(),launch=launch,capture=capture,slack_ns=float(slack),TNS_ns=float(tns),failing=int(failing),endpoints=int(endpoints));allrows.append(row)
  if launch==capture=='clk_27mhz':timing[kind.lower()+'_'+corner.lower()]=row
assert len(timing)==8 and all(x['slack_ns']>0 and x['failing']==0 for x in allrows)
prr=text(PD/'place_route/board_top.prr')
resources=dict(LUT=sum(map(int,re.findall(r'\|\s+LUT\s+\|\s+(\d+)',prr))),FF=sum(map(int,re.findall(r'\|\s+FF\s+\|\s+(\d+)',prr))),DRM36=int(re.search(r'\|\s+Use of DRM\s+\|\s+(\d+)',prr)[1]),DRM18=36,IO=int(re.search(r'\|\s+Use of IO\s+\|\s+(\d+)',prr)[1]))
assert resources['DRM36']==18 and resources['IO']==15
baseline=json.loads((B/'SUMMARY.json').read_text())['resources'];delta={n:resources[n]-baseline[n] for n in ['LUT','FF','DRM36','DRM18','IO']}
expected=json.loads((B/'TIMING_RESOURCE_AUDIT.json').read_text())['pins'];pins={}
for line in prr.splitlines():
 a=[x.strip() for x in line.split('|')]
 if len(a)>8 and a[1] in expected:pins[a[1]]=dict(direction=a[2],loc=a[3],bank=a[4],VCCIO=a[5],standard=a[6])
assert len(pins)==15 and all(pins[n]==expected[n] for n in pins)
assert '0 error(s), 0 critical warning(s), 0 warning(s), out of 94 constraint(s)' in text(PD/'constraint_check/constraint_check.ccr')
assert 'Total Latches: 0' in text(PD/'synthesize/board_top.snr')
tlog=text(PD/'report_timing/run.log');ui=re.findall(r"Timing-4086: Port '([^']+)'",tlog);uo=re.findall(r"Timing-4087: Port '([^']+)'",tlog)
assert len(ui)==5 and len(uo)==9
save('TIMING_RESOURCE_AUDIT.json',dict(status='DECLARED_INTERNAL_CLOCKS_PASS_WITH_PHYSICAL_REVIEW_GATES',tool='PDS2022.2-SP6.4 build146967',target='PG2L100H-6IFBG676',timing=timing,all_reported_rows=allrows,resources=resources,delta_vs_F163_no_debug=delta,pins=pins,constraints=94,unconstrained_inputs=ui,unconstrained_outputs=uo,estimated_fmax_not_measured=True,physical_CDC_IO='NOT_VALIDATED'))
def warnings(s,prefix):return [line for line in s.splitlines() if line.startswith(prefix)]
oldflow=text(B/'pds/flow.log');critical=warnings(flow,'C:');oldcrit=warnings(oldflow,'C:')
norm=lambda x:re.sub(r'^(W: [^:]+):.*',r'\1',x)
wc=collections.Counter(map(norm,warnings(flow,'W:')));oldwc=collections.Counter(map(norm,warnings(oldflow,'W:')))
days=sorted(set(map(int,re.findall(r'will\s+(?:invalid|invaild)\s+in\s+(\d+)\s+days',stdout,re.I))))
assert days==[6]
dmr=text(PD/'device_map/board_top.dmr');assert re.search(r'n:u_CORES/drck_o\s*\|\s*PAP_CLOCK_DEDICATED_ROUTE\s*\|\s*FALSE',dmr)
assert len(critical)==4 and not oldcrit
assert 'Bitstream-2001' not in flow and 'High Voltage' in text(PD/'generate_bitstream/bgr.db')
save('WARNINGS_AUDIT.json',dict(status='STOP_FINAL_ACCEPTANCE_NEW_CRITICAL_CLOCK_ROUTING_WARNINGS',critical=critical,baseline_critical=oldcrit,critical_new=4,warnings=dict(wc),baseline_warnings=dict(oldwc),additional_warning_counts=dict(wc-oldwc),constant_probe=wc['W: Loop was found during constant probe.'],license_actual_days=days,SCBV='High Voltage / unchanged engineering assumption',physical_voltage_verified=False,Bitstream_2001_absent=True,generated_attribute='u_CORES/drck_o PAP_CLOCK_DEDICATED_ROUTE=FALSE',warnings_not_waived=True))
doc=Path('D:/PDS/PDS_2022.2-SP6.4/doc/Fabric_Inserter_User_Guide.pdf')
save('RESET_REVIEW.json',dict(status='OPTIONAL_USER_RESET_PORT_DISABLED_SUPPORTED_DEFAULT_NOT_BOARD_RESET_CONNECTED',source=str(doc),SHA256=sha(doc),version='V1.0 / 2022.07.12',PDF_pages_visually_checked=[13,39],source_facts=['Reset Port optional; example does not use it','Use Reset Port defaults disabled; hidden when disabled'],actual_FIC_reset_channel=None,requested_command_was_not_persisted=True,sys_rst_n_data_channel=38,generated_core_reset_nets_present=['u_CORES/u_debug_core_0/conf_rst','u_CORES/u_debug_core_0/resetn'],independent_internal_reset_fanin_verified=False,board_key_resets_ILA_state='NOT_VERIFIED_NOT_CLAIMED',no_preference_or_RTL_change=True))
protected=json.loads((H/'PROTECTED_ORIGINALS.json').read_text())['files'];assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
for phase in ['pre','build']:
 assert all(sha(H/x['path'])==x['SHA256'] for x in json.loads((H/(phase+'-FROZEN_INPUTS.json')).read_text())['files'])
save('AUDIT_RESULT.json',dict(status='DEBUG_BITSTREAM_GENERATED_CANDIDATE_NOT_FINAL_ACCEPTANCE',stages=stages,artifact=artifact,FIC_SHA256=sha(H/'debug.fic'),data_channels=140,depth=1024,main_27MHz='PASS_REPORTED_INTERNAL_TIMING',minimum_setup_ns=min(v['slack_ns'] for k,v in timing.items() if k.startswith('setup')),minimum_hold_ns=min(v['slack_ns'] for k,v in timing.items() if k.startswith('hold')),resources=resources,resource_delta=delta,critical_warnings_open=4,optional_user_reset_port='DISABLED',INIT_same=1792,license_actual_days=days,protected_originals=len(protected),new_DUT=0,hardware='STOPPED',physical_capture_or_CPU_hardware=False))
print(json.dumps(json.loads((H/'AUDIT_RESULT.json').read_text()),ensure_ascii=False))
