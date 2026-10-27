# One authorized PDS software invocation

D164 scope; existing PDS, ordinary user, separately reviewed external execution. No GCC, Icarus, DUT, hardware server, JTAG or Flash actions. Actual command:

```json
{
  "argv": [
    "D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe",
    "-file",
    "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-board-coremark8-bitstream-m1\\pds\\build.tcl"
  ],
  "cwd": "D:\\A_FPGA_Comp\\work\\fpga\\2026-10-27-board-coremark8-bitstream-m1\\pds",
  "native_rc": 0,
  "timeout_seconds": 1800,
  "wall_seconds": 81.547,
  "PDS_invocations": 1,
  "external_route": "separately approved ordinary-user execution; not Windows administrator",
  "Python": "3.12.14",
  "outputs": "fresh files in new directory checked after PDS exit",
  "hardware": "STOPPED"
}
```

Pipeline: compile, ADS synthesize, dev_map, pnr, report_timing, gen_bit_stream -scbv "High Voltage". Complete native logs are local-only because tools may include license locations/host fields. Public receipts contain only safe parsed fields. Recheck audit_build_v3.py and subordinate JSONs; initial auditors/diagnostic notes remain. Never rerun run_once.py or remove its attempt marker.
