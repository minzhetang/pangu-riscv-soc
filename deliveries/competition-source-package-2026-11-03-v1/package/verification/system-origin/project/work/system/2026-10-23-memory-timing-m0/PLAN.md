# A-MEM-TIMING-M0：冻结前计划

2026-10-23，D115批准范围。CPU整组F108不改；原TB、C/CoreMark、旧模型/结果及队员材料不改。新TB为1ns/1ps，10ns周期，复位在下降沿释放；RF初态沿用原模块initial零值，非热复位承诺。

## 两个编译目标，上限三次；首次异常停止编译线

1. `tb_drm` + 本机PDS官方GTP_DRM18K_E1/GTP_GRS，固定16位、1024深度、单口、NORMAL_WRITE、同步输出复位、GRS禁用、输出寄存0/1双实例；两个字节使能。初始化使用默认INIT全零，不改官方文件、不分发受限模型。读沿前/沿后、输出附加寄存、两lane保留、写后读、正常写保持输出和复位不擦除；不测双口冲突/级联/全容量。
2. `tb_cpu_timing` + 未改四源，同一VVP使用plusargs独立进程选择IF/DATA组合或同一上升沿注册读（四组合），读先于同沿写。行为模型只验证时序假设，非官方模型直接接CPU或PDS资源映射。

每编译60秒、每运行30秒/2000周期。普通编译0xC0000005即停，不运行残留VVP，不换工具/环境重试；沙箱外新固定命令另申请。输入与期望、脚本/TB/官方文件/工具SHA执行前冻结，runner拒绝变化与第二次自动编译。原始stdout/stderr文件保存。

## 小程序与手工预期（先于DUT）

所有未写寄存器0；RAM地址0x100–0x1ff初始化0xa5；ROM256字包含程序与0x80常量0x12345678。未用ROM填EBREAK（非插NOP）。每次运行独立进程。

|ID|真实指令路径/初始条件|手工预期；精确WB/STORE另由独立小解释器生成并冻结|
|---|---|---|
|P01|ADDI x1,128; LW x2,0(x1); ADDI x3,x2,1; EBREAK|x1=128,x2=12345678,x3=12345679；0写；stop PC=12；取指与ROM常量读同时存在|
|P02|ADDI x1,256; ADDI x2,85; SW两次同址; LW x3; ADDI x4,x3,1; ADDI x5,-1; SB x5,1(x1); SH x4,2(x1); LW x6; EBREAK|x3=85,x4=86,x5=ffffffff,x6=0056ff55，RAM首字0056ff55；四次独立STORE（SW、SW、SB、SH），stop PC=40|
|P03T|ADDI x1,256; LW x2; BEQ x2,x0,+12; ADDI x3,7; SW x3,4(x1); EBREAK；首字0|x1=256，其余0；无STORE；stop PC=20；真实load→branch|
|P03N|同程序，首字5|x2=5,x3=7，RAM第二字7；一次STORE；stop PC=20|
|P04|ADDI x1,1; BEQ x1,x1,+12; 错路SW/ADDI; 目标ADDI x8,42; SW x8,264(x0); EBREAK|x1=1,x8=42，x7=0；只一次STORE到264=42；stop PC=24；冲刷旧取指及错误副作用|
|P05|ADDI x1,256; LW x2,4(x1); EBREAK; 年轻SW；第二字deadbeef|x1=256,x2=deadbeef；无STORE；stop PC=8；停止前旧load排空|

每例核32RF、256B RAM、全序WB和STORE分别不去重、load请求数据、IF采样地址/指令与采样后IFID配对、stop kind/PC、停顿/冲刷计数、关键X/Z及停止后8周期无副作用。不会把IF PC当退休PC；WB/STORE两流不等统一提交序。

零等待组应全通过；同步组先按相同架构预期判定，出现失败是探针的反例，不是修改预期后的PASS。不兼容模式可能无法到达后续观察点，须标未覆盖；不为覆盖而修CPU或掩盖失配。按文档建立的注册行为模型不等实际32K物理存储验证。
