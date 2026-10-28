set h [file normalize [file join [file dirname [info script]] ..]]
ins_set_file -input [file join  ins-input configuration-reference.adf]
ins_add_core 1
ins_set_core -core 0 -data_depth 1024 -clock_edge 1 -multi_windows 0 -enable_sq 0
puts {A_R3_NETS_BEGIN}
ins_list_nets
puts {A_R3_NETS_END}
ins_save [file join  debug.fic]
