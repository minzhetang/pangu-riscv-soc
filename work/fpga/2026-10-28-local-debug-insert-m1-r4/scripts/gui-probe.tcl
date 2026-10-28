ins_new {D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r4/debug.fic}
ins_set_file -input {D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r4/pre/synthesize/board_top_syn.adf}
ins_add_core 1
ins_set_core -core 0 -data_depth 1024 -clock_edge 1 -multi_windows 0 -enable_sq 0
puts {A_R4_NETS_BEGIN}
ins_list_nets
puts {A_R4_NETS_END}
ins_save {D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r4/debug.fic}
