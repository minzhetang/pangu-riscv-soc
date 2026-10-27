from pathlib import Path
import json,hashlib,re,collections,time,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2];B=P/'work/fpga/2026-10-25-board-top-m1'
from stage_budget import check
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));text=lambda p:p.read_text(encoding='utf-8-sig',errors='replace').replace('\r\n','\n');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def params(s):return {m[1]:re.sub(r'\s+','',m[2]) for m in re.finditer(r'\.(\w+)\s*\(([^()]*)\)',s)}
def literal(s):
 m=re.fullmatch(r"(\d+)'([bhdo])([0-9a-fA-F_]+)",s);assert m,s;v=int(m[3].replace('_',''),{'b':2,'h':16,'d':10,'o':8}[m[2]]);assert v.bit_length()<=int(m[1]);return v
rx=re.compile(r'GTP_DRM18K_E1\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',re.S)
def blocks(vm):return {m[1].strip():params(m[2]) for m in rx.finditer(vm)}
def init_data(p,name):
 s=text(p).split(name+'_BITS = {',1)[1].split('};',1)[0];parts=re.findall("4096'h([0-9a-fA-F]{1024})",s);assert len(parts)==64;return bytes.fromhex(''.join(parts))[::-1]
def expected_piece(data,bank,half,chunk):
 v=0
 for j in range(32):
  wi=bank*1024+chunk*16+j//2;byte=data[wi*4+half*2+j%2];v|=byte<<(j*9)
 return v
if __name__=='__main__':
 check();exit=read(H/'BUILD_EXIT_RECEIPT.json');proc=exit['process'];assert proc['returncode']==0 and not proc['timed_out'] and not proc['cap'] and proc['error'] is None
 pd=H/'pds';flow=text(pd/'flow.log');assert not re.search(r'^E:',flow,re.M)
 stages=dict(compile='Action compile: Real time elapsed' in flow and (pd/'compile/error_info.txt').stat().st_size==0,synthesis='has been successfully synthesized' in flow,mapping='has been successfully mapped' in flow,pnr='has been placed and routed successfully' in flow,timing='Report timing is finished successfully' in flow,bitstream='Generating Programming File done.' in flow and 'Executing : gen_bit_stream -scbv {High Voltage} successfully.' in flow);assert all(stages.values()),stages
 assert len(exit['artifacts'])==1;artifact=exit['artifacts'][0];ap=Path(artifact['path']);assert ap.is_file() and ap.stat().st_size==artifact['bytes']>0 and sha(ap)==artifact['SHA256'];assert exit['started_epoch']-2<=ap.stat().st_mtime<=exit['ended_epoch']+2
 # Generation settings only: do not read or record license contents/host IDs.
 project_files=list(pd.glob('*.pds'));assert len(project_files)==1;proj=text(project_files[0]);m=re.search(r'\(_option scbv\s+\(_string "([^"]+)"\)\)',proj);assert m and m[1]=='High Voltage'
 db=text(pd/'generate_bitstream/bgr.db');assert 'High Voltage' in db and 'Bitstream-2001' not in flow;save('CONFIGURATION_AUDIT.json',dict(SCBV_project=m[1],SCBV_generator_db='High Voltage',Bitstream_2001_absent=True,engineering_assumption_only=True,physical_voltage_verified=False,bitstream=dict(path=str(ap),bytes=ap.stat().st_size,SHA256=sha(ap)),fresh_artifact_after_process_exit=True))
 # Compute every INIT piece independently from raw bytes and compare both old and new synthesis.
 vm=text(pd/'synthesize/board_top_syn.vm');oldvm=text(B/'pds/synthesize/board_top_syn.vm');new,old=blocks(vm),blocks(oldvm);assert set(new)==set(old) and len(new)==28
 audits=[]
 for root,values in [(pd,new),(B/'pds',old)]:
  rom=init_data(root/'source/init_tables.svh','ROM');ram=init_data(root/'source/init_tables.svh','RAM');checked=0
  for name,pars in values.items():
   mm=re.fullmatch(r'\\bank\[(\d+)\]\.halfword\[(\d+)\]\.(rom|ram)_block',name);assert mm,name;bank,half=int(mm[1]),int(mm[2]);data=rom if mm[3]=='rom' else ram
   keys=[k for k in pars if re.fullmatch('INIT_[0-9A-F]{2}',k)];assert len(keys)==64
   for k in keys:assert literal(pars[k])==expected_piece(data,bank,half,int(k[-2:],16)),(name,k);checked+=1
  audits.append(dict(kind='new8' if root==pd else 'old1_calibration',retained_blocks=len(values),INIT_pieces=checked,independent_raw_byte_mapping=True))
 changed=[]
 for name in new:
  assert {k:v for k,v in new[name].items() if not k.startswith('INIT_')}=={k:v for k,v in old[name].items() if not k.startswith('INIT_')}
  for k in new[name]:
   if k.startswith('INIT_') and literal(new[name][k])!=literal(old[name][k]):changed.append(dict(block=name,piece=k,old=old[name][k],new=new[name][k]))
 assert len(changed)==1,changed;save('MEMORY_INIT_AUDIT.json',dict(status='ALL_RETAINED_SYNTH_INIT_MATCH_NEW_RAW_BYTES',rows=audits,changed_pieces=changed,image=read(H/'INIT_RECEIPT.json'),limitations='Synth INIT/structure audit; no proprietary bitstream decode, readback or post-layout functional simulation; pruned constant regions not invented as retained gates'))
 # Retained reset/RF/GPIO structure, matching prior known board implementation.
 def module(name):
  start=vm.index('module '+name+'\n');return vm[start:vm.index('endmodule',start)]
 ffrx=re.compile(r'GTP_DFF\w*\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',re.S)
 rf=list(ffrx.finditer(module('regfile')));assert len(rf)==992 and all(params(m[2])['INIT']=="1'b0" for m in rf)
 reset=module('board_reset_sync');resetffs=list(ffrx.finditer(reset));assert len(resetffs)==3
 for i,m in enumerate(resetffs):
  assert m[1].strip()==f'\\release_ff[{i}]';assert params(m[2])=={'GRS_EN':'"TRUE"','INIT':"1'b0"};ports=params(m[4]);assert ports['CLK']=='clk' and ports['C']=='N0';assert ports['D']==("1'b1" if i==0 else f'release_ff[{i-1}]')
 assert '.I (key0_n)' in reset and '.Q (sys_rst_n)' in reset
 gff={m[1].strip() for m in ffrx.finditer(module('gpio_core'))};assert all(f'\\{n}[{i}]' in gff for n in ['sync_meta','gpio_in_sync'] for i in range(4))
 pnr=text(pd/'place_route/board_top_pnr.netlist');assert len(re.findall(r';gopDRM18K$',pnr,re.M))==28
 prr=text(pd/'place_route/board_top.prr');pins={};expected=read(B/'pin-plan.json')['pins']
 for line in prr.splitlines():
  a=[x.strip() for x in line.split('|')]
  if len(a)>8 and a[1] in expected:pins[a[1]]=dict(direction=a[2],loc=a[3],bank=a[4],VCCIO=a[5],standard=a[6])
 assert len(pins)==15 and all(pins[n]['loc']==v and pins[n]['VCCIO']=='3.3' and pins[n]['standard']=='LVCMOS33' for n,v in expected.items())
 ccr=text(pd/'constraint_check/constraint_check.ccr');assert '0 error(s), 0 critical warning(s), 0 warning(s), out of 94 constraint(s)' in ccr
 timing={};rtr=text(pd/'report_timing/board_top.rtr')
 assert '2022.2-SP6.4' in rtr and '146967' in rtr and 'PG2L100H' in rtr
 for kind,corner,body in re.findall(r'(Setup|Hold|Recovery|Removal) Summary\((Slow|Fast) Corner\):(.*?)(?=\n\w|\Z)',rtr,re.S):
  m=re.search(r'clk_27mhz\s+clk_27mhz\s+([\d.-]+)\s+([\d.-]+)\s+(\d+)\s+(\d+)',body);assert m;timing[f'{kind.lower()}_{corner.lower()}']=dict(slack_ns=float(m[1]),TNS_ns=float(m[2]),failing=int(m[3]),endpoints=int(m[4]))
 assert len(timing)==8 and all(v['slack_ns']>0 and v['failing']==0 for v in timing.values())
 fmax=re.search(r'clk_27mhz\s+27.0000 MHz\s+([\d.]+) MHz',rtr);assert fmax
 tlog=text(pd/'report_timing/run.log');ui=re.findall(r"Timing-4086: Port '([^']+)'",tlog);uo=re.findall(r"Timing-4087: Port '([^']+)'",tlog);assert len(ui)==5 and len(uo)==9
 lut=sum(map(int,re.findall(r'\|\s+LUT\s+\|\s+(\d+)',prr)));ff=sum(map(int,re.findall(r'\|\s+FF\s+\|\s+(\d+)',prr)));assert lut>1000 and ff>1000 and 'Total Latches: 0' in text(pd/'synthesize/board_top.snr')
 save('TIMING_RESOURCE_AUDIT.json',dict(status='INTERNAL_27MHZ_PASS_WITH_EXTERNAL_LIMITS',tool='PDS2022.2-SP6.4 build146967',device='PG2L100H',speed='-6',package='FBG676',pins=pins,pin_constraints=94,timing=timing,resources=dict(LUT=lut,FF=ff,DRM36=14,DRM18=28,IO=15,latches=0),estimated_internal_MHz=float(fmax[1]),estimate_not_measured_Fmax=True,unconstrained_async_inputs=ui,unconstrained_outputs=uo,physical_CDC_and_IO_timing='NOT_VALIDATED'))
 # Compare warning classes and exact known seven constant-probe messages.
 warn=[x for x in flow.splitlines() if x.startswith('W:')];oldflow=text(B/'pds/flow.log');owarn=[x for x in oldflow.splitlines() if x.startswith('W:')]
 normalize=lambda x:re.sub(r'^(W: [^:]+):.*',r'\1',x)
 counts=collections.Counter(map(normalize,warn));oldcounts=collections.Counter(map(normalize,owarn));constant=counts['W: Loop was found during constant probe.'];extra=counts-oldcounts
 stdout=text(H/'logs/pds-flow-once/stdout.log');days=[int(x) for x in re.findall(r'license will invalid in (\d+) days',stdout)];assert days,'no actual license expiry prompt found'
 pool=[int(x.replace(',','')) for x in re.findall(r'Peak memory pool usage is ([\d,]+) MB',flow)]
 save('WARNINGS_LICENSE_AUDIT.json',dict(warning_counts=dict(counts),old_warning_counts=dict(oldcounts),extra_classes_or_counts=dict(extra),constant_probe_count=constant,old_constant_probe_count=oldcounts['W: Loop was found during constant probe.'],constant_probe_root_cause='OPEN',Bitstream_2001_absent=True,license_checkout='SUCCESS_FOR_THIS_RUN',license_days_remaining_prompts=sorted(set(days)),license_content_or_identifiers_recorded=False,tool_reported_memory_pool_max_MB=max(pool) if pool else None,unredacted_native_logs='LOCAL_ONLY_NOT_FOR_GIT'))
 original=read(H/'PROTECTED_ORIGINALS.json')['files'];assert all(sha(Path(x['path']))==x['SHA256'] for x in original);live=read(H/'FROZEN_INPUTS.json')['files'];assert all(sha(H/x['path'])==x['SHA256'] for x in live)
 # New warning counts are a review gate, never auto-fix RTL to silence them.
 gate='SOFTWARE_BITSTREAM_GENERATED_WITH_KNOWN_LIMITS' if constant==7 and not extra else 'CANDIDATE_BITSTREAM_WARNING_REVIEW_REQUIRED'
 save('AUDIT_RESULT.json',dict(status=gate,stages=stages,artifact=artifact,PDS_process=proc,timing=timing,resources=dict(LUT=lut,FF=ff,DRM36=14,IO=15),changed_INIT_pieces=changed,SCBV='High Voltage engineering assumption',license_days_remaining=sorted(set(days)),constant_probe_count=constant,additional_warnings=dict(extra),original_files_protected=len(original),frozen_execution_files=len(live),new_DUT=0,new_C_build=0,PDS_runs=1,hardware='STOPPED',hardware_or_formal_score=False))
 check();print(json.dumps(dict(status=gate,sbit_bytes=artifact['bytes'],sbit_SHA256=artifact['SHA256'],LUT=lut,FF=ff,minimum_setup_ns=min(timing[k]['slack_ns'] for k in timing if k.startswith('setup')),minimum_hold_ns=min(timing[k]['slack_ns'] for k in timing if k.startswith('hold')),INIT_changed=len(changed),license_days=sorted(set(days)),constant_probe=constant,new_warning_counts=dict(extra)),ensure_ascii=False))
