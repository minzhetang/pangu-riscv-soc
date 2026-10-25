"""Post-exit source/INIT/reset/pin/resource/timing checks, no new build."""
from pathlib import Path
import collections,json,re,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_board as s
pd=H/'pds';r=s.read(H/'pds-process.json');assert r['returncode']==0 and not r['timed_out'] and not r['cap']
flow=s.log(pd/'flow.log');assert not re.search(r'^E:',flow,re.M)
stages=dict(compile='Action compile: Real time elapsed' in flow and (pd/'compile/error_info.txt').stat().st_size==0,
    synthesis='has been successfully synthesized' in flow,mapping='has been successfully mapped' in flow,
    pnr='has been placed and routed successfully' in flow,timing='Report timing is finished successfully' in flow)
assert all(stages.values())
def params(text):return {m[1]:re.sub(r'\s+','',m[2]) for m in re.finditer(r'\.(\w+)\s*\(([^()]*)\)',text)}
rx=re.compile(r'GTP_DRM18K_E1\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',re.S)
vm=s.log(pd/'synthesize/board_top_syn.vm');oldvm=s.log(s.B/'pds/synthesize/soc_top_syn.vm')
def drms(text):return {m[1]:params(m[2]) for m in rx.finditer(text)}
new_drm,old_drm=drms(vm),drms(oldvm);assert len(new_drm)==28 and new_drm==old_drm
assert all(len([k for k in d if re.fullmatch('INIT_[0-9A-F]{2}',k)])==64 for d in new_drm.values())
assert s.sha(pd/'source/init_tables.svh')==s.sha(s.B/'pds/source/init_tables.svh')
def module(name):
    start=vm.index('module '+name+'\n');return vm[start:vm.index('endmodule',start)]
rf=module('regfile');ffrx=re.compile(r'GTP_DFF\w*\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',re.S)
ffs=list(ffrx.finditer(rf));assert len(ffs)==992 and all(params(m[2])['INIT']=="1'b0" for m in ffs)
reset=module('board_reset_sync');resetffs=list(ffrx.finditer(reset));assert len(resetffs)==3
for i,m in enumerate(resetffs):
    assert m[1].strip()==f'\\release_ff[{i}]'
    assert params(m[2])=={'GRS_EN':'"TRUE"','INIT':"1'b0"}
    ports=params(m[4]);assert ports['CLK']=='clk' and ports['C']=='N0'
    assert ports['D']==("1'b1" if i==0 else f'release_ff[{i-1}]')
assert '.I (key0_n)' in reset and '.Q (sys_rst_n)' in reset
gpio=module('gpio_core');gff={m[1].strip() for m in ffrx.finditer(gpio)}
assert all(f'\\{name}[{i}]' in gff for name in ['sync_meta','gpio_in_sync'] for i in range(4))
assert not any(f'\\sync_meta[{i}]' in gff or f'\\gpio_in_sync[{i}]' in gff for i in range(4,8))
pnr=s.log(pd/'place_route/board_top_pnr.netlist');assert len(re.findall(r';gopDRM18K$',pnr,re.M))==28
prr=s.log(pd/'place_route/board_top.prr');pins={}
for l in prr.splitlines():
    a=[v.strip() for v in l.split('|')]
    if len(a)>8 and a[1] in s.read(H/'pin-plan.json')['pins']:
        pins[a[1]]=dict(direction=a[2],loc=a[3],bank=a[4],VCCIO=a[5],standard=a[6])
assert len(pins)==15 and all(pins[n]['loc']==v and pins[n]['VCCIO']=='3.3' and pins[n]['standard']=='LVCMOS33' for n,v in s.read(H/'pin-plan.json')['pins'].items())
ccr=s.log(pd/'constraint_check/constraint_check.ccr');assert '0 error(s), 0 critical warning(s), 0 warning(s), out of 94 constraint(s)' in ccr
rtr=s.log(pd/'report_timing/board_top.rtr');timing={}
for kind,corner,body in re.findall(r'(Setup|Hold|Recovery|Removal) Summary\((Slow|Fast) Corner\):(.*?)(?=\n\w|\Z)',rtr,re.S):
    m=re.search(r'clk_27mhz\s+clk_27mhz\s+([\d.-]+)\s+([\d.-]+)\s+(\d+)\s+(\d+)',body);assert m
    timing[f'{kind.lower()}_{corner.lower()}']=dict(slack_ns=float(m[1]),total_negative_ns=float(m[2]),failing_endpoints=int(m[3]),endpoints=int(m[4]))
assert len(timing)==8 and all(v['slack_ns']>0 and v['failing_endpoints']==0 for v in timing.values())
estimated=re.search(r'clk_27mhz\s+27.0000 MHz\s+([\d.]+) MHz',rtr);assert estimated
warnings=[l for l in flow.splitlines() if l.startswith('W:')];counts=collections.Counter(re.sub(r'^(W: [^:]+):.*',r'\1',l) for l in warnings)
log=s.log(pd/'report_timing/run.log');ui=re.findall(r"Timing-4086: Port '([^']+)'",log);uo=re.findall(r"Timing-4087: Port '([^']+)'",log)
assert len(ui)==5 and len(uo)==9
stdout=s.log(H/'logs/pds-flow-once/stdout.log');days=re.search(r'license will invalid in (\d+) days',stdout);assert days
lut=sum(map(int,re.findall(r'\|\s+LUT\s+\|\s+(\d+)',prr)));ff=sum(map(int,re.findall(r'\|\s+FF\s+\|\s+(\d+)',prr)))
assert lut>1000 and ff>1000 and 'Total Latches: 0' in s.log(pd/'synthesize/board_top.snr')
for row in s.read(s.B/'postflight.json')['source']:
    assert s.sha(H/'source'/row['file'])==row['sha256']==s.sha(H/'source-before'/row['file'])
assert not list(pd.rglob('*.bit')) and not list(pd.rglob('*.sbit'))
assert 'gen_bit_stream' not in s.log(pd/'build.tcl')
result=dict(status='FINITE_BOARD_SOFTWARE_IMPLEMENTATION_PASS_WITH_LIMITS',stages=stages,
    tool='PDS2022.2-SP6.4 build146967',device='PG2L100H',speed='-6',package='FBG676',process=r,
    pin_constraints=dict(status='PASS',count=15,ccr_errors=0,ccr_warnings=0,ccr_commands=94,pins=pins),
    resources=dict(LUT=lut,FF=ff,DRM36=14,DRM18_gates=28,IO=15,APM=0,latches=0),
    memory=dict(INIT_pieces_1792_equal_F141=True,entire_init_table_sha_equal=True,RF_INIT_zero_FFs=992,
                limitation='synthesis INIT equivalence and mapped identities only; no binary config decode/readback/post-layout simulation'),
    reset=dict(retained_FFs=3,INIT_zero=True,three_stage_chain=True,low_GPIO_synchronizer_FFs=8,high_GPIO_constant_zero=True,
               limitation='no debounce, minimum pulse/MTBF/physical CDC guarantee or arbitrary warm restart proof'),
    timing=timing,estimated_internal_MHz=float(estimated[1]),
    estimate_limitation='one pinned design/image/tool estimate, not measured frequency, qualified board Fmax or speedup',
    asynchronous_inputs_without_delay=ui,outputs_without_delay=uo,
    warning_counts=dict(counts),constant_probe_count=counts['W: Loop was found during constant probe.'],
    constant_probe_diagnosis='same seven sdm2adm constant-probe warnings as F141; no named net provided, root cause remains open, not classified as harmless or physical loop',
    license_checkout='SUCCESS_FOR_THIS_RUN',license_warning_days_remaining=int(days[1]),
    all_previous_11_sources_unchanged=True,protected_files=s.protect(),no_bitstream=True,hardware='STOPPED')
s.save(H/'pds-audit.json',result)
print(json.dumps(dict(status=result['status'],resources=result['resources'],timing=timing,IO_pins=15,license_days=int(days[1]),protected=result['protected_files'])))
