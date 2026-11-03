`timescale 1ns/1ps
module cache_tb;
 reg clk=0;always #5 clk=~clk;
 reg rst=1; reg [1:0] bypass=0,qvalid=0,qwrite=0,pready=0;
 reg [63:0] qaddr=0,qdata=0;reg [7:0] qstrb=0;
 wire [1:0] qready,pvalid,perror,mvalid,mwrite,rready,mready,rvalid,rlast;
 wire [63:0] pdata,hits,maddr,mdata,rdata;wire [7:0] mstrb;wire [3:0] mlen;
 integer delay_cycles=0;
 wire [31:0] tx[0:1],nb[0:1],mm[0:1];
 cache_subsystem_m0 dut(.*);
 genvar c;generate for(c=0;c<2;c=c+1) begin: mems
 backend_m0 mem(.clk(clk),.rst(rst),.delay_cycles(delay_cycles),
 .mvalid(mvalid[c]),.mready(mready[c]),.maddr(maddr[c*32+:32]),.mdata(mdata[c*32+:32]),.mwrite(mwrite[c]),.mstrb(mstrb[c*4+:4]),.mlen(mlen[c*2+:2]),
 .rvalid(rvalid[c]),.rready(rready[c]),.rdata(rdata[c*32+:32]),.rlast(rlast[c]),.transactions(tx[c]),.bytes_count(nb[c]),.mmio(mm[c]));
 end endgenerate
 integer cycle=0,accepted[0:1],completed[0:1],i;
 reg [31:0] hold_data[0:1];reg hold_err[0:1],held[0:1];
 reg [72:0] hold_cmd[0:1];reg cmdheld[0:1];
 always @(posedge clk) begin
  cycle<=cycle+1;
  for(integer k=0;k<2;k=k+1) begin
   if(rst) begin held[k]<=0;cmdheld[k]<=0;end
   else begin
    if(qvalid[k]&&qready[k]) accepted[k]<=accepted[k]+1;
    if(pvalid[k]&&pready[k]) completed[k]<=completed[k]+1;
    if(held[k] && (!pvalid[k] || pdata[k*32+:32]!==hold_data[k] || perror[k]!==hold_err[k])) $fatal(1,"response unstable");
    held[k]<=pvalid[k]&&!pready[k];hold_data[k]<=pdata[k*32+:32];hold_err[k]<=perror[k];
    if(cmdheld[k] && (!mvalid[k] || {maddr[k*32+:32],mdata[k*32+:32],mwrite[k],mstrb[k*4+:4],mlen[k*2+:2]}!==hold_cmd[k])) $fatal(1,"command unstable");
    cmdheld[k]<=mvalid[k]&&!mready[k];hold_cmd[k]<={maddr[k*32+:32],mdata[k*32+:32],mwrite[k],mstrb[k*4+:4],mlen[k*2+:2]};
   end
  end
  if(cycle>100000) $fatal(1,"watchdog");
 end
 task reset_all;
 begin @(negedge clk);rst=1;qvalid=0;pready=0;repeat(3) @(negedge clk);rst=0;end endtask
 task request(input integer ch,input [31:0] a,input bit w,input [3:0] mask,input [31:0] data);
 begin
  @(negedge clk);qaddr[ch*32+:32]=a;qwrite[ch]=w;qstrb[ch*4+:4]=mask;qdata[ch*32+:32]=data;qvalid[ch]=1;
  @(posedge clk);while(!qready[ch]) @(posedge clk);
  @(negedge clk);qvalid[ch]=0;
 end endtask
 task response(input integer ch,input [31:0] expected,input bit err,input integer stalls);
 reg [31:0] v;
 begin
  while(!pvalid[ch]) @(negedge clk);
  repeat(stalls) @(negedge clk);
  if(pdata[ch*32+:32]!==expected || perror[ch]!==err) $fatal(1,"data ch%0d expected %h/%b got %h/%b",ch,expected,err,pdata[ch*32+:32],perror[ch]);
  pready[ch]=1;@(negedge clk);pready[ch]=0;
 end endtask
 string vec,wave;integer ro,bp,ch,fd,rc,idx=0,start_cycle,mode=0;
 reg [31:0] a,w,mask,data,expected,err;
 initial begin
  for(i=0;i<2;i=i+1) begin accepted[i]=0;completed[i]=0;held[i]=0;cmdheld[i]=0;end
  rc=$value$plusargs("DELAY=%d",delay_cycles);rc=$value$plusargs("MODE=%d",mode);
  if($value$plusargs("WAVE=%s",wave)) begin $dumpfile(wave);$dumpvars(0,cache_tb);end
  if(mode==0) begin
   rc=$value$plusargs("RO=%d",ro);rc=$value$plusargs("BYPASS=%d",bp);ch=ro?0:1;bypass={2{bp!=0}};
   if(!$value$plusargs("VEC=%s",vec)) $fatal(1,"missing vectors");fd=$fopen(vec,"r");if(!fd) $fatal(1,"file");
   reset_all();start_cycle=cycle;
   while(!$feof(fd)) begin
    rc=$fscanf(fd,"%h %h %h %h %h %h\n",a,w,mask,data,expected,err);
    if(rc!=6) $fatal(1,"vector parse");
    request(ch,a,w!=0,mask[3:0],data);response(ch,expected,err!=0,idx%4);idx=idx+1;
   end
   repeat(5) @(negedge clk);
   if(accepted[ch]!=idx || completed[ch]!=idx || pvalid!=0 || tx[1-ch]!=0) $fatal(1,"exactly once");
   $display("METRIC requests=%0d cycles=%0d hits=%0d transactions=%0d bytes=%0d mmio=%0d",idx,cycle-start_cycle,hits[ch*32+:32],tx[ch],nb[ch],mm[ch]);
  end else if(mode==2) begin
   reset_all();
   @(negedge clk);qvalid[1]=1;qaddr[63:32]=32'h80000ffc;
   @(posedge clk);while(!qready[1]) @(posedge clk);
   @(negedge clk); // Keep valid: the next identical request is waiting.
   while(!pvalid[1]) @(negedge clk);
   repeat(7) @(negedge clk);
   if(accepted[1]!=1 || tx[1]!=1 || mm[1]!=1) $fatal(1,"accepted while busy");
   response(1,0,0,3);
   @(posedge clk);while(!qready[1]) @(posedge clk);
   @(negedge clk);qvalid[1]=0;qaddr[63:32]=32'h44444444;qwrite[1]=1;qdata[63:32]=32'hffffffff;
   response(1,1,0,5);
   repeat(8) @(negedge clk);
   if(accepted[1]!=2 || completed[1]!=2 || tx[1]!=2 || mm[1]!=2 || pvalid!=0) $fatal(1,"repeat/latching");
   reset_all();repeat(8) @(negedge clk);if(pvalid!=0) $fatal(1,"ghost");
   $display("HELD_VALID_PASS");
  end else begin
   reset_all();
   // Cancel after a read command and before fill completion.
   request(1,32'h0,0,0,0);while(tx[1]==0) @(negedge clk);reset_all();
   repeat(12) @(negedge clk);if(pvalid!=0) $fatal(1,"ghost fill");
   request(1,0,0,0,0);response(1,32'h36251403,0,2);
   // Cancel a pending response; next request must miss again.
   request(1,0,0,0,0);while(!pvalid[1]) @(negedge clk);reset_all();
   if(hits!=0) $fatal(1,"reset hits");
   // MMIO command held while busy must have exactly one side effect.
   request(1,32'h80000ffc,0,0,0);response(1,0,0,6);
   if(mm[1]!=1) $fatal(1,"duplicate side effect");
   // Write committed before reset survives reset, cached tags do not.
   request(1,0,1,15,32'hdeadbeef);while(tx[1]<4) @(negedge clk);reset_all();
   fork
    begin request(0,0,0,0,0);response(0,32'h36251403,0,3);end
    begin request(1,0,0,0,0);response(1,32'hdeadbeef,0,4);end
   join
   repeat(8) @(negedge clk);if(pvalid!=0 || mm[1]!=1) $fatal(1,"reset/concurrency");
   $display("RESET_CONCURRENT_PASS");
  end
  $display("PASS cache");$finish;
 end
endmodule
