module tb_cpu;
    reg clk, rst_n;
    wire [31:0] pc;
    wire [31:0] inst;
    wire [31:0] mem_addr, mem_wdata, mem_rdata;
    wire mem_wren;
    
    reg [31:0] imem [0:255];
    reg [31:0] dmem [0:255];
    
    cpu u_cpu (
        .clk(clk), .rst_n(rst_n), .pc(pc),
        .inst(inst), .mem_addr(mem_addr), .mem_wdata(mem_wdata),
        .mem_wren(mem_wren), .mem_rdata(mem_rdata)
    );
    
    always #5 clk = ~clk;
    assign inst = imem[pc[7:2]];
    assign mem_rdata = dmem[mem_addr[7:2]];
    
    always @(posedge clk) begin
        if (mem_wren)
            dmem[mem_addr[7:2]] <= mem_wdata;
    end
    
    initial begin
        for (integer i = 0; i < 256; i = i + 1) begin
            imem[i] = 32'd0;
            dmem[i] = 32'd0;
        end
        
        // 测试程序机器码
        imem[0] = 32'h00A00093;  // addi x1, x0, 10
        imem[1] = 32'h00500113;  // addi x2, x0, 5
        imem[2] = 32'h002081B3;  // add x3, x1, x2
        imem[3] = 32'h40208233;  // sub x4, x1, x2
        imem[4] = 32'h0020F2B3;  // and x5, x1, x2
        imem[5] = 32'h0020E333;  // or x6, x1, x2
        imem[6] = 32'h0020C3B3;  // xor x7, x1, x2
        imem[7] = 32'h0FF00493;  // addi x9, x0, 255
        imem[8] = 32'h00902023;  // sw x9, 0(x0)
        imem[9] = 32'h00002503;  // lw x10, 0(x0)
        imem[10] = 32'h00000013; // nop
        imem[11] = 32'h00000013;
      imem[12] = 32'h00001033;  // sll x0, x0, x0 (示例)
imem[13] = 32'h00005033;  // srl x0, x0, x0
imem[14] = 32'h40005033;  // sra x0, x0, x0
imem[15] = 32'h00F0E133;  // ori x2, x1, 15 (示例)
imem[16] = 32'h000000EF;  // jal x1, 0
imem[17] = 32'h000080E7;  // jalr x1, x1, 0
imem[18] = 32'h00308463;  // bne x1, x3, 8 (示例)
        clk = 0;
        rst_n = 0;
        #15 rst_n = 1;
        #1000;
        $finish;
    end
    
    initial begin
        $dumpfile("tb_cpu.vcd");
        $dumpvars(0, tb_cpu);
    end
endmodule