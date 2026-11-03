from pathlib import Path
import json,re,hashlib,collections
H=Path(__file__).resolve().parent;R=H.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p):return p.read_text(encoding='utf-8-sig',errors='replace')
results=[]
for pred in [0,1,32]:
 d=H/f'pred{pred}';exit=json.loads((H/f'pred{pred}-BUILD_EXIT.json').read_text());flow=text(d/'flow.log');rtr=text(d/'report_timing/board_top_hl4.rtr');prr=text(d/'place_route/board_top_hl4.prr');ccr=text(d/'constraint_check/constraint_check.ccr')
 stages={k:s in flow for k,s in dict(synth='has been successfully synthesized',mapped='has been successfully mapped',routed='has been placed and routed successfully',timing='Report timing is finished successfully').items()}
 perf=re.search(r'^\s*clk_27mhz\s+([\d.]+) MHz\s+([\d.]+) MHz\s+([\d.]+)\s+([\d.]+)\s+(-?[\d.]+)',rtr,re.M)
 if not perf:raise RuntimeError('Missing performance summary')
 timing={}
 for kind,corner,body in re.findall(r'(Setup|Hold|Recovery|Removal) Summary\((Slow|Fast) Corner\):(.*?)(?=\n\w|\Z)',rtr,re.S):
  for launch,capture,slack,tns,failing,endpoints in re.findall(r'^\s*(\S+)\s+(\S+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(\d+)\s+(\d+)\s*$',body,re.M):
   if launch==capture=='clk_27mhz':timing[kind+'_'+corner]=dict(slack_ns=float(slack),failing=int(failing),endpoints=int(endpoints))
 resources=dict(LUT=sum(map(int,re.findall(r'\|\s+LUT\s+\|\s+(\d+)\s*\|',prr))),FF=sum(map(int,re.findall(r'\|\s+FF\s+\|\s+(\d+)\s*\|',prr))),DRM36=float(re.search(r'\|\s+Use of DRM\s+\|\s+([\d.]+)',prr)[1]),IO=int(re.search(r'\|\s+Use of IO\s+\|\s+(\d+)',prr)[1]))
 warnings=[s for s in flow.splitlines() if s.startswith('W:')];crit=[s for s in flow.splitlines() if s.startswith(('C:','E:'))]
 summary=re.search(r'(\d+) error\(s\), (\d+) critical warning\(s\), (\d+) warning\(s\), out of (\d+) constraint',ccr)
 constraints=dict(errors=int(summary[1]),critical=int(summary[2]),warnings=int(summary[3]),count=int(summary[4])) if summary else None
 romtext=text(d/'source/init_tables.svh');parts=re.findall("4096'h([0-9a-f]{1024})",romtext.split('ROM_BITS = ')[1].split(';')[0]);rom=bytes.fromhex(''.join(parts))[::-1];binary=(R/'work/advanced/2026-11-03-coremark-strict-m5/build/performance/program.bin').read_bytes()
 init_ok=rom==binary+bytes(32768-len(binary));init_count=0;init_blocks=[]
 vm=text(d/'synthesize/board_top_hl4_syn.vm');rx=re.compile(r'GTP_DRM18K_E1\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',re.S)
 for match in rx.finditer(vm):
  ident=re.fullmatch(r'\\bank\[(\d+)\]\.halfword\[(\d+)\]\.(rom|ram)_block',match[3])
  if not ident:continue
  bank,half,kind=int(ident[1]),int(ident[2]),ident[3];payload=rom if kind=='rom' else bytes(32768);init_blocks.append(match[3])
  for par in re.finditer(r'\.(INIT_[0-9A-F]{2})\s*\(([^()]*)\)',match[2]):
   chunk=int(par[1][-2:],16);raw=re.sub(r'\s+','',par[2]);literal=raw.split("'")[1];actual=int(literal[1:],{'h':16,'b':2,'d':10,'o':8}[literal[0]])
   expected=sum(payload[(bank*1024+chunk*16+j//2)*4+half*2+j%2]<<(9*j) for j in range(32))
   if actual!=expected:raise RuntimeError(('INIT mismatch',pred,match[3],par[1]))
   init_count+=1
 checks=dict(native=exit['error'] is None and exit['cleanup']['root_exit_code']==0,cleanup=exit['cleanup']['job_empty'] and not exit['cleanup']['forced_cleanup'],inputs=exit['inputs_unchanged'],stages=all(stages.values()),no_critical_error=not crit,constraints=bool(constraints) and constraints['errors']==constraints['critical']==0,clock_checks=len(timing)==8 and all(t['slack_ns']>=0 and t['failing']==0 for t in timing.values()),image=init_ok,primitive_init=init_count==64*len(init_blocks) and init_count>0,no_bitstream=not any(d.rglob('*.sbit')),no_latches='Total Latches: 0' in text(d/'synthesize/board_top_hl4.snr'))
 results.append(dict(pred=pred,checks=checks,stages=stages,resources=resources,primitive_init_pieces=init_count,primitive_init_blocks=init_blocks,performance=dict(requested_MHz=float(perf[1]),estimated_MHz=float(perf[2]),requested_period_ns=float(perf[3]),estimated_period_ns=float(perf[4]),slack_ns=float(perf[5])),timing=timing,constraints=constraints,warnings=warnings,warning_counts=dict(collections.Counter(re.sub(r'^(W: [^:]+):.*',r'\1',s) for s in warnings)),critical_errors=crit,elapsed_seconds=exit['elapsed_seconds'],pass_=all(checks.values())))
diff=[]
for p in sorted((H/'pred0/source').iterdir()):
 q=H/'pred1/source'/p.name
 if p.read_bytes()!=q.read_bytes():
  if p.name!='board_top_hl4.sv' or p.read_text().replace('.BTB_ENABLE     (0)','.BTB_ENABLE     (1)')!=q.read_text():raise RuntimeError('Unmatched comparison input')
  diff.append(p.name)
for name in ['board_pins.fdc','clock_27mhz.fdc','closure_io.fdc','flow.tcl']:
 if (H/'pred0'/name).read_bytes()!=(H/'pred1'/name).read_bytes():raise RuntimeError('Constraint or flow differs')
for p in (H/'pred1/source').iterdir():
 q=H/'pred32/source'/p.name
 if p.read_bytes()!=q.read_bytes() and (p.name!='board_top_hl4.sv' or p.read_text().replace('.BTB_INDEX_BITS (6)','.BTB_INDEX_BITS (5)')!=q.read_text()):raise RuntimeError('32-entry input differs beyond parameter')
for name in ['board_pins.fdc','clock_27mhz.fdc','closure_io.fdc','flow.tcl']:
 if (H/'pred0'/name).read_bytes()!=(H/'pred32'/name).read_bytes():raise RuntimeError('32-entry constraints or flow differ')
protected=[dict(path=x['path'],unchanged=sha(R/x['path']).upper()==x['sha256']) for x in json.loads((H/'PROTECTED_INPUTS.json').read_text())]
result=dict(status='OFFLINE_STA_RESOURCE_PAIR_PASS_NOT_HARDWARE' if all(x['pass_'] for x in results) else 'FAIL',results=results,only_source_difference=diff,protected=protected,physical_IO_CDC_signoff=False,frequency_is='PDS estimated internal clock frequency under specified constraints, NOT measured board Fmax',hardware_calls=0)
(H/'AUDIT.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(status=result['status'],results=[dict(pred=x['pred'],checks=x['checks'],resources=x['resources'],performance=x['performance'],constraints=x['constraints'],warning_counts=x['warning_counts']) for x in results]),indent=2))
if result['status']=='FAIL' or not all(x['unchanged'] for x in protected):raise SystemExit(1)
