from pathlib import Path
import hashlib, json
P=Path('D:/A_FPGA_Comp'); M=P/'.project-memory'; H=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1'
read=lambda p:p.read_text(encoding='utf-8-sig')
names=['CURRENT.md','INDEX.md','FACTS.md','DECISIONS.md','TODO.md','COLLABORATION.md']
old={n:read(M/n) for n in names}
assert '## F-163' not in old['FACTS.md'] and '## D-165' not in old['DECISIONS.md']
assert '## D-164' in old['DECISIONS.md'] and 'COLLAB v1.90' in old['COLLABORATION.md']
assert json.loads(read(H/'POSTFLIGHT.json'))['within_stage_budget']
backup=M/'history/2026-10-27-coremark8-bitstream-result';backup.mkdir(exist_ok=False)
for n in names:(backup/n).write_bytes((M/n).read_bytes())
report='reports/verification/2026-10-27-board-coremark8-bitstream-m1.md'
root='work/fpga/2026-10-27-board-coremark8-bitstream-m1'
fact=f'''## F-163：原8迭代镜像CPU软件位流生成，内部27MHz有限通过

- 2026-10-27；D164明确批准，唯一1次PDS2022.2-SP6.4 build146967正常checkout/六阶段含gen_bit_stream，普通非管理员外部执行经独立工具审核；81.547秒/rc0，退出后新鲜3791112B `pds/generate_bitstream/board_top.sbit` SHA **F548BC8BAA3DDFB5E2EB3158AE108F5A9DFCE7FE6C08919DB8DB245187C8D7A4**。目标PG2L100H/-6/FBG676，13功能RTL及原8镜像不改，不混F146；0新C/仿真编译/DUT/硬件。
- 原8 bin15912B+零到ROM32KiB、RAM32KiB A5；12生产源同字节，memory仅去M0_VERIFY/同INIT内联。28保留DRM18共1792 INIT从原始字节独立核同，旧1版同法校准；仅bank3/halfword0/INIT_38变化，对应offset15904 1→8。不是专有位流反解/读回/布局后功能仿真。
- 内部27MHz八类setup/hold/recovery/removal正裕量，最差setup23.279ns/hold0.129ns，TNS0/无失败；1805LUT/1519FF/14DRM36/15IO/0latch，94原引脚约束不改。5输入+9输出外部delay/物理CDC未验。High Voltage沿D010工程假设，Bitstream-2001无；旧7条constant-probe及其他类别计数同F142，无新增计数，根因仍OPEN。
- 本次许可证提示剩余**7天**，正常checkout仅证明本次可用；提醒正规续期，无许可内容/机器标识记录。入口shell峰103264256B/父64360448B，工具自报内存池1247MB非独立整树峰。阶段闭合910.547秒<=2400秒，41原件/48冻结输入后验同，132文件本地清单。原生日志/专有模型/DB/大初始化/镜像/位流仅本地，不上传。
- 纠错：D163/F162旧scope SHA BB1D…为UTF8/LF规范化值，实际审查CRLF文件6BE782…E4B08与Git blob同，正文不变、原状态保留，见原scope目录SCOPE_IDENTITY_CORRECTION.json。两个产物审计器错误（成功标志日志位置、INIT_MODE数字误判）保留诊断后修正，PDS没有重跑、没有改预期。
- 报告`{report}`；原证据`{root}/SUMMARY.json、COMMANDS.md、CONFIGURATION_AUDIT.json、MEMORY_INIT_AUDIT.json、TIMING_RESOURCE_AUDIT.json、WARNINGS_LICENSE_AUDIT.json、POSTFLIGHT.json、SHA256SUMS.json`。F162“无新8 CPU位流”仅此缺口被取代，旧热点/硬件限制保留；历史JTAG识别不抹去，本轮0扫描/下载，CPU实机/ILA/正式成绩未验，over_temp STOP。Git待本单元检查同步，不以提交升级验收。

'''
decision='''## D-165：接受CPU短程序软件位流，保留安全及实机取证门槛

- 2026-10-27，F163原始日志/新位流/INIT/时序/保护收据支持，仅接受“8迭代CPU软件位流生成与内部27MHz”有限结果，不宣布CPU已上板、正式CoreMark或完整作品；D164单次PDS许可已用完，阶段完成停止，不自动160/ILA/硬件。
- 采用原13功能源/原8程序及F142生产绑定/约束；未采用改CPU、混F146、复用旧1初始化、添加虚假外部delay或以exit0替产物验收。7旧constant-probe、外部14IO/物理CDC及实际配置供电仍未闭，不因SCBV告警消失推断电压或安全。
- D164“未验收”由本有限结果取代；D163待批已由D164批准，原文件与旧PENDING保留。旧scope SHA元数据仅含义纠正：BB1D…为LF规范化、6BE782…E4B08为实际CRLF文件，与已审Git blob同，无授权内容变化，纠错侧件保留；不回写历史。
- 下一最有价值是安全可用FPGA平台及真实CPU/时基/ILA取证范围；只推荐、不批准硬件/远程登录上传/安装。许可证本次7天应及时正规续期，尚无需修改现有许可。B按D158三组守卫差额独立，不阻A、不重复核心/改承诺；当前新ETA未知/未代发反馈。over_temp STOP不变。

'''
def insert_after_title(text,section):
    title,rest=text.split('\n',1); return title+'\n\n'+section+rest.lstrip('\n')
new=dict(old)
new['FACTS.md']=insert_after_title(old['FACTS.md'],fact)
new['DECISIONS.md']=insert_after_title(old['DECISIONS.md'],decision)
new['CURRENT.md']=f'''# 当前阶段与入口

更新：2026-10-27，F163/D164–165；恢复完整读WORKING_POLICY v1.3。

- **已验主线**：F160性能8纯软件有限通过；F163同源/同8镜像CPU软件位流已生成，内部27MHz通过。1次PDS许可已用完；非正式CoreMark/FPGA运行。
- **当前阶段**：本轮到此停止，下一是安全可用平台与真实CPU/时基/ILA取证范围收敛；尚未批准恢复硬件/插ILA/160长跑。7旧constant-probe和14外部IO/CDC限制未闭，当前许可正常、本次提示余7天需正规续期。
- **协作/安全**：B v02有条件接收，D158三守卫差额回复已备未代发/新ETA未知；原10/27 18外设窗保持。F146暂缓/F147告警、over_temp STOP、实际配置供电/CPU实机/ILA缺口不变，A不等B工具。

入口：`{report}`；`{root}/SUMMARY.json、COMMANDS.md、POSTFLIGHT.json、SHA256SUMS.json`；scope哈希换行纠错在原交付目录SCOPE_IDENTITY_CORRECTION.json，内容未改。B与旧验收按INDEX/TODO/COLLAB v1.91。

Git：本单元普通脚本/脱敏收据/报告待精确检查同步；完整原始日志、厂商模型/数据库、镜像/初始化大表及位流仅本地。前基线1bde3da4/631路径；以实际同步收据为准，不以Git升级验收。
'''
new['INDEX.md']=old['INDEX.md'].replace('最近更新：2026-10-27，F162/D163：只读8迭代窗口/热点与CPU位流差距核实，下一唯一1次PDS软件位流scope PENDING；0新DUT/PDS/硬件，B差额独立。',f'最近更新：2026-10-27，F163/D164–165：唯一1次PDS生成8迭代CPU软件位流，INIT/内部27MHz有限通过；0新C/仿真/DUT/硬件，over_temp STOP。原scope PENDING被批准/结果取代，旧文件留存；旧BB1D SHA为LF规范化值，实际CRLF见纠错侧件。')
route=f'|当前CPU8软件位流/有限结果|F163/D164–165；`../{report}`及`../{root}/SUMMARY.json、SOURCE_RECEIPTS.json、SOURCE_CHANGE_SUMMARY.json、COMMANDS.md、CONFIGURATION_AUDIT.json、MEMORY_INIT_AUDIT.json、TIMING_RESOURCE_AUDIT.json、WARNINGS_LICENSE_AUDIT.json、POSTFLIGHT.json、SHA256SUMS.json`。1PDS/0新DUT，41原件48冻结核同/1792INIT/内部27MHz；7旧警告14外部IO限制、许可实余7天。scope原件不改，SCOPE_IDENTITY_CORRECTION纠正换行SHA含义；无实机/ILA/正式成绩、停止不变|\n'
new['INDEX.md']=new['INDEX.md'].replace('|---|---|\n','|---|---|\n'+route,1)
new['TODO.md']=insert_after_title(old['TODO.md'],f'''## 当前CPU8软件位流 F163/D165（2026-10-27）

- [x] D164批准后唯一1次PDS构建/退出后新位流、1792INIT、内部27MHz/资源/告警/许可/41原件48冻结输入验收；证据按INDEX。本阶段已完成停止。
- [ ] 下一收敛安全可用FPGA平台及真实CPU/时基/ILA取证范围，保留over_temp停止与实际供电缺口；不把软件位流当硬件放行，不自动160长跑。
- [ ] 许可本次提示7天；在需重新构建前安排正规续期，由人完成必要申请/授权，不记录许可内容。
- [ ] 复用已核证据准备匿名交付，按11/4 18:00保留上传余量；CPU实机/片上证据未完成，不宣布作品达标。

### 以下F162待批/无8位流为历史：由D164批准和F163结果取代，热点/安全限制保留

''')
new['COLLABORATION.md']=insert_after_title(old['COLLABORATION.md'],'''版本：COLLAB v1.91；2026-10-27，F163/D164–165。A完成唯一1次PDS CPU8软件位流/内部27MHz有限验收，13功能RTL/外设/程序不改；下一安全可用平台/真实CPU/时基/ILA取证范围尚未实施，不自动硬件/长跑。B仍D158三守卫差额，新反馈已备未代发/ETA未知，不重派核心/不等B工具/不改原10/27 18窗口。7旧告警、外部IO/CDC及实际供电缺口/over_temp STOP不变；许可证本次7天。

### 历史v1.90（仅PDS待批/未执行由D164和F163取代）

''')
for n in names:
    assert read(M/n)==old[n], 'parallel change '+n
for n in names:(M/n).write_text(new[n],encoding='utf-8')
assert all(read(M/n)==new[n] for n in names)
print(json.dumps(dict(updated=names,readback=True, fact='F163',decision='D165'),ensure_ascii=False))
