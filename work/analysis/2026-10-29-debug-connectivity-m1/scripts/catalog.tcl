set a_dir {D:/A_FPGA_Comp/work/analysis/2026-10-29-debug-connectivity-m1}
set a_f [open [file join $a_dir COMMAND_CATALOG.txt] w]
puts $a_f [join [lsort [info commands]] \n]
close $a_f
