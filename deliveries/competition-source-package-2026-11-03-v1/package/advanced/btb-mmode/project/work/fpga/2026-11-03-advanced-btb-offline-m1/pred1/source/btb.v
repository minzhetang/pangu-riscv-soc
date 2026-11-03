`timescale 1ns/1ps
// Direct-mapped BTB with a 2-bit saturating direction counter per entry.
// - Branches use the counter (>=2 predicts taken).
// - JAL/JALR entries are marked always-taken.
// - The target is stored on every update so a taken prediction has a PC.
module btb #(
    parameter integer INDEX_BITS = 6
) (
    input  wire        clk,
    input  wire        rst_n,

    // Lookup is combinational and uses the current IF PC.
    input  wire [31:0] lookup_pc,
    output wire        lookup_hit,
    output wire        lookup_taken,
    output wire [31:0] lookup_target,

    // Update is performed by the EX stage after resolution.
    input  wire        update_valid,
    input  wire        update_is_jump,
    input  wire        update_taken,
    input  wire [31:0] update_pc,
    input  wire [31:0] update_target
);
    localparam integer ENTRIES = (1 << INDEX_BITS);
    localparam integer TAG_BITS = 32 - INDEX_BITS - 2;

    reg                 valid  [0:ENTRIES-1];
    reg                 is_jump[0:ENTRIES-1];
    reg [TAG_BITS-1:0]  tag    [0:ENTRIES-1];
    reg [31:0]          target [0:ENTRIES-1];
    reg [1:0]           state  [0:ENTRIES-1];

    wire [INDEX_BITS-1:0] lookup_index = lookup_pc[INDEX_BITS+1:2];
    wire [TAG_BITS-1:0]   lookup_tag   = lookup_pc[31:INDEX_BITS+2];
    wire [INDEX_BITS-1:0] update_index = update_pc[INDEX_BITS+1:2];
    wire [TAG_BITS-1:0]   update_tag   = update_pc[31:INDEX_BITS+2];

    assign lookup_hit    = valid[lookup_index] && (tag[lookup_index] == lookup_tag);
    assign lookup_taken  = lookup_hit && (is_jump[lookup_index] || state[lookup_index][1]);
    assign lookup_target = target[lookup_index];

    integer i;
    initial begin
        for (i = 0; i < ENTRIES; i = i + 1) begin
            valid[i]   = 1'b0;
            is_jump[i] = 1'b0;
            tag[i]     = {TAG_BITS{1'b0}};
            target[i]  = 32'd0;
            state[i]   = 2'b00;
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < ENTRIES; i = i + 1) begin
                valid[i]   <= 1'b0;
                is_jump[i] <= 1'b0;
                tag[i]     <= {TAG_BITS{1'b0}};
                target[i]  <= 32'd0;
                state[i]   <= 2'b00;
            end
        end else if (update_valid) begin
            valid[update_index]  <= 1'b1;
            tag[update_index]    <= update_tag;
            target[update_index] <= update_target;
            if (update_is_jump) begin
                is_jump[update_index] <= 1'b1;
                state[update_index]   <= 2'b11;
            end else begin
                is_jump[update_index] <= 1'b0;
                if (update_taken) begin
                    if (state[update_index] != 2'b11)
                        state[update_index] <= state[update_index] + 1'b1;
                end else begin
                    if (state[update_index] != 2'b00)
                        state[update_index] <= state[update_index] - 1'b1;
                end
            end
        end
    end
endmodule
