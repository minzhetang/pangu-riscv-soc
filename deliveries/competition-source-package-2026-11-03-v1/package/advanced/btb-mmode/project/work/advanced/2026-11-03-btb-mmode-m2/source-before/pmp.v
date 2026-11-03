`timescale 1ns/1ps
// =================================================================
// RISC-V PMP checker for the HL3 privileged candidate.
//
// - 16 entries, RV32 pmpcfg0..3 / pmpaddr0..15 layout.
// - OFF, TOR, NA4 and NAPOT modes.
// - Lowest-numbered matching entry wins.
// - S/U accesses require a matching entry with the required permission.
// - M-mode accesses bypass unlocked entries; locked entries are enforced.
//
// The CPU passes the *effective* privilege for data accesses (MPRV is
// resolved by the CPU before the checker).
// =================================================================
module pmp #(
    parameter integer ENTRIES = 16
) (
    input  wire [1:0]          priv,       // 00=U, 01=S, 11=M
    input  wire [31:0]         addr,
    input  wire [1:0]          access,     // 0=fetch, 1=load, 2=store
    input  wire [3:0]          size,       // bytes (1,2,4)
    input  wire [8*ENTRIES-1:0] cfg_flat,  // 8 bits per entry
    input  wire [32*ENTRIES-1:0] addr_flat,// pmpaddr per entry
    output reg                 allow,
    output reg                 matched
);
    localparam integer CFG_W = 8 * ENTRIES;
    localparam integer ADDR_W = 32 * ENTRIES;

    function automatic [5:0] trailing_ones;
        input [31:0] value;
        begin
            // Constant casez avoids a loop in the function body; some PDS
            // versions mis-handle loop variables inside automatic functions.
            casez (value)
                32'b???????????????????????????????0: trailing_ones = 6'd0;
                32'b??????????????????????????????01: trailing_ones = 6'd1;
                32'b?????????????????????????????011: trailing_ones = 6'd2;
                32'b????????????????????????????0111: trailing_ones = 6'd3;
                32'b???????????????????????????01111: trailing_ones = 6'd4;
                32'b??????????????????????????011111: trailing_ones = 6'd5;
                32'b?????????????????????????0111111: trailing_ones = 6'd6;
                32'b????????????????????????01111111: trailing_ones = 6'd7;
                32'b???????????????????????011111111: trailing_ones = 6'd8;
                32'b??????????????????????0111111111: trailing_ones = 6'd9;
                32'b?????????????????????01111111111: trailing_ones = 6'd10;
                32'b????????????????????011111111111: trailing_ones = 6'd11;
                32'b???????????????????0111111111111: trailing_ones = 6'd12;
                32'b??????????????????01111111111111: trailing_ones = 6'd13;
                32'b?????????????????011111111111111: trailing_ones = 6'd14;
                32'b????????????????0111111111111111: trailing_ones = 6'd15;
                32'b???????????????01111111111111111: trailing_ones = 6'd16;
                32'b??????????????011111111111111111: trailing_ones = 6'd17;
                32'b?????????????0111111111111111111: trailing_ones = 6'd18;
                32'b????????????01111111111111111111: trailing_ones = 6'd19;
                32'b???????????011111111111111111111: trailing_ones = 6'd20;
                32'b??????????0111111111111111111111: trailing_ones = 6'd21;
                32'b?????????01111111111111111111111: trailing_ones = 6'd22;
                32'b????????011111111111111111111111: trailing_ones = 6'd23;
                32'b???????0111111111111111111111111: trailing_ones = 6'd24;
                32'b??????01111111111111111111111111: trailing_ones = 6'd25;
                32'b?????011111111111111111111111111: trailing_ones = 6'd26;
                32'b????0111111111111111111111111111: trailing_ones = 6'd27;
                32'b???01111111111111111111111111111: trailing_ones = 6'd28;
                32'b??011111111111111111111111111111: trailing_ones = 6'd29;
                32'b?0111111111111111111111111111111: trailing_ones = 6'd30;
                32'b01111111111111111111111111111111: trailing_ones = 6'd31;
                32'b11111111111111111111111111111111: trailing_ones = 6'd32;
                default: trailing_ones = 6'd0;
            endcase
        end
    endfunction

    function automatic permitted;
        input [7:0] cfg;
        input [1:0] acc;
        begin
            case (acc)
                2'd0: permitted = cfg[2]; // execute
                2'd1: permitted = cfg[0]; // read
                default: permitted = cfg[1]; // write
            endcase
        end
    endfunction

    reg [7:0]  cfg_i;
    reg [31:0] pa_i;
    reg [5:0]  ones_i;
    reg [63:0] base_i, end_i, size_i, mask_i;
    reg [63:0] addr64, access_end;
    reg        match_i;
    reg [7:0]  found_cfg;
    reg        found;

    integer i;

    always @(*) begin
        matched   = 1'b0;
        found     = 1'b0;
        found_cfg = 8'd0;
        allow     = 1'b0;
        addr64    = {32'd0, addr};
        access_end = addr64 + {60'd0, size} - 64'd1;

        for (i = 0; i < ENTRIES; i = i + 1) begin
            cfg_i = cfg_flat[i*8 +: 8];
            pa_i  = addr_flat[i*32 +: 32];
            match_i = 1'b0;
            base_i  = 64'd0;
            end_i   = 64'd0;

            case (cfg_i[4:3])
                2'b00: begin
                    // OFF: no match.
                    match_i = 1'b0;
                end
                2'b01: begin
                    // TOR: [previous pmpaddr, current pmpaddr)
                    base_i = (i == 0) ? 64'd0
                           : ({32'd0, addr_flat[(i-1)*32 +: 32]} << 2);
                    end_i  = {32'd0, pa_i} << 2;
                    match_i = (end_i > base_i) &&
                              (addr64 >= base_i) &&
                              (access_end < end_i);
                end
                2'b10: begin
                    // NA4: one naturally aligned 4-byte region.
                    base_i = {32'd0, pa_i} << 2;
                    end_i  = base_i + 64'd4;
                    match_i = (addr64 >= base_i) && (access_end < end_i);
                end
                default: begin
                    // NAPOT: trailing ones encode the region size.
                    ones_i = trailing_ones(pa_i);
                    if (ones_i >= 6'd32) begin
                        // All ones: region covers the entire 32-bit space.
                        base_i = 64'd0;
                        size_i = 64'd1 << 35;
                    end else begin
                        mask_i = (64'd1 << ones_i) - 64'd1;
                        base_i = ({32'd0, pa_i} & ~mask_i) << 2;
                        size_i = 64'd1 << (ones_i + 6'd3);
                    end
                    end_i = base_i + size_i;
                    match_i = (addr64 >= base_i) && (access_end < end_i);
                end
            endcase

            if (match_i && !found) begin
                found     = 1'b1;
                found_cfg = cfg_i;
                matched   = 1'b1;
            end
        end

        if (!matched) begin
            // No PMP entry matches.  M-mode is allowed; S/U are denied.
            allow = (priv == 2'b11);
        end else if ((priv == 2'b11) && !found_cfg[7]) begin
            // Unlocked entries are not enforced for M-mode.
            allow = 1'b1;
        end else begin
            allow = permitted(found_cfg, access);
        end
    end

    // Keep the unused parameters visible for lint.
    wire unused_cfg_w = |CFG_W;
    wire unused_addr_w = |ADDR_W;
endmodule
