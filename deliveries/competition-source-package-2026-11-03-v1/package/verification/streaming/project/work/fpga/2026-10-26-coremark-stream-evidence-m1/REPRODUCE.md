# Finite stage evidence and reproduction boundaries

Start with SUMMARY.json, TEST_PLAN.json, COMMANDS.md and the report. Historical output/attempt markers are immutable; do not rerun preparation/compile/capture scripts in this directory or remove the markers. Exact source/image/oracle identities are recorded; vendor GTP models remain external from the existing PDS installation and are not redistributed.

The ordinary Python guarded_entry.py status command reads state only. -O/-OO is unsupported and rejected. compile/capture/check actions are single-use and are not an authorization to repeat this completed stage. A new reproduction requires an independent new directory plus the appropriate compile/DUT scope and tool permission. No PATH or system changes are needed.

Git stores reviewed small code/metadata only, not vendor models, VVP, generated initialization, raw 32MiB overbudget fixture, compressed trace payloads, ELF/bin or native VCD. Full local evidence and old immutable inputs remain available; a Git clone alone does not include them.
