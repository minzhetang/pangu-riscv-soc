`timescale 1ns/1ps
module fc_m0(
 input wire clk,rst,
 input wire cfg_valid,output wire cfg_ready,input wire [1:0] cfg_kind,
 input wire [7:0] cfg_addr,input wire [31:0] cfg_data,
 input wire start_valid,output wire start_ready,
 output wire out_valid,input wire out_ready,output wire [2:0] out_index,
 output wire out_last,output wire out_error,
 output wire signed [39:0] out_acc,output wire signed [7:0] out_y
);
 localparam IDLE=0,RUN=1,EMIT=2;
 reg [1:0] state=IDLE;
 reg signed [7:0] x[0:15],w[0:127];reg signed [31:0] bias[0:7];
 reg [15:0] xv;reg [127:0] wv;reg [7:0] bv;
 reg [2:0] row;reg [3:0] col;reg error_flag;
 reg signed [39:0] acc;
 wire signed [15:0] product=$signed(x[col])*$signed(w[{row,col}]);
 wire signed [39:0] product_ext={{24{product[15]}},product};
 wire signed [39:0] next_acc=acc+product_ext;
 function automatic signed [7:0] requant(input signed [39:0] value);
  reg [40:0] magnitude,rounded;
  begin
   magnitude=value[39] ? -$signed({value[39],value}):{1'b0,value};
   rounded=(magnitude+41'd32)>>6;
   if(value[39]) begin if(rounded>128) requant=-8'sd128;else requant=-$signed(rounded[7:0]);end
   else begin if(rounded>127) requant=8'sd127;else requant=rounded[7:0];end
  end
 endfunction
 assign cfg_ready=!rst && state==IDLE;
 assign start_ready=!rst && state==IDLE && !cfg_valid;
 assign out_valid=!rst && state==EMIT;
 assign out_index=row;
 assign out_last=error_flag || row==7;
 assign out_error=error_flag;
 assign out_acc=acc;
 assign out_y=error_flag ? 8'sd0:requant(acc);
 always @(posedge clk) begin
  if(rst) begin state<=IDLE;xv<=0;wv<=0;bv<=0;row<=0;col<=0;acc<=0;error_flag<=0;end
  else begin
   if(cfg_valid && cfg_ready) case(cfg_kind)
    0: if(cfg_addr<16) begin x[cfg_addr]<=cfg_data[7:0];xv[cfg_addr]<=1;end
    1: if(cfg_addr<128) begin w[cfg_addr]<=cfg_data[7:0];wv[cfg_addr]<=1;end
    2: if(cfg_addr<8) begin bias[cfg_addr]<=cfg_data;bv[cfg_addr]<=1;end
    default: begin end
   endcase
   case(state)
    IDLE: if(start_valid && start_ready) begin
     row<=0;col<=0;error_flag<=0;
     if((&xv) && (&wv) && (&bv)) begin acc<={{8{bias[0][31]}},bias[0]};state<=RUN;end
     else begin acc<=0;error_flag<=1;state<=EMIT;end
    end
    RUN: begin
     acc<=next_acc;
     if(col==15) state<=EMIT;else col<=col+1;
    end
    EMIT: if(out_ready) begin
     if(out_last) state<=IDLE;
     else begin row<=row+1;col<=0;acc<={{8{bias[row+1][31]}},bias[row+1]};state<=RUN;end
    end
   endcase
  end
 end
endmodule
