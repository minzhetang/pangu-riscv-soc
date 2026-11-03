from pathlib import Path
import hashlib, json, re, shutil, difflib

H = Path(__file__).resolve().parent
R = H.parents[2]
B = R / 'work/fpga/2026-10-30-coremark256-nodebug-m1/performance256/pds'
OLD = R / 'work/fpga/2026-10-28-local-debug-insert-m1-r4'
SW = R / 'work/software/2026-10-29-formal-coremark-m1/build/performance256'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(name, value):
    with (H / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)

assert not (H / 'SOURCE_RECEIPTS.json').exists(), 'Preserve existing preparation'
assert sha(SW / 'program.bin') == '0160BF311C70A8CCDDDF1B4F19B96C4F5B7357CB2E4BD04E69DB9A87DBC8C21E'
assert sha(SW / 'program.elf') == 'FA9822A21D61AE72E807541CFB9676EE308D3F247EF7180F84E74151AD7B0D1C'
strip = lambda s: re.sub(r' /\* synthesis PAP_MARK_DEBUG="true" \*/', '', s)
protected, sources, patches = [], [], []
for p in sorted((B / 'source').iterdir()):
    if not p.is_file(): continue
    protected.append(dict(path=str(p.relative_to(R)), sha256=sha(p)))
    for folder in ['source-before', 'source', 'pre/source', 'build/source']:
        (H / folder).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, H / folder / p.name)
    if p.name in ['cpu.v', 'board_top.sv', 'soc_top.sv']:
        original = p.read_text()
        marked = (OLD / 'source' / p.name).read_text()
        assert strip(marked) == original, 'Functional source mismatch: ' + p.name
        for folder in ['source', 'pre/source', 'build/source']:
            (H / folder / p.name).write_text(marked, encoding='utf-8')
        patches.extend(difflib.unified_diff(original.splitlines(True), marked.splitlines(True),
                                         fromfile='source-before/' + p.name, tofile='source/' + p.name))
    else:
        assert (H / 'source' / p.name).read_bytes() == p.read_bytes()
    sources.append(dict(name=p.name, original_sha256=sha(p), observed_sha256=sha(H / 'source' / p.name),
                        functional_text_equal=strip((H / 'source' / p.name).read_text()) == p.read_text()))
assert all(x['functional_text_equal'] for x in sources)
(H / 'OBSERVABILITY_ONLY.patch').write_text(''.join(patches), encoding='utf-8')
(H / 'firmware').mkdir()
for name in ['program.bin', 'program.elf', 'program.map', 'FROZEN_BUILD.json']:
    shutil.copyfile(SW / name, H / 'firmware' / name)
    protected.append(dict(path=str((SW / name).relative_to(R)), sha256=sha(SW / name)))
for phase in ['pre', 'build']:
    for name in ['board_pins.fdc', 'clock_27mhz.fdc']:
        shutil.copyfile(B / name, H / phase / name)
    flow = (OLD / phase / 'flow.tcl').read_text()
    (H / phase / 'flow.tcl').write_text(flow, encoding='utf-8')
    if phase == 'pre': assert 'gen_bit_stream' not in flow and 'add_fic' not in flow
fic = (OLD / 'debug.fic').read_text()
old_adf = str(OLD / 'pre/synthesize/board_top_syn.adf').replace('\\', '/')
new_adf = str(H / 'pre/synthesize/board_top_syn.adf').replace('\\', '/')
assert old_adf in fic
fic = '# Derived from frozen R4 ordered probe template; no new GUI-generation claim.\n' + fic.replace(old_adf, new_adf)
(H / 'debug.fic').write_text(fic, encoding='utf-8')
protected += [dict(path=str((OLD / x).relative_to(R)), sha256=sha(OLD / x))
              for x in ['debug.fic', 'source/cpu.v', 'source/soc_top.sv', 'source/board_top.sv']]
save('SOURCE_RECEIPTS.json', dict(sources=sources, firmware_fixed=True,
     program_binary_sha256=sha(H / 'firmware/program.bin'), original_sources_unchanged=True,
     modifications='Only seven previously-used PAP_MARK_DEBUG retention annotations in three copied files',
     no_functional_RTL_or_software_changes=True))
save('PROTECTED_INPUTS.json', protected)
save('SCOPE.json', dict(decision='D288', user_resume_and_connections_reported=True,
     goal='Real FPGA pipeline/control-flow efficiency windows and report for frozen performance256 program',
     pre_synthesis_max=1, implementation_max=1, pre_limit_seconds=180, implementation_limit_seconds=1800,
     FIC_reuse='Same140 ordered probes, new pre ADF; require structural synthesis identity before insertion',
     new_functional_RTL=False, software_builds=0, new_CPU_ISA=False,
     hardware_initial_configurations=1, load_method='Audited full original vendor CRAM SVF100kHz',
     configuration_seconds=600, controller_seconds=700,
     planned_windows=['list','matrix','state','matrix_repeat'], physical_user_KEY0_only_after_fresh_arm=True,
     metrics='EX event density, physical-vs-logical slots, qualified stalls/flushes and function ownership; not retired IPC',
     old_clock_Critical_and_CDC_not_waived=True, Flash=False, protection_changes=False,
     SCBV_setting='Existing High Voltage engineering decision unchanged',
     GUI_native_tools_authorized_by_current_user=True, new_installs=False, D245_no_commit_push=True))
print('Prepared fixed-performance256 observation-only copy; no PDS or hardware executed.')
