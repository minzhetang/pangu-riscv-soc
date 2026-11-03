`timescale 1ns/1ps
// N<8 must be rejected explicitly by uart_rx.  This TB only supplies a clock
// and reset; the DUT's illegal-configuration message is the observable result.
module tb_uart_rx_illegal;

    localparam integer N = 4;

    reg clk;
    reg rst_n;
    reg rx;
    reg rx_ready;
    reg clear_errors;

    wire       rx_valid;
    wire [7:0] rx_data;
    wire       frame_error;
    wire       overrun;

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

    initial begin
        rst_n        = 1'b0;
        rx           = 1'b1;
        rx_ready     = 1'b0;
        clear_errors = 1'b0;
        repeat (3) @(posedge clk);
        @(negedge clk);
        #1;
        rst_n = 1'b1;
        repeat (20) @(posedge clk);
        $display("RX_ILLEGAL_TEST_NO_REJECT");
        $finish;
    end

endmodule
