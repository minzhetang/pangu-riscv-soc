# 本次实际执行命令

16次编译经单批权限审批；781次仿真为普通权限。以下JSON argv不经shell拆分；cwd、限时、原生rc和墙时见对应process.json。

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_mem_adapt", "-Ptb_mem_adapt.SYNC=0", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\memory_model.sv", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\tb_mem_adapt.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_mem_adapt", "-Ptb_mem_adapt.SYNC=1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\memory_model.sv", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\tb_mem_adapt.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_lbu_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_lb_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_lhu_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_lh_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_sb_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_sh_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_fence_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_eei_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_zero_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_r4_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_rcmp_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_addsub_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_cpu_selfcheck_v1", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\cpu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\alu.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\control.v", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\source\\regfile.v", "D:\\A_FPGA_Comp\\work\\icarus\\2026-10-21-cpu-shifti-reject\\tb_cpu_rshift_selfcheck_v1.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1", "timeout_seconds": 60}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T01_addi_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T01_addi_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T01_addi_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T02_alu_isolated", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T02_alu_isolated"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T02_alu_isolated", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T03_memory_isolated", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T03_memory_isolated"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T03_memory_isolated", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T04_beq_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T04_beq_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T04_beq_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T05_beq_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T05_beq_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T05_beq_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T06_bne_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T06_bne_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T06_bne_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T07_bne_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T07_bne_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T07_bne_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T08_raw_adjacent", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T08_raw_adjacent"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T08_raw_adjacent", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T09_store_raw_adjacent", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T09_store_raw_adjacent"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T09_store_raw_adjacent", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T10_load_use_adjacent", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T10_load_use_adjacent"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T10_load_use_adjacent", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T11_load_use_same_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T11_load_use_same_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T11_load_use_same_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T12_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T12_jal"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T12_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=T13_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/T13_jalr"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\T13_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=B01_priority_dual_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/B01_priority_dual_store"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\B01_priority_dual_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=B02_x0_immediate_store_address", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/B02_x0_immediate_store_address"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\B02_x0_immediate_store_address", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=B03_wb_id_same_edge", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/B03_wb_id_same_edge"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\B03_wb_id_same_edge", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=C01_wb_id_dual_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/C01_wb_id_dual_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\C01_wb_id_dual_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=C02_wb_id_store_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/C02_wb_id_store_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\C02_wb_id_store_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=C03_wb_id_x0_excluded", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/C03_wb_id_x0_excluded"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\C03_wb_id_x0_excluded", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=L01_load_dual_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/L01_load_dual_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\L01_load_dual_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=L02_load_store_reload", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/L02_load_store_reload"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\L02_load_store_reload", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=L03_false_rs2_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/L03_false_rs2_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\L03_false_rs2_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=J01_negative_jal_link_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/J01_negative_jal_link_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\J01_negative_jal_link_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=J02_jalr_forward_odd_negative", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/J02_jalr_forward_odd_negative"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\J02_jalr_forward_odd_negative", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=J03_load_jalr_same_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/J03_load_jalr_same_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\J03_load_jalr_same_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=J04_jump_x0_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/J04_jump_x0_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\J04_jump_x0_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X01_wrap_signed_logic", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X01_wrap_signed_logic"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X01_wrap_signed_logic", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X02_shift_mask_sign", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X02_shift_mask_sign"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X02_shift_mask_sign", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X03_branch_dual_forward", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X03_branch_dual_forward"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X03_branch_dual_forward", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X04_backward_branch_load_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X04_backward_branch_load_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X04_backward_branch_load_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X05_load_branch_squash_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X05_load_branch_squash_jump"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X05_load_branch_squash_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X06_load_address_store_chain", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X06_load_address_store_chain"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X06_load_address_store_chain", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X07_latest_load_same_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X07_latest_load_same_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X07_latest_load_same_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=X08_jal_target_jalr_return", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/X08_jal_target_jalr_return"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\X08_jal_target_jalr_return", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I01_xori_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I01_xori_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I01_xori_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I02_andi_alias_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I02_andi_alias_store"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I02_andi_alias_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I03_zero_control", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I03_zero_control"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I03_zero_control", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I04_signed_pattern", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I04_signed_pattern"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I04_signed_pattern", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I05_ones_signbit", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I05_ones_signbit"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I05_ones_signbit", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I06_bypass_distances", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I06_bypass_distances"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I06_bypass_distances", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I07_x0_self_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I07_x0_self_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I07_x0_self_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=I08_false_rs2_regression", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/I08_false_rs2_regression"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\I08_false_rs2_regression", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S01_slli_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S01_slli_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S01_slli_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S02_zero_shift_control", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S02_zero_shift_control"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S02_zero_shift_control", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S03_pattern_truncation", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S03_pattern_truncation"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S03_pattern_truncation", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S04_ones_signbit", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S04_ones_signbit"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S04_ones_signbit", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S05_bypass_distances", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S05_bypass_distances"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S05_bypass_distances", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S06_x0_self_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S06_x0_self_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S06_x0_self_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S07_false_rs2_regression", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S07_false_rs2_regression"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S07_false_rs2_regression", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=S08_load_store_chain", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S08_load_store_chain"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S08_load_store_chain", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R01_srli_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R01_srli_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R01_srli_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R02_zero_shift_control", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R02_zero_shift_control"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R02_zero_shift_control", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R03_unsigned_pattern", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R03_unsigned_pattern"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R03_unsigned_pattern", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R04_ones_zero_fill", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R04_ones_zero_fill"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R04_ones_zero_fill", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R05_bypass_distances", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R05_bypass_distances"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R05_bypass_distances", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R06_x0_self_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R06_x0_self_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R06_x0_self_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R07_false_rs2_regression", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R07_false_rs2_regression"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R07_false_rs2_regression", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=R08_load_store_chain", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/R08_load_store_chain"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\R08_load_store_chain", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A01_srai_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A01_srai_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A01_srai_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A02_zero_shift", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A02_zero_shift"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A02_zero_shift", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A03_signed_pattern", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A03_signed_pattern"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A03_signed_pattern", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A04_ones_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A04_ones_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A04_ones_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A05_bypass_distances", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A05_bypass_distances"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A05_bypass_distances", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A06_x0_self_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A06_x0_self_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A06_x0_self_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A07_false_rs2_regression", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A07_false_rs2_regression"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A07_false_rs2_regression", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=A08_load_store_chain", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/A08_load_store_chain"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\A08_load_store_chain", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K01_slt_signed_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K01_slt_signed_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K01_slt_signed_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K02_slt_positive_order", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K02_slt_positive_order"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K02_slt_positive_order", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K03_slt_extreme_overflow", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K03_slt_extreme_overflow"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K03_slt_extreme_overflow", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K04_slt_negative_order", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K04_slt_negative_order"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K04_slt_negative_order", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K05_slt_rs1_bypasses", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K05_slt_rs1_bypasses"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K05_slt_rs1_bypasses", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K06_slt_rs2_bypasses", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K06_slt_rs2_bypasses"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K06_slt_rs2_bypasses", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K07_slt_load_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K07_slt_load_rs1"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K07_slt_load_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K08_slt_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K08_slt_load_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K08_slt_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K09_slt_x0_self_sources", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K09_slt_x0_self_sources"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K09_slt_x0_self_sources", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K10_slt_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K10_slt_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K10_slt_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=K11_slt_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/K11_slt_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\K11_slt_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U01_sltu_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U01_sltu_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U01_sltu_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U02_sltu_signed_distinction", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U02_sltu_signed_distinction"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U02_sltu_signed_distinction", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U03_sltu_sign_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U03_sltu_sign_boundary"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U03_sltu_sign_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U04_sltu_max_neighbours", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U04_sltu_max_neighbours"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U04_sltu_max_neighbours", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U05_sltu_rs1_bypasses", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U05_sltu_rs1_bypasses"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U05_sltu_rs1_bypasses", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U06_sltu_rs2_bypasses", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U06_sltu_rs2_bypasses"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U06_sltu_rs2_bypasses", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U07_sltu_load_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U07_sltu_load_rs1"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U07_sltu_load_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U08_sltu_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U08_sltu_load_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U08_sltu_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U09_sltu_x0_self_sources", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U09_sltu_x0_self_sources"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U09_sltu_x0_self_sources", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U10_sltu_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U10_sltu_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U10_sltu_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=U11_sltu_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/U11_sltu_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\U11_sltu_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V01_slti_equal_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V01_slti_equal_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V01_slti_equal_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V02_slti_negative_immediate", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V02_slti_negative_immediate"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V02_slti_negative_immediate", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V03_slti_extremes", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V03_slti_extremes"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V03_slti_extremes", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V04_slti_low_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V04_slti_low_boundary"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V04_slti_low_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V05_slti_high_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V05_slti_high_boundary"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V05_slti_high_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V06_slti_bypasses", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V06_slti_bypasses"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V06_slti_bypasses", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V07_slti_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V07_slti_load"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V07_slti_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V08_slti_false_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V08_slti_false_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V08_slti_false_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V09_slti_x0_self_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V09_slti_x0_self_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V09_slti_x0_self_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V10_slti_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V10_slti_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V10_slti_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=V11_slti_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/V11_slti_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\V11_slti_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W01_sltiu_alias", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W01_sltiu_alias"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W01_sltiu_alias", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W02_sltiu_signext_pair", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W02_sltiu_signext_pair"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W02_sltiu_signext_pair", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W03_sltiu_negative_threshold", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W03_sltiu_negative_threshold"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W03_sltiu_negative_threshold", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W04_sltiu_zero_detection", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W04_sltiu_zero_detection"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W04_sltiu_zero_detection", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W05_sltiu_positive_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W05_sltiu_positive_boundary"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W05_sltiu_positive_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W06_sltiu_bypasses", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W06_sltiu_bypasses"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W06_sltiu_bypasses", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W07_sltiu_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W07_sltiu_load"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W07_sltiu_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W08_sltiu_false_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W08_sltiu_false_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W08_sltiu_false_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W09_sltiu_x0_self_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W09_sltiu_x0_self_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W09_sltiu_x0_self_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W10_sltiu_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W10_sltiu_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W10_sltiu_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=W11_sltiu_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/W11_sltiu_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\W11_sltiu_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z01_blt_alias_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z01_blt_alias_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z01_blt_alias_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z02_blt_alias_signed", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z02_blt_alias_signed"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z02_blt_alias_signed", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z03_blt_equal_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z03_blt_equal_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z03_blt_equal_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z04_blt_equal_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z04_blt_equal_zero"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z04_blt_equal_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z05_blt_extreme", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z05_blt_extreme"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z05_blt_extreme", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z06_blt_extreme_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z06_blt_extreme_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z06_blt_extreme_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z07_blt_equal_min", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z07_blt_equal_min"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z07_blt_equal_min", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z08_blt_equal_max", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z08_blt_equal_max"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z08_blt_equal_max", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z09_blt_negative_order", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z09_blt_negative_order"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z09_blt_negative_order", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z10_blt_negative_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z10_blt_negative_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z10_blt_negative_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z11_blt_positive_less", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z11_blt_positive_less"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z11_blt_positive_less", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z12_blt_rs1_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z12_blt_rs1_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z12_blt_rs1_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z13_blt_rs1_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z13_blt_rs1_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z13_blt_rs1_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z14_blt_rs1_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z14_blt_rs1_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z14_blt_rs1_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z15_blt_rs2_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z15_blt_rs2_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z15_blt_rs2_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z16_blt_rs2_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z16_blt_rs2_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z16_blt_rs2_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z17_blt_rs2_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z17_blt_rs2_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z17_blt_rs2_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z18_blt_latest_priority", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z18_blt_latest_priority"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z18_blt_latest_priority", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z19_blt_load_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z19_blt_load_rs1"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z19_blt_load_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z20_blt_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z20_blt_load_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z20_blt_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z21_blt_load_same_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z21_blt_load_same_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z21_blt_load_same_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z22_blt_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z22_blt_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z22_blt_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z23_blt_backward_loop", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z23_blt_backward_loop"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z23_blt_backward_loop", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z24_blt_plus4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z24_blt_plus4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z24_blt_plus4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z25_blt_zero_offset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z25_blt_zero_offset"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z25_blt_zero_offset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=Z26_blt_squash_jump_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Z26_blt_squash_jump_load"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Z26_blt_squash_jump_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G01_bge_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G01_bge_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G01_bge_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G02_bge_signed_false", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G02_bge_signed_false"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G02_bge_signed_false", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G03_bge_equal_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G03_bge_equal_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G03_bge_equal_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G04_bge_equal_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G04_bge_equal_zero"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G04_bge_equal_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G05_bge_extreme", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G05_bge_extreme"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G05_bge_extreme", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G06_bge_extreme_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G06_bge_extreme_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G06_bge_extreme_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G07_bge_equal_min", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G07_bge_equal_min"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G07_bge_equal_min", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G08_bge_equal_max", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G08_bge_equal_max"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G08_bge_equal_max", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G09_bge_negative_order", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G09_bge_negative_order"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G09_bge_negative_order", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G10_bge_negative_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G10_bge_negative_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G10_bge_negative_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G11_bge_signed_true", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G11_bge_signed_true"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G11_bge_signed_true", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G12_bge_rs1_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G12_bge_rs1_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G12_bge_rs1_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G13_bge_rs1_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G13_bge_rs1_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G13_bge_rs1_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G14_bge_rs1_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G14_bge_rs1_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G14_bge_rs1_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G15_bge_rs2_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G15_bge_rs2_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G15_bge_rs2_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G16_bge_rs2_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G16_bge_rs2_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G16_bge_rs2_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G17_bge_rs2_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G17_bge_rs2_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G17_bge_rs2_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G18_bge_latest_priority", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G18_bge_latest_priority"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G18_bge_latest_priority", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G19_bge_load_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G19_bge_load_rs1"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G19_bge_load_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G20_bge_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G20_bge_load_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G20_bge_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G21_bge_load_same_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G21_bge_load_same_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G21_bge_load_same_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G22_bge_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G22_bge_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G22_bge_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G23_bge_backward_loop", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G23_bge_backward_loop"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G23_bge_backward_loop", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G24_bge_plus4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G24_bge_plus4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G24_bge_plus4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G25_bge_zero_offset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G25_bge_zero_offset"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G25_bge_zero_offset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=G26_bge_squash_jump_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/G26_bge_squash_jump_load"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\G26_bge_squash_jump_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H01_bltu_alias_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H01_bltu_alias_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H01_bltu_alias_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H02_bltu_unsigned_false", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H02_bltu_unsigned_false"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H02_bltu_unsigned_false", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H03_bltu_unsigned_true", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H03_bltu_unsigned_true"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H03_bltu_unsigned_true", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H04_bltu_equal_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H04_bltu_equal_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H04_bltu_equal_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H05_bltu_sign_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H05_bltu_sign_boundary"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H05_bltu_sign_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H06_bltu_sign_boundary_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H06_bltu_sign_boundary_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H06_bltu_sign_boundary_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H07_bltu_borrow_true", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H07_bltu_borrow_true"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H07_bltu_borrow_true", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H08_bltu_borrow_false", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H08_bltu_borrow_false"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H08_bltu_borrow_false", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H09_bltu_max_neighbour", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H09_bltu_max_neighbour"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H09_bltu_max_neighbour", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H10_bltu_max_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H10_bltu_max_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H10_bltu_max_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H11_bltu_positive_less", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H11_bltu_positive_less"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H11_bltu_positive_less", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H12_bltu_rs1_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H12_bltu_rs1_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H12_bltu_rs1_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H13_bltu_rs1_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H13_bltu_rs1_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H13_bltu_rs1_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H14_bltu_rs1_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H14_bltu_rs1_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H14_bltu_rs1_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H15_bltu_rs2_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H15_bltu_rs2_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H15_bltu_rs2_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H16_bltu_rs2_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H16_bltu_rs2_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H16_bltu_rs2_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H17_bltu_rs2_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H17_bltu_rs2_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H17_bltu_rs2_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H18_bltu_latest_priority", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H18_bltu_latest_priority"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H18_bltu_latest_priority", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H19_bltu_load_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H19_bltu_load_rs1"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H19_bltu_load_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H20_bltu_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H20_bltu_load_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H20_bltu_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H21_bltu_load_same_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H21_bltu_load_same_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H21_bltu_load_same_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H22_bltu_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H22_bltu_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H22_bltu_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H23_bltu_backward_loop", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H23_bltu_backward_loop"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H23_bltu_backward_loop", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H24_bltu_plus4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H24_bltu_plus4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H24_bltu_plus4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H25_bltu_zero_offset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H25_bltu_zero_offset"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H25_bltu_zero_offset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=H26_bltu_squash_jump_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H26_bltu_squash_jump_load"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H26_bltu_squash_jump_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N01_bgeu_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N01_bgeu_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N01_bgeu_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N02_bgeu_unsigned_true", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N02_bgeu_unsigned_true"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N02_bgeu_unsigned_true", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N03_bgeu_unsigned_false", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N03_bgeu_unsigned_false"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N03_bgeu_unsigned_false", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N04_bgeu_equal_positive", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N04_bgeu_equal_positive"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N04_bgeu_equal_positive", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N05_bgeu_sign_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N05_bgeu_sign_boundary"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N05_bgeu_sign_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N06_bgeu_sign_boundary_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N06_bgeu_sign_boundary_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N06_bgeu_sign_boundary_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N07_bgeu_borrow_false", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N07_bgeu_borrow_false"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N07_bgeu_borrow_false", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N08_bgeu_borrow_true", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N08_bgeu_borrow_true"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N08_bgeu_borrow_true", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N09_bgeu_max_neighbour", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N09_bgeu_max_neighbour"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N09_bgeu_max_neighbour", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N10_bgeu_max_reverse", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N10_bgeu_max_reverse"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N10_bgeu_max_reverse", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N11_bgeu_equal_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N11_bgeu_equal_zero"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N11_bgeu_equal_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N12_bgeu_rs1_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N12_bgeu_rs1_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N12_bgeu_rs1_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N13_bgeu_rs1_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N13_bgeu_rs1_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N13_bgeu_rs1_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N14_bgeu_rs1_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N14_bgeu_rs1_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N14_bgeu_rs1_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N15_bgeu_rs2_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N15_bgeu_rs2_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N15_bgeu_rs2_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N16_bgeu_rs2_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N16_bgeu_rs2_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N16_bgeu_rs2_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N17_bgeu_rs2_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N17_bgeu_rs2_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N17_bgeu_rs2_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N18_bgeu_latest_priority", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N18_bgeu_latest_priority"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N18_bgeu_latest_priority", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N19_bgeu_load_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N19_bgeu_load_rs1"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N19_bgeu_load_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N20_bgeu_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N20_bgeu_load_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N20_bgeu_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N21_bgeu_load_same_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N21_bgeu_load_same_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N21_bgeu_load_same_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N22_bgeu_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N22_bgeu_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N22_bgeu_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N23_bgeu_backward_loop", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N23_bgeu_backward_loop"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N23_bgeu_backward_loop", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N24_bgeu_plus4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N24_bgeu_plus4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N24_bgeu_plus4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N25_bgeu_zero_offset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N25_bgeu_zero_offset"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N25_bgeu_zero_offset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=N26_bgeu_squash_jump_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/N26_bgeu_squash_jump_load"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\N26_bgeu_squash_jump_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O01_lui_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O01_lui_zero"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O01_lui_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O02_lui_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O02_lui_one"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O02_lui_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O03_lui_positive_max_upper", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O03_lui_positive_max_upper"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O03_lui_positive_max_upper", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O04_lui_sign_bit", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O04_lui_sign_bit"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O04_lui_sign_bit", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O05_lui_all_upper_ones", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O05_lui_all_upper_ones"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O05_lui_all_upper_ones", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O06_lui_mixed", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O06_lui_mixed"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O06_lui_mixed", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O07_lui_all_pseudo_funct3", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O07_lui_all_pseudo_funct3"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O07_lui_all_pseudo_funct3", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O08_lui_ignore_pseudo_rs1_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O08_lui_ignore_pseudo_rs1_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O08_lui_ignore_pseudo_rs1_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O09_lui_ignore_pseudo_rs1_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O09_lui_ignore_pseudo_rs1_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O09_lui_ignore_pseudo_rs1_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O10_lui_ignore_pseudo_rs1_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O10_lui_ignore_pseudo_rs1_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O10_lui_ignore_pseudo_rs1_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O11_lui_load_pseudo_rs1_zero_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O11_lui_load_pseudo_rs1_zero_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O11_lui_load_pseudo_rs1_zero_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O12_lui_load_pseudo_rs2_zero_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O12_lui_load_pseudo_rs2_zero_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O12_lui_load_pseudo_rs2_zero_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O13_lui_to_ALU_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O13_lui_to_ALU_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O13_lui_to_ALU_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O14_lui_to_ALU_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O14_lui_to_ALU_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O14_lui_to_ALU_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O15_lui_to_ALU_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O15_lui_to_ALU_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O15_lui_to_ALU_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O16_lui_to_STORE_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O16_lui_to_STORE_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O16_lui_to_STORE_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O17_lui_to_STORE_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O17_lui_to_STORE_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O17_lui_to_STORE_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O18_lui_to_STORE_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O18_lui_to_STORE_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O18_lui_to_STORE_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O19_lui_rd_x0_load_x0_exclusion", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O19_lui_rd_x0_load_x0_exclusion"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O19_lui_rd_x0_load_x0_exclusion", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=O20_lui_overlap_repeat_latest", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/O20_lui_overlap_repeat_latest"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\O20_lui_overlap_repeat_latest", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P01_auipc_pc0_U0_legal_zero_WB", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P01_auipc_pc0_U0_legal_zero_WB"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P01_auipc_pc0_U0_legal_zero_WB", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P02_auipc_nonzero_PC_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P02_auipc_nonzero_PC_one"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P02_auipc_nonzero_PC_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P03_auipc_nonzero_PC_positive_max_upper", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P03_auipc_nonzero_PC_positive_max_upper"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P03_auipc_nonzero_PC_positive_max_upper", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P04_auipc_nonzero_PC_sign_bit", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P04_auipc_nonzero_PC_sign_bit"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P04_auipc_nonzero_PC_sign_bit", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P05_auipc_nonzero_PC_all_upper_ones", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P05_auipc_nonzero_PC_all_upper_ones"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P05_auipc_nonzero_PC_all_upper_ones", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P06_auipc_nonzero_PC_mixed", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P06_auipc_nonzero_PC_mixed"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P06_auipc_nonzero_PC_mixed", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P07_auipc_all_pseudo_funct3", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P07_auipc_all_pseudo_funct3"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P07_auipc_all_pseudo_funct3", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P08_auipc_ignore_pseudo_rs1_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P08_auipc_ignore_pseudo_rs1_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P08_auipc_ignore_pseudo_rs1_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P09_auipc_ignore_pseudo_rs1_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P09_auipc_ignore_pseudo_rs1_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P09_auipc_ignore_pseudo_rs1_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P10_auipc_ignore_pseudo_rs1_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P10_auipc_ignore_pseudo_rs1_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P10_auipc_ignore_pseudo_rs1_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P11_auipc_load_pseudo_rs1_zero_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P11_auipc_load_pseudo_rs1_zero_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P11_auipc_load_pseudo_rs1_zero_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P12_auipc_load_pseudo_rs2_zero_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P12_auipc_load_pseudo_rs2_zero_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P12_auipc_load_pseudo_rs2_zero_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P13_auipc_to_ALU_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P13_auipc_to_ALU_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P13_auipc_to_ALU_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P14_auipc_to_ALU_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P14_auipc_to_ALU_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P14_auipc_to_ALU_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P15_auipc_to_ALU_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P15_auipc_to_ALU_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P15_auipc_to_ALU_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P16_auipc_to_STORE_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P16_auipc_to_STORE_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P16_auipc_to_STORE_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P17_auipc_to_STORE_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P17_auipc_to_STORE_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P17_auipc_to_STORE_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P18_auipc_to_STORE_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P18_auipc_to_STORE_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P18_auipc_to_STORE_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P19_auipc_rd_x0_load_x0_exclusion", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P19_auipc_rd_x0_load_x0_exclusion"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P19_auipc_rd_x0_load_x0_exclusion", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P20_auipc_repeat_rd_latest_priority", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P20_auipc_repeat_rd_latest_priority"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P20_auipc_repeat_rd_latest_priority", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P21_auipc_taken_branch_squash_clear_flag", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P21_auipc_taken_branch_squash_clear_flag"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P21_auipc_taken_branch_squash_clear_flag", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P22_auipc_JALR_target_link", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P22_auipc_JALR_target_link"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P22_auipc_JALR_target_link", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P23_auipc_PC_relative_LW_SW", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P23_auipc_PC_relative_LW_SW"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P23_auipc_PC_relative_LW_SW", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P24_auipc_after_real_load_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P24_auipc_after_real_load_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P24_auipc_after_real_load_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P25_auipc_negative_U_plus_LUI_cancel", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P25_auipc_negative_U_plus_LUI_cancel"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P25_auipc_negative_U_plus_LUI_cancel", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-base.vvp", "+case=P26_auipc_nonzero_PC_U0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/P26_auipc_nonzero_PC_U0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\P26_auipc_nonzero_PC_U0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D01_lbu_four_lanes", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D01_lbu_four_lanes"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D01_lbu_four_lanes", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D02_lbu_zero_ff_signbit", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D02_lbu_zero_ff_signbit"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D02_lbu_zero_ff_signbit", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D03_lbu_ram_last_bytes", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D03_lbu_ram_last_bytes"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D03_lbu_ram_last_bytes", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D04_lbu_negative_offsets", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D04_lbu_negative_offsets"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D04_lbu_negative_offsets", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D05_lbu_positive_high_offset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D05_lbu_positive_high_offset"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D05_lbu_positive_high_offset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D06_lbu_base_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D06_lbu_base_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D06_lbu_base_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D07_lbu_base_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D07_lbu_base_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D07_lbu_base_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D08_lbu_base_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D08_lbu_base_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D08_lbu_base_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D09_lbu_to_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D09_lbu_to_alu"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D09_lbu_to_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D10_lbu_to_store_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D10_lbu_to_store_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D10_lbu_to_store_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D11_lbu_to_store_address", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D11_lbu_to_store_address"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D11_lbu_to_store_address", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D12_lw_to_lbu_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D12_lw_to_lbu_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D12_lw_to_lbu_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D13_lbu_pseudo_rs2_no_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D13_lbu_pseudo_rs2_no_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D13_lbu_pseudo_rs2_no_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D14_lbu_x0_loads_observed", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D14_lbu_x0_loads_observed"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D14_lbu_x0_loads_observed", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D15_lbu_rd_equals_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D15_lbu_rd_equals_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D15_lbu_rd_equals_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D16_lbu_latest_base_producer", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D16_lbu_latest_base_producer"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D16_lbu_latest_base_producer", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D17_lbu_to_lbu_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D17_lbu_to_lbu_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D17_lbu_to_lbu_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D18_lbu_unsigned_branch_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D18_lbu_unsigned_branch_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D18_lbu_unsigned_branch_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D19_lbu_taken_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D19_lbu_taken_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D19_lbu_taken_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D20_lbu_jal_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D20_lbu_jal_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D20_lbu_jal_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D21_lbu_after_word_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D21_lbu_after_word_store"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D21_lbu_after_word_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D22_lbu_loop_repeat_read_and_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D22_lbu_loop_repeat_read_and_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D22_lbu_loop_repeat_read_and_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D23_lbu_load_blocks_older_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D23_lbu_load_blocks_older_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D23_lbu_load_blocks_older_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lbu.vvp", "+case=D24_lbu_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/D24_lbu_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\D24_lbu_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E01_lb_four_lanes", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E01_lb_four_lanes"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E01_lb_four_lanes", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E02_lb_zero_ff_signbit", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E02_lb_zero_ff_signbit"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E02_lb_zero_ff_signbit", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E03_lb_lbu_same_bytes", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E03_lb_lbu_same_bytes"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E03_lb_lbu_same_bytes", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E04_lb_negative_offsets", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E04_lb_negative_offsets"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E04_lb_negative_offsets", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E05_lb_last_byte_high_offset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E05_lb_last_byte_high_offset"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E05_lb_last_byte_high_offset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E06_lb_base_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E06_lb_base_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E06_lb_base_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E07_lb_base_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E07_lb_base_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E07_lb_base_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E08_lb_base_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E08_lb_base_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E08_lb_base_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E09_lb_to_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E09_lb_to_alu"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E09_lb_to_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E10_lb_to_store_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E10_lb_to_store_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E10_lb_to_store_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E11_lb_to_store_address", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E11_lb_to_store_address"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E11_lb_to_store_address", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E12_lw_to_lb_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E12_lw_to_lb_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E12_lw_to_lb_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E13_lb_pseudo_rs2_no_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E13_lb_pseudo_rs2_no_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E13_lb_pseudo_rs2_no_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E14_lb_x0_loads_observed", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E14_lb_x0_loads_observed"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E14_lb_x0_loads_observed", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E15_lb_rd_equals_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E15_lb_rd_equals_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E15_lb_rd_equals_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E16_lb_latest_base_producer", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E16_lb_latest_base_producer"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E16_lb_latest_base_producer", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E17_lb_to_lb_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E17_lb_to_lb_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E17_lb_to_lb_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E18_lb_negative_branch_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E18_lb_negative_branch_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E18_lb_negative_branch_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E19_lb_negative_branch_rs2_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E19_lb_negative_branch_rs2_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E19_lb_negative_branch_rs2_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E20_lb_jal_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E20_lb_jal_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E20_lb_jal_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E21_lb_after_word_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E21_lb_after_word_store"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E21_lb_after_word_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E22_lb_loop_repeat_read_and_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E22_lb_loop_repeat_read_and_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E22_lb_loop_repeat_read_and_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E23_lb_load_blocks_older_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E23_lb_load_blocks_older_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E23_lb_load_blocks_older_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lb.vvp", "+case=E24_lb_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/E24_lb_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\E24_lb_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q01_lhu_two_halves", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q01_lhu_two_halves"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q01_lhu_two_halves", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q02_lhu_unsigned_boundaries", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q02_lhu_unsigned_boundaries"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q02_lhu_unsigned_boundaries", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q03_lhu_existing_loads", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q03_lhu_existing_loads"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q03_lhu_existing_loads", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q04_lhu_negative_offsets", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q04_lhu_negative_offsets"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q04_lhu_negative_offsets", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q05_lhu_last_aligned_half", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q05_lhu_last_aligned_half"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q05_lhu_last_aligned_half", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q06_lhu_base_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q06_lhu_base_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q06_lhu_base_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q07_lhu_base_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q07_lhu_base_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q07_lhu_base_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q08_lhu_base_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q08_lhu_base_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q08_lhu_base_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q09_lhu_to_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q09_lhu_to_alu"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q09_lhu_to_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q10_lhu_to_store_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q10_lhu_to_store_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q10_lhu_to_store_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q11_lhu_to_store_address", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q11_lhu_to_store_address"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q11_lhu_to_store_address", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q12_lw_to_lhu_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q12_lw_to_lhu_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q12_lw_to_lhu_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q13_lhu_pseudo_rs2_no_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q13_lhu_pseudo_rs2_no_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q13_lhu_pseudo_rs2_no_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q14_lhu_x0_loads_observed", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q14_lhu_x0_loads_observed"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q14_lhu_x0_loads_observed", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q15_lhu_rd_equals_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q15_lhu_rd_equals_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q15_lhu_rd_equals_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q16_lhu_latest_base_producer", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q16_lhu_latest_base_producer"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q16_lhu_latest_base_producer", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q17_lhu_to_lhu_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q17_lhu_to_lhu_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q17_lhu_to_lhu_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q18_lhu_signed_branch_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q18_lhu_signed_branch_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q18_lhu_signed_branch_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q19_lhu_taken_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q19_lhu_taken_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q19_lhu_taken_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q20_lhu_jal_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q20_lhu_jal_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q20_lhu_jal_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q21_lhu_after_word_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q21_lhu_after_word_store"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q21_lhu_after_word_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q22_lhu_loop_repeat_read_and_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q22_lhu_loop_repeat_read_and_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q22_lhu_loop_repeat_read_and_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q23_lhu_load_blocks_older_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q23_lhu_load_blocks_older_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q23_lhu_load_blocks_older_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lhu.vvp", "+case=Q24_lhu_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Q24_lhu_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Q24_lhu_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y01_lh_two_halves", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y01_lh_two_halves"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y01_lh_two_halves", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y02_lh_signed_boundaries", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y02_lh_signed_boundaries"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y02_lh_signed_boundaries", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y03_lh_lhu_existing_loads", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y03_lh_lhu_existing_loads"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y03_lh_lhu_existing_loads", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y04_lh_negative_offsets", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y04_lh_negative_offsets"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y04_lh_negative_offsets", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y05_lh_last_aligned_half", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y05_lh_last_aligned_half"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y05_lh_last_aligned_half", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y06_lh_base_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y06_lh_base_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y06_lh_base_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y07_lh_base_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y07_lh_base_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y07_lh_base_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y08_lh_base_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y08_lh_base_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y08_lh_base_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y09_lh_to_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y09_lh_to_alu"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y09_lh_to_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y10_lh_to_store_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y10_lh_to_store_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y10_lh_to_store_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y11_lh_to_store_address", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y11_lh_to_store_address"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y11_lh_to_store_address", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y12_lw_to_lh_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y12_lw_to_lh_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y12_lw_to_lh_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y13_lh_pseudo_rs2_no_stall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y13_lh_pseudo_rs2_no_stall"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y13_lh_pseudo_rs2_no_stall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y14_lh_x0_loads_observed", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y14_lh_x0_loads_observed"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y14_lh_x0_loads_observed", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y15_lh_rd_equals_negative_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y15_lh_rd_equals_negative_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y15_lh_rd_equals_negative_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y16_lh_latest_base_producer", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y16_lh_latest_base_producer"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y16_lh_latest_base_producer", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y17_lh_to_lh_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y17_lh_to_lh_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y17_lh_to_lh_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y18_lh_signed_branch_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y18_lh_signed_branch_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y18_lh_signed_branch_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y19_lh_branch_rs2_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y19_lh_branch_rs2_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y19_lh_branch_rs2_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y20_lh_jal_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y20_lh_jal_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y20_lh_jal_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y21_lh_after_word_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y21_lh_after_word_store"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y21_lh_after_word_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y22_lh_loop_repeat_read_and_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y22_lh_loop_repeat_read_and_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y22_lh_loop_repeat_read_and_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y23_lh_load_blocks_older_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y23_lh_load_blocks_older_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y23_lh_load_blocks_older_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-lh.vvp", "+case=Y24_lh_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/Y24_lh_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\Y24_lh_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S01_sb_four_lanes", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S01_sb_four_lanes"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S01_sb_four_lanes", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S02_sb_byte_patterns", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S02_sb_byte_patterns"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S02_sb_byte_patterns", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S03_sb_discard_upper24", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S03_sb_discard_upper24"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S03_sb_discard_upper24", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S04_sb_signed_offsets", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S04_sb_signed_offsets"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S04_sb_signed_offsets", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S05_sb_last_byte", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S05_sb_last_byte"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S05_sb_last_byte", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S06_sb_base_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S06_sb_base_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S06_sb_base_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S07_sb_base_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S07_sb_base_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S07_sb_base_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S08_sb_base_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S08_sb_base_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S08_sb_base_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S09_sb_data_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S09_sb_data_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S09_sb_data_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S10_sb_data_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S10_sb_data_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S10_sb_data_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S11_sb_data_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S11_sb_data_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S11_sb_data_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S12_sb_latest_same_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S12_sb_latest_same_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S12_sb_latest_same_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S13_sb_load_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S13_sb_load_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S13_sb_load_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S14_sb_load_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S14_sb_load_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S14_sb_load_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S15_sb_load_both_sources", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S15_sb_load_both_sources"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S15_sb_load_both_sources", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S16_sb_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S16_sb_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S16_sb_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S17_sb_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S17_sb_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S17_sb_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S18_sb_pseudo_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S18_sb_pseudo_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S18_sb_pseudo_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S19_sb_then_all_load_widths", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S19_sb_then_all_load_widths"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S19_sb_then_all_load_widths", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S20_sb_sw_order", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S20_sb_sw_order"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S20_sb_sw_order", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S21_sb_repeat_same_write", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S21_sb_repeat_same_write"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S21_sb_repeat_same_write", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S22_sb_loop_repeat", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S22_sb_loop_repeat"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S22_sb_loop_repeat", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S23_sb_taken_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S23_sb_taken_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S23_sb_taken_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S24_sb_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S24_sb_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S24_sb_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S25_sb_jal_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S25_sb_jal_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S25_sb_jal_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S26_sb_jalr_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S26_sb_jalr_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S26_sb_jalr_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S27_sb_new_load_over_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S27_sb_new_load_over_old_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S27_sb_new_load_over_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S28_sw_only_control", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S28_sw_only_control"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S28_sw_only_control", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S29_sb_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S29_sb_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S29_sb_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sb.vvp", "+case=S30_sb_negative_load_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/S30_sb_negative_load_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\S30_sb_negative_load_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H01_sh_two_lanes", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H01_sh_two_lanes"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H01_sh_two_lanes", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H02_sh_half_patterns", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H02_sh_half_patterns"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H02_sh_half_patterns", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H03_sh_discard_upper16", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H03_sh_discard_upper16"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H03_sh_discard_upper16", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H04_sh_signed_offsets", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H04_sh_signed_offsets"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H04_sh_signed_offsets", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H05_sh_last_half", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H05_sh_last_half"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H05_sh_last_half", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H06_sh_base_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H06_sh_base_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H06_sh_base_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H07_sh_base_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H07_sh_base_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H07_sh_base_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H08_sh_base_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H08_sh_base_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H08_sh_base_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H09_sh_data_EX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H09_sh_data_EX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H09_sh_data_EX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H10_sh_data_WBEX", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H10_sh_data_WBEX"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H10_sh_data_WBEX", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H11_sh_data_WBID", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H11_sh_data_WBID"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H11_sh_data_WBID", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H12_sh_latest_same_source", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H12_sh_latest_same_source"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H12_sh_latest_same_source", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H13_sh_load_base", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H13_sh_load_base"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H13_sh_load_base", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H14_sh_load_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H14_sh_load_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H14_sh_load_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H15_sh_load_both_sources", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H15_sh_load_both_sources"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H15_sh_load_both_sources", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H16_sh_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H16_sh_load_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H16_sh_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H17_sh_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H17_sh_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H17_sh_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H18_sh_pseudo_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H18_sh_pseudo_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H18_sh_pseudo_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H19_sh_then_all_load_widths", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H19_sh_then_all_load_widths"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H19_sh_then_all_load_widths", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H20_sh_sb_sw_order", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H20_sh_sb_sw_order"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H20_sh_sb_sw_order", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H21_sh_repeat_same_write", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H21_sh_repeat_same_write"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H21_sh_repeat_same_write", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H22_sh_loop_repeat", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H22_sh_loop_repeat"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H22_sh_loop_repeat", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H23_sh_taken_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H23_sh_taken_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H23_sh_taken_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H24_sh_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H24_sh_not_taken"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H24_sh_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H25_sh_jal_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H25_sh_jal_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H25_sh_jal_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H26_sh_jalr_squash", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H26_sh_jalr_squash"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H26_sh_jalr_squash", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H27_sh_new_load_over_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H27_sh_new_load_over_old_wb"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H27_sh_new_load_over_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H28_sb_sw_control", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H28_sb_sw_control"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H28_sb_sw_control", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H29_sh_zero_coincidence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H29_sh_zero_coincidence"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H29_sh_zero_coincidence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-sh.vvp", "+case=H30_sh_negative_load_data", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/H30_sh_negative_load_data"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\H30_sh_negative_load_data", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC01_sw_f_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC01_sw_f_lw"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC01_sw_f_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC02_sb_loads", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC02_sb_loads"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC02_sb_loads", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC03_sh_loads", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC03_sh_loads"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC03_sh_loads", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC04_read_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC04_read_x0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC04_read_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC05_read_write", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC05_read_write"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC05_read_write", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC06_write_write", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC06_write_write"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC06_write_write", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC07_ignored_rs1_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC07_ignored_rs1_rd"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC07_ignored_rs1_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC08_fake_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC08_fake_rs2"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC08_fake_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC09_two_fences", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC09_two_fences"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC09_two_fences", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC10_empty_pred", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC10_empty_pred"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC10_empty_pred", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC10_empty_succ", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC10_empty_succ"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC10_empty_succ", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC10_iorw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC10_iorw"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC10_iorw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC11_tso", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC11_tso"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC11_tso", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC11_reserved_fm", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC11_reserved_fm"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC11_reserved_fm", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC11_pause_hint", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC11_pause_hint"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC11_pause_hint", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC12_same_pc_loop", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC12_same_pc_loop"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC12_same_pc_loop", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-fence.vvp", "+case=FC13_wrongpath_flush", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/FC13_wrongpath_flush"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\FC13_wrongpath_flush", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE01_ecall_pc0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE01_ecall_pc0", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE01_ecall_pc0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE02_ebreak_nonzero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE02_ebreak_nonzero", "+stop_kind=2", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE02_ebreak_nonzero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE03_two_old_wb", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE04_old_sw", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE05_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE05_sb", "+stop_kind=2", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE05_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE05_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE05_sh", "+stop_kind=2", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE05_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE06_old_lw", "+stop_kind=1", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE06_old_lb", "+stop_kind=1", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE06_old_lbu", "+stop_kind=1", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE06_old_lh", "+stop_kind=1", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE06_old_lhu", "+stop_kind=1", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE07_load_x0_1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE07_load_x0_1", "+stop_kind=1", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE07_load_x0_1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE07_load_x0_2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE07_load_x0_2", "+stop_kind=2", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE07_load_x0_2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE08_young_load", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE08_young_store", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE08_young_jump", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE10_jal", "+stop_kind=2", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE10_jalr", "+stop_kind=1", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE11_not_taken", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE12_load_use", "+stop_kind=2", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE13_first_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE13_first_ecall", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE13_first_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE13_first_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE13_first_ebreak", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE13_first_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE14_fence", "+stop_kind=1", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE16_neighbor_rd", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE16_neighbor_rd", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE16_neighbor_rd", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE16_neighbor_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE16_neighbor_rs1", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE16_neighbor_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE16_neighbor_imm", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE16_neighbor_imm", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE16_neighbor_imm", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE16_neighbor_csr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE16_neighbor_csr", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE16_neighbor_csr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE16_neighbor_mret", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE16_neighbor_mret", "+stop_kind=1", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE16_neighbor_mret", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-eei.vvp", "+case=EE17_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/EE17_reset", "+stop_kind=2", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\EE17_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF01_zero_pc0_migration", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF01_zero_pc0_migration", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF01_zero_pc0_migration", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF02_nonzero_pc", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF02_nonzero_pc", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF02_nonzero_pc", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF03_two_old_wb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF04_old_sw", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF05_old_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF05_old_sb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF05_old_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF05_old_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF05_old_sh", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF05_old_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF06_old_lb", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF06_old_lbu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF06_old_lh", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF06_old_lhu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF07_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF07_load_x0", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF07_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF08_young_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF08_young_alu", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF08_young_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF08_young_load", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF08_young_jump", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF10_jal", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF10_jalr", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF11_not_taken", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF13_first_zero_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF13_first_zero_ecall", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF13_first_zero_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF13_first_zero_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF13_first_zero_ebreak", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF13_first_zero_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF13_first_zero_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF13_first_zero_zero", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF13_first_zero_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF13_first_ecall_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF13_first_ecall_zero", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF13_first_ecall_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF13_first_ebreak_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF13_first_ebreak_zero", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF13_first_ebreak_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF14_fence", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF15_nonzero_bit16", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF15_nonzero_bit16", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF15_nonzero_bit16", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF15_nonzero_bit0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF15_nonzero_bit0", "+stop_kind=2", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF15_nonzero_bit0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-zero.vvp", "+case=ZF16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/ZF16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\ZF16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_7_f7_0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_7_f7_0", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_7_f7_0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_7_f7_1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_7_f7_1", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_7_f7_1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_7_f7_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_7_f7_32", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_7_f7_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_7_f7_127", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_7_f7_127", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_7_f7_127", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_6_f7_0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_6_f7_0", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_6_f7_0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_6_f7_1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_6_f7_1", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_6_f7_1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_6_f7_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_6_f7_32", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_6_f7_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_6_f7_127", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_6_f7_127", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_6_f7_127", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_4_f7_0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_4_f7_0", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_4_f7_0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_4_f7_1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_4_f7_1", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_4_f7_1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_4_f7_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_4_f7_32", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_4_f7_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_4_f7_127", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_4_f7_127", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_4_f7_127", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_1_f7_0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_1_f7_0", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_1_f7_0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_1_f7_1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_1_f7_1", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_1_f7_1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_1_f7_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_1_f7_32", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_1_f7_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF01_f3_1_f7_127", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF01_f3_1_f7_127", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF01_f3_1_f7_127", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF02_pc0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF02_pc0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF02_pc0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF03_two_old_wb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF04_old_sw", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF05_old_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF05_old_sb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF05_old_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF05_old_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF05_old_sh", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF05_old_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF06_old_lb", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF06_old_lbu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF06_old_lh", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF06_old_lhu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF07_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF07_load_x0", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF07_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF08_young_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF08_young_alu", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF08_young_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF08_young_load", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF08_young_jump", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF10_jal", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF10_jalr", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF11_not_taken", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF13_first_r4_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF13_first_r4_ecall", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF13_first_r4_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF13_first_r4_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF13_first_r4_ebreak", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF13_first_r4_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF13_first_r4_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF13_first_r4_zero", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF13_first_r4_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF13_first_zero_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF13_first_zero_r4", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF13_first_zero_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF13_first_ecall_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF13_first_ecall_r4", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF13_first_ecall_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF13_first_ebreak_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF13_first_ebreak_r4", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF13_first_ebreak_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF14_fence", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF15_rd_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF15_rd_x0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF15_rd_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF15_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF15_load_rs2", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF15_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-r4.vvp", "+case=RF16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RF16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RF16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_0_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_0_equal_one", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_0_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_0_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_0_signed_boundary", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_0_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_1_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_1_equal_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_1_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_1_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_1_signed_boundary", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_1_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_32_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_32_equal_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_32_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_32_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_32_signed_boundary", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_32_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_127_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_127_equal_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_127_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_2_f7_127_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_2_f7_127_signed_boundary", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_2_f7_127_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_0_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_0_equal_one", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_0_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_0_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_0_signed_boundary", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_0_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_1_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_1_equal_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_1_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_1_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_1_signed_boundary", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_1_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_32_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_32_equal_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_32_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_32_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_32_signed_boundary", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_32_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_127_equal_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_127_equal_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_127_equal_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC01_f3_3_f7_127_signed_boundary", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC01_f3_3_f7_127_signed_boundary", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC01_f3_3_f7_127_signed_boundary", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC02_pc0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC02_pc0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC02_pc0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC03_two_old_wb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC04_old_sw", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC05_old_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC05_old_sb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC05_old_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC05_old_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC05_old_sh", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC05_old_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC06_old_lb", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC06_old_lbu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC06_old_lh", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC06_old_lhu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC07_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC07_load_x0", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC07_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC08_young_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC08_young_alu", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC08_young_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC08_young_load", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC08_young_jump", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC10_jal", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC10_jalr", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC11_not_taken", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC13_first_r4_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC13_first_r4_ecall", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC13_first_r4_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC13_first_r4_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC13_first_r4_ebreak", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC13_first_r4_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC13_first_r4_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC13_first_r4_zero", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC13_first_r4_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC13_first_zero_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC13_first_zero_r4", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC13_first_zero_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC13_first_ecall_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC13_first_ecall_r4", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC13_first_ecall_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC13_first_ebreak_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC13_first_ebreak_r4", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC13_first_ebreak_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC14_fence", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC15_rd_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC15_rd_x0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC15_rd_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC15_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC15_load_rs2", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC15_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC17_first_R4_RCMP", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC17_first_R4_RCMP", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC17_first_R4_RCMP", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rcmp.vvp", "+case=RC17_first_RCMP_R4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RC17_first_RCMP_R4", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RC17_first_RCMP_R4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_000_small", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_000_small", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_000_small", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_000_wrap", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_000_wrap", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_000_wrap", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_000_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_000_zero", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_000_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_032_small", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_032_small", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_032_small", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_032_wrap", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_032_wrap", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_032_wrap", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_032_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_032_zero", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_032_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_001_small", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_001_small", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_001_small", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_001_wrap", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_001_wrap", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_001_wrap", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_001_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_001_zero", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_001_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_127_small", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_127_small", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_127_small", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_127_wrap", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_127_wrap", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_127_wrap", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS01_f7_127_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS01_f7_127_zero", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS01_f7_127_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS02_pc0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS02_pc0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS02_pc0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS03_two_old_wb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS04_old_sw", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS05_old_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS05_old_sb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS05_old_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS05_old_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS05_old_sh", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS05_old_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS06_old_lb", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS06_old_lbu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS06_old_lh", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS06_old_lhu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS07_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS07_load_x0", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS07_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS08_young_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS08_young_alu", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS08_young_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS08_young_load", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS08_young_jump", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS10_jal", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS10_jalr", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS11_not_taken", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS13_first_r4_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS13_first_r4_ecall", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS13_first_r4_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS13_first_r4_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS13_first_r4_ebreak", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS13_first_r4_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS13_first_r4_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS13_first_r4_zero", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS13_first_r4_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS13_first_zero_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS13_first_zero_r4", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS13_first_zero_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS13_first_ecall_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS13_first_ecall_r4", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS13_first_ecall_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS13_first_ebreak_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS13_first_ebreak_r4", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS13_first_ebreak_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS14_fence", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS15_rd_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS15_rd_x0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS15_rd_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS15_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS15_load_rs2", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS15_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS17_first_R4_AS", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS17_first_R4_AS", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS17_first_R4_AS", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-addsub.vvp", "+case=AS17_first_AS_R4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/AS17_first_AS_R4", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\AS17_first_AS_R4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_000_negative_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_000_negative_one", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_000_negative_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_000_ones_31", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_000_ones_31", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_000_ones_31", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_000_mask_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_000_mask_32", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_000_mask_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_000_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_000_zero", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_000_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_032_negative_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_032_negative_one", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_032_negative_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_032_ones_31", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_032_ones_31", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_032_ones_31", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_032_mask_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_032_mask_32", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_032_mask_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_032_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_032_zero", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_032_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_001_negative_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_001_negative_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_001_negative_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_001_ones_31", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_001_ones_31", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_001_ones_31", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_001_mask_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_001_mask_32", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_001_mask_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_001_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_001_zero", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_001_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_127_negative_one", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_127_negative_one", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_127_negative_one", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_127_ones_31", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_127_ones_31", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_127_ones_31", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_127_mask_32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_127_mask_32", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_127_mask_32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS01_f7_127_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS01_f7_127_zero", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS01_f7_127_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS02_pc0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS02_pc0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS02_pc0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS03_two_old_wb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS04_old_sw", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS05_old_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS05_old_sb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS05_old_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS05_old_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS05_old_sh", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS05_old_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS06_old_lb", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS06_old_lbu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS06_old_lh", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS06_old_lhu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS07_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS07_load_x0", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS07_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS08_young_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS08_young_alu", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS08_young_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS08_young_load", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS08_young_jump", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS10_jal", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS10_jalr", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS11_not_taken", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS13_first_r4_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS13_first_r4_ecall", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS13_first_r4_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS13_first_r4_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS13_first_r4_ebreak", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS13_first_r4_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS13_first_r4_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS13_first_r4_zero", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS13_first_r4_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS13_first_zero_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS13_first_zero_r4", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS13_first_zero_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS13_first_ecall_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS13_first_ecall_r4", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS13_first_ecall_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS13_first_ebreak_r4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS13_first_ebreak_r4", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS13_first_ebreak_r4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS14_fence", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS15_rd_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS15_rd_x0", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS15_rd_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS15_load_rs2", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS15_load_rs2", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS15_load_rs2", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS17_first_R4_RS", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS17_first_R4_RS", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS17_first_R4_RS", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=RS17_first_RS_R4", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/RS17_first_RS_R4", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\RS17_first_RS_R4", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP01_zero_pc0_migration", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP01_zero_pc0_migration", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP01_zero_pc0_migration", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP02_nonzero_pc", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP02_nonzero_pc", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP02_nonzero_pc", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP03_two_old_wb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP04_old_sw", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP05_old_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP05_old_sb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP05_old_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP05_old_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP05_old_sh", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP05_old_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP06_old_lb", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP06_old_lbu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP06_old_lh", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP06_old_lhu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP07_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP07_load_x0", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP07_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP08_young_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP08_young_alu", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP08_young_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP08_young_load", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP08_young_jump", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP10_jal", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP10_jalr", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP11_not_taken", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP13_first_zero_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP13_first_zero_ecall", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP13_first_zero_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP13_first_zero_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP13_first_zero_ebreak", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP13_first_zero_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP13_first_zero_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP13_first_zero_zero", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP13_first_zero_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP13_first_ecall_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP13_first_ecall_zero", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP13_first_ecall_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP13_first_ebreak_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP13_first_ebreak_zero", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP13_first_ebreak_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP14_fence", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IM01_bit16_context", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IM01_bit16_context", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IM01_bit16_context", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IM02_high_sign", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IM02_high_sign", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IM02_high_sign", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IM03_high_ones", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IM03_high_ones", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IM03_high_ones", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IM04_all_ones", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IM04_all_ones", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IM04_all_ones", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IM05_zero_control", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IM05_zero_control", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IM05_zero_control", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IM06_NOP_control", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IM06_NOP_control", "+stop_kind=3", "+stop_pc=14"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IM06_NOP_control", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IM07_wrongpath_pair", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IM07_wrongpath_pair", "+stop_kind=3", "+stop_pc=1c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IM07_wrongpath_pair", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP_PC0_00010000", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP_PC0_00010000", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP_PC0_00010000", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP_PC0_80000000", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP_PC0_80000000", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP_PC0_80000000", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=IP_PC0_ffff0000", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/IP_PC0_ffff0000", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\IP_PC0_ffff0000", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI01_zero_pc0_migration", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI01_zero_pc0_migration", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI01_zero_pc0_migration", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI02_nonzero_pc", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI02_nonzero_pc", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI02_nonzero_pc", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI03_two_old_wb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI03_two_old_wb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI03_two_old_wb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI04_old_sw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI04_old_sw", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI04_old_sw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI05_old_sb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI05_old_sb", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI05_old_sb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI05_old_sh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI05_old_sh", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI05_old_sh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI06_old_lb", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI06_old_lb", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI06_old_lb", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI06_old_lbu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI06_old_lbu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI06_old_lbu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI06_old_lh", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI06_old_lh", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI06_old_lh", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI06_old_lhu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI06_old_lhu", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI06_old_lhu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI07_load_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI07_load_x0", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI07_load_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI08_young_alu", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI08_young_alu", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI08_young_alu", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI08_young_load", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI08_young_load", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI08_young_load", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI08_young_jump", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI08_young_jump", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI08_young_jump", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI09_wrongpath_beq", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI09_wrongpath_beq", "+stop_kind=0", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI09_wrongpath_beq", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI10_jal", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI10_jal", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI10_jal", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI10_jalr", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI10_jalr", "+stop_kind=3", "+stop_pc=10"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI10_jalr", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI11_not_taken", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI11_not_taken", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI11_not_taken", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI13_first_zero_ecall", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI13_first_zero_ecall", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI13_first_zero_ecall", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI13_first_zero_ebreak", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI13_first_zero_ebreak", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI13_first_zero_ebreak", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI13_first_zero_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI13_first_zero_zero", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI13_first_zero_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI13_first_ecall_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI13_first_ecall_zero", "+stop_kind=1", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI13_first_ecall_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI13_first_ebreak_zero", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI13_first_ebreak_zero", "+stop_kind=2", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI13_first_ebreak_zero", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI14_fence", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI14_fence", "+stop_kind=3", "+stop_pc=c"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI14_fence", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SI16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SI16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SI16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SR_SI01_zero_pc0_migration", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SR_SI01_zero_pc0_migration", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SR_SI01_zero_pc0_migration", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SR_SI06_old_lw", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SR_SI06_old_lw", "+stop_kind=3", "+stop_pc=4"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SR_SI06_old_lw", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SR_SI08_young_store", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SR_SI08_young_store", "+stop_kind=3", "+stop_pc=0"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SR_SI08_young_store", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SR_SI12_load_use", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SR_SI12_load_use", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SR_SI12_load_use", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SR_SI16_reset", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SR_SI16_reset", "+stop_kind=3", "+stop_pc=8", "+reset_check"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SR_SI16_reset", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM01_left_hi1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM01_left_hi1", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM01_left_hi1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM02_left_hi32", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM02_left_hi32", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM02_left_hi32", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM03_left_hi127", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM03_left_hi127", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM03_left_hi127", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM04_right_hi1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM04_right_hi1", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM04_right_hi1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM05_right_hi31", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM05_right_hi31", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM05_right_hi31", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM06_right_hi33", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM06_right_hi33", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM06_right_hi33", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM07_right_hi127", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM07_right_hi127", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM07_right_hi127", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM08_SLLI", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM08_SLLI", "+stop_kind=3", "+stop_pc=14"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM08_SLLI", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM09_SRLI", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM09_SRLI", "+stop_kind=3", "+stop_pc=14"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM09_SRLI", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM10_SRAI", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM10_SRAI", "+stop_kind=3", "+stop_pc=14"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM10_SRAI", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM11_rd_x0", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM11_rd_x0", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM11_rd_x0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM12_real_load_rs1", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM12_real_load_rs1", "+stop_kind=3", "+stop_pc=8"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM12_real_load_rs1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\regression-rshift.vvp", "+case=SM13_wrongpath", "+inputs=D:/A_FPGA_Comp/work/icarus/2026-10-21-cpu-shifti-reject/cases/SM13_wrongpath", "+stop_kind=3", "+stop_pc=18"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\regression\\SM13_wrongpath", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P01.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P01.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P01-sync0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P02.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P02.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P02-sync0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03T.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03T.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P03T-sync0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03N.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03N.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P03N-sync0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P04.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P04.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P04-sync0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P05.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P05.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P05-sync0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P01.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P01.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P01-sync1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P02.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P02.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P02-sync1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03T.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03T.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P03T-sync1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03N.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P03N.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P03N-sync1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P04.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P04.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P04-sync1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P05.program.hex", "+WORDS=256", "+ROM_BYTES=1024", "+RAM_BYTES=256", "+RAM_BASE=256", "+RAM_IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-timing-m0\\inputs\\P05.data.hex", "+MAX_CYCLES=4000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\P05-sync1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-c-boot-m1\\inputs\\smoke.mem32.hex", "+WORDS=144", "+ROM_BYTES=16384", "+RAM_BYTES=16384", "+RAM_BASE=65536", "+MAX_CYCLES=100000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\cboot-sync0", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-c-boot-m1\\inputs\\smoke.mem32.hex", "+WORDS=144", "+ROM_BYTES=16384", "+RAM_BYTES=16384", "+RAM_BASE=65536", "+MAX_CYCLES=100000"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\cboot-sync1", "timeout_seconds": 30}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-coremark-correctness-m1\\performance\\image.hex", "+WORDS=3792", "+ROM_BYTES=32768", "+RAM_BYTES=32768", "+RAM_BASE=65536", "+MAX_CYCLES=2202758"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\performance-sync0", "timeout_seconds": 180}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-coremark-correctness-m1\\performance\\image.hex", "+WORDS=3792", "+ROM_BYTES=32768", "+RAM_BYTES=32768", "+RAM_BASE=65536", "+MAX_CYCLES=2202758"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\performance-sync1", "timeout_seconds": 180}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-0.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-coremark-correctness-m1\\validation\\image.hex", "+WORDS=3794", "+ROM_BYTES=32768", "+RAM_BYTES=32768", "+RAM_BASE=65536", "+MAX_CYCLES=2361578"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\validation-sync0", "timeout_seconds": 180}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\compile\\generic-1.vvp", "+IMAGE=D:\\A_FPGA_Comp\\work\\system\\2026-10-23-coremark-correctness-m1\\validation\\image.hex", "+WORDS=3794", "+ROM_BYTES=32768", "+RAM_BYTES=32768", "+RAM_BASE=65536", "+MAX_CYCLES=2361578"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-23-memory-adapt-m1\\runs\\validation-sync1", "timeout_seconds": 180}
```

