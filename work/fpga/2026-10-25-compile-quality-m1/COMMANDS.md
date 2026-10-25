# A-COMPILE-QUALITY-M1 可复现命令与本次执行记录

2026-10-25，D135。原O2不重跑；所有路径为本机证据，不保证干净克隆一键复现。

Python：`C:/Users/tamii/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`；启动使用`-B`。无PATH/安装/系统环境修改。

顺序：stage_coremark.py prepare → build → freeze → compile（固定2目标，非管理员外部许可一次，用完）→ run（普通权限2新DUT）→ audit_uart.py → audit_wave.py → quality_compare.py → finalize_evidence.py。

编译各120s，DUT各600万物理拍/360s，trace/bus/VCD各256MiB；TB显式1ns/1ps、物理37037ps周期。当前无超时/清树/截断，不能据此认证通用runner清理机制。

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-gcc.exe",
    "-march=rv32i",
    "-mabi=ilp32",
    "-O3",
    "-ffreestanding",
    "-fno-builtin",
    "-fno-common",
    "-fno-pie",
    "-fno-stack-protector",
    "-fno-unwind-tables",
    "-fno-asynchronous-unwind-tables",
    "-mno-relax",
    "-msmall-data-limit=0",
    "-Wall",
    "-Wextra",
    "-Werror",
    "-nostdlib",
    "-nostartfiles",
    "-Wl,--no-relax",
    "-Wl,--build-id=none",
    "-Wl,-T,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\firmware\\link.ld",
    "-Wl,-Map,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance\\program.map",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\firmware",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\port",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream",
    "-DTOTAL_DATA_SIZE=2000",
    "-DITERATIONS=1",
    "-DPERFORMANCE_RUN=1",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\firmware\\start.S",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_list_join.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_main.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_matrix.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_state.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_util.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\port\\core_portme.c",
    "-lgcc"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.953,
  "timeout_seconds": 60,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-compile\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-compile\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objcopy.exe",
    "-O",
    "binary",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance\\program.bin"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.125,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-objcopy\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-objcopy\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objdump.exe",
    "-d",
    "-M",
    "no-aliases",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.141,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-objdump\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-objdump\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-readelf.exe",
    "-h",
    "-A",
    "-l",
    "-sW",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.125,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-readelf\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-readelf\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-nm.exe",
    "-u",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.14,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-undefined\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-performance-undefined\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-gcc.exe",
    "-march=rv32i",
    "-mabi=ilp32",
    "-O3",
    "-ffreestanding",
    "-fno-builtin",
    "-fno-common",
    "-fno-pie",
    "-fno-stack-protector",
    "-fno-unwind-tables",
    "-fno-asynchronous-unwind-tables",
    "-mno-relax",
    "-msmall-data-limit=0",
    "-Wall",
    "-Wextra",
    "-Werror",
    "-nostdlib",
    "-nostartfiles",
    "-Wl,--no-relax",
    "-Wl,--build-id=none",
    "-Wl,-T,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\firmware\\link.ld",
    "-Wl,-Map,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation\\program.map",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\firmware",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\port",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream",
    "-DTOTAL_DATA_SIZE=2000",
    "-DITERATIONS=1",
    "-DVALIDATION_RUN=1",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\firmware\\start.S",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_list_join.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_main.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_matrix.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_state.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\upstream\\core_util.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\port\\core_portme.c",
    "-lgcc"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.813,
  "timeout_seconds": 60,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-compile\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-compile\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objcopy.exe",
    "-O",
    "binary",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation\\program.bin"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.109,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-objcopy\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-objcopy\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objdump.exe",
    "-d",
    "-M",
    "no-aliases",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.11,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-objdump\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-objdump\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-readelf.exe",
    "-h",
    "-A",
    "-l",
    "-sW",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.109,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-readelf\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-readelf\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-nm.exe",
    "-u",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 0.109,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-undefined\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\build-validation-undefined\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe",
    "-B",
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "-g2012",
    "-Wall",
    "-DM0_VERIFY",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-24-implementability-m0\\verification",
    "-s",
    "tb_board_coremark",
    "-Ptb_board_coremark.PHASE_ADDR=67584",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\compile\\performance-N234.vvp",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\alu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\control.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\cpu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\gpio_core.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\local_regif_txgpio_m1.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\regfile.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\uart_tx.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\board_reset_sync.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\board_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\cycle_counter64.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\memory_model.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\soc_data_adapter.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\performance-N234\\source\\soc_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\tests\\tb_board_coremark.sv",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_DRM18K_E1.v",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_GRS.v"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 43.313,
  "timeout_seconds": 120,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\compile-performance-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\compile-performance-N234\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe",
    "-B",
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "-g2012",
    "-Wall",
    "-DM0_VERIFY",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-24-implementability-m0\\verification",
    "-s",
    "tb_board_coremark",
    "-Ptb_board_coremark.PHASE_ADDR=67592",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\compile\\validation-N234.vvp",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\alu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\control.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\cpu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\gpio_core.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\local_regif_txgpio_m1.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\regfile.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\uart_tx.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\board_reset_sync.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\board_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\cycle_counter64.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\memory_model.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\soc_data_adapter.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\cases\\validation-N234\\source\\soc_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\tests\\tb_board_coremark.sv",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_DRM18K_E1.v",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_GRS.v"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 43.515,
  "timeout_seconds": 120,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\compile-validation-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\compile-validation-N234\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe",
    "-N",
    "-M-",
    "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\compile\\performance-N234.vvp",
    "+MAX_CYCLES=6000000"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\runs\\performance-N234",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 201.015,
  "timeout_seconds": 360,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\run-performance-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\run-performance-N234\\stderr.log"
}
```

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe",
    "-N",
    "-M-",
    "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\compile\\validation-N234.vvp",
    "+MAX_CYCLES=6000000"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\runs\\validation-N234",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "elapsed_seconds": 209.125,
  "timeout_seconds": 360,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\run-validation-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1\\logs\\run-validation-N234\\stderr.log"
}
```
