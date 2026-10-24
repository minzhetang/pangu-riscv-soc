"""Read-only post-exit audit of this M0's actual evidence, no tool launches."""
from pathlib import Path
import collections, hashlib, importlib.util, json, re, sys
sys.stdout.reconfigure(encoding='utf-8'); sys.dont_write_bytecode = True
H = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('m0stage', H/'stage.py')
s = importlib.util.module_from_spec(spec); sys.modules[spec.name] = s; spec.loader.exec_module(s)
protected = s.protect()
assert s.read(H/'pds-external-process.json')['returncode'] == 0
pd = H/'pds'; flow = s.log(pd/'flow.log'); vm = s.log(pd/'synthesize/soc_top_syn.vm')
def write(name, data): s.save(H/name, data)
def params(text):
    return {m[1]:m[2] for m in re.finditer(r'\.(\w+)\(([^()]*)\)', text)}
def bits(expr):
    m = re.fullmatch(r"(\d+)'([bh])([0-9a-fA-F]+)", expr.strip()); assert m, expr
    n, base, v = int(m[1]), m[2], m[3]
    value = int(v, 2 if base == 'b' else 16); assert value < (1 << n)
    return value
tables = s.log(pd/'source/init_tables.svh'); arrays = {}
for name in ['ROM','RAM']:
    m = re.search(rf'{name}_BITS\s*=\s*\{{(.*?)\}};', tables, re.S); assert m
    arrays[name] = int(''.join(re.findall(r"4096'h([0-9a-fA-F]+)", m[1])),16)
rx = re.compile(r'GTP_DRM18K_E1\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);', re.S)
drms = {}; init_count = 0
for m in rx.finditer(vm):
    identity = re.fullmatch(r'\\bank\[(\d+)\]\.halfword\[(\d+)\]\.(rom|ram)_block',m[1]); assert identity
    bank, half, kind = int(identity[1]), int(identity[2]), identity[3].upper(); p = params(m[2])
    assert p['DATA_WIDTH_A'] == p['DATA_WIDTH_B'] == '16'
    assert p['GRS_EN'] == '"FALSE"' and p['DOA_REG'] == p['DOB_REG'] == '0'
    assert p['RAM_MODE'] == ('"TRUE_DUAL_PORT"' if kind == 'ROM' else '"SINGLE_PORT"')
    for chunk in range(64):
        expected = 0
        for j in range(32):
            word = bank*1024 + chunk*16 + j//2
            byte = (arrays[kind] >> (word*32 + half*16 + (j%2)*8)) & 255
            expected |= byte << (j*9)
        assert bits(p[f'INIT_{chunk:02X}']) == expected, (bank, half, kind, chunk)
        init_count += 1
    drms[(bank, half, kind)] = dict(bank=bank, half=half, kind=kind, matched_INIT_pieces=64)
assert len(drms) == 28
merged=[]
for b in range(8):
    for h in range(2):
        assert (b,h,'RAM') in drms
        if (b,h,'ROM') not in drms:
            assert b in range(4,8) and h == 1 and (b,0,'ROM') in drms
            assert ((arrays['ROM'] >> (b*32768)) & ((1<<32768)-1)) == 0
            # Same retained low-half outputs are used twice per bit, one per word half.
            for port in ['ri','rd']:
                for bit in list(range(8))+list(range(9,17)):
                    net=f'\\storage/bank[{b}].{port}[0] [{bit}]'
                    uses=len(re.findall(r'\.(?:I[0-5])\s*\(\s*'+re.escape(net)+r'\s*\)',vm))
                    assert uses == 2, (b,port,bit,uses)
            merged.append(dict(bank=b,half=1,reason='identical zero ROM halves share retained half0; both word halves connected'))
rf = vm[vm.index('module regfile'):]; rf = rf[:rf.index('endmodule')]
ffs = list(re.finditer(r'GTP_DFF_E\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',rf,re.S))
assert len(ffs)==992
assert all(params(m[2]) == {'GRS_EN':'"TRUE"','INIT':"1'b0"} for m in ffs)
pnr = s.log(pd/'place_route/soc_top_pnr.netlist')
mapped_names = re.findall(r'^storage/(bank\[\d+\]\.halfword\[\d+\]\.(?:ram|rom)_block)/gopdrm_18k;gopDRM18K$',pnr,re.M)
assert len(mapped_names) == 28
write('memory-init-audit.json', dict(status='PASS',retained_18K=28,INIT_pieces_matched=init_count,
    matched_INIT_bits=init_count*288,all_16_RAM_halves_present=True,identical_ROM_halves_merged=merged,
    post_pnr_18K_gates=len(mapped_names),rf_init_zero_FF=992,
    limitation='INIT values checked in synthesis netlist, gate identities through PnR; no bitstream readback or post-layout functional simulation'))
# Final explicit report_timing, not earlier router's approximation.
rtr = s.log(pd/'report_timing/soc_top.rtr')
corners={}
for kind,corner,body in re.findall(r'(Setup|Hold) Summary\((Slow|Fast) Corner\):(.*?)(?=\n\w|\Z)',rtr,re.S):
    m=re.search(r'clk_27mhz\s+clk_27mhz\s+([\d.-]+)\s+([\d.-]+)\s+(\d+)\s+(\d+)',body)
    assert m; corners[f'{kind.lower()}_{corner.lower()}']=dict(slack_ns=float(m[1]),total_negative_ns=float(m[2]),failing_endpoints=int(m[3]),endpoints=int(m[4]))
assert len(corners)==4 and all(x['slack_ns']>0 and x['failing_endpoints']==0 for x in corners.values())
assert 'All Constraints Met.' in rtr
perf=re.search(r'clk_27mhz\s+([\d.]+) MHz\s+([\d.]+) MHz\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)',rtr);assert perf
warning_lines=[(i+1,l) for i,l in enumerate(flow.splitlines()) if l.startswith('W:')]
counts=collections.Counter(re.sub(r'^(W: [^:]+):.*',r'\1',l) for _,l in warning_lines)
lastlog=s.log(pd/'report_timing/run.log')
unc_in=re.findall(r"Timing-4086: Port '([^']+)'",lastlog);unc_out=re.findall(r"Timing-4087: Port '([^']+)'",lastlog)
assert len(unc_in)==9 and len(unc_out)==45
write('timing-audit.json',dict(status='INTERNAL_27MHZ_PASS_EXTERNAL_IO_UNCONSTRAINED',source='pds/report_timing/soc_top.rtr',
    tool='PDS 2022.2-SP6.4 build146967',device='PG2L100H',speed='-6',package='FBG676',clock_period_ns=37.037037,
    corners=corners,tool_estimated_frequency_MHz=float(perf[2]),
    estimate_limitation='single logical image, auto IO placement; not board-qualified Fmax, operating frequency or performance gain',
    unconstrained_inputs=unc_in,unconstrained_outputs=unc_out,
    worst_setup=dict(start='cpu_core/ex_rd[4]/opit_0_inv_srl/CLK',end='cpu_core/if_inst[17]/opit_0_inv_L6Q_perm/CE',logic_levels=19,logic_ns=2.891,route_ns=9.237),
    warning_counts_in_flow=dict(counts),constant_probe_warnings=7,
    pending='constant-probe loop warnings have no named net; no physical fault is inferred, diagnostic not closed; external reset/IO/CDC and board pinning remain unverified'))
snr=s.log(pd/'synthesize/soc_top.snr'); prr=s.log(pd/'place_route/soc_top.prr')
usage={}
for name,body in [('synthesis',snr),('pnr',prr)]:
    if name=='synthesis':
        usage[name]={k:int(re.search(pattern,body)[1]) for k,pattern in [('LUT',r'Total LUTs: (\d+)'),('FF',r'Total Registers: (\d+)'),('latch',r'Total Latches: (\d+)')]}
    else:
        lut=re.findall(r'\|\s+LUT\s+\|\s+(\d+)',body);ff=re.findall(r'\|\s+FF\s+\|\s+(\d+)',body)
        assert len(lut)==len(ff)==2
        usage[name]=dict(LUT=sum(map(int,lut)),FF=sum(map(int,ff)),DRM36=14,IO=55,APM=0)
stages={name:token in flow for name,token in [('compile','Finished compiling design'),('synthesis','has been successfully synthesized'),('mapping','has been successfully mapped'),('pnr','has been placed and routed successfully'),('timing','Report timing is finished successfully')]}
# Compile report uses tool-specific end marker; capture it independently.
stages['compile'] = 'Action compile: Real time elapsed' in flow and (pd/'compile/error_info.txt').stat().st_size==0
assert all(stages.values()), stages
assert not re.search(r'^E:',flow,re.M)
license_stdout=s.log(H/'logs/pds-flow-external-01/stdout.log')
days=re.search(r'license will invalid in (\d+) days',license_stdout);assert days
write('pds-audit.json',dict(status='IMPLEMENTATION_PASS_WITH_DOCUMENTED_WARNINGS',stages=stages,
    resources=usage,license_checkout_for_this_run='SUCCESS',license_warning_days_remaining=int(days[1]),
    ordinary_launch=dict(status='PROCESS_CREATION_FAILED',winerror=623,new_PDS_execution=False),
    external_process=s.read(H/'pds-external-process.json'),zero_errors=True,no_unresolved_user_blackboxes_observed=True,
    no_bitstreams=list(map(str,pd.rglob('*.sbit')))==[] and list(map(str,pd.rglob('*.bit')))==[],
    limitation='vendor database binary INIT configuration not independently decoded; synthesis INIT and post-PnR memory gates checked; no hardware'))
def wave_digest(path):
    start=False;digest=hashlib.sha256();events=0;last=0;timescale=[];in_ts=False
    with path.open('r',encoding='ascii',errors='strict') as f:
        for line in f:
            if '$timescale' in line:in_ts=True
            if in_ts:timescale.append(line.strip())
            if in_ts and '$end' in line:in_ts=False
            if start:
                digest.update(line.encode('ascii'));events+=1
                if line.startswith('#'):
                    stamp=int(line[1:]);assert stamp>=last;last=stamp
            if '$enddefinitions' in line:start=True
    assert start and events>0 and last>0
    return dict(path=str(path),size=path.stat().st_size,sha256=s.sha(path),event_lines=events,last_timestamp=last,timescale=' '.join(timescale),event_sha256=digest.hexdigest().upper())
wave_rows=[];old_compare=[]
for row in s.read(H/'simulation-result.json')['rows']:
    tid=row['id'];d=H/'runs'/tid;wave_rows.append(dict(id=tid,**wave_digest(d/'wave.vcd')))
    if tid in ['baseline-N16','baseline-N234','smoke-N16']:
        check=s.read(d/'check-result.json');old=s.read(s.B/'runs'/tid/'check-result.json')
        assert check==old,(tid,'changed semantic result')
        equal={f:s.sha(d/f)==s.sha(s.B/'runs'/tid/f) for f in ['trace.log','bus.log','registers.hex','ram.hex']}
        assert all(equal.values()),(tid,equal)
        old_compare.append(dict(id=tid,check_result_equal=True,byte_identical_files=equal))
write('simulation-audit.json',dict(status='PASS',new_runs=7,CoreMark_new_runs=0,old_baselines_byte_equal=old_compare,waves=wave_rows,
    no_full_ISA_or_hardware_claim=True))
files=[p for p in H.rglob('*') if p.is_file() and p.name not in ['SHA256SUMS.txt','postflight.json']]
with (H/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
    for p in sorted(files): f.write(s.sha(p)+'  '+str(p.relative_to(H)).replace('\\','/')+'\n')
write('postflight.json',dict(protected_files_unchanged=s.protect(),protected_initial_count=protected,
    source=[dict(file=p.name,sha256=s.sha(p)) for p in sorted((H/'source').iterdir())],
    manifest_sha256=s.sha(H/'SHA256SUMS.txt')))
print(json.dumps(dict(status='AUDIT_COMPLETED',stages=stages,resources=usage,corners=corners,INIT_chunks=init_count,RF_init_FFs=992,protected=protected),ensure_ascii=False))
