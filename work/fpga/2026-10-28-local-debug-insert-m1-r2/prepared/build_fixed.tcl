set project_dir [file normalize [file dirname [info script]]]
cd $project_dir
add_design [file join $project_dir source alu.v]
add_design [file join $project_dir source board_reset_sync.sv]
add_design [file join $project_dir source board_top.sv]
add_design [file join $project_dir source control.v]
add_design [file join $project_dir source cpu.v]
add_design [file join $project_dir source cycle_counter64.sv]
add_design [file join $project_dir source gpio_core.v]
add_design [file join $project_dir source local_regif_txgpio_m1.v]
add_design [file join $project_dir source memory_model.sv]
add_design [file join $project_dir source regfile.v]
add_design [file join $project_dir source soc_data_adapter.sv]
add_design [file join $project_dir source soc_top.sv]
add_design [file join $project_dir source uart_tx.v]
add_constraint [file join $project_dir board_pins.fdc]
add_constraint [file join $project_dir clock_27mhz.fdc]
set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676
compile -top_module board_top
synthesize -ads -selected_syn_tool_opt 2

set f [open [file join $project_dir .. SYNTH_READY.json] w]
puts $f {{"status":"SYNTHESIS_FINISHED_AWAITING_FIC"}}
close $f
set a_wait_count 0
while {![file exists [file join $project_dir .. FIC_READY.json]]} {
    if {[file exists [file join $project_dir .. GUI_ABORT.json]]} {error "A_GUI_ABORT"}
    if {$a_wait_count>=3600} {error "A_FIC_WAIT_DEADLINE"}
    after 200
    incr a_wait_count
}
add_fic [file join $project_dir .. debug.fic]
puts {A_FIC_ATTACHED_BEFORE_MAP}
dev_map
pnr
report_timing
gen_bit_stream -scbv "High Voltage"
