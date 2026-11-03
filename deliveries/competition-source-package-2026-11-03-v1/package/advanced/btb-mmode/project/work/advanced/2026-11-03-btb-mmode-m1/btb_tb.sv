`timescale 1ns/1ps
module btb_tb;
reg clk=0,rst=0;reg[31:0]pc=0,upc=0,target=0;reg uv=0,jump=0,taken=0;
wire hit,pred;wire[31:0]dest;
btb #(.INDEX_BITS(2)) dut(.clk(clk),.rst_n(rst),.lookup_pc(pc),.lookup_hit(hit),.lookup_taken(pred),.lookup_target(dest),.update_valid(uv),.update_is_jump(jump),.update_taken(taken),.update_pc(upc),.update_target(target));
always #5 clk=~clk;
integer checks=0;
task check(input bit h,input bit p,input[31:0]t);
 begin #1;if(hit!==h||pred!==p||(h&&dest!==t))$fatal(1,"BTB mismatch %b %b %h",hit,pred,dest);checks=checks+1;end
endtask
task update(input bit j,input bit t,input[31:0]addr,input[31:0]dst);
 begin @(negedge clk);uv=1;jump=j;taken=t;upc=addr;target=dst;@(negedge clk);uv=0;end
endtask
initial begin
 $dumpfile("btb.vcd");$dumpvars(0,btb_tb);repeat(3)@(negedge clk);rst=1;
 check(0,0,0);update(0,1,0,32'h40);check(1,0,32'h40);
 update(0,1,0,32'h40);check(1,1,32'h40);
 update(0,1,0,32'h44);check(1,1,32'h44);
 update(0,0,0,32'h44);check(1,1,32'h44);
 update(0,0,0,32'h44);check(1,0,32'h44);
 repeat(5)update(0,0,0,32'h44);check(1,0,32'h44);
 update(1,1,0,32'h80);check(1,1,32'h80);
 /* disabled update must neither train nor change target */
 @(negedge clk);target=32'hdeadbeef;taken=0;repeat(4)@(negedge clk);check(1,1,32'h80);
 update(1,1,32'h10,32'h90);check(0,0,0);pc=32'h10;check(1,1,32'h90);
 rst=0;#1;check(0,0,0);$display("BTB_MODULE_PASS checks=%0d",checks);$finish;
end
initial begin #20000;$fatal(1,"timeout");end
endmodule
