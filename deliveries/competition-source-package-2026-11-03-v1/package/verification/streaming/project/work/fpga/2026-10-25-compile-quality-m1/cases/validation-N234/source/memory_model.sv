`timescale 1ns/1ps
// Own binding only. Licensed Pango primitive implementation stays in PDS.
module memory_model #(parameter integer LATENCY=1, parameter integer CASE=0)(
    input wire clk,rst_n,
    input wire [31:0] pc,output wire [31:0] inst,
    input wire [31:0] addr,wdata,input wire wren,input wire [3:0] wstrb,
    output wire [31:0] rdata
);
    `include "init_tables.svh"
    function automatic [287:0] init_piece;
        input integer bank,halfword,chunk,is_ram;
        integer j,w;reg [31:0] value;
        begin
            init_piece=0;
            for(j=0;j<32;j=j+1) begin
                w=bank*1024+chunk*16+j/2;
                value=is_ram ? RAM_BITS[w*32+:32] : ROM_BITS[w*32+:32];
                init_piece[j*9+:9]={1'b0,value[halfword*16+(j%2)*8+:8]};
            end
        end
    endfunction
    wire [31:0] local_addr=addr-RAM_BASE;
    wire if_en=pc<ROM_BYTES;
    wire data_ram=(addr>=RAM_BASE)&&(addr<RAM_BASE+RAM_BYTES);
    wire data_rom=(addr<ROM_BYTES)&&!data_ram;
    reg [2:0] if_bank_q=0,data_bank_q=0;
    reg if_valid_q=0;reg [1:0] region_q=0;
    wire [31:0] rom_if[0:7],rom_data[0:7],ram_data[0:7];
    // Verification-only read-only views. NOT a functional shadow RAM.
`ifdef M0_VERIFY
    `include "memory_observe_decl.svh"
`endif
    genvar b,h,w;
    generate for(b=0;b<8;b=b+1) begin:bank
        wire [17:0] ri[0:1],rd[0:1],rq[0:1];
        for(h=0;h<2;h=h+1) begin:halfword
            wire [15:0] wd=wdata[h*16+:16];
            GTP_DRM18K_E1 #(
                .GRS_EN("FALSE"),.DATA_WIDTH_A(16),.DATA_WIDTH_B(16),
                .RAM_MODE("TRUE_DUAL_PORT"),.DOA_REG(0),.DOB_REG(0),
                .WRITE_MODE_A("NORMAL_WRITE"),.WRITE_MODE_B("NORMAL_WRITE"),
                .RST_TYPE("SYNC"),
                .INIT_00(init_piece(b,h,0,0)),
                .INIT_01(init_piece(b,h,1,0)),
                .INIT_02(init_piece(b,h,2,0)),
                .INIT_03(init_piece(b,h,3,0)),
                .INIT_04(init_piece(b,h,4,0)),
                .INIT_05(init_piece(b,h,5,0)),
                .INIT_06(init_piece(b,h,6,0)),
                .INIT_07(init_piece(b,h,7,0)),
                .INIT_08(init_piece(b,h,8,0)),
                .INIT_09(init_piece(b,h,9,0)),
                .INIT_0A(init_piece(b,h,10,0)),
                .INIT_0B(init_piece(b,h,11,0)),
                .INIT_0C(init_piece(b,h,12,0)),
                .INIT_0D(init_piece(b,h,13,0)),
                .INIT_0E(init_piece(b,h,14,0)),
                .INIT_0F(init_piece(b,h,15,0)),
                .INIT_10(init_piece(b,h,16,0)),
                .INIT_11(init_piece(b,h,17,0)),
                .INIT_12(init_piece(b,h,18,0)),
                .INIT_13(init_piece(b,h,19,0)),
                .INIT_14(init_piece(b,h,20,0)),
                .INIT_15(init_piece(b,h,21,0)),
                .INIT_16(init_piece(b,h,22,0)),
                .INIT_17(init_piece(b,h,23,0)),
                .INIT_18(init_piece(b,h,24,0)),
                .INIT_19(init_piece(b,h,25,0)),
                .INIT_1A(init_piece(b,h,26,0)),
                .INIT_1B(init_piece(b,h,27,0)),
                .INIT_1C(init_piece(b,h,28,0)),
                .INIT_1D(init_piece(b,h,29,0)),
                .INIT_1E(init_piece(b,h,30,0)),
                .INIT_1F(init_piece(b,h,31,0)),
                .INIT_20(init_piece(b,h,32,0)),
                .INIT_21(init_piece(b,h,33,0)),
                .INIT_22(init_piece(b,h,34,0)),
                .INIT_23(init_piece(b,h,35,0)),
                .INIT_24(init_piece(b,h,36,0)),
                .INIT_25(init_piece(b,h,37,0)),
                .INIT_26(init_piece(b,h,38,0)),
                .INIT_27(init_piece(b,h,39,0)),
                .INIT_28(init_piece(b,h,40,0)),
                .INIT_29(init_piece(b,h,41,0)),
                .INIT_2A(init_piece(b,h,42,0)),
                .INIT_2B(init_piece(b,h,43,0)),
                .INIT_2C(init_piece(b,h,44,0)),
                .INIT_2D(init_piece(b,h,45,0)),
                .INIT_2E(init_piece(b,h,46,0)),
                .INIT_2F(init_piece(b,h,47,0)),
                .INIT_30(init_piece(b,h,48,0)),
                .INIT_31(init_piece(b,h,49,0)),
                .INIT_32(init_piece(b,h,50,0)),
                .INIT_33(init_piece(b,h,51,0)),
                .INIT_34(init_piece(b,h,52,0)),
                .INIT_35(init_piece(b,h,53,0)),
                .INIT_36(init_piece(b,h,54,0)),
                .INIT_37(init_piece(b,h,55,0)),
                .INIT_38(init_piece(b,h,56,0)),
                .INIT_39(init_piece(b,h,57,0)),
                .INIT_3A(init_piece(b,h,58,0)),
                .INIT_3B(init_piece(b,h,59,0)),
                .INIT_3C(init_piece(b,h,60,0)),
                .INIT_3D(init_piece(b,h,61,0)),
                .INIT_3E(init_piece(b,h,62,0)),
                .INIT_3F(init_piece(b,h,63,0))
            ) rom_block(
                .DOA(ri[h]),.DOB(rd[h]),.DIA(18'd0),.DIB(18'd0),
                .ADDRA({pc[11:2],4'd0}),.ADDRB({addr[11:2],4'd0}),
                .ADDRA_HOLD(1'b0),.ADDRB_HOLD(1'b0),.BWEA(4'd0),.BWEB(2'd0),
                .CLKA(clk),.CLKB(clk),.CEA(if_en&&(pc[14:12]==b)),
                .CEB(data_rom&&(addr[14:12]==b)),.WEA(1'b0),.WEB(1'b0),
                .ORCEA(1'b1),.ORCEB(1'b1),.RSTA(1'b0),.RSTB(1'b0));
            GTP_DRM18K_E1 #(
                .GRS_EN("FALSE"),.DATA_WIDTH_A(16),.DATA_WIDTH_B(16),
                .RAM_MODE("SINGLE_PORT"),.DOA_REG(0),.DOB_REG(0),
                .WRITE_MODE_A("NORMAL_WRITE"),.WRITE_MODE_B("NORMAL_WRITE"),
                .RST_TYPE("SYNC"),
                .INIT_00(init_piece(b,h,0,1)),
                .INIT_01(init_piece(b,h,1,1)),
                .INIT_02(init_piece(b,h,2,1)),
                .INIT_03(init_piece(b,h,3,1)),
                .INIT_04(init_piece(b,h,4,1)),
                .INIT_05(init_piece(b,h,5,1)),
                .INIT_06(init_piece(b,h,6,1)),
                .INIT_07(init_piece(b,h,7,1)),
                .INIT_08(init_piece(b,h,8,1)),
                .INIT_09(init_piece(b,h,9,1)),
                .INIT_0A(init_piece(b,h,10,1)),
                .INIT_0B(init_piece(b,h,11,1)),
                .INIT_0C(init_piece(b,h,12,1)),
                .INIT_0D(init_piece(b,h,13,1)),
                .INIT_0E(init_piece(b,h,14,1)),
                .INIT_0F(init_piece(b,h,15,1)),
                .INIT_10(init_piece(b,h,16,1)),
                .INIT_11(init_piece(b,h,17,1)),
                .INIT_12(init_piece(b,h,18,1)),
                .INIT_13(init_piece(b,h,19,1)),
                .INIT_14(init_piece(b,h,20,1)),
                .INIT_15(init_piece(b,h,21,1)),
                .INIT_16(init_piece(b,h,22,1)),
                .INIT_17(init_piece(b,h,23,1)),
                .INIT_18(init_piece(b,h,24,1)),
                .INIT_19(init_piece(b,h,25,1)),
                .INIT_1A(init_piece(b,h,26,1)),
                .INIT_1B(init_piece(b,h,27,1)),
                .INIT_1C(init_piece(b,h,28,1)),
                .INIT_1D(init_piece(b,h,29,1)),
                .INIT_1E(init_piece(b,h,30,1)),
                .INIT_1F(init_piece(b,h,31,1)),
                .INIT_20(init_piece(b,h,32,1)),
                .INIT_21(init_piece(b,h,33,1)),
                .INIT_22(init_piece(b,h,34,1)),
                .INIT_23(init_piece(b,h,35,1)),
                .INIT_24(init_piece(b,h,36,1)),
                .INIT_25(init_piece(b,h,37,1)),
                .INIT_26(init_piece(b,h,38,1)),
                .INIT_27(init_piece(b,h,39,1)),
                .INIT_28(init_piece(b,h,40,1)),
                .INIT_29(init_piece(b,h,41,1)),
                .INIT_2A(init_piece(b,h,42,1)),
                .INIT_2B(init_piece(b,h,43,1)),
                .INIT_2C(init_piece(b,h,44,1)),
                .INIT_2D(init_piece(b,h,45,1)),
                .INIT_2E(init_piece(b,h,46,1)),
                .INIT_2F(init_piece(b,h,47,1)),
                .INIT_30(init_piece(b,h,48,1)),
                .INIT_31(init_piece(b,h,49,1)),
                .INIT_32(init_piece(b,h,50,1)),
                .INIT_33(init_piece(b,h,51,1)),
                .INIT_34(init_piece(b,h,52,1)),
                .INIT_35(init_piece(b,h,53,1)),
                .INIT_36(init_piece(b,h,54,1)),
                .INIT_37(init_piece(b,h,55,1)),
                .INIT_38(init_piece(b,h,56,1)),
                .INIT_39(init_piece(b,h,57,1)),
                .INIT_3A(init_piece(b,h,58,1)),
                .INIT_3B(init_piece(b,h,59,1)),
                .INIT_3C(init_piece(b,h,60,1)),
                .INIT_3D(init_piece(b,h,61,1)),
                .INIT_3E(init_piece(b,h,62,1)),
                .INIT_3F(init_piece(b,h,63,1))
            ) ram_block(
                .DOA(rq[h]),.DOB(),.DIA({1'b0,wd[15:8],1'b0,wd[7:0]}),.DIB(18'd0),
                .ADDRA({local_addr[11:2],4'd0}),.ADDRB(14'd0),
                .ADDRA_HOLD(1'b0),.ADDRB_HOLD(1'b0),
                .BWEA({2'b00,wstrb[h*2+:2]}),.BWEB(2'd0),
                .CLKA(clk),.CLKB(clk),.CEA(data_ram&&(local_addr[14:12]==b)),
                .CEB(1'b0),.WEA(rst_n&&wren),.WEB(1'b0),
                .ORCEA(1'b1),.ORCEB(1'b0),.RSTA(1'b0),.RSTB(1'b0));
        end
        assign rom_if[b]={ri[1][16:9],ri[1][7:0],ri[0][16:9],ri[0][7:0]};
        assign rom_data[b]={rd[1][16:9],rd[1][7:0],rd[0][16:9],rd[0][7:0]};
        assign ram_data[b]={rq[1][16:9],rq[1][7:0],rq[0][16:9],rq[0][7:0]};
`ifdef M0_VERIFY
        `include "memory_observe_bank.svh"
`endif
    end endgenerate
    // Region and bank travel WITH the one-edge memory response.
    always @(posedge clk) begin
        if_bank_q<=pc[14:12];if_valid_q<=if_en;
        region_q<=data_ram?2'd2:(data_rom?2'd1:2'd0);
        data_bank_q<=data_ram?local_addr[14:12]:addr[14:12];
`ifdef M0_VERIFY
        `include "memory_protocol_checks.svh"
`endif
    end
    assign inst=if_valid_q?rom_if[if_bank_q]:32'd0;
    assign rdata=region_q==2?ram_data[data_bank_q]:(region_q==1?rom_data[data_bank_q]:32'd0);
`ifdef M0_VERIFY
    initial begin
        if(LATENCY!=1) $fatal(1,"only fixed one-edge memory supported");
    end
`endif
endmodule

