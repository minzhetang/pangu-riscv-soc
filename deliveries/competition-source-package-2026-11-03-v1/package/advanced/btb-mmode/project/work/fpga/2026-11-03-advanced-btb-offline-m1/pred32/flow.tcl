set project_dir [file normalize [file dirname [info script]]]
cd $project_dir

add_design [file join $project_dir source alu.v]
add_design [file join $project_dir source board_reset_sync.sv]
add_design [file join $project_dir source board_top_hl4.sv]
add_design [file join $project_dir source btb.v]
add_design [file join $project_dir source control.v]
add_design [file join $project_dir source cpu_hl4.v]
add_design [file join $project_dir source csr_file_hl3.v]
add_design [file join $project_dir source cycle_counter64.sv]
add_design [file join $project_dir source gpio_core.v]
add_design [file join $project_dir source local_regif_hl2.v]
add_design [file join $project_dir source memory_model.sv]
add_design [file join $project_dir source mmu_sv32.v]
add_design [file join $project_dir source pmp.v]
add_design [file join $project_dir source regfile.v]
add_design [file join $project_dir source soc_data_adapter.sv]
add_design [file join $project_dir source soc_top_hl4.sv]
add_design [file join $project_dir source uart_tx.v]

add_constraint [file join $project_dir board_pins.fdc]
add_constraint [file join $project_dir clock_27mhz.fdc]
add_constraint [file join $project_dir closure_io.fdc]

set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676
compile -top_module board_top_hl4
synthesize -ads -selected_syn_tool_opt 2
dev_map
pnr
report_timing
