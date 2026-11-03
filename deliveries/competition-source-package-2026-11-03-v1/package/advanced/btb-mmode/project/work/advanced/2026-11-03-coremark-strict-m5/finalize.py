"""Finalize existing evidence only. Never builds, simulates, or contacts hardware."""
from pathlib import Path
import hashlib
import json
import re
import difflib

H = Path(__file__).resolve().parent
R = H.parents[2]
F = R / 'work/fpga/2026-11-03-advanced-btb-offline-m1'
M = R / '.project-memory'

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest().upper()

def new_json(p, obj):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

a = json.loads((H / 'AUDIT.json').read_text())
f = json.loads((F / 'AUDIT.json').read_text())
if not a['pass_'] or len(f['results']) != 3 or not all(x['pass_'] for x in f['results']):
    raise SystemExit('Existing audit has not passed')
for pred in [0, 1, 32]:
    x = json.loads((F / f'pred{pred}-BUILD_EXIT.json').read_text())
    if x['error'] or x['cleanup']['root_exit_code'] != 0 or not x['cleanup']['job_empty']:
        raise SystemExit('Unfinished or failed PDS process')
    if not x['inputs_unchanged'] or x['hardware_calls'] != 0:
        raise SystemExit('PDS scope mismatch')

resources = [dict(entries=0 if x['pred'] == 0 else (32 if x['pred'] == 32 else 64),
                  resources=x['resources'], performance=x['performance'],
                  constraints=x['constraints'], native_exit=0)
             for x in f['results']]
summary = dict(date='2026-11-03', status='FINITE_SOFTWARE_AND_OFFLINE_IMPLEMENTATION_ACCEPTED',
               recommended=dict(BTB_ENABLE=1, BTB_INDEX_BITS=5, SYNC_MEMORY=1),
               coremark_runs=10, coremark_all_pass=True, formal_CoreMark_score=False,
               coremark_iterations=1, coremark_crc={'performance':['E714','1FD7','8E3A'],
                                                   'validation':['E3C1','0747','8D84']},
               comparisons=a['comparisons'], timing=a['timing'], offline_PDS=resources,
               access_fault_and_CSR_cases=24, related_32entry_regression=46,
               independent_comparison_controls=10,
               control_scope='Offline equality/assertion controls only; not complete runner/parser/timeout fault injection',
               native_software_commands=102, protected_production_files=89,
               CPU_RTL_same_as_M4=True, production_replaced=False,
               hardware_calls=0, bitstream_generated=False, physical_IO_CDC_signoff=False,
               limitations=a['limitations'],
               evidence={'software_audit':'AUDIT.json', 'commands':'COMMANDS_FINAL.json',
                         'report':'../../../reports/verification/2026-11-03-coremark-resource-no-board.md',
                         'offline_implementation':'../../fpga/2026-11-03-advanced-btb-offline-m1/START_HERE.md'})
new_json(H / 'SUMMARY.json', summary)
new_json(F / 'SUMMARY.json', dict(date='2026-11-03', status=f['status'],
          configurations=resources, recommended_entries=32, hardware_calls=0,
          bitstream_generated=False, physical_IO_CDC_signoff=False,
          frequency_is=f['frequency_is'], software_source_identity='../../advanced/2026-11-03-coremark-strict-m5/AUDIT.json'))

for name, left, right in [
    ('BTB_OFF_TO_64.diff', F/'pred0/source/board_top_hl4.sv', F/'pred1/source/board_top_hl4.sv'),
    ('BTB_64_TO_32.diff', F/'pred1/source/board_top_hl4.sv', F/'pred32/source/board_top_hl4.sv'),
]:
    with (F/name).open('x', encoding='utf-8', newline='\n') as out:
        out.writelines(difflib.unified_diff(left.read_text().splitlines(True), right.read_text().splitlines(True),
                                          fromfile=left.relative_to(F).as_posix(), tofile=right.relative_to(F).as_posix()))

# Recheck before changing memory. Preserve the previous CURRENT as history.
paths = [M / n for n in ['CURRENT.md','INDEX.md','DECISIONS.md','FACTS.md','TODO.md']]
before = {p: p.read_bytes() for p in paths}
texts = {p.name: b.decode('utf-8-sig') for p, b in before.items()}
if re.search(r'^## D327\b', texts['DECISIONS.md'], re.M) or re.search(r'^## F286\b', texts['FACTS.md'], re.M):
    raise SystemExit('Decision/fact number now exists: do not overwrite parallel work')
new_json(H / 'MEMORY_BEFORE.json', {p.name:dict(sha256=sha(p),bytes=len(before[p])) for p in paths})
(H / 'CURRENT-before-D327.md').write_bytes(before[M/'CURRENT.md'])
decision = '''## D327｜2026-11-03｜接受32项BTB离线候选及可信CoreMark/资源取舍
沿D326不板目标，完成独立M5有限CoreMark、真实仿真计时规则、M-mode故障补验与三组合法PDS离线实现；既有CPU RTL八模块不再改，生产D300/SM2/D320不替换。根据F286，同条件32项比关闭预测减少17.7560%/18.2796%计算周期，相对64项只多约0.6%周期而少611 LUT/1888 FF，推荐BTB_INDEX_BITS=5同步配置作独立离线候选，不因64项周期略少忽略资源代价。固定27MHz八项内部STA通过；估算33.9006MHz仅工具一次布局结果，不作实机Fmax或校频。拒绝将一次迭代CRC/轨迹通过称正式CoreMark（<10秒）、完整高阶2或全特权；全S/U/PMP/Sv32、全IO/CDC/旧调试Critical继续保留。零计时mock与真实时钟方程六次运行分层，动态规则先冻、数值后由独立地址序列核验，不称全部数值预冻。共享命令覆盖缺口保留，r2每命令唯一记录关闭32项过程元数据缺项；原model.timer错误标签保留并另注。无位流/服务器/JTAG/硬件/安装/许可证改动，无新B工单，D245待审文档不提交推送。D326“执行中/两配置/仅mock”当前状态被本完成记录及原始结果限定取代，历史不回写。入口reports/verification/2026-11-03-coremark-resource-no-board.md；下一价值是按该范围纳入作品证据与报告，不再无界扩测或自动上板。

'''
fact = '''## F286｜2026-11-03｜CoreMark严格短测、M-mode故障补验与三配置PDS离线对照
M5 work/advanced/2026-11-03-coremark-strict-m5：原算法SHA同已收B上游，RV32I/ILP32 O2、2000数据、一次迭代，双程序15932/15940B。固定零计时参考先冻结四次，加时钟方程先冻结真实模拟mtime六次，共10新DUT PASS；逐笔WB/STORE（不去重）、全寄存器/测试内存/UART及端口错误/种子/返回/完成状态严格比较。CRC性能E714/1FD7/8E3A，验证E3C1/0747/8D84；真实计时每例12读按同步口N−2规则核查，phase差固定4拍。<10秒告警保留、非正式成绩/非实机时间。计算周期off/64/32项分别性能2103652/1719152/1730128，验证2263004/1837836/1849336；32项降17.7560%/18.2796%。新增访问错误/非法CSR等六程序四配置24PASS；32项同步相关46程序PASS；离线10比较/断言负向拒绝只有限比较器自检，不是完整runner故障测试。102原生命令记录均rc0且无剩余所属任务，旧共享记录覆盖与标签错误详报告，原件保留。
离线work/fpga/2026-11-03-advanced-btb-offline-m1三组各一次compile/synth/map/pnr/STA完成，native0/Job空；同PG2L100H/-6/FBG676、27MHz、同镜像/约束，仅BTB开关或INDEX_BITS差异。off/64/32分别LUT10437/11910/11299、FF3068/6976/5088、DRM36均16、IO均15；STA估算MHz32.3593/30.9665/33.9006，Setup裕量ns6.134/4.744/7.539，内部Slow/Fast八检查均无负裕量。各97条约束检查0 error/critical/warning不等全flow零warning，原IO/扇出等告警及物理CDC限制保留。每组28个存活DRM18K的1792 INIT片段逐值核同、八CPU模块同本次仿真/M4、89生产保护项同SHA。无位流或任何硬件调用，未合生产，完整高阶2/全特权未完成。报告reports/verification/2026-11-03-coremark-resource-no-board.md，双START_HERE/SUMMARY/AUDIT/COMMANDS_FINAL及SHA清单为入口。

'''
def insert_after_title(text, section):
    head, sep, tail = text.partition('\n')
    return head + '\n\n' + section + tail.lstrip('\r\n')

texts['DECISIONS.md'] = insert_after_title(texts['DECISIONS.md'], decision)
texts['FACTS.md'] = insert_after_title(texts['FACTS.md'], fact)
texts['TODO.md'] = insert_after_title(texts['TODO.md'], '''## 2026-11-03 D327：不板候选质量与对照已形成
- [有限完成，取代D325候选CoreMark/资源频率未运行状态] 双参数10次严格CoreMark短测、真实模拟计时核验；24故障边界与32项46相关回归，三组离线PDS综合/P&R/STA、初始化核对及同条件资源对照。详F286和新报告。
- [技术推荐/独立候选] 32项BTB：计算周期较off少17.7560–18.2796%，相对64项少611 LUT/1888 FF；代价与频率估算限制必须一起说明。生产D300/D320不替换。
- [下一唯一价值项] 将本阶段准确范围、CoreMark周期与资源/STA对照纳入技术报告及提交证据，保留正式成绩/实机/全特权/IO-CDC等未完成状态，不自动扩实现或硬件。
- [保留未完成] 正式>=10秒CoreMark、本候选实机/ILA、完整S/U/PMP/Sv32/高阶2、物理IO/CDC签核；用户不板不等免除官方要求，D245文档本地门保持。

''')
texts['INDEX.md'] = insert_after_title(texts['INDEX.md'], '''**2026-11-03 D327/F286：无板CoreMark与资源/时序对照完成，推荐独立32项BTB**
入口[报告](../reports/verification/2026-11-03-coremark-resource-no-board.md)、[M5](../work/advanced/2026-11-03-coremark-strict-m5/START_HERE.md)、[PDS三配置](../work/fpga/2026-11-03-advanced-btb-offline-m1/START_HERE.md)。10次严格CoreMark有限短测、24故障、32项46相关回归PASS；三离线实现native0/Job空/同镜像INIT，32项计算周期降17.7560–18.2796%，11299LUT/5088FF、27MHz约束内部时序通过/估算33.9006MHz。非正式CoreMark/实机频率/完整高阶2；八CPU仍M4，89保护同SHA，不改生产/不板，D245本地门保持。D326下文“执行中/仅mock”是历史快照，当前按此条和AUDIT；共享记录覆盖/错误标签及修补详报告。

''')
texts['CURRENT.md'] = '''# 当前阶段与入口

2026-11-03 D327/F286：不板的候选软件质量与离线实现对照已完成。推荐独立32项BTB；10次严格CoreMark短测、24故障边界及46相关回归PASS，三配置PDS离线资源/内部STA完成。入口reports/verification/2026-11-03-coremark-resource-no-board.md及work/advanced/2026-11-03-coremark-strict-m5/START_HERE.md；实现入口work/fpga/2026-11-03-advanced-btb-offline-m1/START_HERE.md。下一仅将准确范围与取舍纳入提交证据，不自动扩实现/硬件。

D300/SM2、D320应用及D325原包保持；八CPU源码仍M3/M4，89保护项同SHA。非正式>=10秒CoreMark、非实机Fmax/ILA、非完整高阶2/全特权/物理IO-CDC签核。用户本阶段不板，无位流/服务器/JTAG/Flash或新B工单。D245待审文档不提交推送。三场景手机原片未接收/未视觉验收。完整长期规则WORKING_POLICY，历史与未闭项见INDEX/TODO。
'''
for p in paths:
    if p.read_bytes() != before[p]:
        raise SystemExit(f'Parallel memory update: {p.name}')
for p in paths:
    p.write_text(texts[p.name], encoding='utf-8', newline='\n')

# Freeze all current local evidence. A SHA manifest is integrity, not functional proof.
manifest_results = []
for root in [H, F]:
    if (root/'SHA256SUMS.txt').exists() or (root/'INTEGRITY.json').exists():
        raise SystemExit('Manifest already exists')
    entries = []
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise SystemExit(f'Unexpected link {p}')
        if p.is_file():
            entries.append((p.relative_to(root).as_posix(), sha(p), p.stat().st_size))
    with (root/'SHA256SUMS.txt').open('x', encoding='utf-8', newline='\n') as out:
        for rel, digest, size in entries:
            out.write(f'{digest}  {rel}\n')
    mismatches = [rel for rel, digest, _ in entries if sha(root/rel) != digest]
    result = dict(status='PASS' if not mismatches else 'FAIL', file_count=len(entries),
                  bytes=sum(size for _, _, size in entries), mismatches=mismatches,
                  manifest_sha256=sha(root/'SHA256SUMS.txt'),
                  excludes=['SHA256SUMS.txt itself','INTEGRITY.json written after verification'],
                  claim='Local material integrity only, not a new DUT or hardware run')
    new_json(root/'INTEGRITY.json', result)
    manifest_results.append(dict(path=str(root), **result))
    if mismatches:
        raise SystemExit('Manifest mismatch')
print(json.dumps(manifest_results, ensure_ascii=False, indent=2))
