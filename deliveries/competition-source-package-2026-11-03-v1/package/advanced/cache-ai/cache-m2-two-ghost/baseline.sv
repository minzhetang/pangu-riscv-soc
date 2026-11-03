`timescale 1ns/1ps
module cache_m0 #(parameter READ_ONLY=0)(
 input wire clk,rst,bypass,
 input wire qvalid, output wire qready, input wire [31:0] qaddr,qdata,
 input wire qwrite, input wire [3:0] qstrb,
 output wire pvalid, input wire pready, output reg [31:0] pdata, output reg perror,
 output wire mvalid, input wire mready, output reg [31:0] maddr,mdata,
 output reg mwrite, output reg [3:0] mstrb, output reg [1:0] mlen,
 input wire rvalid, output wire rready, input wire [31:0] rdata, input wire rlast,
 output reg [31:0] hits
);
 localparam IDLE=0,CMD=1,FILL=2,RESP=3;
 reg [1:0] state=IDLE;
 reg [31:0] words[0:3][0:1][0:3];
 reg [25:0] tags[0:3][0:1]; reg valid[0:3][0:1]; reg lru[0:3];
 reg [1:0] saved_set,saved_word,beat; reg saved_way,allocate;
 reg [25:0] saved_tag;
 integer i,j,b; reg hit,way,victim;
 wire [1:0] si=qaddr[5:4]; wire [25:0] tag=qaddr[31:6];
 assign qready=!rst && state==IDLE;
 assign pvalid=!rst && state==RESP;
 assign mvalid=!rst && state==CMD;
 assign rready=!rst && state==FILL;
 always @* begin
   hit=0; way=0;
   if(valid[si][0] && tags[si][0]==tag) begin hit=1;way=0;end
   else if(valid[si][1] && tags[si][1]==tag) begin hit=1;way=1;end
   if(!valid[si][0]) victim=0;
   else if(!valid[si][1]) victim=1;
   else victim=lru[si];
 end
 always @(posedge clk) begin
  if(rst) begin
   state<=IDLE; pdata<=0;perror<=0; hits<=0;
   maddr<=0;mdata<=0;mwrite<=0;mstrb<=0;mlen<=0;
   saved_set<=0;saved_word<=0;saved_way<=0;saved_tag<=0;beat<=0;allocate<=0;
   for(i=0;i<4;i=i+1) begin lru[i]<=0;for(j=0;j<2;j=j+1) valid[i][j]<=0;end
  end else case(state)
   IDLE: if(qvalid) begin
    pdata<=0;perror<=0; allocate<=0;beat<=0;
    saved_set<=si;saved_word<=qaddr[3:2];saved_tag<=tag;
    if(qaddr[1:0]!=0 || (READ_ONLY && qwrite)) begin perror<=1;state<=RESP;end
    else begin
     if(!bypass && !qaddr[31] && hit) lru[si]<=!way;
     if(qwrite) begin
      if(qstrb==0) state<=RESP;
      else begin
       if(!bypass && !qaddr[31] && hit)
        for(b=0;b<4;b=b+1) if(qstrb[b]) words[si][way][qaddr[3:2]][b*8+:8]<=qdata[b*8+:8];
       maddr<=qaddr;mdata<=qdata;mwrite<=1;mstrb<=qstrb;mlen<=0;state<=CMD;
      end
     end else if(!bypass && !qaddr[31] && hit) begin
      pdata<=words[si][way][qaddr[3:2]];hits<=hits+1;state<=RESP;
     end else begin
      mdata<=0;mwrite<=0;mstrb<=0;
      if(!bypass && !qaddr[31]) begin
       maddr<={qaddr[31:4],4'b0};mlen<=3;allocate<=1;saved_way<=victim;
       valid[si][victim]<=0;
      end else begin maddr<=qaddr;mlen<=0;end
      state<=CMD;
     end
    end
   end
   CMD: if(mready) state<=FILL;
   FILL: if(rvalid) begin
    if(allocate) begin
     words[saved_set][saved_way][beat]<=rdata;
     if(beat==saved_word) pdata<=rdata;
     if(rlast) begin valid[saved_set][saved_way]<=1;tags[saved_set][saved_way]<=saved_tag;lru[saved_set]<=!saved_way;end
    end else if(!mwrite) pdata<=rdata;
    if(rlast) state<=RESP; else beat<=beat+1;
   end
   RESP: if(pready) state<=IDLE;
  endcase
 end
endmodule

// Independent I/D channels; no CPU adapter or shared-bus arbitration is implied.
module cache_subsystem_m0(
 input wire clk,rst, input wire [1:0] bypass,qvalid,qwrite,pready,
 input wire [63:0] qaddr,qdata, input wire [7:0] qstrb,
 output wire [1:0] qready,pvalid,perror,
 output wire [63:0] pdata,hits,
 output wire [1:0] mvalid,mwrite,rready, input wire [1:0] mready,rvalid,rlast,
 output wire [63:0] maddr,mdata, input wire [63:0] rdata,
 output wire [7:0] mstrb,output wire [3:0] mlen
);
 genvar c;
 generate for(c=0;c<2;c=c+1) begin: channel
 cache_m0 #(.READ_ONLY(c==0)) u(
 .clk(clk),.rst(rst),.bypass(bypass[c]),.qvalid(qvalid[c]),.qready(qready[c]),
 .qaddr(qaddr[c*32+:32]),.qdata(qdata[c*32+:32]),.qwrite(qwrite[c]),.qstrb(qstrb[c*4+:4]),
 .pvalid(pvalid[c]),.pready(pready[c]),.pdata(pdata[c*32+:32]),.perror(perror[c]),
 .mvalid(mvalid[c]),.mready(mready[c]),.maddr(maddr[c*32+:32]),.mdata(mdata[c*32+:32]),
 .mwrite(mwrite[c]),.mstrb(mstrb[c*4+:4]),.mlen(mlen[c*2+:2]),
 .rvalid(rvalid[c]),.rready(rready[c]),.rdata(rdata[c*32+:32]),.rlast(rlast[c]),.hits(hits[c*32+:32]));
 end endgenerate
endmodule
