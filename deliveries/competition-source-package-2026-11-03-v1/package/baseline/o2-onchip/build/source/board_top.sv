`timescale 1ns/1ps
// MES2L676-100HP: KEY0 reset, KEY1..4 GPIO low nibble, eight LEDs, TX only.
// CPU, peripheral cores/wrapper, address map and memory protocol unchanged.
module board_top(input wire clk, input wire [4:0] key_n,
                 output wire uart_tx, output wire [7:0] led);
    wire sys_rst_n;
    wire [7:0] gpio_keys = {4'b0000, ~key_n[4:1]};
    wire stopped /* synthesis PAP_MARK_DEBUG="true" */, write_error /* synthesis PAP_MARK_DEBUG="true" */;
    wire [1:0] stop_kind /* synthesis PAP_MARK_DEBUG="true" */;
    wire [31:0] stop_pc;
    board_reset_sync reset_sync(.clk(clk), .key0_n(key_n[0]),
                                .sys_rst_n(sys_rst_n));
    soc_top #(.CLKS_PER_BIT(234)) soc(
        .clk(clk), .rst_n(sys_rst_n), .gpio_in_async(gpio_keys),
        .uart_tx(uart_tx), .gpio_out(led), .stopped(stopped),
        .stop_kind(stop_kind), .stop_pc(stop_pc), .write_error(write_error));
endmodule
