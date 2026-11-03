"""Record completed iter2 stage; preserve original decision and baseline status."""
from stage_coremark import *
def run():
    result=read(H/'RESULTS.json');assert result['new_DUT_runs']==2 and result['outcome']=='PASS_LIMITED_DOUBLE_ITERATION_CALIBRATION'
    Mem=P/'.project-memory'
    assert '## F-151' not in (Mem/'FACTS.md').read_text(encoding='utf-8-sig') and '## D-150' not in (Mem/'DECISIONS.md').read_text(encoding='utf-8-sig')
    def prepend(n,s):
        p=Mem/n;t=p.read_text(encoding='utf-8-sig');a,b=t.split('\n',1);p.write_text(a+'\n\n'+s+'\n'+b,encoding='utf-8',newline='\n')
    prepend('FACTS.md',r'''## F-151：双种子各2迭代真实C执行校准有限通过

- 2026-10-25，D149批准/D150验收边界；报告`reports/verification/2026-10-25-coremark-iter2-m1.md`；`work/fpga/2026-10-25-coremark-iter2-m1/RESULTS.json、ORACLE_SUMMARIES.json、SOURCE_RECEIPTS.json、IMAGE_DIFF.json、quality-compare.json、COMMANDS.md、postflight*.json`及原native日志/trace/bus/pin/VCD。130相关原件/80 pre-DUT冻结核同，13RTL/官方六源/B/启动链接/计时语义不改；port新副本接ITERATIONS、TB预算6→8M，参考副本仅步限2→5M。
- 新两bin仍15912/15920B，各仅offset15904初值1→2，ELF/真实报告Iterations2匹配。现有GCC原10构建/格式工具调用、2已另核外部Icarus编译44.406/44.532s及2新普通DUT真实完成，无超时/截断/强杀。保留继承timescale/无显式时间单位/官方grsn警告，不改RTL消警告；本轮0PDS/许可/安装/环境/硬件。
- 新独立时序参考先对两个旧F143程序重放校准全部RF/RAM/流摘要/12时间LOAD/报告/物理拍（非旧DUT重跑），再于新DUT前冻结2迭代完整预期。实际性能raw4207378、finalCRC72be、物理5888943、EX1900604/WB1296943/READ245317/STORE34868、stall173406/flush435221；验证raw4526490、CRCfe8c、物理6205395、EX2005976/WB1364865/READ246042/STORE34675、stall174246/flush461228，全部匹配先验参考。main0/SP18000、32尾拍无副作用，全RF/RAM、每笔有序副作用不去重，phase0/1/2/3/4/空窗口26/单次start-stop/12计时LOAD独立核同、无X-Z/计时或port错误。
- 实际UART662/661字节，公开pin独立完整时间/中心解码3838/3826次跳变，原生窗口VCD2720/2750稳定检查通过（各2183可见拍，明确停采，不当完整算法波形/ILA）。新frozen判据1控制+7篡改、实际pin日志4类损坏均拒绝，只有host自检/重审不计DUT。
- C2−2*C1为+82/+490拍，实际第二迭代增量2103730/2263490，不能拿单次乘2当精确新预期或据两点保长测线性；新trace84,091,326/87,958,340B，bus110,243,503/110,178,225B；DUT主机320.390/357.453s仅资源成本，不是FPGA性能。两组名义27MHz仅0.155829/0.167648秒，短测/Errors detected/NO VALID SCORE保留，非正式≥10秒成绩/优化收益/CPU整体正确。
- 稳定F143/O2不覆盖，F151为新双迭代校准成果；F146候选仍暂缓/F147告警未知，硬件over_temp STOP与外部时基/CDC/ILA缺口保持。B只继续原R1–R3/10月27日18北京时间窗口，用户已报告转交，未推定新ACK或v02；A未代发。下一仅建议正式长测验证与资源方案，不自动数小时长跑/CPU修复/PDS或硬件。
''')
    prepend('DECISIONS.md',r'''## D-150：接收双迭代有限校准，保持稳定硬件/软件发布边界

- 2026-10-25，F151新2C镜像/2RTL编译/2真实DUT及独立预期/全态/逐笔副作用/计时/UART证据。接受A-COREMARK-ITER2-M1有限目标：迭代初始化接线真实生效、重复算法和完整输出正确；保留原F143和所有旧输入，不把新校准或Git提交当正式10秒/FPGA/完整ISA/创新收益。
- 采用先验物理调度+ISA参考（在两旧完整程序严格校准后才冻新预期），与逐周期外设/计时和实际引脚检查分离；不从DUT回填期望，不删BSS/合法重复写回/访存。参考原2M预算不够新验证2005976步，按D149已批5M只调验证副本预算，不改CPU或指令语义；所有旧模型/失败不覆盖。
- C2非简单2*C1，下一应先按实际资源/增量收敛正式长测验证与预算方案，保留每笔检查，不能直接放开日志/运行时间或宣称129/120次一定够。当前阶段至多2新DUT已完成，本轮收尾后不自动长跑、改CPU/PDS或恢复硬件；新实施/成本/硬件范围仍核准。
- B原R1–R3等待答复但不阻本阶段，不重派核心/重复索包或改变原窗/承诺。F146暂缓/F147告警未闭/over_temp STOP保持，用户报告已转交不推定B新ACK/新包。
''')
    current=r'''# 当前阶段与入口

更新：2026-10-25，F151/D149–150。双种子各2迭代纯软件校准有限通过；启动/恢复完整读WORKING_POLICY v1.3。

- **A成果**：新端口迭代参数真实接通；2新DUT与先冻结参考/全态/逐笔副作用/计时/完整UART匹配，raw4207378/4526490、CRC72be/fe8c、662/661字节。13RTL/官方六源不改；F143稳定保留、F146候选仍暂缓/F147告警未闭。本轮0PDS/许可/硬件。
- **下一**：正式长测验证与资源方案，依据实际增量/文件量，不能直接盲放大或删副作用；本轮2DUT许可范围已完成，不自动≥10秒长跑。仍非有效CoreMark成绩/实机或完整CPU验收。
- **协作/安全**：用户报告已人工转B最终v01回复，等待R1–R3答复，新ACK/v02未推定，10/27 18北京时间窗口保持。over_temp STOP、时基/外部CDC/FPGA/ILA缺口不变；许可余9天仅F146历史提示。

入口：`reports/verification/2026-10-25-coremark-iter2-m1.md`；`work/fpga/2026-10-25-coremark-iter2-m1/RESULTS.json、ORACLE_SUMMARIES.json、SOURCE_RECEIPTS.json、SOURCE_DIFFS.json、CHECKER_DIFF.patch、quality-compare.json、COMMANDS.md、postflight*.json、SHA256SUMS-final.txt`；COLLAB v1.78/TODO。F150就绪/原scope及F149/B、F147/F146/F143按INDEX。阶段前CURRENT在history/2026-10-25-coremark-iter2-m1保留。
'''
    (Mem/'CURRENT.md').write_text(current,encoding='utf-8',newline='\n')
    p=Mem/'INDEX.md';text=p.read_text(encoding='utf-8-sig');lines=text.splitlines();lines[2]='最近更新：2026-10-25，F151/D149–150。双种子各2迭代新DUT严格有限通过，参数接通/先验参考/完整副作用/计时/UART；非正式成绩。F143稳定/F146暂缓/硬件STOP，B等待原R1–R3答复。';text='\n'.join(lines)+'\n'
    marker='|任务|最小读取入口与权威证据|\n|---|---|';assert marker in text
    text=text.replace(marker,marker+'\n|当前双2迭代有限通过/真实参数与资源增量|F151/D149–150；`../reports/verification/2026-10-25-coremark-iter2-m1.md`；`../work/fpga/2026-10-25-coremark-iter2-m1/RESULTS.json、ORACLE_SUMMARIES.json、SOURCE_RECEIPTS.json、IMAGE_DIFF.json、SOURCE_DIFFS.json、CHECKER_DIFF.patch、quality-compare.json、COMMANDS.md、postflight*.json、SHA256SUMS-final.txt`。2新DUT/新raw4207378/4526490/CRC72be/fe8c/完整662+661UART，原件130/冻结80核同。13RTL不改/非正式或实机；下一正式长测资源方案、无自动扩大|',1)
    text=text.replace('|进行中双迭代校准 D149|','|历史D149实施入口（现F151有限完成）|').replace('当前结果以实际产物/日志和CURRENT为准','现已F151有限完成，具体结果按新入口和CURRENT').replace('现态以F150/D147–148（主线就绪/用户转交）','现态以F151/D149–150（主线校准）、F150/D147–148（历史就绪/用户转交）')
    p.write_text(text,encoding='utf-8',newline='\n')
    prepend('TODO.md',r'''## 当前双迭代校准完成 F151/D149–150（2026-10-25）

- [x] 新port ITERATIONS接线/默认1/正值保护，双镜像实际seed4=2、各只一字节差；13RTL/算法/启动链接/计时不改，原件130/冻结80 SHA保持。准确diff/源收据见本阶段目录。
- [x] 两旧程序独立时序参考校准/两新程序先验冻结（非DUT），2批内固定RTL编译/2普通新DUT严格通过，全RF/RAM/每笔EX/WB/MEM/计时/相位/尾部和完整1323UART；1+7判据、实际pin4损坏拒绝与窗口VCD检查分列。报告`reports/verification/2026-10-25-coremark-iter2-m1.md`。
- [x] C2−2*C1 +82/+490、两实际日志/主机资源量单独记录；不把CPU名义秒当主机秒/正式成绩，不要求C2精确2倍，不删除上游短测告警。F143稳定/F146暂缓/硬件STOP保持。
- [ ] 下一正式长测验证与资源方案：依据实际增量/输出量选择有界策略，解决逐笔trace超256MiB与主机数小时预算，保留每笔合法副作用核验；尚未实施≥10秒长跑/新CPU/PDS/硬件。额外参考/工具执行/成本范围另核，不静默扩上限。
- [ ] 等B原R1–R3/v02差额，按F149只核必要差额/导入，无新核心任务；用户报告已转交，不重复索发。Pango确切告警外部事实/正式时基/外部CDC/FPGA/ILA/过温停止缺口保持，10月27日18北京时间窗口不变。

### 以下F150待批提案当前已由D149批准/F151有限完成取代，旧原件保留
''')
    p=Mem/'COLLABORATION.md';text=p.read_text(encoding='utf-8-sig');a,b=text.split('\n',1);p.write_text(a+'\n\n'+r'''版本：COLLAB v1.78；2026-10-25，F151/D149–150。A独立完成双种子各2迭代校准：2真实新DUT/全态与逐笔副作用/计时/1323UART有限通过，13RTL与B核心包装不改，非正式成绩/新系统硬件验收；F143稳定/F146暂缓/F147告警和over_temp STOP保持。

B仍原R1–R3验证/最终封包与10/27 18北京时间窗口，用户已报告人工转交；未推定新ACK/v02、无自动外发，不要求B解决A计时/长测/工具或重做核心/W06/GPIO。A下一仅长测验证与资源方案，原本轮2DUT范围已完成，不自动加新CPU/PDS或硬件权限。

### 历史v1.77（其中双迭代待批已由D149批准/F151有限完成取代）
'''+b,encoding='utf-8',newline='\n')
    p=P/'README.md';raw=p.read_bytes();marker='|当前系统上板、片上波形|'.encode();i=raw.index(marker);row='|双种子各2迭代校准|F151新2DUT严格有限通过，raw4207378/4526490、finalCRC72be/fe8c、完整662/661UART；只新端口迭代接线/验证预算，13RTL不改，先验参考与每笔副作用/全态核同。仍不足10秒、非正式或实机验收|\n'.encode();raw=raw[:i]+row+raw[i:]
    marker='- [F150正式测量就绪]'.encode();i=raw.index(marker);row='- [F151双迭代真实校准](reports/verification/2026-10-25-coremark-iter2-m1.md)：新参数初始化、先验参考、2个实际DUT/计时/全状态/有序副作用及完整串行证据，旧源/失败保留；F143稳定/F146暂缓，下一长测资源方案未自动实施。\n'.encode();p.write_bytes(raw[:i]+row+raw[i:])
    memory={}
    for name in ['CURRENT.md','INDEX.md','FACTS.md','DECISIONS.md','TODO.md','COLLABORATION.md']:
        t=(Mem/name).read_text(encoding='utf-8-sig');assert 'F151' in t or 'F-151' in t;memory[name]=dict(SHA256=sha(Mem/name),lines=len(t.splitlines()))
    assert memory['CURRENT.md']['lines']<20
    save(H/'postflight-final.json',dict(status='MEMORY_READBACK_AND_PROTECTION_PASS',memory=memory,originals=protect(),frozen=len(read(H/'frozen.json')['files']),new_DUT=2,actual_result='PASS_LIMITED_DOUBLE_ITERATION_CALIBRATION',source13_unchanged=True,hardware='STOPPED',candidate_promoted=False,report_SHA256=sha(P/'reports/verification/2026-10-25-coremark-iter2-m1.md')))
    files=sorted(p for p in H.rglob('*') if p.is_file() and p.name!='SHA256SUMS-final.txt')
    with (H/'SHA256SUMS-final.txt').open('x',encoding='utf-8',newline='\n') as f:
        for p in files:f.write(sha(p)+'  '+p.relative_to(H).as_posix()+'\n')
    print(json.dumps(dict(memory_readback='PASS',fact='F151',decision='D150',frozen=len(read(H/'frozen.json')['files']),new_DUT=2,hardware='STOPPED',snapshot_files=len(files))))
if __name__=='__main__':run()
