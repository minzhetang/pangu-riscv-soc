# R1 actual commands — historical evidence, do not rerun

All native GUI interactions ran as an ordinary user through separately reviewed tool execution. No administrator or execution-policy override.

Two launches, each same absolute argv (second uses corrected own wrapper; first wrapper is not separately archived, first result retained):

```
D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe
```

Supervisor entry:

```
<existing Python> -B work/fpga/2026-10-28-local-debug-insert-m1-r1/gui_session.py
```

GUI clicks/restore/captures recorded in GUI_ACTIONS.json; typed commands/path in type-adf.json and type-query.json. Actual successful GUI Tcl:

```
ins_set_core -core 0 -data_depth 1024 -clock_edge 1 -multi_windows 0 -enable_sq 0
ins_list_nets
ins_save D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r1/partial.fic
```

No ins_new CLI probe or PDS build in this stage. type-connect.json was prepared but **not executed**: own title lookup failed before sending any characters. It is not proof of a connection.

Host-only preparation and postflight:

```
<existing Python> -B work/fpga/2026-10-28-local-debug-insert-m1-r1/prepare_marked_candidate.py
<existing Python> -B work/fpga/2026-10-28-local-debug-insert-m1-r1/finalize.py
```

Python 3.12 runtime already present; exact runtime location is a local environment detail, not a new installation. Historical GUI helper paths/commands and raw logs remain local. No Icarus/GCC/DUT/hardware actions.
