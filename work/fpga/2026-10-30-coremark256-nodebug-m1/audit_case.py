from pathlib import Path
import re,json,hashlib,time,collections
H=Path(__file__).resolve().parent;P=H.parents[2];F=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1'
from stage_budget import check,deadline
from host_checks import stages
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def text(p):
 assert p.stat().st_size<=32*1024**2
 return p.read_text(encoding='utf-8-sig',errors='strict').replace('\r\n','\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def params(s):return {m[1]:re.sub(r'\s+','',m[2]) for m in re.finditer(r'\.(\w+)\s*\(([^()]*)\)',s)}
def literal(s):
 m=re.fullmatch(r"(\d+)'([bhdo])([0-9a-fA-F_]+)",s);assert m,s;v=int(m[3].replace('_',''),{'b':2,'h':16,'d':10,'o':8}[m[2]]);assert v.bit_length()<=int(m[1]);return v
def blocks(vm):return {m[1].strip():params(m[2]) for m in re.finditer(r'GTP_DRM18K_E1\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',vm,re.S)}
def expected_piece(data,bank,half,chunk):
 v=0
 for j in range(32):v|=data[(bank*1024+chunk*16+j//2)*4+half*2+j%2]<<(j*9)
 return v
def audit(tid):
 end=deadline(300);d=H/tid;pd=d/'pds';e=read(d/'BUILD_EXIT_RECEIPT.json');proc=e['process'];assert proc['returncode']==0 and proc['error'] is None and not proc['cap'] and not proc['timed_out']
 flow=text(pd/'flow.log');stdout=text(Path(proc['stdout']));assert not re.search(r'^E:',flow,re.M)
 stage=stages(flow,stdout);assert all(stage.values()),stage
 assert (pd/'compile/error_info.txt').stat().st_size==0
 artifacts=list(pd.rglob('*.sbit'));assert len(artifacts)==1;p=artifacts[0];assert p.stat().st_size>0 and e['started_epoch']-2<=p.stat().st_mtime<=e['ended_epoch']+2
 artifact=dict(path=str(p),bytes=p.stat().st_size,SHA256=sha(p))
 projects=list(pd.glob('*.pds'));assert len(projects)==1;proj=text(projects[0]);assert re.search(r'\(_option scbv\s+\(_string "High Voltage"\)\)',proj)
 assert 'High Voltage' in text(pd/'generate_bitstream/bgr.db') and 'Bitstream-2001' not in flow
 vm=text(pd/'synthesize/board_top_syn.vm');new=blocks(vm);old=blocks(text(F/'pds/synthesize/board_top_syn.vm'));assert set(new)==set(old) and len(new)==28
 image=(d/'firmware/program.bin').read_bytes();rom=image+bytes(32768-len(image));ram=b'\xa5'*32768;count=0;changed=[]
 for name,pars in new.items():
  check(end);m=re.fullmatch(r'\\bank\[(\d+)\]\.halfword\[(\d+)\]\.(rom|ram)_block',name);assert m,name
  bank,half=int(m[1]),int(m[2]);data=rom if m[3]=='rom' else ram
  keys=[k for k in pars if re.fullmatch('INIT_[0-9A-F]{2}',k)];assert len(keys)==64
  for k in keys:
   assert literal(pars[k])==expected_piece(data,bank,half,int(k[-2:],16)),(name,k)
   count+=1
   if literal(pars[k])!=literal(old[name][k]):changed.append(dict(block=name,piece=k))
  assert {k:v for k,v in pars.items() if k not in keys}=={k:v for k,v in old[name].items() if k not in keys}
 assert count==1792
 pnr=text(pd/'place_route/board_top_pnr.netlist');assert len(re.findall(r';gopDRM18K$',pnr,re.M))==28
 expected=read(F/'TIMING_RESOURCE_AUDIT.json')['pins'];pins={};prr=text(pd/'place_route/board_top.prr')
 for line in prr.splitlines():
  a=[x.strip() for x in line.split('|')]
  if len(a)>8 and a[1] in expected:pins[a[1]]=dict(direction=a[2],loc=a[3],bank=a[4],VCCIO=a[5],standard=a[6])
 assert pins==expected and len(pins)==15
 assert '0 error(s), 0 critical warning(s), 0 warning(s), out of 94 constraint(s)' in text(pd/'constraint_check/constraint_check.ccr')
 timing={};rtr=text(pd/'report_timing/board_top.rtr');assert all(x in rtr for x in ['2022.2-SP6.4','146967','PG2L100H'])
 for kind,corner,body in re.findall(r'(Setup|Hold|Recovery|Removal) Summary\((Slow|Fast) Corner\):(.*?)(?=\n\w|\Z)',rtr,re.S):
  m=re.search(r'clk_27mhz\s+clk_27mhz\s+([\d.-]+)\s+([\d.-]+)\s+(\d+)\s+(\d+)',body);assert m
  timing[kind.lower()+'_'+corner.lower()]=dict(slack_ns=float(m[1]),TNS_ns=float(m[2]),failing=int(m[3]),endpoints=int(m[4]))
 assert len(timing)==8 and all(x['slack_ns']>0 and x['TNS_ns']==0 and x['failing']==0 for x in timing.values())
 assert re.search(r'clk_27mhz\s+27.0000 MHz',rtr)
 tlog=text(pd/'report_timing/run.log');ui=re.findall(r"Timing-4086: Port '([^']+)'",tlog);uo=re.findall(r"Timing-4087: Port '([^']+)'",tlog);assert len(ui)==5 and len(uo)==9
 warnings=[x for x in flow.splitlines() if x.startswith('W:')];basewarn=[x for x in text(F/'pds/flow.log').splitlines() if x.startswith('W:')]
 # Normalize only the relocated project prefix, preserving full message/line/count.
 norm=lambda line,root:line.replace(str(root).replace('\\','/'),'<CASE_PDS>').replace(str(root),'<CASE_PDS>')
 counts=collections.Counter(norm(x,pd) for x in warnings);basecounts=collections.Counter(norm(x,F/'pds') for x in basewarn);extra=counts-basecounts
 const=sum('Loop was found during constant probe.' in x for x in warnings)
 days=sorted(set(int(x) for x in re.findall(r'license will invalid in (\d+) days',stdout)));assert days
 pool=[int(x.replace(',','')) for x in re.findall(r'Peak memory pool usage is ([\d,]+) MB',flow)];assert not pool or max(pool)<=2048
 critical=re.findall(r'^.*(?:Critical Warning|CRITICAL WARNING).+$',flow,re.M)
 resources=dict(LUT=sum(map(int,re.findall(r'\|\s+LUT\s+\|\s+(\d+)',prr))),FF=sum(map(int,re.findall(r'\|\s+FF\s+\|\s+(\d+)',prr))),DRM18=28,IO=15,latches=0)
 assert resources['LUT']>0 and resources['FF']>0 and 'Total Latches: 0' in text(pd/'synthesize/board_top.snr')
 check(end)
 result=dict(id=tid,status='SOFTWARE_BITSTREAM_GENERATED_WITH_KNOWN_LIMITS' if not extra and const==7 and not critical else 'WARNING_REVIEW_REQUIRED_STOPPED',artifact=artifact,stages=stage,timing=timing,resources=resources,pins=pins,INIT_pieces=count,changed_INIT_pieces=changed,warning_counts=dict(collections.Counter(re.sub(r'^(W: [^:]+):.*',r'\1',x) for x in warnings)),extra_warning_messages=dict(extra),constant_probe=const,critical_count=len(critical),license_days_remaining=days,license_checkout='SUCCESS_THIS_RUN',memory_pool_reported_MB=max(pool) if pool else None,physical_CDC='NOT_VALIDATED',external_input_delays_unspecified=ui,external_output_delays_unspecified=uo,hardware='STOPPED',hardware_valid=False,formal_score_valid=False,source_bin_SHA256=sha(d/'firmware/program.bin'),source_ELF_SHA256=sha(d/'firmware/program.elf'),INIT_table_SHA256=sha(pd/'source/init_tables.svh'),SCBV='High Voltage engineering decision only',long256_DUT='NOT_RUN')
 with (d/'AUDIT_RESULT.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
 assert result['status']=='SOFTWARE_BITSTREAM_GENERATED_WITH_KNOWN_LIMITS','new warnings retained, no follow-on execution'
 print(json.dumps(dict(id=tid,status=result['status'],SHA256=artifact['SHA256'],license_days=days,INIT=count,resources=resources)),flush=True)
 return result
