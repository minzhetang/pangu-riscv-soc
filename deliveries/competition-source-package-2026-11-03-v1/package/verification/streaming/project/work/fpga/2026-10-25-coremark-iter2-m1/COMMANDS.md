# 实际可复查命令与原生结果

每例编译120s、DUT600s/8M拍、每trace/bus/VCD256MiB；现有工具、绝对路径/B/VPI、不改PATH。外部编译仅本批2项、已用完。原生退出后才检查新产物，退出0不是功能证明。完整参数为JSON argv，按数组分词，不把它拼接当shell命令。

GCC build/objcopy/objdump/readelf/nm共10调用；RTL编译2；新DUT2。独立参考旧2校准/新2预计算、1+7纯检查器控制、UART/VCD重审和日志负例均不计DUT。

## build performance

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-gcc.exe",
    "-march=rv32i",
    "-mabi=ilp32",
    "-O2",
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
    "-Wl,-T,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\firmware\\link.ld",
    "-Wl,-Map,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance\\program.map",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\firmware",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\port",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream",
    "-DTOTAL_DATA_SIZE=2000",
    "-DITERATIONS=2",
    "-DPERFORMANCE_RUN=1",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\firmware\\start.S",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_list_join.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_main.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_matrix.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_state.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_util.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\port\\core_portme.c",
    "-lgcc"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.938,
  "timeout_seconds": 60,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-compile\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-compile\\stderr.log"
}
```

## build performance

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objcopy.exe",
    "-O",
    "binary",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance\\program.bin"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.14,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-objcopy\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-objcopy\\stderr.log"
}
```

## build performance

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objdump.exe",
    "-d",
    "-M",
    "no-aliases",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.141,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-objdump\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-objdump\\stderr.log"
}
```

## build performance

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-readelf.exe",
    "-h",
    "-A",
    "-l",
    "-sW",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.125,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-readelf\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-readelf\\stderr.log"
}
```

## build performance

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-nm.exe",
    "-u",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\performance",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.141,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-undefined\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-performance-undefined\\stderr.log"
}
```

## build validation

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-gcc.exe",
    "-march=rv32i",
    "-mabi=ilp32",
    "-O2",
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
    "-Wl,-T,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\firmware\\link.ld",
    "-Wl,-Map,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation\\program.map",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\firmware",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\port",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream",
    "-DTOTAL_DATA_SIZE=2000",
    "-DITERATIONS=2",
    "-DVALIDATION_RUN=1",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\firmware\\start.S",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_list_join.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_main.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_matrix.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_state.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\upstream\\core_util.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\port\\core_portme.c",
    "-lgcc"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.718,
  "timeout_seconds": 60,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-compile\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-compile\\stderr.log"
}
```

## build validation

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objcopy.exe",
    "-O",
    "binary",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation\\program.bin"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.094,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-objcopy\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-objcopy\\stderr.log"
}
```

## build validation

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objdump.exe",
    "-d",
    "-M",
    "no-aliases",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.094,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-objdump\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-objdump\\stderr.log"
}
```

## build validation

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-readelf.exe",
    "-h",
    "-A",
    "-l",
    "-sW",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.109,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-readelf\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-readelf\\stderr.log"
}
```

## build validation

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-nm.exe",
    "-u",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\build\\validation",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 0.109,
  "timeout_seconds": 20,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-undefined\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\build-validation-undefined\\stderr.log"
}
```

## RTL performance-N234

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
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-24-implementability-m0\\verification",
    "-s",
    "tb_board_coremark",
    "-Ptb_board_coremark.PHASE_ADDR=67584",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\compile\\performance-N234.vvp",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\alu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\control.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\cpu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\gpio_core.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\local_regif_txgpio_m1.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\regfile.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\uart_tx.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\board_reset_sync.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\board_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\cycle_counter64.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\memory_model.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\soc_data_adapter.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\performance-N234\\source\\soc_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\tests\\tb_board_coremark.sv",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_DRM18K_E1.v",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_GRS.v"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 44.406,
  "timeout_seconds": 120,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\compile-performance-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\compile-performance-N234\\stderr.log"
}
```

## RTL validation-N234

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
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-24-implementability-m0\\verification",
    "-s",
    "tb_board_coremark",
    "-Ptb_board_coremark.PHASE_ADDR=67592",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\compile\\validation-N234.vvp",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\alu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\control.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\cpu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\gpio_core.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\local_regif_txgpio_m1.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\regfile.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\uart_tx.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\board_reset_sync.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\board_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\cycle_counter64.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\memory_model.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\soc_data_adapter.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\cases\\validation-N234\\source\\soc_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\tests\\tb_board_coremark.sv",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_DRM18K_E1.v",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_GRS.v"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 44.532,
  "timeout_seconds": 120,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\compile-validation-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\compile-validation-N234\\stderr.log"
}
```

## DUT performance-N234

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe",
    "-N",
    "-M-",
    "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\compile\\performance-N234.vvp",
    "+MAX_CYCLES=8000000"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\runs\\performance-N234",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 320.39,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\run-performance-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\run-performance-N234\\stderr.log"
}
```

## DUT validation-N234

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe",
    "-N",
    "-M-",
    "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\compile\\validation-N234.vvp",
    "+MAX_CYCLES=8000000"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\runs\\validation-N234",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "cleanup": null,
  "elapsed_seconds": 357.453,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\run-validation-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-coremark-iter2-m1\\logs\\run-validation-N234\\stderr.log"
}
```
