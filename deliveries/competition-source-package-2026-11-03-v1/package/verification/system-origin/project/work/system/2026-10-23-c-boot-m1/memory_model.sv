`timescale 1ns/1ps
// Verification-only zero-wait Harvard ports with shared read-only ROM image.
// Not synchronous FPGA BRAM, not MMIO, and not a new CPU public interface.
module memory_model(
    input wire clk, input wire rst_n,
    input wire [31:0] pc, output wire [31:0] inst,
    input wire [31:0] addr, input wire [31:0] wdata,
    input wire wren, input wire [3:0] wstrb,
    output reg [31:0] rdata
);
    reg [31:0] rom [0:4095];
    reg [7:0] ram [0:16383];
    integer i, lane;
    initial begin
        for (i=0; i<4096; i=i+1) rom[i]=0;
        for (i=0; i<16384; i=i+1) ram[i]=8'ha5;
        $readmemh("inputs/smoke.mem32.hex", rom, 0, 143);
    end
    assign inst = (pc < 32'h4000) ? rom[pc[13:2]] : 32'h00000000;
    always @* begin
        rdata=0;
        if (addr < 32'h4000) rdata=rom[addr[13:2]];
        else if (addr >= 32'h10000 && addr < 32'h14000)
            rdata={ram[{addr[13:2],2'b00}+3],ram[{addr[13:2],2'b00}+2],
                   ram[{addr[13:2],2'b00}+1],ram[{addr[13:2],2'b00}]};
    end
    always @(posedge clk) begin
        if (rst_n && wren === 1'b1) begin
            if (addr < 32'h10000 || addr >= 32'h14000 ||
                (^addr === 1'bx) || (^wdata === 1'bx) || (^wstrb === 1'bx))
                $fatal(1,"MEMORY_PROTOCOL invalid RAM write");
            for (lane=0; lane<4; lane=lane+1)
                if (wstrb[lane]) ram[{addr[13:2],2'b00}+lane] <= wdata[8*lane+:8];
        end
    end
endmodule
