`timescale 1ns/1ps
// Diagnostic only: same board ports; no external-reset dependency for heartbeat.
module led_test #(
    parameter HEARTBEAT_BIT = 24
)(
    input wire clk,
    input wire rstn,
    output wire [7:0] led
);
    reg [HEARTBEAT_BIT:0] heartbeat_count = 0;
    always @(posedge clk)
        heartbeat_count <= heartbeat_count + 1'b1;

    assign led[7:6] = 2'b10;
    assign led[5] = rstn;
    assign led[4] = ~rstn;
    assign led[3:1] = 3'b010;
    assign led[0] = heartbeat_count[HEARTBEAT_BIT];
endmodule
