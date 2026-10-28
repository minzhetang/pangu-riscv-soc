set h [file normalize [file join [file dirname [info script]] ..]]
ins_new [file join $h debug.fic]
ins_set_file -input [file join $h pds synthesize board_top_syn.adf]
ins_add_core 1
ins_set_core -core 0 -data_depth 1024 -clock_edge 1 -multi_windows 0 -enable_sq 0
puts {A_R2_NETS_BEGIN}
ins_list_nets
puts {A_R2_NETS_END}
ins_save [file join $h debug.fic]
