`timescale 1ns/1ps
`ifndef TB_MAX_CYCLES
 `define TB_MAX_CYCLES 200
`endif

// Deliberate bounded-watchdog test: no DUT stimulus completes, so the TB
// cycle watchdog must terminate the run with a marker.  The runner classifies
// this marker as TIMEOUT, not as a functional FAIL.
module tb_uart_rx_watchdog;

    localparam integer N = 16;
    localparam integer MAX_CYCLES = `TB_MAX_CYCLES;

    reg clk;
    reg rst_n;
    reg rx;
    reg rx_ready;
    reg clear_errors;

    wire       rx_valid;
    wire [7:0] rx_data;
    wire       frame_error;
    wire       overrun;

    integer cycle_count;

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

    initial clk = 1'b0;
    always #5 clk = ~clk;

    initial cycle_count = 0;
    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        if (cycle_count > MAX_CYCLES) begin
            $display("TB_WATCHDOG_TIMEOUT cycles=%0d limit=%0d", cycle_count, MAX_CYCLES);
            $finish;
        end
    end

    initial begin
        rst_n        = 1'b0;
        rx           = 1'b1;
        rx_ready     = 1'b0;
        clear_errors = 1'b0;
        repeat (3) @(posedge clk);
        @(negedge clk);
        #1;
        rst_n = 1'b1;
        forever @(posedge clk);
    end

endmodule
