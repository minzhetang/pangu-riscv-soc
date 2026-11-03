
module memory_model #(parameter LATENCY=1,CASE=0)(input clk,rst_n,input [31:0] pc,output reg [31:0] inst,input [31:0] addr,wdata,input wren,input [3:0] wstrb,output reg [31:0] rdata);
reg [31:0] rom[0:8191],ram[0:8191];integer i,k;
initial begin for(i=0;i<8192;i=i+1)begin rom[i]=0;ram[i]=0;end $readmemh("program.hex",rom);end
always @(posedge clk)begin
 inst<=pc<32768?rom[pc>>2]:0;
 rdata<=addr<32768?rom[addr>>2]:((addr>=65536&&addr<98304)?ram[(addr-65536)>>2]:0);
 if(wren)begin if(addr<65536||addr>=98304)$fatal(1,"bad RAM write");for(k=0;k<4;k=k+1)if(wstrb[k])ram[(addr-65536)>>2][8*k+:8]<=wdata[8*k+:8];end
end
endmodule
