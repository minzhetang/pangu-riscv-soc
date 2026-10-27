# M2 actual commands and native results

D160 scope, one GNU build plus auxiliary commands, one separately approved external-route Icarus compile, one ordinary vvp DUT. Nonadministrator. JSON argv entries are arguments, not shell expressions. Exact local Python path stays in COMMANDS-exact-local.json, excluded from Git.

## build-compile

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
    "-Wl,-T,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\firmware\\link.ld",
    "-Wl,-Map,D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8\\program.map",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\firmware",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\port",
    "-ID:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\upstream",
    "-DTOTAL_DATA_SIZE=2000",
    "-DITERATIONS=8",
    "-DPERFORMANCE_RUN=1",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\firmware\\start.S",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\upstream\\core_list_join.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\upstream\\core_main.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\upstream\\core_matrix.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\upstream\\core_state.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\upstream\\core_util.c",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\port\\core_portme.c",
    "-lgcc"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 7262208,
  "parent_peak_working_set_bytes": 27926528,
  "child_memory_samples": 31,
  "elapsed_seconds": 1.0,
  "timeout_seconds": 60,
  "child_cpu": {
    "kernel_s": 0.09375,
    "user_s": 0.0
  },
  "parent_cpu_before": {
    "kernel_s": 0.046875,
    "user_s": 0.046875
  },
  "parent_cpu_after": {
    "kernel_s": 0.046875,
    "user_s": 0.046875
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-compile\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-compile\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## build-nm

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-nm.exe",
    "-u",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 2248704,
  "parent_peak_working_set_bytes": 27926528,
  "child_memory_samples": 1,
  "elapsed_seconds": 0.062,
  "timeout_seconds": 20,
  "child_cpu": {
    "kernel_s": 0.015625,
    "user_s": 0.0
  },
  "parent_cpu_before": {
    "kernel_s": 0.0625,
    "user_s": 0.0625
  },
  "parent_cpu_after": {
    "kernel_s": 0.09375,
    "user_s": 0.0625
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-nm\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-nm\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## build-objcopy

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objcopy.exe",
    "-O",
    "binary",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8\\program.elf",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8\\program.bin"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 2248704,
  "parent_peak_working_set_bytes": 27926528,
  "child_memory_samples": 1,
  "elapsed_seconds": 0.062,
  "timeout_seconds": 20,
  "child_cpu": {
    "kernel_s": 0.0,
    "user_s": 0.0
  },
  "parent_cpu_before": {
    "kernel_s": 0.046875,
    "user_s": 0.046875
  },
  "parent_cpu_after": {
    "kernel_s": 0.046875,
    "user_s": 0.046875
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-objcopy\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-objcopy\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## build-objdump

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-objdump.exe",
    "-d",
    "-M",
    "no-aliases",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 2244608,
  "parent_peak_working_set_bytes": 27926528,
  "child_memory_samples": 1,
  "elapsed_seconds": 0.063,
  "timeout_seconds": 20,
  "child_cpu": {
    "kernel_s": 0.0,
    "user_s": 0.0
  },
  "parent_cpu_before": {
    "kernel_s": 0.046875,
    "user_s": 0.046875
  },
  "parent_cpu_after": {
    "kernel_s": 0.046875,
    "user_s": 0.0625
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-objdump\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-objdump\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## build-readelf

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\xpack-riscv-none-elf-gcc-15.2.0-1\\bin\\riscv-none-elf-readelf.exe",
    "-h",
    "-A",
    "-l",
    "-sW",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8\\program.elf"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\build\\performance8",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 2248704,
  "parent_peak_working_set_bytes": 27926528,
  "child_memory_samples": 1,
  "elapsed_seconds": 0.047,
  "timeout_seconds": 20,
  "child_cpu": {
    "kernel_s": 0.015625,
    "user_s": 0.0
  },
  "parent_cpu_before": {
    "kernel_s": 0.046875,
    "user_s": 0.0625
  },
  "parent_cpu_after": {
    "kernel_s": 0.0625,
    "user_s": 0.0625
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-readelf\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\build-readelf\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## compile-performance8

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
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-24-implementability-m0\\verification",
    "-s",
    "tb_board_coremark",
    "-Ptb_board_coremark.PHASE_ADDR=67584",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\compile\\performance8-N234.vvp",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\alu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\control.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\cpu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\gpio_core.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\local_regif_txgpio_m1.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\regfile.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\uart_tx.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\board_reset_sync.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\board_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\cycle_counter64.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\memory_model.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\soc_data_adapter.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\cases\\performance8-N234\\source\\soc_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\tests\\tb_board_coremark.sv",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_DRM18K_E1.v",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_GRS.v"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 5193728,
  "parent_peak_working_set_bytes": 22663168,
  "child_memory_samples": 1475,
  "elapsed_seconds": 46.109,
  "timeout_seconds": 120,
  "child_cpu": {
    "kernel_s": 0.0,
    "user_s": 0.03125
  },
  "parent_cpu_before": {
    "kernel_s": 0.9375,
    "user_s": 0.28125
  },
  "parent_cpu_after": {
    "kernel_s": 1.234375,
    "user_s": 0.484375
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\compile-performance8\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\compile-performance8\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## container-controls

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\container_controls.py"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 45735936,
  "parent_peak_working_set_bytes": 19365888,
  "child_memory_samples": 759,
  "elapsed_seconds": 23.656,
  "timeout_seconds": 900,
  "child_cpu": {
    "kernel_s": 9.84375,
    "user_s": 12.828125
  },
  "parent_cpu_before": {
    "kernel_s": 0.015625,
    "user_s": 0.03125
  },
  "parent_cpu_after": {
    "kernel_s": 0.109375,
    "user_s": 0.09375
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\container-controls\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\container-controls\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## final-functional-performance8

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\final_worker.py"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 231190528,
  "parent_peak_working_set_bytes": 19673088,
  "child_memory_samples": 2399,
  "elapsed_seconds": 74.89,
  "timeout_seconds": 1800,
  "child_cpu": {
    "kernel_s": 2.140625,
    "user_s": 71.140625
  },
  "parent_cpu_before": {
    "kernel_s": 0.03125,
    "user_s": 0.03125
  },
  "parent_cpu_after": {
    "kernel_s": 0.390625,
    "user_s": 0.265625
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\final-functional-performance8\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\final-functional-performance8\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## negative-configured-memory

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "-c",
    "import time;time.sleep(1)"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 1,
  "returncode_hex": "0x00000001",
  "timed_out": false,
  "cap": true,
  "error": "PARENT_MEMORY_CAP",
  "termination": "STOPPED",
  "peak_working_set_bytes": 0,
  "parent_peak_working_set_bytes": 20463616,
  "child_memory_samples": 0,
  "elapsed_seconds": 0.031,
  "timeout_seconds": 2,
  "child_cpu": {
    "kernel_s": 0.0,
    "user_s": 0.0
  },
  "parent_cpu_before": {
    "kernel_s": 0.03125,
    "user_s": 0.03125
  },
  "parent_cpu_after": {
    "kernel_s": 0.03125,
    "user_s": 0.03125
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\negative-configured-memory\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\negative-configured-memory\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## negative-no-memory

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "-c",
    "import time;time.sleep(2)"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 1,
  "returncode_hex": "0x00000001",
  "timed_out": false,
  "cap": false,
  "error": "CHILD_MEMORY_UNAVAILABLE",
  "termination": "STOPPED",
  "peak_working_set_bytes": 0,
  "parent_peak_working_set_bytes": 45735936,
  "child_memory_samples": 0,
  "elapsed_seconds": 0.031,
  "timeout_seconds": 1,
  "child_cpu": {
    "kernel_s": 0.0,
    "user_s": 0.0
  },
  "parent_cpu_before": {
    "kernel_s": 9.8125,
    "user_s": 12.8125
  },
  "parent_cpu_after": {
    "kernel_s": 9.8125,
    "user_s": 12.828125
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\negative-no-memory\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\negative-no-memory\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## negative-parent-deadline

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "-c",
    "import time;time.sleep(2)"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 1,
  "returncode_hex": "0x00000001",
  "timed_out": true,
  "cap": false,
  "error": "ABSOLUTE_DEADLINE",
  "termination": "STOPPED",
  "peak_working_set_bytes": 11010048,
  "parent_peak_working_set_bytes": 45735936,
  "child_memory_samples": 5,
  "elapsed_seconds": 0.156,
  "timeout_seconds": 0.15,
  "child_cpu": {
    "kernel_s": 0.0,
    "user_s": 0.015625
  },
  "parent_cpu_before": {
    "kernel_s": 9.8125,
    "user_s": 12.828125
  },
  "parent_cpu_after": {
    "kernel_s": 9.828125,
    "user_s": 12.828125
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\negative-parent-deadline\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\negative-parent-deadline\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## oracle-performance8

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\oracle.py"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 81182720,
  "parent_peak_working_set_bytes": 19619840,
  "child_memory_samples": 596,
  "elapsed_seconds": 18.625,
  "timeout_seconds": 900,
  "child_cpu": {
    "kernel_s": 0.34375,
    "user_s": 18.09375
  },
  "parent_cpu_before": {
    "kernel_s": 0.015625,
    "user_s": 0.046875
  },
  "parent_cpu_after": {
    "kernel_s": 0.125,
    "user_s": 0.109375
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\oracle-performance8\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\oracle-performance8\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## replay-performance

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\host_worker.py",
    "replay",
    "performance"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 1,
  "returncode_hex": "0x00000001",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 216211456,
  "parent_peak_working_set_bytes": 19652608,
  "child_memory_samples": 339,
  "elapsed_seconds": 10.593,
  "timeout_seconds": 600,
  "child_cpu": {
    "kernel_s": 0.3125,
    "user_s": 9.9375
  },
  "parent_cpu_before": {
    "kernel_s": 0.03125,
    "user_s": 0.015625
  },
  "parent_cpu_after": {
    "kernel_s": 0.203125,
    "user_s": 0.171875
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\replay-performance\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\replay-performance\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## replay-ready-performance

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\host_worker.py",
    "replay",
    "performance"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 253378560,
  "parent_peak_working_set_bytes": 19599360,
  "child_memory_samples": 987,
  "elapsed_seconds": 30.813,
  "timeout_seconds": 600,
  "child_cpu": {
    "kernel_s": 1.359375,
    "user_s": 28.53125
  },
  "parent_cpu_before": {
    "kernel_s": 0.015625,
    "user_s": 0.046875
  },
  "parent_cpu_after": {
    "kernel_s": 0.3125,
    "user_s": 0.234375
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\replay-ready-performance\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\replay-ready-performance\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## replay-ready-validation

```json
{
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\host_worker.py",
    "replay",
    "validation"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 253198336,
  "parent_peak_working_set_bytes": 19644416,
  "child_memory_samples": 1024,
  "elapsed_seconds": 31.984,
  "timeout_seconds": 600,
  "child_cpu": {
    "kernel_s": 1.34375,
    "user_s": 30.03125
  },
  "parent_cpu_before": {
    "kernel_s": 0.3125,
    "user_s": 0.234375
  },
  "parent_cpu_after": {
    "kernel_s": 0.75,
    "user_s": 0.375
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\replay-ready-validation\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\replay-ready-validation\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

## run-performance8-N234

```json
{
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe",
    "-N",
    "-M-",
    "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\compile\\performance8-N234.vvp",
    "+MAX_CYCLES=32000000"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\runs\\performance8-N234",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 60706816,
  "parent_peak_working_set_bytes": 45666304,
  "child_memory_samples": 33866,
  "elapsed_seconds": 1063.828,
  "timeout_seconds": 2400.0,
  "child_cpu": {
    "kernel_s": 23.5625,
    "user_s": 1017.90625
  },
  "parent_cpu_before": {
    "kernel_s": 0.390625,
    "user_s": 0.125
  },
  "parent_cpu_after": {
    "kernel_s": 146.375,
    "user_s": 24.171875
  },
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\run-performance8-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-coremark-longrun-ready-m2\\logs\\run-performance8-N234\\stderr.log",
  "measurement_scope": "direct child and this parent; native compiler internal descendants not separately measured",
  "absolute_deadline_used": true
}
```

Preparation failure replay-performance is retained: missing build-result metadata before the build completed, no CPU/DUT run or failed functional comparison. After dependency readiness replay-ready-* passed. No C/RTL/DUT retry. The extra callback deadline guard rejected correctly but its first auxiliary wrapper used a lowercase error token; original wrapper/fixture retained and independently qualified with the exact uppercase error. Negative controls intentionally reject.
