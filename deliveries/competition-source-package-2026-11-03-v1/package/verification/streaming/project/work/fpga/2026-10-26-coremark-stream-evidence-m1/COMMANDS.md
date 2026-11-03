# Reproducible commands and native results

D156 business scope; only compile-performance-N234 used the separately reviewed external tool route. All calls nonadministrator; existing tools only. JSON argv arrays are argument lists, not shell strings. Exact local arrays are in COMMANDS-exact-local.json; <EXISTING_PYTHON> denotes the already verified local Python runtime.

## compile-performance-N234

```json
{
  "id": "compile-performance-N234",
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\iverilog.exe",
    "-B",
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "-g2012",
    "-Wall",
    "-DM0_VERIFY",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source",
    "-I",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-24-implementability-m0\\verification",
    "-s",
    "tb_board_coremark",
    "-Ptb_board_coremark.PHASE_ADDR=67584",
    "-o",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\compile\\performance-N234.vvp",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\alu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\control.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\cpu.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\gpio_core.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\local_regif_txgpio_m1.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\regfile.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\uart_tx.v",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\board_reset_sync.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\board_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\cycle_counter64.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\memory_model.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\soc_data_adapter.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\cases\\performance-N234\\source\\soc_top.sv",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\tests\\tb_board_coremark.sv",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_DRM18K_E1.v",
    "D:\\PDS\\PDS_2022.2-SP6.4\\arch\\vendor\\pango\\verilog\\simulation\\GTP_GRS.v"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 5464064,
  "elapsed_seconds": 55.14,
  "timeout_seconds": 120,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\compile-performance-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\compile-performance-N234\\stderr.log"
}
```

## final-functional-check

```json
{
  "id": "final-functional-check",
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\final_check_worker.py"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 229031936,
  "elapsed_seconds": 53.672,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\final-functional-check\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\final-functional-check\\stderr.log"
}
```

## model

```json
{
  "id": "model",
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\host_worker.py",
    "model"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 1,
  "returncode_hex": "0x00000001",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 16773120,
  "elapsed_seconds": 0.109,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\model\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\model\\stderr.log"
}
```

## model-v2

```json
{
  "id": "model-v2",
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\host_worker.py",
    "model"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 19652608,
  "elapsed_seconds": 0.172,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\model-v2\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\model-v2\\stderr.log"
}
```

## pipeline-controls

```json
{
  "id": "pipeline-controls",
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\pipeline_controls.py"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 257560576,
  "elapsed_seconds": 239.11,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\pipeline-controls\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\pipeline-controls\\stderr.log"
}
```

## replay-performance

```json
{
  "id": "replay-performance",
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\host_worker.py",
    "replay",
    "performance"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 1,
  "returncode_hex": "0x00000001",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 251596800,
  "elapsed_seconds": 33.938,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\replay-performance\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\replay-performance\\stderr.log"
}
```

## replay-performance-qualification-v2

```json
{
  "id": "replay-performance-qualification-v2",
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\host_worker.py",
    "qualify-existing"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 59572224,
  "elapsed_seconds": 2.109,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\replay-performance-qualification-v2\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\replay-performance-qualification-v2\\stderr.log"
}
```

## replay-validation

```json
{
  "id": "replay-validation",
  "argv": [
    "<EXISTING_PYTHON>",
    "-B",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\host_worker.py",
    "replay",
    "validation"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 251707392,
  "elapsed_seconds": 35.203,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\replay-validation\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\replay-validation\\stderr.log"
}
```

## run-performance-N234

```json
{
  "id": "run-performance-N234",
  "argv": [
    "D:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\bin\\vvp.exe",
    "-N",
    "-M-",
    "-MD:\\A_FPGA_Comp\\tools\\iverilog-13.0-msys2-ucrt64\\ucrt64\\lib\\ivl",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\compile\\performance-N234.vvp",
    "+MAX_CYCLES=8000000"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\runs\\performance-N234",
  "returncode": 0,
  "returncode_hex": "0x00000000",
  "timed_out": false,
  "cap": false,
  "error": null,
  "termination": "PROCESS_EXIT",
  "peak_working_set_bytes": 60805120,
  "elapsed_seconds": 449.313,
  "timeout_seconds": 600,
  "stdout": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\run-performance-N234\\stdout.log",
  "stderr": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-26-coremark-stream-evidence-m1\\logs\\run-performance-N234\\stderr.log"
}
```

The initial model import and performance replay qualification failures are retained. They are not failed new CPU DUTs or silently rewritten PASS. guarded_entry.py is the required future nonoptimized launch boundary; its status/-O/-OO controls launch no compiler or DUT. Existing attempt/output directories prohibit reruns; use a separately authorized new directory for a reproduction.
