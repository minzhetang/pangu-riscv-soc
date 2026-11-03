`timescale 1ns/1ps
// Shared public-port RX event capture used by the formal RX TB and the
// negative capture-path TB.  It records ACCEPT/CONSUME/DROP/CANCEL from public
// valid/ready/data/line_good/line_data/cancel only.
module rx_public_capture (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       valid,
    input  wire       ready,
    input  wire       line_good_accept,
    input  wire       line_good_drop,
    input  wire [7:0] data,
    input  wire [7:0] line_data,
    input  wire       cancel,
    input  wire [31:0] cancel_edge
);
    localparam integer MAX = 512;
    integer count;
    integer etype [0:MAX-1];
    integer edata [0:MAX-1];
    integer eedge [0:MAX-1];
    reg valid_q;
    reg [31:0] cycle_count;

    initial begin
        count = 0;
        valid_q = 1'b0;
        cycle_count = 0;
    end

    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        if (!rst_n) begin
            count = 0;
            valid_q = 1'b0;
        end else begin
            if (valid && !valid_q) begin
                etype[count] = 1;
                edata[count] = data;
                eedge[count] = cycle_count;
                count = count + 1;
            end
            if (valid && ready) begin
                etype[count] = 2;
                edata[count] = data;
                eedge[count] = cycle_count + 1;
                count = count + 1;
                if (valid_q && line_good_accept) begin
                    // The new byte is published after NBA; its pre-edge serial
                    // value is line_data.  Record it at the same event edge,
                    // after CONSUME, with the actual one-based edge.
                    etype[count] = 1;
                    edata[count] = line_data;
                    eedge[count] = cycle_count + 1;
                    count = count + 1;
                end
            end
            if (line_good_drop && valid_q && !ready) begin
                etype[count] = 3;
                edata[count] = line_data;
                eedge[count] = cycle_count;
                count = count + 1;
            end
            if (cancel) begin
                etype[count] = 4;
                edata[count] = 8'h00;
                eedge[count] = cancel_edge;
                count = count + 1;
            end
            valid_q <= valid;
        end
    end
endmodule
