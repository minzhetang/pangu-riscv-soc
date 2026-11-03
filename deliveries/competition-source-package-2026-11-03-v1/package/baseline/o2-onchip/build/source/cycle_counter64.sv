`timescale 1ns/1ps
// RESET_VALUE is nonzero ONLY in labelled carry-boundary unit-test instances.
// Production soc_top does not override its zero default.
module cycle_counter64 #(parameter [63:0] RESET_VALUE=64'd0)(
    input wire clk,rst_n,output reg [63:0] ticks
);
    always @(posedge clk or negedge rst_n)
        if(!rst_n) ticks<=RESET_VALUE;
        else ticks<=ticks+64'd1;
endmodule
