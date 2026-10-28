from pathlib import Path
import json,hashlib
P=Path('D:/A_FPGA_Comp');M=P/'.project-memory';H=Path(__file__).resolve().parent
read=lambda p:p.read_text(encoding='utf-8-sig')
def save(n,v):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
index=json.loads(read(H/'PDF_INDEX.json'))
save('SOURCES.json',dict(date_client='2026-10-28',PDS_documents=[dict(path=x['path'],SHA256=x['SHA256'],pages=x['pages']) for x in index],remote=dict(publication='https://szlogicmatrix.com/1501.html',file='remote_lab_developer_manual.pdf',SHA256=hashlib.sha256((H/'remote_lab_developer_manual.pdf').read_bytes()).hexdigest().upper(),version='1.0',date='2026/1/7',pages=24),public_entry='http://www.logicmatrixsemi.com:5174/',thermal_previous_report='reports/hardware/2026-10-15-systematic-hardware-evidence-review.md',thermal_query_already_prepared='deliveries/pango-overtemp-question-2026-10-20-v01/package/START_HERE.md',document_download_is_not_vendor_signature_or_device_compatibility=True))
names=['CURRENT.md','INDEX.md','FACTS.md','DECISIONS.md','TODO.md','COLLABORATION.md'];old={n:read(M/n) for n in names}
assert '## F-164' not in old['FACTS.md'] and '## D-166' not in old['DECISIONS.md']
assert 'F163/D164–165' in old['CURRENT.md'] and 'COLLAB v1.91' in old['COLLABORATION.md']
backup=M/'history/2026-10-28-fpga-evidence-readiness';backup.mkdir(exist_ok=False)
for n in names:(backup/n).write_bytes((M/n).read_bytes())
def prepend(s,t):
    title,rest=s.split('\n',1);return title+'\n\n'+t+rest.lstrip('\n')
new=dict(old)
new['FACTS.md']=prepend(old['FACTS.md'],'''## F-164：远程平台内部Debugger新增资料与片上取证只读准备

- 2026-10-28，独立`work/analysis/2026-10-28-fpga-evidence-readiness-m0/`；公开板厂1501页面关联24页开发者手册V1.0/2026-1-7，3187357B/SHA05FE830148F5638E0A6986938BE06DA916E700F283B28BA9ECA253A82620FDD0。全篇文字及2/8/11/13/17/23/24页视觉；17页外部68IO与23–24页PDS FIC/内部ILA/PCIe DMA是不同功能。仅厂商文档说明，不是当前设备清单/项目复现/账号许可；截图含100H对200H不匹配提示，不把位流或引脚兼容推成跨器件可用。
- 普通公开网络Win10013失败保留；系统独立审核后两个固定公开GET：PDF及指南5174入口200/FPGA LAB HTML标题，未执行JS/登录/预约/上传/硬件。HTTPS工具失败不等不存在，安全入口、费用/配额/时段/实际芯片约束、UART完整导出和远程DMA包装要求未知，不从默认10分钟推免费。
- 安装版Fabric Inserter V1.0/2022.07.12及Debugger V1.1/2023.04.24相关页视觉：必须插核构建/对应FIC，数据时钟和复位/存储设置需准确；FIC连接用list_nets索引非直接照RTL层次。Debugger支持WDF/ASCII/VCD/TXT导出；真实FPGA导出VCD可作片上原始证据，旧仿真VCD不行。PDS两本全文提取156页、11相关页视觉，不称全视觉。
- F160/F163的13源三副本及位流/两FDC/三PDF共45文件SHA后验同；0新C/编译/DUT/PDS/硬件/账号/外发。新探针仅技术草案140bit×1024=143360bit（容量下界，非实际资源），源位置/合成名称词项计数不是可连接性验证；无新FIC或调试位流/实机波形。许可仅复用10/27实提示7天，不冒10/28新查询。
- 报告`reports/progress/2026-10-28-fpga-evidence-readiness-m0.md`；证据SOURCES/INPUTS/BASELINE_CHECK/PROBE_PLAN_DRAFT/READING_COVERAGE/PLATFORM_GATES/POSTFLIGHT。已备人工平台四问`deliveries/mainline-fpga-platform-check-2026-10-28-v1/PLATFORM_QUESTIONS.txt`，未代发；旧过温问题包复用不重做，未取得新答复。本地over_temp STOP及供电/7告警/外部IO/正式分数限制保持；B三守卫差额独立、新ETA未知，原10/27 18窗口不自动延期。

''')
new['DECISIONS.md']=prepend(old['DECISIONS.md'],'''## D-166：优先查实安全平台与匹配调试入口，不盲插核或扩ISA

- 2026-10-28，F164新增远程内部Debugger手册证据，F160/F163保护核同。本轮按长期规则只读调查/技术定案，非新实现许可。选择保留现CPU短程序位流，先由人取得准确设备/约束、FIC/DMA接入、UART/时基、安全登录/配额四组平台事实；已备可直接转发文字，A负责分析答复，不让用户研究信号。
- 探针技术草案收敛为单核/1024点/物理27MHz每拍/All Data，先禁过滤和多窗口，140bit逻辑载荷；真实网表连接、采样时相、资源和时序须后续新范围。优先非功能网表插核；需要保留元数据、不同器件/时钟/DMA包装时另明确范围，不冒本轮已批。未选择重跑长仿真、扩ISA/Cache、在未知远程200H直接套100H sbit，或用外部逻辑分析/LED代内部CPU证据。
- 替代“当前远程内容全不可访问”仅覆盖结论：公开手册与门户壳本次已取得，但不是可用设备/运行权限/服务验收。本地过温不因远程存在解禁；新GUI/账号/预约/费用/上传/硬件和插核构建仍需范围/权限。旧热调查复用，已有咨询包不重复生成或声称已送达。
- B仍原D158守卫差额，不接管重写/派新核心、不等待其工具准入；原10/27 18已过且不自动顺延，新ETA不猜。当前唯一需人动作是转平台四问/反馈真实答复；不需要连板、重拍下载器或发凭据。11/4 18既有截止与实机/ILA未闭合风险明示，不承诺新工期。

''')
new['CURRENT.md']='''# 当前阶段与入口

更新：2026-10-28，F164/D166；恢复完整读WORKING_POLICY v1.3。

- **已验主线**：F160有限8迭代纯软件；F163同源CPU8位流/内部27MHz有限通过。未有CPU实机、正式CoreMark、ILA；旧1次PDS额度已用完。
- **当前阶段**：真实平台/片上取证只读准备完成。已取得板厂远程内部Debugger手册，但当前设备/FIC兼容/UART/安全入口/费用时段未知；等人工平台四问答复后定新适配/插核范围，不自动构建或登录/硬件。
- **协作/安全**：B D158三守卫差额/反馈已备未代发，新ETA未知；原10/27 18窗口已过、不自动顺延。7旧告警/外部IO与CDC/实际配置供电及over_temp STOP不变。许可最后10/27提示余7天，并非今日重新查询。

入口：`reports/progress/2026-10-28-fpga-evidence-readiness-m0.md`；`work/analysis/2026-10-28-fpga-evidence-readiness-m0/PLATFORM_GATES.json、PROBE_PLAN_DRAFT.json、POSTFLIGHT.json`；唯一人工事项`deliveries/mainline-fpga-platform-check-2026-10-28-v1/PLATFORM_QUESTIONS.txt`。COLLAB v1.92，余项按INDEX/TODO。

Git：本只读准备单元待精确审查同步；前18a1e223/670路径，原模型/位流/原生日志/厂商PDF及大提取仅本地；不以Git升级验收。
'''
new['INDEX.md']=old['INDEX.md'].replace(old['INDEX.md'].splitlines()[2],'最近更新：2026-10-28，F164/D166：取得板厂远程内部Debugger公开手册，完成PDS片上观察只读准备；当前资源/接入/安全入口仍未知，平台四问已备未代发。0新PDS/DUT/硬件，F160/F163保留。',1)
route='|当前真实FPGA/片上取证准入|F164/D166；`../reports/progress/2026-10-28-fpga-evidence-readiness-m0.md`及`../work/analysis/2026-10-28-fpga-evidence-readiness-m0/SOURCES.json、BASELINE_CHECK.json、PLATFORM_GATES.json、PROBE_PLAN_DRAFT.json、READING_COVERAGE.json、POSTFLIGHT.json`。远程24页手册内部ILA仅文档级支持/HTTP门户壳200，不是可用设备或接入验收。人工四问`../deliveries/mainline-fpga-platform-check-2026-10-28-v1/PLATFORM_QUESTIONS.txt`，未代发；无FIC/新调试位流/硬件，旧过温包复用|\n'
new['INDEX.md']=new['INDEX.md'].replace('|---|---|\n','|---|---|\n'+route,1)
new['TODO.md']=prepend(old['TODO.md'],'''## 当前FPGA取证准入 F164/D166（2026-10-28）

- [x] 公开板厂远程手册24页、内部Debugger/FIC与外部68IO差异、门户壳200核实；安装PDS调试文档及140bit/1024点草案、45原件保护完成，0PDS/DUT/硬件。
- [ ] 唯一当前人工动作：转`deliveries/mainline-fpga-platform-check-2026-10-28-v1/PLATFORM_QUESTIONS.txt`给老师/平台管理员；获取准确器件/封装/约束、FIC/DMA接入、UART/可信时基、安全入口/配额/时段四项真实答复。A准备/分析；未代发，不先申请/预约/上传或读账号。
- [ ] A收到可核答复后确定匹配独立调试构建/非功能保留/校准范围并申请必要权限；不同器件/DMA包装须另界定，不能直接上传100H sbit；当前未批/未实施。
- [ ] 并行复用证据形成匿名技术材料，保留正式>=10秒/时基/实机/ILA空缺；旧Pango三问包可直接复用，无新安全答复不恢复本板。截止沿已核11/4 18，非本轮新公告核验。
- [ ] B仍原D158三守卫差额，新回执/ETA未知；原10/27 18已过不自动顺延、不把原外设窗口当新工具承诺；A不等B工具阻主线。

### 以下F163平台收敛待办的只读准备由本条完成；设备准入/实际取证仍未完成

''')
new['COLLABORATION.md']=prepend(old['COLLABORATION.md'],'''版本：COLLAB v1.92；2026-10-28，F164/D166。A只读取得远程内部Debugger手册并收敛片上观察草案，F160/F163有限基线保护；当前需人工确认实际设备/接入/UART/时基及安全入口/费用时段，不要求B设计平台适配或重跑外设。B原D158 G1–G3保持、新ETA未知，原10/27 18节点已过但未自动顺延/宣布完成；原外设有限接收保持。CPU/FIC/新构建/硬件不增权、over_temp STOP。本轮不外发四问，负责人可转，A分析落实。

### 历史v1.91（软件位流结果保留，平台只读准备由F164补充）

''')
for n in names:assert read(M/n)==old[n],'PARALLEL_CHANGE '+n
for n in names:(M/n).write_text(new[n],encoding='utf-8')
assert all(read(M/n)==new[n] for n in names)
print(json.dumps(dict(updated=names,readback=True,fact='F164',decision='D166')))
