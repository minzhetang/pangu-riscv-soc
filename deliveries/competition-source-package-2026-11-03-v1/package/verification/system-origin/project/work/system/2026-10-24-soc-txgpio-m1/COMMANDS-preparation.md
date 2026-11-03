# 已实际执行的原生命令

六项普通工具链命令＋一次单目标外部仅编译＋一次普通路由单元仿真；不含完整SoC。Python合成/参考/推导与语法测试另有对应JSON，非CPU实跑。

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-gcc.exe", "--version"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build", "timeout_seconds": 20, "returncode": 0, "elapsed_seconds": 0.078}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-gcc.exe", "-march=rv32i", "-mabi=ilp32", "-O2", "-ffreestanding", "-fno-builtin", "-fno-common", "-fno-pie", "-fno-stack-protector", "-fno-unwind-tables", "-fno-asynchronous-unwind-tables", "-mno-relax", "-msmall-data-limit=0", "-Wall", "-Wextra", "-Werror", "-nostdlib", "-nostartfiles", "-Wl,--no-relax", "-Wl,--build-id=none", "-Wl,-T,D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\firmware\\link.ld", "-Wl,-Map,D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\soc.map", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\soc.elf", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\firmware\\start.S", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\firmware\\main.c", "-lgcc"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build", "timeout_seconds": 60, "returncode": 0, "elapsed_seconds": 0.484}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-readelf.exe", "-h", "-A", "-l", "-sW", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\soc.elf"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build", "timeout_seconds": 20, "returncode": 0, "elapsed_seconds": 0.094}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objdump.exe", "-d", "-M", "no-aliases", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\soc.elf"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build", "timeout_seconds": 20, "returncode": 0, "elapsed_seconds": 0.156}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objcopy.exe", "-O", "binary", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\soc.elf", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\soc.bin"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build", "timeout_seconds": 20, "returncode": 0, "elapsed_seconds": 0.078}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-nm.exe", "-u", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\soc.elf"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build", "timeout_seconds": 20, "returncode": 0, "elapsed_seconds": 0.094}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe", "-B", "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "-g2012", "-Wall", "-s", "tb_data_adapter", "-o", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\adapter.vvp", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\source\\soc_data_adapter.sv", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\tests\\tb_data_adapter.sv"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build", "timeout_seconds": 60, "returncode": 0, "elapsed_seconds": 0.093}
```

```json
{"argv": ["D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe", "-N", "-M-", "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl", "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\build\\adapter.vvp"], "cwd": "D:\\A_FPGA_Comp\\work\\system\\2026-10-24-soc-txgpio-m1\\tests\\adapter-run", "timeout_seconds": 30, "returncode": 0, "elapsed_seconds": 0.078}
```

