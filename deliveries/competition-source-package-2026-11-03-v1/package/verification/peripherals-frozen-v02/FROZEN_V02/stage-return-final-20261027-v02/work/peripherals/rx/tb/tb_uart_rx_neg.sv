`timescale 1ns/1ps
`include "rx_ledger_check.svh"
`ifndef TB_MAX_CYCLES
 `define TB_MAX_CYCLES 20000
`endif
// Negative proof for the RX independent checker.  The DUT sends 0x55 but
// the checker is deliberately given 0xAA.  A working checker must flag the
// mismatch; this TB passes only when that expected detection occurs.
module rx_neg_checker (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       valid,
    input  wire [7:0] actual,
    input  wire [7:0] expected,
    output reg        check_error,
    output reg        check_seen
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            check_error <= 1'b0;
            check_seen  <= 1'b0;
        end else begin
            if (valid === 1'b1) begin
                check_seen  <= 1'b1;
                if (actual !== expected)
                    check_error <= 1'b1;
            end
        end
    end
endmodule

// Public-port event capture used by the negative proof.  The test drives only
// valid/ready/data/line_good/line_data; the capture source (not a hand-filled
// actual array) produces the ordered event stream consumed by the comparator.


module tb_uart_rx_neg;

    localparam integer N = 16;
    localparam integer HARD_CAP = 1000000;

    reg clk;
    reg rst_n;
    reg rx;
    reg rx_ready;
    reg clear_errors;

    wire       rx_valid;
    wire [7:0] rx_data;
    wire       frame_error;
    wire       overrun;

    wire checker_error;
    wire checker_seen;

    localparam integer MAX_LEDGER_EVENTS = 512;
    integer exp_ledger_type [0:MAX_LEDGER_EVENTS-1];
    integer exp_ledger_data [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_type [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_data [0:MAX_LEDGER_EVENTS-1];
    integer exp_ledger_count;
    integer act_ledger_count;
    integer ledger_i;
    integer ledger_errors;

    reg        cap_rst_n;
    reg        cap_valid;
    reg        cap_ready;
    reg        cap_line_good;
    reg [7:0]  cap_data;
    reg [7:0]  cap_line_data;
    reg        cap_cancel;

    integer cycle_count;
    integer i;

    uart_rx #(.CLKS_PER_BIT(N)) dut (
        .clk         (clk),
        .rst_n       (rst_n),
        .rx          (rx),
        .rx_ready    (rx_ready),
        .clear_errors(clear_errors),
        .rx_valid    (rx_valid),
        .rx_data     (rx_data),
        .frame_error (frame_error),
        .overrun     (overrun)
    );

    rx_neg_checker neg_chk (
        .clk      (clk),
        .rst_n    (rst_n),
        .valid    (rx_valid),
        .actual   (rx_data),
        .expected (8'hAA),
        .check_error(checker_error),
        .check_seen (checker_seen)
    );

    rx_public_capture cap (
        .clk       (clk),
        .rst_n     (cap_rst_n),
        .valid     (cap_valid),
        .ready     (cap_ready),
        .line_good_accept (cap_line_good),
        .line_good_drop (cap_line_good),
        .data      (cap_data),
        .line_data (cap_line_data),
        .cancel    (cap_cancel),
        .cancel_edge(32'd0)
    );

    initial clk = 1'b0;
    always #5 clk = ~clk;

    string wave_file;
    initial begin
        if ($value$plusargs("WAVE_FILE=%s", wave_file)) begin
            $dumpfile(wave_file);
            $dumpvars(0, tb_uart_rx_neg);
        end
    end

    initial begin
        if (`TB_MAX_CYCLES > HARD_CAP) begin
            $display("TB_HARD_CAP_REJECT limit=%0d hard_cap=%0d", `TB_MAX_CYCLES, HARD_CAP);
            $finish;
        end
    end

    initial cycle_count = 0;
    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        if (cycle_count > `TB_MAX_CYCLES) begin
            $display("TB_WATCHDOG_TIMEOUT cycles=%0d limit=%0d", cycle_count, `TB_MAX_CYCLES);
            $finish;
        end
    end

    task automatic send_byte(input [7:0] data);
        integer k;
        begin
            @(posedge clk);
            #1;
            rx = 1'b0;
            for (k = 0; k < 8; k = k + 1) begin
                repeat (N) @(posedge clk);
                #1;
                rx = data[k];
            end
            repeat (N) @(posedge clk);
            #1;
            rx = 1'b1;
            repeat (N) @(posedge clk);
            #1;
            rx = 1'b1;
        end
    endtask

    task automatic cap_reset;
        begin
            cap_rst_n = 1'b0;
            cap_valid = 1'b0;
            cap_ready = 1'b0;
            cap_line_good = 1'b0;
            cap_data = 8'h00;
            cap_line_data = 8'h00;
            cap_cancel = 1'b0;
            repeat (2) @(posedge clk);
            @(negedge clk);
            #1;
            cap_rst_n = 1'b1;
            repeat (2) @(posedge clk);
            #1;
        end
    endtask

    task automatic cap_accept(input [7:0] d);
        begin
            @(negedge clk);
            cap_valid = 1'b1;
            cap_ready = 1'b0;
            cap_line_good = 1'b0;
            cap_data = d;
            @(posedge clk);
            #1;
            cap_valid = 1'b0;
            @(posedge clk);
            #1;
        end
    endtask

    task automatic copy_cap;
        begin
            act_ledger_count = cap.count;
            for (ledger_i = 0; ledger_i < cap.count; ledger_i = ledger_i + 1) begin
                act_ledger_type[ledger_i] = cap.etype[ledger_i];
                act_ledger_data[ledger_i] = cap.edata[ledger_i];
            end
        end
    endtask

    task automatic cap_same_edge(input [7:0] old_data, input [7:0] new_data);
        begin
            @(negedge clk);
            cap_valid = 1'b1; cap_ready = 1'b0; cap_line_good = 1'b0; cap_data = old_data;
            @(posedge clk); #1;
            @(negedge clk);
            cap_valid = 1'b1; cap_ready = 1'b1; cap_line_good = 1'b1; cap_data = new_data; cap_line_data = new_data;
            @(posedge clk); #1;
            @(negedge clk);
            cap_ready = 1'b1; cap_line_good = 1'b0;
            @(posedge clk); #1;
            @(negedge clk);
            cap_valid = 1'b0; cap_ready = 1'b0; cap_line_good = 1'b0;
            @(posedge clk); #1;
        end
    endtask

    task automatic cap_drop(input [7:0] accepted, input [7:0] dropped);
        begin
            @(negedge clk);
            cap_valid = 1'b1; cap_ready = 1'b0; cap_line_good = 1'b0; cap_data = accepted;
            @(posedge clk); #1;
            @(negedge clk);
            cap_valid = 1'b1; cap_ready = 1'b0; cap_line_good = 1'b1;
            cap_line_data = dropped;
            @(posedge clk); #1;
            @(negedge clk);
            cap_valid = 1'b0; cap_line_good = 1'b0;
            @(posedge clk); #1;
        end
    endtask

    task automatic cap_cancel_one;
        begin
            @(negedge clk);
            cap_cancel = 1'b1;
            @(posedge clk); #1;
            @(negedge clk);
            cap_cancel = 1'b0;
            @(posedge clk); #1;
        end
    endtask

    initial begin
        rst_n        = 1'b0;
        rx           = 1'b1;
        rx_ready     = 1'b0;
        clear_errors = 1'b0;
        cap_rst_n    = 1'b0;
        cap_valid    = 1'b0;
        cap_ready    = 1'b0;
        cap_line_good = 1'b0;
        cap_data     = 8'h00;
        cap_line_data = 8'h00;
        cap_cancel   = 1'b0;
        repeat (3) @(posedge clk);
        @(negedge clk);
        #1;
        rst_n = 1'b1;
        repeat (4) @(posedge clk);
        #1;

        send_byte(8'h55);
        repeat (4) @(posedge clk);
        #1;

        if (rx_valid === 1'b1 && rx_data === 8'h55 && checker_seen === 1'b1) begin
            $display("NEG_CONTROL_PASS expected=aa actual=55");
        end else begin
            $display("NEG_CONTROL_FAIL valid=%b data=%02x seen=%b", rx_valid, rx_data, checker_seen);
        end

        if (checker_error === 1'b1)
            $display("NEG_CHECKER_PASS");
        else
            $display("NEG_CHECKER_MISSED");

        // Public-stream capture source plus the same ordered comparator macro
        // as the formal RX TB.  Control: one expected/actual ACCEPT.
        cap_reset();
        cap_accept(8'h55);
        copy_cap();
        exp_ledger_count = 1;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors == 0)
            $display("NEG_EXTRA_VALID_CONTROL_PASS count=%0d", act_ledger_count);
        else
            $display("NEG_EXTRA_VALID_CONTROL_FAIL count=%0d", act_ledger_count);

        // Extra: one expected ACCEPT but two captured ACCEPT events.
        cap_reset();
        cap_accept(8'h55);
        cap_accept(8'hAA);
        copy_cap();
        exp_ledger_count = 1;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_EXTRA_VALID_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_EXTRA_VALID_MISSED count=%0d", act_ledger_count);

        // Missing: two expected ACCEPT events but only one captured.
        cap_reset();
        cap_accept(8'h55);
        copy_cap();
        exp_ledger_count = 2;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        exp_ledger_type[1] = 1; exp_ledger_data[1] = 8'h66;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_MISSING_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_MISSING_MISSED count=%0d", act_ledger_count);

        // Wrong order: expected 55 then AA, captured AA then 55.
        cap_reset();
        cap_accept(8'hAA);
        cap_accept(8'h55);
        copy_cap();
        exp_ledger_count = 2;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        exp_ledger_type[1] = 1; exp_ledger_data[1] = 8'hAA;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_ORDER_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_ORDER_MISSED count=%0d", act_ledger_count);

        // Wrong byte: captured 56, expected 55.
        cap_reset();
        cap_accept(8'h56);
        copy_cap();
        exp_ledger_count = 1;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_WRONG_BYTE_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_WRONG_BYTE_MISSED count=%0d", act_ledger_count);

        // Two-event control.
        cap_reset();
        cap_accept(8'h55);
        cap_accept(8'h66);
        copy_cap();
        exp_ledger_count = 2;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        exp_ledger_type[1] = 1; exp_ledger_data[1] = 8'h66;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors == 0)
            $display("NEG_TWO_EVENT_CONTROL_PASS count=%0d", act_ledger_count);
        else
            $display("NEG_TWO_EVENT_CONTROL_FAIL count=%0d", act_ledger_count);

        // Formal capture-path same-byte same-edge control.
        cap_reset();
        cap_same_edge(8'hA1, 8'hA1);
        copy_cap();
        exp_ledger_count = 4;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'hA1;
        exp_ledger_type[1] = 2; exp_ledger_data[1] = 8'hA1;
        exp_ledger_type[2] = 1; exp_ledger_data[2] = 8'hA1;
        exp_ledger_type[3] = 2; exp_ledger_data[3] = 8'hA1;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors == 0)
            $display("NEG_CAPTURE_SAME_EDGE_CONTROL_PASS count=%0d", act_ledger_count);
        else
            $display("NEG_CAPTURE_SAME_EDGE_CONTROL_FAIL count=%0d", act_ledger_count);

        // Formal capture-path DROP control and missing/wrong-byte negatives.
        cap_reset();
        cap_drop(8'h55, 8'h44);
        copy_cap();
        exp_ledger_count = 2;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        exp_ledger_type[1] = 3; exp_ledger_data[1] = 8'h44;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors == 0)
            $display("NEG_CAPTURE_DROP_CONTROL_PASS count=%0d", act_ledger_count);
        else
            $display("NEG_CAPTURE_DROP_CONTROL_FAIL count=%0d", act_ledger_count);

        exp_ledger_count = 3;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        exp_ledger_type[1] = 3; exp_ledger_data[1] = 8'h44;
        exp_ledger_type[2] = 3; exp_ledger_data[2] = 8'h44;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_CAPTURE_DROP_MISSING_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_CAPTURE_DROP_MISSING_MISSED count=%0d", act_ledger_count);

        exp_ledger_count = 2;
        exp_ledger_type[0] = 1; exp_ledger_data[0] = 8'h55;
        exp_ledger_type[1] = 3; exp_ledger_data[1] = 8'h45;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_CAPTURE_DROP_WRONG_BYTE_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_CAPTURE_DROP_WRONG_BYTE_MISSED count=%0d", act_ledger_count);

        // Formal capture-path CANCEL control and missing/extra negatives.
        cap_reset();
        cap_cancel_one();
        copy_cap();
        exp_ledger_count = 1;
        exp_ledger_type[0] = 4; exp_ledger_data[0] = 8'h00;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors == 0)
            $display("NEG_CAPTURE_CANCEL_CONTROL_PASS count=%0d", act_ledger_count);
        else
            $display("NEG_CAPTURE_CANCEL_CONTROL_FAIL count=%0d", act_ledger_count);

        exp_ledger_count = 2;
        exp_ledger_type[0] = 4; exp_ledger_data[0] = 8'h00;
        exp_ledger_type[1] = 4; exp_ledger_data[1] = 8'h00;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_CAPTURE_CANCEL_MISSING_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_CAPTURE_CANCEL_MISSING_MISSED count=%0d", act_ledger_count);

        exp_ledger_count = 0;
        `RX_LEDGER_COMPARE(ledger_errors);
        if (ledger_errors > 0)
            $display("NEG_CAPTURE_CANCEL_EXTRA_DETECTED count=%0d errors=%0d", act_ledger_count, ledger_errors);
        else
            $display("NEG_CAPTURE_CANCEL_EXTRA_MISSED count=%0d", act_ledger_count);

        $finish;
    end

endmodule
