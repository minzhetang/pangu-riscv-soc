"""Evidence aggregation only. No compiler, DUT, PDS or hardware invocation."""
import sys,json,re,collections
sys.dont_write_bytecode=True
import run_m2 as m
h=m.H
compiled=m.read(h/'compile-result.json');programs=m.read(h/'programs-result.json')
selftest=m.read(h/'selftest-result.json');waves=m.read(h/'wave-audit.json')
assert compiled['status']=='ALL_COMPILED_NOT_SIMULATED'
for r in compiled['rows']:assert m.s.sha(r['output'])==r['sha256']
protected=m.check_frozen()
assert programs['status']==selftest['status']==waves['status']=='PASS'
old={r['id']:r for r in m.read(m.M1/'small-result.json')['cases']+m.read(m.M1/'programs-result.json')['cases'] if r['sync']==1}
comparisons=[]
for r in programs['cases']:
    o=old[r['id']]
    metrics_same=r['metrics']==o['metrics']
    streams_same=r['actual_streams']==o['actual_streams']
    assert metrics_same and streams_same
    comparisons.append(dict(id=r['id'],metrics_equal_to_M1=metrics_same,streams_equal_to_M1=streams_same,
        actual_metrics=r['metrics'],actual_streams=r['actual_streams'],wall_seconds=r['process']['elapsed_seconds']))
warning_rows=[]
for r in compiled['rows']:
    text=m.s.text_log(r['process']['stderr'])
    warning_rows.append(dict(id=r['id'],stderr=text,warning_lines=text.count('warning:'),
        elapsed_seconds=r['process']['elapsed_seconds']))
m.save(h/'compile-diagnostics.json',dict(targets=warning_rows))
log=m.s.text_log(selftest['cases'][0]['process']['stdout'])
checks,writes=map(int,re.findall(r'MAP_SELFTEST_PASS checks=(\d+) write_edges=(\d+)',log)[0])
sources=[dict(file=n,source_sha=m.s.sha(h/'source'/n),before_sha=m.s.sha(h/'source-before'/n),M1_sha=m.s.sha(m.M1/'source'/n)) for n in ['cpu.v','alu.v','control.v','regfile.v']]
assert all(r['source_sha']==r['before_sha']==r['M1_sha'] for r in sources)
summary=dict(stage='A-MEM-MAP-M2',date_beijing='2026-10-24',status='LIMITED_PRIMITIVE_MODEL_ACCEPTED',
    CPU_changed=False,sources=sources,frozen_files_rechecked=protected,primitive_model=str(m.VENDOR/'GTP_DRM18K_E1.v'),
    primitive_sha=m.s.sha(m.VENDOR/'GTP_DRM18K_E1.v'),primitive_instances=32,ROM_instances=16,RAM_instances=16,
    ROM_bytes=32768,RAM_bytes=32768,ROM='two16-bit true-dual-port halves x eight1024-word banks',
    RAM='two16-bit single-port halves x eight1024-word banks, NORMAL_WRITE',
    revision1_compile=dict(status='FAIL_BEFORE_DUT',returncode=2,reason='Icarus lexer input buffer overflow on65536-hex-digit token',DUT_runs=0,
        preserved_directory=str(h.parent/'2026-10-24-memory-map-m2')),
    revision2_literal_equivalence=m.read(h/'literal-equivalence.json'),
    host_pack_roundtrip_checks=m.read(h/'initialization-receipts.json')['synthetic_roundtrip_checks'],
    new_compiles=10,compile_errors=0,compile_seconds=sum(r['process']['elapsed_seconds'] for r in compiled['rows']),
    compile_permission='v1 failed first/ended; v2 separately approved10 fixed targets, consumed; non-admin external compilation only',
    ordinary_DUT_runs=13,positive_runs=10,expected_protocol_rejections=3,functional_FAIL=0,TIMEOUT=0,
    full_capacity_selftest_checks=checks,selftest_real_write_edges=writes,
    complete_NEW_CPU_VCDs=len(waves['cases']),independent_wave_checks=sum(r['checks'] for r in waves['cases']),
    programs=programs['cases'],comparison_to_behavioral_M1=comparisons,
    limitations=['functional official-primitive MODEL binding, not PDS mapping/synthesis/resource/Fmax or board verification',
        'fullcapacity selftest pattern; old six probes use their frozen visible apertures inside fullallocated primitives',
        'RAM same-port NORMAL_WRITE outputs not consumed as read data during STORE; no cross-port RAM collision promise',
        'no complete CoreMark VCD: first4096physical clocks plus stopped tail, full streams/state and invariants separate',
        'same~two-clock pipeline advance cost, no efficiency gain or valid CoreMark timing/score',
        'no real retirement PC/unifiedWB-STORE commit stream; fixed memory/reset-state limits',
        'no UART/GPIO integration, no hardware; over_tempSTOP unchanged'])
m.save(h/'summary.json',summary)
with (h/'RESULT_MATRIX.md').open('x',encoding='utf-8') as f:
    f.write('# 逐项实测\n\n|项目|结果|证据|\n|---|---|---|\n')
    for r in selftest['cases']:
        f.write(f"|selftest-{r['id']} {r['expected']}|{r['status']}|{r['process']['stdout']}|\n")
    f.write('\n|CPU程序|结果|物理沿|推进沿|stall/flush|墙时秒|\n|---|---|---:|---:|---|---:|\n')
    for r in programs['cases']:
        a=r['metrics'];f.write(f"|{r['id']}|{r['status']}|{a['physical']}|{a['advances']}|{a['stall']}/{a['flush']}|{r['process']['elapsed_seconds']}|\n")
with (h/'COMMANDS.md').open('x',encoding='utf-8') as f:
    f.write('# 实际命令\n\nv1失败原命令/rc见兄弟目录；本页为v2十次权限编译、十三次普通仿真。早期selftest及程序只有在其各自编译已结束rc0/产物SHA核对后运行，最终还核整个compile-result。无外部仿真。\n\n')
    for r in compiled['rows']+selftest['cases']+programs['cases']:
        p=r['process'];f.write('```json\n'+json.dumps({k:p[k] for k in ['argv','cwd','timeout_seconds','returncode','elapsed_seconds']},ensure_ascii=False)+'\n```\n\n')
with (h/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
    for p in sorted(h.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS.txt':f.write(m.s.sha(p)+'  '+p.relative_to(h).as_posix()+'\n')
print(json.dumps(dict(status=summary['status'],protected=protected,CPU_unchanged=True,compile_seconds=summary['compile_seconds'],
    selftest_checks=checks,wave_checks=summary['independent_wave_checks'],programs=[dict(id=r['id'],status=r['status'],wall=r['process']['elapsed_seconds']) for r in programs['cases']])))
