`timescale 1ns/1ps
module tb_reset;
    reg clk=0,key0_n=1;
    wire sys_rst_n;
    integer checks=0;
    board_reset_sync dut(.*);
    task ck(input reg okay);
        begin checks=checks+1; if (!okay) $fatal(1,"RESET_CHECK_FAIL %0d",checks); end
    endtask
    task tick(input reg expected);
        begin #5;clk=1;#1;ck(sys_rst_n===expected);#4;clk=0;end
    endtask
    initial begin
        $dumpfile("wave.vcd");$dumpvars(0,tb_reset);
        #1;ck(sys_rst_n===0); // cold configuration, button never pressed
        tick(0);tick(0);tick(1);
        #2;key0_n=0;#1;ck(sys_rst_n===0); // assertion between clock edges
        #2;key0_n=1;#10;ck(sys_rst_n===0); // no clock means no release
        tick(0);tick(0);tick(1);
        #2;key0_n=0;#1;ck(sys_rst_n===0);
        key0_n=1;tick(0); // release bounce interrupted after one clock
        #2;key0_n=0;#1;ck(sys_rst_n===0);
        key0_n=1;tick(0);tick(0);tick(1);
        tick(1);tick(1);
        $display("RESET_PASS checks=%0d",checks);$finish;
    end
    initial begin #1000;$fatal(1,"RESET_TIMEOUT");end
endmodule
