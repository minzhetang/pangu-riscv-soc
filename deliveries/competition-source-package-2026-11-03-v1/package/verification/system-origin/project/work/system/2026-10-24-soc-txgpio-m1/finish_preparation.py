"""Preparation-only postflight; complete system always remains NOT_RUN here."""
from pathlib import Path
import sys,json,ast
sys.dont_write_bytecode=True
import build_prepare as b
h=b.H
protected=b.s.read(h/'preparation-frozen.json')['files']
assert all(b.s.sha(r['path'])==r['sha256'] for r in protected)
for p in h.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
build=b.s.read(h/'firmware-build.json');a=b.s.read(h/'adapter-result.json')
c=b.s.read(h/'checker-selftest.json');ref=b.s.read(h/'software-reference-selftest.json')
assert build['status']==a['status']==c['status']==ref['status']=='PASS'
assert all(not p.exists() for p in [h/'build/soc.vvp',h/'system-result.json'])
rows=[]
for r in build['commands']:
    stderr=b.s.text_log(r['stderr']);assert not stderr.strip(),stderr
    rows.append(dict(id=r['id'],process=r))
adapter_compile=b.s.read(h/'adapter-compile-result.json');assert adapter_compile['status']=='PASS_NOT_RUN'
assert b.s.sha(h/'build/adapter.vvp')==adapter_compile['sha256']
sources=[dict(file=n,sha256=b.s.sha(h/'source'/n)) for n in ['cpu.v','alu.v','control.v','regfile.v','memory_model.sv']]
out=dict(stage='A-SOC-TXGPIO-M1',authorization='D120 explicitly approved',date_beijing='2026-10-24',
    status='PREPARATION_VERIFIED_SYSTEM_PENDING_B_PACKAGE',sources=sources,protected_files=len(protected),
    firmware=b.s.read(h/'firmware-artifacts.json'),firmware_CPU_DUT_runs=0,complete_SoC_compile='NOT_RUN',
    complete_SoC_simulation='NOT_RUN',B_module_reproduction='NOT_RUN_NEW_PACKAGE_NOT_RECEIVED',
    candidate_live_checker='PYTHON_SYNTAX_ONLY; end-to-end positive/negative tests NOT_RUN',
    routing_unit=a,contract_checker_synthetic=c,software_reference_synthetic=ref,
    GPIO_stimulus_bound=b.s.read(h/'gpio-stimulus-bound.json'),
    B_contract='LOCAL-REGIF-TXGPIO-M1/1.0.0 unchanged; no A replacement implementation',
    hardware='STOP over_temp unchanged',new_external_compile_permission='one adapter-only target, consumed',
    next='continue SAME approved stage after B intake, separately gate new external compiler execution')
b.s.save(h/'preparation-summary.json',out)
with (h/'COMMANDS-preparation.md').open('x',encoding='utf-8') as f:
    f.write('# 已实际执行的原生命令\n\n六项普通工具链命令＋一次单目标外部仅编译＋一次普通路由单元仿真；不含完整SoC。Python合成/参考/推导与语法测试另有对应JSON，非CPU实跑。\n\n')
    for p in build['commands']+[adapter_compile['process'],a['process']]:
        f.write('```json\n'+json.dumps({k:p[k] for k in ['argv','cwd','timeout_seconds','returncode','elapsed_seconds']},ensure_ascii=False)+'\n```\n\n')
with (h/'SHA256SUMS-preparation.txt').open('x',encoding='utf-8') as f:
    for p in sorted(h.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS-preparation.txt':f.write(b.s.sha(p)+'  '+p.relative_to(h).as_posix()+'\n')
print(json.dumps(dict(status=out['status'],protected_files=len(protected),firmware_bytes=out['firmware']['bytes'],
    CPU_runs=0,SoC_runs=0,route_unit_checks=a['checks'],checker_synthetic=c['checks'])))
