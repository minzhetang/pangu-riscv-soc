`timescale 1ns/1ps
// Verification memory only; not an inferred/mapped Pango DRM implementation.
module memory_model #(parameter integer LATENCY=0)(
    input wire clk,rst_n,
    input wire [31:0] pc,output wire [31:0] inst,
    input wire [31:0] addr,wdata,input wire wren,input wire [3:0] wstrb,
    output wire [31:0] rdata
);
    reg [31:0] rom[0:8191],ram[0:8191];
    reg [31:0] iq=0,dq=0,async_data;
    integer rom_bytes=32768,ram_bytes=32768,ram_base=65536,words,i,lane;
    reg [2047:0] image,ram_image;
    initial begin
        if(!$value$plusargs("IMAGE=%s",image) || !$value$plusargs("WORDS=%d",words)) $fatal(1,"INPUT image");
        if(!$value$plusargs("ROM_BYTES=%d",rom_bytes)) rom_bytes=32768;
        if(!$value$plusargs("RAM_BYTES=%d",ram_bytes)) ram_bytes=32768;
        if(!$value$plusargs("RAM_BASE=%d",ram_base)) ram_base=65536;
        if(words<1 || words>8192 || rom_bytes<4 || rom_bytes>32768 || ram_bytes<4 || ram_bytes>32768 || (ram_bytes%4)!=0)
            $fatal(1,"INPUT bounds");
        for(i=0;i<8192;i=i+1) begin rom[i]=0;ram[i]=32'ha5a5a5a5;end
        $readmemh(image,rom,0,words-1);
        if($value$plusargs("RAM_IMAGE=%s",ram_image)) $readmemh(ram_image,ram,0,(ram_bytes/4)-1);
    end
    wire [31:0] async_inst=(pc<rom_bytes)?rom[pc>>2]:32'd0;
    always @* begin
        async_data=0;
        if(addr>=ram_base && addr<(ram_base+ram_bytes)) async_data=ram[(addr-ram_base)>>2];
        else if(addr<rom_bytes) async_data=rom[addr>>2];
    end
    assign inst=LATENCY ? iq : async_inst;
    assign rdata=LATENCY ? dq : async_data;
    // Sample every rising edge, including CPU reset for ROM first-word warmup.
    // Read-before-write on this model; external collision guarantees unclaimed.
    always @(posedge clk) begin
        iq<=async_inst;dq<=async_data;
        if(rst_n && wren) begin
            if((^{addr,wdata,wstrb})===1'bx || addr<ram_base || addr>=ram_base+ram_bytes || wstrb==0)
                $fatal(1,"MEMORY_PROTOCOL store");
            for(lane=0;lane<4;lane=lane+1)
                if(wstrb[lane]) ram[(addr-ram_base)>>2][8*lane+:8]<=wdata[8*lane+:8];
        end
    end
endmodule
