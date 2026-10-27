# CoreMark8 software bitstream baseline

Start with SUMMARY, APPROVAL, INIT_RECEIPT, SOURCE_RECEIPTS, SOURCE_CHANGE_SUMMARY, COMMANDS, CONFIGURATION_AUDIT, MEMORY_INIT_AUDIT, TIMING_RESOURCE_AUDIT and WARNINGS_LICENSE_AUDIT. The single PDS call is consumed. A reproduction needs a new independent directory, the pinned F16013 source/8 image, F142 FDC, existing licensed PDS and separately scoped permission. Do not rerun build scripts in this immutable evidence directory or reset its absolute2400-second clock.

The original proposal scope stays unchanged; its previous SHA was UTF8/LF-normalized. Read SCOPE_IDENTITY_CORRECTION in the proposal directory for the actual reviewed CRLF file SHA. This is a metadata erratum, not a different authorized build.

Twelve production files equal F160 bytes. memory_model only excludes M0_VERIFY views and inlines the unchanged new initializer; functional source/source-before remain identical. The raw image is15912 bytes padded to32KiB, RAM32KiB A5, and all1792 retained synthesis INIT fragments were independently computed from raw bytes. No claim of proprietary bitstream decoding or hardware readback.

Git excludes tool/vendor models, generated initializer/large expanded memory source, synthesized/netlist/PDS databases, firmwareELF/bin, native raw logs, sbit/smsk and license details. All full original local evidence is preserved; a Git clone alone does not include these artifacts. Hardware STOP remains even when software generation succeeds. Historical JTAG recognition is separate from this round's zero hardware actions and unverified CPU/ILA run.
