set m0_dir [file normalize [file dirname [info script]]]
cd $m0_dir
add_design [file join $m0_dir source alu.v]
add_design [file join $m0_dir source control.v]
add_design [file join $m0_dir source cpu.v]
add_design [file join $m0_dir source cycle_counter64.sv]
add_design [file join $m0_dir source gpio_core.v]
add_design [file join $m0_dir source local_regif_txgpio_m1.v]
add_design [file join $m0_dir source memory_model.sv]
add_design [file join $m0_dir source regfile.v]
add_design [file join $m0_dir source soc_data_adapter.sv]
add_design [file join $m0_dir source soc_top.sv]
add_design [file join $m0_dir source uart_tx.v]
add_constraint [file join $m0_dir clock_27mhz.fdc]
set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676
compile -top_module soc_top
synthesize -ads -selected_syn_tool_opt 2
dev_map
pnr
report_timing
