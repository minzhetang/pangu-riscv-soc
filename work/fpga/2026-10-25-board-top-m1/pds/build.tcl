set m1_dir [file normalize [file dirname [info script]]]
cd $m1_dir
add_design [file join $m1_dir source alu.v]
add_design [file join $m1_dir source board_reset_sync.sv]
add_design [file join $m1_dir source board_top.sv]
add_design [file join $m1_dir source control.v]
add_design [file join $m1_dir source cpu.v]
add_design [file join $m1_dir source cycle_counter64.sv]
add_design [file join $m1_dir source gpio_core.v]
add_design [file join $m1_dir source local_regif_txgpio_m1.v]
add_design [file join $m1_dir source memory_model.sv]
add_design [file join $m1_dir source regfile.v]
add_design [file join $m1_dir source soc_data_adapter.sv]
add_design [file join $m1_dir source soc_top.sv]
add_design [file join $m1_dir source uart_tx.v]
add_constraint [file join $m1_dir board_pins.fdc]
add_constraint [file join $m1_dir clock_27mhz.fdc]
set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676
compile -top_module board_top
synthesize -ads -selected_syn_tool_opt 2
dev_map
pnr
report_timing
