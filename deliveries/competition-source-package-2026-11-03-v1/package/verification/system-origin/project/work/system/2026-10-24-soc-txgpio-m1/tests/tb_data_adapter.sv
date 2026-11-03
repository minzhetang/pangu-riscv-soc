`timescale 1ns/1ps
module tb_data_adapter;
    reg [31:0] address=0,write_data=32'h11223344,memory_read_data=32'haabbccdd,io_read_data=32'h55667788;
    reg write_enable=0,io_write_error=0;reg [3:0] write_strobe=0;
    wire [31:0] cpu_read_data,io_write_data;
    wire memory_write_enable,io_select,io_write_enable,invalid_write,write_error;
    wire [3:0] memory_write_strobe,io_write_strobe;wire [7:0] io_address;
    integer checks=0,i,j,k;
    reg [31:0] addresses[0:16];
    soc_data_adapter dut(.*);
    task ck(input reg ok,input [255:0] label_text);
        begin checks=checks+1;if(!ok)$fatal(1,"ADAPTER_FAIL %0s addr=%h",label_text,address);end
    endtask
    task expected(input integer region);
        begin
            ck(io_select===(region==3),"IO exact aperture");
            ck(memory_write_enable===(write_enable&&(region==2)),"RAM write qualify");
            ck(memory_write_strobe===((write_enable&&(region==2))?write_strobe:0),"RAM strobe no IO leak");
            ck(io_write_enable===write_enable,"actual CPU write enable passed");
            ck(io_address===address[7:0],"byte offset low bits retained");
            ck(io_write_data===write_data && io_write_strobe===write_strobe,"IO data/strobe unchanged");
            ck(invalid_write===(write_enable&&(region!=2)&&(region!=3)),"invalid STORE observation");
            ck(write_error===(invalid_write|io_write_error),"error not hidden");
            ck(cpu_read_data===((region==3)?io_read_data:((region==1||region==2)?memory_read_data:0)),"read select");
        end
    endtask
    initial begin
        $dumpfile("wave.vcd");$dumpvars(0,tb_data_adapter);
        addresses[0]=0;addresses[1]=32'h7fff;addresses[2]=32'h8000;
        addresses[3]=32'hffff;addresses[4]=32'h10000;addresses[5]=32'h17fff;addresses[6]=32'h18000;
        addresses[7]=32'h1fffffff;addresses[8]=32'h20000000;addresses[9]=32'h20000001;
        addresses[10]=32'h20000008;addresses[11]=32'h2000000c;addresses[12]=32'h20000010;
        addresses[13]=32'h200000ff;addresses[14]=32'h20000100;addresses[15]=32'hffffffff;addresses[16]=32'h20010000;
        for(i=0;i<17;i=i+1) begin
            address=addresses[i];
            for(j=0;j<16;j=j+1) begin
                write_strobe=j;
                for(k=0;k<4;k=k+1) begin
                    write_enable=k%2;io_write_error=k/2;#1;
                    // Explicit address-set classification, independent of DUT comparator expressions.
                    case(i)
                        0,1:expected(1);
                        4,5:expected(2);
                        8,9,10,11,12,13:expected(3);
                        default:expected(0);
                    endcase
                end
            end
        end
        $display("ADAPTER_UNIT_PASS checks=%0d",checks);$finish;
    end
    initial begin #20000;$fatal(1,"ADAPTER_UNIT_TIMEOUT");end
endmodule
