# 旧O2固定256次 真实片上分析工程

本目录保存原pre/build源与相对flow、约束、debug.fic/runtime-debug.fic、140位探针顺序，四个合格窗口的WDF/dprj/CSV及原分析器。软件来自对应原O2固定256程序，不是SM2。读WDF、波形与CSV不要求接板，首次复验应先按原数据身份核对。

build/flow.tcl依赖../debug.fic；FIC的designInputFile仍是原预综合ADF绝对路径，不能原地照跑。本包不分发ADF/DB/综合网表及厂商调试模型，复建时须在包外新工程用相同PDS生成pre网表，再在新FIC副本仅绑定新pre路径并保存差异，才进入build流程。不能靠改文件名假定FIC物理连接完全验收。

旧调试版保留4条扫描链时钟Critical。四窗完整统计及原串口共同支撑限定观察，不等调试时钟/CDC/全部IO签核。有效EX必须满足复位有效、eei_hold=0、pipeline_advance=1、id_valid=1；固定两相的保持拍不能重复数指令，局部EX密度不是退休IPC。

analyze_windows.py带原工作区数据位置，read_wdf_current.py只支持既定140通道/1024点WDF子集；工具入口要按随包数据位置配置，不能把旧文件重读称新采集。Pillow只用于可选图形重绘。全量VCD非必要，本包保留四WDF/CSV及图像，无新采样。
