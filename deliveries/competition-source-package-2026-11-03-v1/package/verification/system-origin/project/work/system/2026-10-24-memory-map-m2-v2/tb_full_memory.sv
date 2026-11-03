`timescale 1ns/1ps
module tb_full_memory;
    reg clk=0,rst_n=1,wren=0;
    reg [31:0] pc=0,addr=0,wdata=0;
    reg [3:0] wstrb=0;
    wire [31:0] inst,rdata;
    integer checks=0,i,b,m,idx,lane,bad=0,write_edges=0;
    reg [31:0] expected_ram[0:8191];
    reg [31:0] old_i,old_d,value;
    GTP_GRS GRS_INST(.GRS_N(1'b1));
    memory_model #(.CASE(9)) memory(.*);
    always #5 clk=~clk;
    function automatic [31:0] rom_pattern(input integer index);
        rom_pattern=(32'h31415927+index*32'h00010103) ^ (index<<19);
    endfunction
    function automatic [31:0] ram_pattern(input integer index);
        ram_pattern=(32'hdeadbeef-index*32'h00030107) ^ (index<<17);
    endfunction
    task ck(input reg ok,input [255:0] label_text);
        begin
            checks=checks+1;
            if(!ok) $fatal(1,"MAP_CHECK_FAIL %0s checks=%0d idx=%0d t=%0t i=%h d=%h",label_text,checks,idx,$time,inst,rdata);
        end
    endtask
    task read_ram(input integer word_index);
        begin
            @(negedge clk);addr=32'h10000+word_index*4;wren=0;wstrb=0;
            @(posedge clk);#1;ck(rdata===expected_ram[word_index],"RAM read/mask/bank");
        end
    endtask
    always @(posedge clk) if(rst_n&&wren) write_edges=write_edges+1;
    initial begin
        $dumpfile("wave.vcd");$dumpvars(1,tb_full_memory);$dumpvars(1,memory);
        if(!$value$plusargs("BAD=%d",bad)) bad=0;
        for(i=0;i<8192;i=i+1) expected_ram[i]=ram_pattern(i);
        repeat(4) @(negedge clk);
        if(bad!=0) begin
            if(bad==1) begin addr=4;wren=1;wstrb=15;end
            if(bad==2) begin addr=32'h10000;wren=1;wstrb=0;end
            if(bad==3) begin addr=32'h10000;wren=0;wstrb=1;end
            @(posedge clk);#2;$fatal(1,"NEGATIVE_NOT_REJECTED");
        end
        // Full ROM coverage, two independent simultaneous read addresses.
        for(i=0;i<8192;i=i+1) begin
            idx=i;@(negedge clk);old_i=inst;old_d=rdata;
            pc=i*4;addr=(8191-i)*4;
            #1;ck(inst===old_i && rdata===old_d,"not asynchronous");
            @(posedge clk);#1;
            ck(inst===rom_pattern(i),"ROM A full capacity");
            ck(rdata===rom_pattern(8191-i),"ROM B independent full capacity");
        end
        $display("FULL_ROM_PASS checks=%0d",checks);
        // Full RAM initial contents and cross-bank selector timing.
        for(i=0;i<8192;i=i+1) begin
            idx=i;@(negedge clk);old_d=rdata;addr=32'h10000+i*4;pc=((i+3073)%8192)*4;
            #1;ck(rdata===old_d,"RAM not asynchronous");
            @(posedge clk);#1;ck(rdata===ram_pattern(i),"RAM initialization full capacity");
            ck(inst===rom_pattern((i+3073)%8192),"ROM across bank simultaneous RAM");
        end
        $display("FULL_RAM_PASS checks=%0d",checks);
        for(b=0;b<8;b=b+1) begin
            for(m=0;m<16;m=m+1) begin
                idx=b*1024+((m%2)?1023:0);value=32'h10203040 ^ (b<<24) ^ (m*32'h01010101);
                @(negedge clk);addr=32'h10000+idx*4;wdata=value;wstrb=m;wren=(m!=0);
                @(posedge clk);#1;
                for(lane=0;lane<4;lane=lane+1)
                    if(m&(1<<lane)) expected_ram[idx][lane*8+:8]=value[lane*8+:8];
                read_ram(idx);
                read_ram(b*1024+511); // unrelated word must retain its own bytes
            end
        end
        ck(write_edges==120,"all nonzero masks exactly once");
        // Repeated identical writes are still two real transactions.
        @(negedge clk);addr=32'h17ffc;wdata=32'h55aaff00;wstrb=15;wren=1;
        repeat(2) begin @(posedge clk);#1;end
        expected_ram[8191]=32'h55aaff00;
        read_ram(8191);ck(write_edges==122,"two repeated writes preserved");
        @(negedge clk);rst_n=0;
        repeat(3) begin @(posedge clk);#1;ck(rdata===32'h55aaff00,"CPU reset retains RAM");end
        @(negedge clk);rst_n=1;pc=32'h8000;addr=32'h18000;
        @(posedge clk);#1;ck(inst===0 && rdata===0,"upper bounds invalid zero");
        @(negedge clk);pc=32'hffff0000;addr=32'hffff0000;
        @(posedge clk);#1;ck(inst===0 && rdata===0,"invalid high address zero");
        $display("MAP_SELFTEST_PASS checks=%0d write_edges=%0d",checks,write_edges);$finish;
    end
    initial begin #1000000;$fatal(1,"MAP_SELFTEST_TIMEOUT");end
endmodule
