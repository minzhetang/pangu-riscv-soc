`timescale 1ns/1ps
module tb_led_path;
    reg clk = 0;
    reg rstn = 1;
    wire [7:0] led;
    integer cycle;
    integer checks = 0;
    integer transitions = 0;
    reg previous_bit = 0;
    reg [7:0] expected;
    led_test #(.HEARTBEAT_BIT(3)) dut(.clk(clk), .rstn(rstn), .led(led));

    task check_output(input integer completed_cycles);
        begin
            // Hand-frozen contract values; independent of DUT internal state.
            expected = rstn ? 8'hA4 : 8'h94;
            expected[0] = (completed_cycles / 8) % 2;
            if ((^led) === 1'bx) $fatal(1,"FAIL X/Z cycle=%0d",completed_cycles);
            if (led !== expected)
                $fatal(1,"FAIL cycle=%0d rstn=%b expected=%h actual=%h",completed_cycles,rstn,expected,led);
            checks = checks + 1;
        end
    endtask

    initial begin
        $dumpfile("led-path.vcd");
        $dumpvars(0,tb_led_path);
        #1; check_output(0);
        for (cycle=1;cycle<=96;cycle=cycle+1) begin
            rstn = ((cycle % 7) >= 3);
            #1; check_output(cycle-1); // Raw reset lamps respond without clock.
            #3; clk=1;
            #1; check_output(cycle);
            if (led[0] !== previous_bit) transitions=transitions+1;
            previous_bit=led[0];
            #5; clk=0;
        end
        if (transitions != 12) $fatal(1,"FAIL transitions=%0d",transitions);
        $display("PASS checks=%0d cycles=96 transitions=12 simulated_time=%0t",checks,$time);
        $finish;
    end
    initial begin #2000; $fatal(1,"TIMEOUT cycle watchdog"); end
endmodule
