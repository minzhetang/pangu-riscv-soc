`timescale 1ns/1ps
// Synthetic public uart_tx capture selfcheck.  Uses the same shared monitor
// module as the formal wrapper TB; only the external pin is driven here.
module tb_regif_tx_capture_neg;
    localparam integer N = 16;

    reg clk;
    reg rst_n;
    reg uart_tx;
    integer errors;
    integer expected_complete;
    integer expected_bad_stop;

    regif_tx_public_monitor #(.N(N)) mon (
        .clk(clk), .rst_n(rst_n), .uart_tx(uart_tx)
    );

    initial clk = 1'b0;
    always #5 clk = ~clk;

    task automatic send_frame(input [7:0] data, input stop_level);
        integer k;
        begin
            @(negedge clk);
            uart_tx = 1'b0;
            for (k = 0; k < 8; k = k + 1) begin
                repeat (N) @(negedge clk);
                uart_tx = data[k];
            end
            repeat (N) @(negedge clk);
            uart_tx = stop_level;
            repeat (N) @(negedge clk);
            uart_tx = 1'b1;
            repeat (4) @(posedge clk);
            #1;
        end
    endtask

    task automatic check(input integer complete, input integer bad_stop, input [255:0] label);
        begin
            if (mon.tx_complete_count !== complete || mon.tx_bad_stop_count !== bad_stop) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s complete=%0d expected=%0d bad_stop=%0d expected=%0d",
                         label, mon.tx_complete_count, complete, mon.tx_bad_stop_count, bad_stop);
            end
        end
    endtask

    task automatic send_frame_reset_last_half(input [7:0] data);
        integer k;
        begin
            @(negedge clk);
            uart_tx = 1'b0;
            for (k = 0; k < 8; k = k + 1) begin
                repeat (N) @(negedge clk);
                uart_tx = data[k];
            end
            repeat (N) @(negedge clk);
            uart_tx = 1'b1;                 // stop starts
            repeat (N/2 + 2) @(negedge clk); // after stop center, before E+10N
            rst_n = 1'b0;
            #1;
            repeat (2) @(negedge clk);
            rst_n = 1'b1;
            repeat (3) @(posedge clk);
            #1;
        end
    endtask

    initial begin
        errors = 0;
        rst_n = 1'b0;
        uart_tx = 1'b1;
        repeat (3) @(posedge clk);
        @(negedge clk); #1; rst_n = 1'b1;
        repeat (2) @(posedge clk); #1;

        // Correct control: one complete frame 0x5A.
        send_frame(8'h5A, 1'b1);
        check(1, 0, "good frame");
        if (mon.complete_data[0] === 8'h5A)
            $display("REGIF_CAP_GOOD_PASS data=5a");
        else
            $display("REGIF_CAP_GOOD_FAIL data=%02x", mon.complete_data[0]);

        // Bad stop must be detected by the same serial monitor and not counted
        // as a complete frame.
        send_frame(8'h33, 1'b0);
        check(1, 1, "bad stop");
        if (mon.tx_bad_stop_count === 1)
            $display("REGIF_CAP_BAD_STOP_DETECTED");
        else
            $display("REGIF_CAP_BAD_STOP_MISSED");

        // Extra frame: expected one, actual two -> checker must reject.
        send_frame(8'h66, 1'b1);
        if (mon.tx_complete_count !== 1)
            $display("REGIF_CAP_EXTRA_DETECTED complete=%0d", mon.tx_complete_count);
        else
            $display("REGIF_CAP_EXTRA_MISSED");

        // Missing frame control: expected three but only two captured.
        if (mon.tx_complete_count !== 3)
            $display("REGIF_CAP_MISSING_DETECTED complete=%0d expected=3", mon.tx_complete_count);
        else
            $display("REGIF_CAP_MISSING_MISSED");

        // Reset in the last half of the stop bit: the 10N frame is not complete,
        // so it must be CANCEL, not COMPLETE.
        send_frame_reset_last_half(8'hA5);
        if (mon.tx_cancel_count === 1 && mon.tx_complete_count === 2)
            $display("REGIF_CAP_LAST_HALF_STOP_CANCEL cancel=1 complete=2");
        else
            $display("REGIF_CAP_LAST_HALF_STOP_FAIL cancel=%0d complete=%0d",
                     mon.tx_cancel_count, mon.tx_complete_count);

        if (mon.tx_complete_count === 2 && mon.tx_bad_stop_count === 1 &&
            mon.complete_data[0] === 8'h5A && mon.complete_data[1] === 8'h66)
            $display("REGIF_CAP_CONTROL_PASS complete=2 bad_stop=1");
        else
            $display("REGIF_CAP_CONTROL_FAIL complete=%0d bad_stop=%0d",
                     mon.tx_complete_count, mon.tx_bad_stop_count);

        if (errors == 0)
            $display("REGIF_CAP_SELFCHECK_PASS");
        else
            $display("REGIF_CAP_SELFCHECK_FAIL errors=%0d", errors);
        $finish;
    end
endmodule
