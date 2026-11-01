# CoreMark256恢复诊断与验证种子实测（2026-11-01）

## 阶段结论

本轮真实串口已两次取得验证种子256迭代完整报告，1119字节逐字节匹配，五CRC及64位目标计时一致。结合此前F244性能种子的两轮，已见证两种种子各两轮、都超过10标称秒的物理输出。但最后指定加载文件为性能镜像，实际报告仍为验证种子，文件—ROM—运行内容的身份链未闭合；本轮不签固定镜像正式总验收，不把它标为性能正控制通过。阶段结束，全部所属工具/Job退出，不继续追加下载。

|实际观测|轮次|目标ticks|标称27MHz时间|原始报告SHA|
|---|---:|---:|---:|---|
|性能种子：此前H30/H32|2|538539600|19.945911111s|73425EECBAB76C9DDE20D58A7F1E85014F346B3242C995C9B6F64B1DCDC0679E|
|验证种子：本次H45/H46|2|579425414|21.460200519s|964A824A23C19E1626DE0986CD904776133FA44B4A258E63B7DC70DE6D9ACADC|

验证CRC：seed18f2/list e3c1/matrix0747/state8d84/final798f。start=0x0000f3a1，end=0x228a4827，64位差=0x22895486=579425414。两轮均新接收窗口、用户明确KEY0、全字节校验、0串口写/无串口错误、原生0/Job空/无强清，非旧数据重放或仅exit0判PASS。计算区停止计时后才输出串口。独立校准时钟未做，27MHz来源及D18/无分频计时器证据沿用M1 CLOCK_BASIS；不以宿主耗时或固件整数速率12/13报精确成绩。性能精确换算12.834710762迭代/秒、0.475359658/MHz；验证种子不混用为性能分数，不称EEMBC认证。

## 按实际顺序的证据

以下目录均位于D:/A_FPGA_Comp/work/pds-jtag，机器记录见resume-m2/RESULTS.json：

1. H36新只读：PG2L100H/公开ID00602899；00180c80，DONE0/GOUTEN0/OT0、CRC/ID错误0；正常退出。
2. H37原属性3/500k配置验证镜像：165.734秒成功，后两次081efca0，DONE1/GOUTEN0/OT1/CRC-ID错误0；自动UART0。不能将本次成功追认为旧H33失败已定位。
3. H39只一次简化JWAKEUP：官方UG040005 V1.3实际24/印刷23表2-5视觉核28D；前后GOUTEN0/输出0，0Program，正常退出。非保护关闭。旧APPROVAL中SHA使用规范化LF字符串，与磁盘CRLF字节不同，实际执行有精确read_text守卫；H39_SVF_HASH_CLARIFICATION另存真实字节SHA，旧文件保留。
4. H40属性1关断配置、不启用ISC：安装版Fabric Configuration V1.0实际45表2及83位定义已视觉核Logo/Logos2适用性；同验证位流、同频，唯一实际参数3→1；62.109秒成功，仍GOUTEN0/自动UART0。下载耗时变化不等CPU性能提升，也不证明ISC唯一因果。
5. H38提前COM22后用户KEY0：300秒窗口0字节/无串口错误、正常结束；无验证算法输出，不能称CRC失败。
6. H41：主机把PDS精确的“输出不存在、现在创建”W:Configuration-4002警告中的failed误判为致命错误，0字节即强制清树。是主机误判，不是已确认芯片故障，不能称0硬件尝试。
7. H41-r1：只豁免同一命令/同一目标路径的该精确警告，生产判断片段8项正负控通过；实际ISC回读单命令200秒超时，保存393216字节不完整原始文件，所属Job强清/最终为空。原始数据恰等源FDRI[4:393220]，零差异；不移动原数据、不冒称完整Verify PASS。该前缀两种镜像本来相同，不能用它识别当前ROM程序，也不能从配置回读推断CPU完成计算。固定一个32位字偏移与旧LED读回现象一致，引入层仍未知。
8. H42离线SVF：首试缺虚拟器件；r1已按官方cfg_add_device从本地sbit添加，但又被同类输出创建警告误拦；r2修正精确警告后，官方纯离线导出7643949字节SVF，0硬件连接/原生0/Job空。前两次失败均保留，未执行整份生成文件。
9. H43仅执行原厂SVF大SDR后8条启动收尾：TAP Reset100TCK/IDLE1000/JWAKEUP28D/IDLE1000/BYPASS3FF/159的DONE只读校验/STATE RESET，原厂命令逐条核同，0大配置SDR/0JRST FPGA复位/0Program/0保护写；成功但GOUTEN仍0。首次磁盘CRLF/LF字符串SHA不一致被预检拦在ATTEMPT前，0硬件；旧文件及纠正记录保留，正式执行以真实磁盘SHA冻结。
10. H44已验收性能镜像正控制：固定A86C7ECB…FF644CC4、原属性3/500k，165.750秒Program成功；两次081ffca0，GOUTEN0→1，自动UART0。此为本轮第3次Program，分阶段初始上限和新增证据/预算分别保留于D276/D278/D282，不伪装成未增加或0Program。
11. H45/H46当前KEY0后各实收1119字节，严格匹配验证种子，非H44意图的性能种子。只接受该真实观测及重复性，未再配置、未改预期；末轮工具正常退出。

全部前后OT读数保留，D237下不单独停止、不修改芯片保护；不将用户判断或正常输出当实温/供电正常证明。没有Flash操作、安装、GUI、新RTL/GCC/仿真/PDS构建或Git提交推送。

## 身份异常的独立审查

PROGRAM_IDENTITY_AUDIT核了H44真实原生命令cfg_assign_file路径与实际磁盘位流SHA，确为性能文件；H45/H46采集脚本指向各自新目录、CreateNew原始文件、0串口写，且有新用户KEY0回执，排除这里已检查的复用旧raw/复制脚本旧BASE路径问题。不得将最后assign成功等同ROM内容已更新。

两源.sbit的2084字节头部只在98/100/101处不同，落在HH:MM:SS格式的生成时间字符串10:45:44与10:47:07；未把厂商头部完整私有格式假装已解码。非FDRI28控制包仅两次CRC寄存器0不同；第一2960512字节FDRI块完全相同，第二827392字节块有1255字节差异。未凭块位置就宣称已完整映射所有DRM/逻辑配置位。相关JSON保存全部数字/哈希；不由此断言两镜像功能无差异或某个唯一根因。

存储初始化/保留、实际编程覆盖范围、工具缓存等只是下一轮待查假设。当前仅有功能RTL相同及实际输出元数据/CRC匹配的有限身份线索，没有完整ROM读回或独立冷启动单镜像证明。原performance文件基线和H33失败不删除、不静默改成通过。本轮新记录为“观测到验证运行”，不是“验证位流992…已独立可重载验收”。

## 复查入口、命令与边界

总入口work/pds-jtag/2026-11-01-coremark256-resume-m2/{RESULTS,POST_INPUT_HASH_CHECK,EVIDENCE_SHA256}.json；原始证据各H目录RESULT/SERIAL_RESULT/native-sanitized/raw；本次观测索引work/hardware-baselines/2026-11-01-coremark256-observed-validation-v1/BASELINE.json（明确非独立重载基线）。原M1报告和基线保持历史原样。

执行工具为既有PDS2022.2-SP6.4官方下载CLI及Windows PowerShell5串口接收，COM22 115200/8N1/无流控/DTR-RTS false。没有重查许可证剩余有效期，不沿用旧提示编造天数。Python绝对路径C:/Users/tamii/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe，所有执行均-X utf8 -B <各H目录脚本> --run；旧ATTEMPT已消费，禁止盲重跑。各RESULT.commands保留完整原生参数；H42相关只离线、不连接硬件。H45/H46新离线核验原命令为同一Python -X utf8 -B work/pds-jtag/2026-11-01-coremark256-measurement-m1/check_measurement.py validation256 <对应uart-raw.bin绝对路径>，独占生成MEASUREMENT_CHECK，不能覆盖重跑。

237项旧构建证据、21项本轮冻结输入执行后SHA全部一致；只新增诊断脚本和报告，不改CPU/SoC/外设、旧TB、参考模型或冻结预期。有限运行不等完整RV32I或每笔退休/WB/STORE过程正确，无真实退休PC、WB/STORE分流、固定存储/初态、IO/CDC/SCBV物理接线、温度等局限保留；本轮无新ILA采样，不将串口或旧WDF包装为本版新片上波形。

下一唯一重点：建立“指定文件→实际程序存储内容→冷启动输出”的身份闭环，再签收可独立恢复的正式测量镜像；必要时先审完整原厂SVF与DRM初始化规则，对照须明确计为额外配置，不能伪装只读。当前观测序列仅历史，不是保证可复现的生产加载配方。本轮已结束，不自动执行该下一阶段。
