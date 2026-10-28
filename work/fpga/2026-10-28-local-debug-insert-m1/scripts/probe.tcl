puts {A_INS_PROBE_BEGIN}
foreach name {ins_new ins_set_file ins_list_nets} {
    if {[llength [info commands $name]] == 0} { error "Required command missing: $name" }
}
set root [file normalize [file join [file dirname [info script]] ..]]
ins_new [file join $root ins-input probe.fic]
ins_set_file -input [file join $root ins-input board_top_syn.adf]
puts {A_INS_NETS_BEGIN}
ins_list_nets
puts {A_INS_NETS_END}
puts {A_INS_PROBE_END}
exit 0
