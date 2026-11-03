`timescale 1ns/1ps
// Verification-only combinational read, synchronous byte-write memory.
module memory_model(
    input wire clk, rst_n, input wire [31:0] pc, output wire [31:0] inst,
    input wire [31:0] addr,wdata, input wire wren, input wire [3:0] wstrb,
    output reg [31:0] rdata
);
    reg [31:0] rom[0:8191];
    reg [7:0] ram[0:32767];
    integer i,lane,words;
    reg [1023:0] image;
    initial begin
        for(i=0;i<8192;i=i+1) rom[i]=0;
        for(i=0;i<32768;i=i+1) ram[i]=8'ha5;
        if (!$value$plusargs("IMAGE=%s",image) || !$value$plusargs("WORDS=%d",words))
            $fatal(1,"INPUT image parameters missing");
        if(words<=0 || words>8192) $fatal(1,"INPUT image size");
        $readmemh(image,rom,0,words-1);
    end
    assign inst=(pc<32'h8000)?rom[pc[14:2]]:32'h00000000;
    always @* begin
        rdata=0;
        if(addr<32'h8000) rdata=rom[addr[14:2]];
        else if(addr>=32'h10000 && addr<32'h18000)
            rdata={ram[{addr[14:2],2'b00}+3],ram[{addr[14:2],2'b00}+2],
                   ram[{addr[14:2],2'b00}+1],ram[{addr[14:2],2'b00}]};
    end
    always @(posedge clk) if(rst_n && wren===1'b1) begin
        if((^{addr,wdata,wstrb})===1'bx || addr<32'h10000 || addr>=32'h18000 || wstrb==0)
            $fatal(1,"MEMORY_PROTOCOL invalid store");
        for(lane=0;lane<4;lane=lane+1)
            if(wstrb[lane]) ram[{addr[14:2],2'b00}+lane]<=wdata[8*lane+:8];
    end
endmodule
