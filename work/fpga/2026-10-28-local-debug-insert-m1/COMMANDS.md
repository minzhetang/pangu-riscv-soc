# Actual software-only call and stop

D169 approved scope, ordinary nonadministrator external call separately reviewed. Fixed argv:

```text
D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe -batch D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1/scripts/probe.tcl
cwd: D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1/ins-input
timeout: 60 seconds; per-stream cap: 32MiB
```

First Python wrapper failed at creating a missing log parent before Popen (0 native calls). Original script, counter reservation, traceback route and frozen inputs remain; PREPARATION_ERROR corrects its interface-failure classification. The separate v2 wrapper created only the missing parent and made the first actual native call using identical argv/Tcl/ADF. Native result: guard stopped on UNEXPECTED_GUI_VISIBLE after1.718s, rc1. No Tcl marker completed, no FIC/bitstream/PDS build. Native raw logs local-only; no conclusive fresh license success/expiry is claimed.

No native retry or GUI interaction followed. Root process exited; taskkill rc255 and absent independent descendant enumeration remain explicit. A subsequent ordinary Get-Process filter found zero cdt_ins processes; CIM was denied, not represented as a successful snapshot. No device enumeration/JTAG or hardware commands.

Read SUMMARY, PREPARATION_ERROR, PROBE_RESULT/V2 and logs/inserter-probe-01/process.json. Do not rerun wrappers, reset the absolute stage clock/counters or treat unused build budget as permission to cross GUI boundary.
