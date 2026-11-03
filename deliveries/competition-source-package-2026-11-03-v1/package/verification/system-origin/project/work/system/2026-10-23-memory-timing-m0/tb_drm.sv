`timescale 1ns/1ps
// Verification only; vendor models remain at their original installed paths.
module tb_drm;
  reg clk=0;
  always #5 clk=~clk;
  reg rst=1, we=0;
  reg [13:0] addr=0;
  reg [15:0] data=0;
  reg [3:0] be=0;
  wire [17:0] d0,d1;
  wire [15:0] q0={d0[16:9],d0[7:0]};
  wire [15:0] q1={d1[16:9],d1[7:0]};
  integer checks=0;
  GTP_GRS GRS_INST(.GRS_N(1'b1));
  GTP_DRM18K_E1 #(.GRS_EN("FALSE"),.DATA_WIDTH_A(16),.DATA_WIDTH_B(16),
    .RAM_MODE("SINGLE_PORT"),.WRITE_MODE_A("NORMAL_WRITE"),
    .RST_TYPE("SYNC"),.DOA_REG(0),.DOB_REG(0)) m0(
    .DOA(d0),.DOB(),.DIA({1'b0,data[15:8],1'b0,data[7:0]}),.DIB(18'd0),
    .ADDRA(addr),.ADDRB(14'd0),.ADDRA_HOLD(1'b0),.ADDRB_HOLD(1'b0),
    .BWEA(be),.BWEB(2'd0),.CLKA(clk),.CLKB(clk),.CEA(1'b1),.CEB(1'b0),
    .WEA(we),.WEB(1'b0),.ORCEA(1'b1),.ORCEB(1'b0),.RSTA(rst),.RSTB(rst));
  GTP_DRM18K_E1 #(.GRS_EN("FALSE"),.DATA_WIDTH_A(16),.DATA_WIDTH_B(16),
    .RAM_MODE("SINGLE_PORT"),.WRITE_MODE_A("NORMAL_WRITE"),
    .RST_TYPE("SYNC"),.DOA_REG(1),.DOB_REG(0)) m1(
    .DOA(d1),.DOB(),.DIA({1'b0,data[15:8],1'b0,data[7:0]}),.DIB(18'd0),
    .ADDRA(addr),.ADDRB(14'd0),.ADDRA_HOLD(1'b0),.ADDRB_HOLD(1'b0),
    .BWEA(be),.BWEB(2'd0),.CLKA(clk),.CLKB(clk),.CEA(1'b1),.CEB(1'b0),
    .WEA(we),.WEB(1'b0),.ORCEA(1'b1),.ORCEB(1'b0),.RSTA(rst),.RSTB(rst));
  task ck(input [15:0] want0,input [15:0] want1,input [255:0] label_text);
    begin
      checks=checks+1;
      $display("CHECK %0d %0s time_ps=%0t q0=%04h q1=%04h expected=%04h/%04h",
        checks,label_text,$time,q0,q1,want0,want1);
      if(q0!==want0 || q1!==want1) $fatal(1,"DRM_CHECK_FAIL");
    end
  endtask
  task edge_after;
    begin @(posedge clk); #1; end
  endtask
  initial begin
    $dumpfile("wave.vcd"); $dumpvars(0,tb_drm);
    repeat(3) edge_after();
    @(negedge clk); rst=0;
    repeat(2) edge_after(); ck(0,0,"init_zero");
    @(negedge clk); we=1; data=16'h1234; be=4'b0011;
    edge_after(); ck(0,0,"normal_write_output_hold");
    @(negedge clk); we=0;
    #1; ck(0,0,"read_before_edge_old_output");
    edge_after(); ck(16'h1234,0,"read_after_edge_extra_reg_old");
    edge_after(); ck(16'h1234,16'h1234,"extra_reg_one_more_edge");
    @(negedge clk); addr=14'h0010;
    #1; ck(16'h1234,16'h1234,"address_change_not_async");
    edge_after(); ck(0,16'h1234,"next_word_after_edge");
    edge_after(); ck(0,0,"next_word_extra_reg");
    @(negedge clk); addr=0; we=1; data=16'h00aa; be=4'b0001;
    edge_after();
    @(negedge clk); we=0;
    edge_after(); ck(16'h12aa,0,"low_byte_preserves_high");
    edge_after();
    @(negedge clk); we=1; data=16'hbb00; be=4'b0010;
    edge_after();
    @(negedge clk); we=0;
    edge_after(); ck(16'hbbaa,16'h12aa,"high_byte_preserves_low");
    edge_after(); ck(16'hbbaa,16'hbbaa,"full_readback");
    @(negedge clk); rst=1;
    repeat(2) edge_after(); ck(0,0,"output_reset");
    @(negedge clk); rst=0;
    repeat(3) edge_after(); ck(16'hbbaa,16'hbbaa,"reset_does_not_erase_memory");
    $display("DRM_PASS checks=%0d",checks); $finish;
  end
  initial begin #20000; $fatal(1,"DRM_TIMEOUT"); end
endmodule
