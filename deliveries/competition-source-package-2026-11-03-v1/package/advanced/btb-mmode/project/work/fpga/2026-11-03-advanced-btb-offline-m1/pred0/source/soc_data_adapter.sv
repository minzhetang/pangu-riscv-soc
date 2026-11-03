`timescale 1ns/1ps
// A-owned decode. B's 256-byte contract window is unchanged.
module soc_data_adapter(
    input wire [31:0] address,write_data,
    input wire write_enable,input wire [3:0] write_strobe,
    input wire [31:0] memory_read_data,io_read_data,
    input wire [63:0] timer_ticks,
    input wire io_write_error,
    output wire [31:0] cpu_read_data,
    output wire memory_write_enable,output wire [3:0] memory_write_strobe,
    output wire io_select,io_write_enable,output wire [7:0] io_address,
    output wire [31:0] io_write_data,output wire [3:0] io_write_strobe,
    output wire invalid_write,write_error
);
    wire rom_selected=address<32'h00008000;
    wire ram_selected=(address>=32'h00010000)&&(address<32'h00018000);
    wire timer_low=address==32'h20000100;
    wire timer_high=address==32'h20000104;
    assign io_select=address[31:8]==24'h200000;
    assign memory_write_enable=write_enable&&ram_selected;
    assign memory_write_strobe=memory_write_enable?write_strobe:4'd0;
    assign io_write_enable=write_enable;
    assign io_address=address[7:0];
    assign io_write_data=write_data;
    assign io_write_strobe=write_strobe;
    assign cpu_read_data=timer_low?timer_ticks[31:0]:timer_high?timer_ticks[63:32]:
        io_select?io_read_data:((rom_selected||ram_selected)?memory_read_data:32'd0);
    // Timer is read-only. This is an observation, NOT a CPU trap.
    assign invalid_write=write_enable&&!ram_selected&&!io_select;
    assign write_error=invalid_write|io_write_error;
endmodule
