`timescale 1ns/1ps
module backend_m0(
 input wire clk,rst, input integer delay_cycles,
 input wire mvalid, output wire mready,input wire [31:0] maddr,mdata,
 input wire mwrite,input wire [3:0] mstrb,input wire [1:0] mlen,
 output reg rvalid=0, input wire rready,output reg [31:0] rdata=0,output wire rlast,
 output integer transactions=0,bytes_count=0,mmio=0
);
 reg [7:0] mem[0:4095]; integer i,b,cycle=0,waits=0,beat=0,n=0;
 reg active=0,wr; reg [31:0] addr; reg [31:0] sampled;
 initial for(i=0;i<4096;i=i+1) mem[i]=(i*17+3)&255;
 assign mready=!rst && !active && !rvalid && (cycle%4!=1);
 assign rlast=beat==n;
 always @(posedge clk) begin
  cycle<=cycle+1;
  if(rst) begin active<=0;rvalid<=0;waits<=0;beat<=0;n<=0;end
  else begin
   if(mvalid && mready) begin
    active<=1;wr<=mwrite;addr<=maddr;beat<=0;n<=mlen;waits<=delay_cycles;
    transactions<=transactions+1;
    if(mwrite) begin
     sampled<=0;
     for(b=0;b<4;b=b+1) if(mstrb[b]) mem[(maddr[11:0]+b)%4096]<=mdata[b*8+:8];
     bytes_count<=bytes_count+mstrb[0]+mstrb[1]+mstrb[2]+mstrb[3];
    end else if(maddr==32'h80000ffc) begin sampled<=mmio;mmio<=mmio+1;end
   end
   if(active && !rvalid) begin
    if(waits>0) waits<=waits-1;
    else if(cycle%3!=1) begin
     rvalid<=1;
     if(wr || addr==32'h80000ffc) rdata<=sampled;
     else rdata<={mem[(addr[11:0]+beat*4+3)%4096],mem[(addr[11:0]+beat*4+2)%4096],mem[(addr[11:0]+beat*4+1)%4096],mem[(addr[11:0]+beat*4)%4096]};
    end
   end
   if(rvalid && rready) begin
    rvalid<=0;
    if(!wr) bytes_count<=bytes_count+4;
    if(rlast) active<=0;
    else begin beat<=beat+1;waits<=delay_cycles;end
   end
  end
 end
endmodule
