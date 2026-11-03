`timescale 1ns/1ps
module tb_timer_unit;
    reg clk=0,rst_n=0;wire [63:0] ticks,carry;
    reg [31:0] address=0,write_data=32'hcafef00d;
    reg write_enable=0;reg [3:0] write_strobe=15;
    wire [31:0] cpu_read_data,io_write_data;wire [3:0] memory_write_strobe,io_write_strobe;
    wire memory_write_enable,io_select,io_write_enable,invalid_write,write_error;wire [7:0] io_address;
    integer checks=0,i;reg [63:0] expected=0,expected_carry=64'h00000000fffffff0;
    reg [31:0] hi1,lo,hi2;integer retries=0;
    cycle_counter64 a(.clk(clk),.rst_n(rst_n),.ticks(ticks));
    cycle_counter64 #(.RESET_VALUE(64'h00000000fffffff0)) b(.clk(clk),.rst_n(rst_n),.ticks(carry));
    soc_data_adapter d(.address(address),.write_data(write_data),.write_enable(write_enable),.write_strobe(write_strobe),
        .memory_read_data(32'h12345678),.io_read_data(32'h87654321),.timer_ticks(ticks),.io_write_error(1'b0),
        .cpu_read_data(cpu_read_data),.memory_write_enable(memory_write_enable),.memory_write_strobe(memory_write_strobe),
        .io_select(io_select),.io_write_enable(io_write_enable),.io_address(io_address),.io_write_data(io_write_data),
        .io_write_strobe(io_write_strobe),.invalid_write(invalid_write),.write_error(write_error));
    always #5 clk=~clk;
    task check(input bit ok);begin if(!ok)$fatal(1,"UNIT_CHECK %0d",checks);checks=checks+1;end endtask
    always @(posedge clk) begin
        if(rst_n) begin expected=expected+1;expected_carry=expected_carry+1;end
        else begin expected=0;expected_carry=64'hfffffff0;end
        #1;check(ticks===expected);check(carry===expected_carry);
    end
    task probe(input [31:0] addr,input bit wr,input [3:0] mask,input [31:0] data,input bit ram,input bit io,input bit err);
        begin @(negedge clk);address=addr;write_enable=wr;write_strobe=mask;#1;
            check(cpu_read_data===data);check(memory_write_enable==ram);check(io_select==io);check(write_error==err);
        end
    endtask
    initial begin
        $dumpfile("wave.vcd");$dumpvars(0,tb_timer_unit);
        repeat(2)@(negedge clk);check(ticks==0);rst_n=1;
        // Consume a high/low/high read across the low-word carry, then retry.
        hi1=carry[63:32];repeat(18)@(negedge clk);lo=carry[31:0];hi2=carry[63:32];
        check(hi1!=hi2);retries=retries+1;
        hi1=carry[63:32];@(negedge clk);lo=carry[31:0];@(negedge clk);hi2=carry[63:32];
        check(hi1==hi2);check(({hi2,lo})>=64'h100000000);check(retries==1);
        probe(0,0,0,32'h12345678,0,0,0);
        probe(32'h10000,1,15,32'h12345678,1,0,0);
        probe(32'h20000000,0,0,32'h87654321,0,1,0);
        probe(32'h20000104,0,0,0,0,0,0);
        for(i=0;i<16;i=i+1)begin
            @(negedge clk);address=32'h20000100;write_enable=1;write_strobe=i;#1;
            check(cpu_read_data===ticks[31:0]);check(!memory_write_enable&&!io_select&&write_error);
        end
        for(i=1;i<4;i=i+1)probe(32'h20000100+i,0,0,0,0,0,0);
        probe(32'h20000108,0,0,0,0,0,0);
        @(negedge clk);write_enable=0;rst_n=0;#1;check(ticks===0);
        repeat(2)@(negedge clk);rst_n=1;@(negedge clk);check(ticks==1);
        $display("TIMER_UNIT_PASS checks=%0d carry_retries=%0d",checks,retries);$finish;
    end
    initial begin #10000;$fatal(1,"UNIT_TIMEOUT");end
endmodule
