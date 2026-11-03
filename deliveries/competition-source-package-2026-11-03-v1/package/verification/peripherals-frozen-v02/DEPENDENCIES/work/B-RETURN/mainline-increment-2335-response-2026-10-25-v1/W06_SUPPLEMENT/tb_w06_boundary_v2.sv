`timescale 1ns/1ps
`ifndef CLKS_PER_BIT
`define CLKS_PER_BIT 16
`endif
// Original contract W06, two rounds: one return-edge pulse must not queue;
// consecutive return/next-edge requests use PRE-edge ready, never lookahead.
module tb_w06_boundary;
    localparam integer N=`CLKS_PER_BIT;
    reg clk=0, rst_n, io_sel=0, io_wr_en=0;
    reg [7:0] io_addr=0, gpio_in_async=0;
    reg [31:0] io_wdata=0;
    reg [3:0] io_wstrb=0;
    wire [31:0] io_rdata;
    wire io_wr_error,uart_tx;
    wire [7:0] gpio_out;
    integer errors=0, edge_count=0, accepts=0, rejects=0, e;
    reg [1023:0] wave_file;
    local_regif_txgpio_m1 #(.CLKS_PER_BIT(N)) dut(.*);
    always #5 clk=~clk;
    always @(posedge clk) begin
        edge_count<=edge_count+1;
        if (rst_n && io_sel && io_wr_en) begin
            if (dut.tx_accept) accepts=accepts+1;
            else rejects=rejects+1;
            $display("W06_REQ edge=%0d ready=%b busy=%b accept=%b error=%b data=%02x",
                     edge_count+1,dut.tx_ready,dut.tx_busy,dut.tx_accept,io_wr_error,io_wdata[7:0]);
        end
        if(edge_count>12000) begin $display("W06_FAIL watchdog");$finish;end
    end
    task automatic ck(input bit ok,input [255:0] label);
        if(!ok) begin errors=errors+1;$display("W06_FAIL %0s edge=%0d",label,edge_count);end
    endtask
    task automatic idle_bus;
        begin io_sel=0;io_wr_en=0;io_wstrb=0;end
    endtask
    task automatic drive(input [7:0] data);
        begin io_sel=1;io_wr_en=1;io_addr=0;io_wdata={24'd0,data};io_wstrb=15;end
    endtask
    task automatic first_frame;
        begin
            @(negedge clk);drive(8'h5a);#1;
            ck(dut.tx_ready===1 && io_wr_error===0,"primary ready");
            @(posedge clk);e=edge_count+1;#1;idle_bus();
            ck(uart_tx===0 && dut.tx_busy===1,"primary start");
        end
    endtask
    task automatic return_request;
        begin
            repeat(10*N-1) @(posedge clk);
            @(negedge clk);drive(8'ha6);#1;
            ck(dut.tx_ready===0 && dut.tx_busy===1 && io_wr_error===1,"before return reject");
            @(posedge clk);
            ck(dut.tx_accept===0 && io_wr_error===1,"return edge uses old ready");
            #1;ck(edge_count==e+10*N && dut.tx_ready===1 && dut.tx_busy===0 && uart_tx===1,"exact return edge");
            idle_bus();
        end
    endtask
    task automatic finish_frame;
        begin repeat(10*N+2) @(posedge clk);#1;ck(dut.tx_ready===1 && uart_tx===1,"frame complete");end
    endtask
    initial begin
        rst_n=0; // real X->0 assertion after all always blocks are registered
        if($value$plusargs("WAVE_FILE=%s",wave_file)) begin $dumpfile(wave_file);$dumpvars(0,tb_w06_boundary);end
        repeat(3) @(posedge clk);@(negedge clk);rst_n=1;
        repeat(2) @(posedge clk);#1;
        first_frame();return_request();
        repeat(2*N) begin @(posedge clk);#1;ck(dut.tx_ready===1 && dut.tx_busy===0 && uart_tx===1,"rejected pulse no replay");end
        @(negedge clk);drive(8'h3c);@(posedge clk);#1;idle_bus();finish_frame();
        first_frame();return_request();
        @(negedge clk);drive(8'h3c);#1;ck(io_wr_error===0,"next ready request legal");
        @(posedge clk);ck(dut.tx_accept===1,"first possible next edge accepts");#1;idle_bus();
        ck(edge_count==e+10*N+1 && uart_tx===0 && dut.tx_busy===1,"next edge start");
        finish_frame();
        ck(accepts==4 && rejects==2 && gpio_out===0,"counts no extra side effects");
        if(errors==0)$display("W06_BOUNDARY_PASS N=%0d accepts=%0d rejects=%0d",N,accepts,rejects);
        else $display("W06_BOUNDARY_FAIL N=%0d errors=%0d",N,errors);
        $finish;
    end
endmodule
