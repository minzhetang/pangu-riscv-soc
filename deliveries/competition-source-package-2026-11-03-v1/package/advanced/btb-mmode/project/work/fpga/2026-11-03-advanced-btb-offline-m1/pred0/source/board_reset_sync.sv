`timescale 1ns/1ps
// KEY0: asynchronous assertion, three rising edges to synchronous release.
// No debouncing, minimum pulse guarantee or physical MTBF claim.
module board_reset_sync(input wire clk, input wire key0_n,
                        output wire sys_rst_n);
    reg [2:0] release_ff /* synthesis syn_preserve=1 */ = 3'b000;
    always @(posedge clk or negedge key0_n) begin
        if (!key0_n) release_ff <= 3'b000;
        else release_ff <= {release_ff[1:0], 1'b1};
    end
    assign sys_rst_n = release_ff[2];
endmodule
