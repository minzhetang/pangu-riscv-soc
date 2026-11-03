`timescale 1ns/1ps
// Verification only. Never writes/forces DUT internals. One process per case.
// RAM-BYTE-0.1: byte-addressed little-endian RAM, containing aligned word read.
// RAM-WSTRB-0.1: SB byte, SH even, SW word aligned; SH-only new TB.
module tb_cpu_selfcheck_v1;
    reg clk = 0;
    reg rst_n = 1;
    wire [31:0] pc, mem_addr, mem_wdata;
    wire mem_wren;
    wire [3:0] mem_wstrb;
    integer byte_lane;
    reg did_store = 0;
    reg [31:0] store_address_snapshot = 0;
    reg [31:0] store_before_snapshot = 0;
    reg [31:0] inst, mem_rdata;
    reg [31:0] imem [0:255];
    reg [31:0] dmem [0:63];
    wire [31:0] observed_store_word = dmem[store_address_snapshot[7:2]];
    reg [31:0] expected_regs [0:31];
    reg [31:0] expected_mem [0:63];
    string case_name, input_dir;
    integer i, cycle = 0, marker_cycle = -1, errors = 0;
    integer stall_cycles = 0, flush_cycles = 0, stores = 0;
    integer checks = 0, mismatches = 0;
    localparam integer MAX_CYCLES = 64;
    wire eei_stop_valid;
    wire [1:0] eei_stop_kind;
    wire [31:0] eei_stop_pc;
    integer want_kind=0, stop_cycle=-1, reset_check=0;
    reg [31:0] want_pc=0, stopped_fetch_pc=0;
`ifdef LEGACY_NO_EEI
    // Observer reports the absence of old-source event ports; no DUT patch/force.
    assign eei_stop_valid=0; assign eei_stop_kind=0; assign eei_stop_pc=0;
`endif

    cpu dut(.clk(clk), .rst_n(rst_n), .pc(pc), .inst(inst),
`ifndef LEGACY_NO_EEI
        .eei_stop_valid(eei_stop_valid), .eei_stop_kind(eei_stop_kind), .eei_stop_pc(eei_stop_pc),
`endif
        .mem_addr(mem_addr), .mem_wdata(mem_wdata),
`ifndef LEGACY_WORD_PORT
        .mem_wstrb(mem_wstrb),
`endif
        .mem_wren(mem_wren), .mem_rdata(mem_rdata));
`ifdef LEGACY_WORD_PORT
    // Explicit old word-only port adaptation; never inspect f3 to repair old CPU.
    assign mem_wstrb = mem_wren ? 4'b1111 : 4'b0000;
`endif

    always #5 clk = ~clk;
    always @(*) begin
        inst = 32'hxxxxxxxx;
        if ((^pc !== 1'bx) && pc[1:0] == 0 && pc < 1024)
            inst = imem[pc[9:2]];
    end
    always @(*) begin
        mem_rdata = 32'hxxxxxxxx;
        if ((^mem_addr !== 1'bx) && mem_addr < 256)
            mem_rdata = dmem[mem_addr[7:2]];
    end

    task check_word(input string kind, input integer index,
                    input [31:0] actual, input [31:0] expected);
        begin
            checks = checks + 1;
            if (actual !== expected) begin
                mismatches = mismatches + 1;
                $display("MISMATCH|%s|%0d|expected=%08h|actual=%08h|xz=%0d",
                         kind, index, expected, actual, (^actual === 1'bx));
            end
        end
    endtask

    task finish_case(input integer watchdog);
        begin
            if (want_kind!=0 && stop_cycle<0) begin
                errors=errors+1;
                $display("PROTOCOL_ERROR|missing_EEI_event");
            end
            // Called #1 after posedge: RF and synchronous memory NBAs settled.
            for (i = 0; i < 32; i = i + 1) begin
                $display("REG|%0d|%08h", i, dut.rf.regs[i]);
                check_word("REG", i, dut.rf.regs[i], expected_regs[i]);
            end
            for (i = 0; i < 64; i = i + 1) begin
                $display("MEM|%0d|%08h", i * 4, dmem[i]);
                check_word("MEM", i * 4, dmem[i], expected_mem[i]);
            end
            $display("METRICS|cycles=%0d|marker_cycle=%0d|checks=%0d|mismatches=%0d|protocol_errors=%0d|stall_cycles=%0d|flush_cycles=%0d|stores=%0d|sim_ns=%0t",
                     cycle, marker_cycle, checks, mismatches, errors,
                     stall_cycles, flush_cycles, stores, $time);
            if (watchdog) begin
                $display("CASE_RESULT|%s|TIMEOUT", case_name);
                $fatal(2, "Completion WB marker missing by cycle limit");
            end else if (mismatches || errors) begin
                $display("CASE_RESULT|%s|FAIL", case_name);
                $fatal(1, "Architectural state or protocol mismatch");
            end else begin
                $display("CASE_RESULT|%s|PASS", case_name);
                $finish;
            end
        end
    endtask

    initial begin
        if (!$value$plusargs("case=%s", case_name) ||
            !$value$plusargs("inputs=%s", input_dir))
            $fatal(1, "Missing case/input path");
        if (!$value$plusargs("stop_kind=%d",want_kind) || !$value$plusargs("stop_pc=%h",want_pc))
            $fatal(1,"Missing explicit EEI expectation");
        if ($test$plusargs("reset_check")) reset_check=1;
        $readmemh({input_dir, "/imem.hex"}, imem);
        $readmemh({input_dir, "/dmem.hex"}, dmem);
        $readmemh({input_dir, "/expected-regs.hex"}, expected_regs);
        $readmemh({input_dir, "/expected-mem.hex"}, expected_mem);
        $dumpfile("wave.vcd");
        $dumpvars(0, tb_cpu_selfcheck_v1);
        $display("BEGIN|%s|timescale=1ns/1ps|clock_period_ns=10|max_cycles=%0d",
                 case_name, MAX_CYCLES);
        // Real asynchronous reset edge, release at falling clock edge, no race.
        #1 rst_n = 0;
        #19 rst_n = 1;
    end

    always @(posedge clk) begin
        if (rst_n === 1'b1) begin
            did_store = 0;
            cycle = cycle + 1;
            // Pre-NBA snapshot: these are the transactions occurring this edge.
            $display("TRACE|cycle=%0d|pc=%08h|inst=%08h|id_pc=%08h|stall=%b|flush=%b|wb_en=%b|wb_rd=%0d|wb_data=%08h",
                     cycle, pc, inst, dut.id_pc, dut.stall_if, dut.flush_if,
                     dut.mem_reg_write, dut.mem_rd, dut.wb_write_data);
            if ((^pc === 1'bx) || pc[1:0] !== 0 || pc >= 1024 || (^inst === 1'bx)) begin
                errors = errors + 1;
                $display("PROTOCOL_ERROR|fetch|pc=%08h|inst=%08h", pc, inst);
            end
            if (dut.stall_if === 1'b1) stall_cycles = stall_cycles + 1;
            if (dut.flush_if === 1'b1) flush_cycles = flush_cycles + 1;
            if ((^ {dut.stall_if, dut.flush_if, mem_wren, dut.ex_mem_to_reg,
                    dut.mem_reg_write} === 1'bx)) begin
                errors = errors + 1;
                $display("PROTOCOL_ERROR|unknown_control");
            end
            if (mem_wren === 1'b0 && mem_wstrb !== 4'b0000) begin
                errors = errors + 1;
                $display("PROTOCOL_ERROR|idle_write_mask|mask=%h", mem_wstrb);
            end
            // mem_addr is also driven during ALU operations: check only active access.
            if ((mem_wren === 1'b1) || (dut.ex_mem_to_reg === 1'b1)) begin
                if ((^mem_addr === 1'bx) || mem_addr >= 256 ||
                    (^dut.ex_funct3 === 1'bx) ||
                    ((mem_wren === 1'b1) &&
                        !((dut.ex_funct3 === 3'b000) ||
                          (dut.ex_funct3 === 3'b001 && mem_addr[0] === 0) ||
                          (dut.ex_funct3 === 3'b010 && mem_addr[1:0] === 0))) ||
                    ((mem_wren !== 1'b1) && dut.ex_funct3 !== 3'b100 &&
                        dut.ex_funct3 !== 3'b000 &&
                        !(((dut.ex_funct3 === 3'b101 || dut.ex_funct3 === 3'b001) && mem_addr[0] === 1'b0) ||
                          (dut.ex_funct3 === 3'b010 && mem_addr[1:0] === 2'b00)))) begin
                    errors = errors + 1;
                    $display("PROTOCOL_ERROR|memory_address|addr=%08h", mem_addr);
                end else if (mem_wren === 1'b1) begin
                    if (^mem_wdata === 1'bx) begin
                        errors = errors + 1;
                        $display("PROTOCOL_ERROR|unknown_store_data");
                    end
                    if (mem_wstrb !== ((dut.ex_funct3 === 3'b000) ? (4'b0001 << mem_addr[1:0]) :
                        ((dut.ex_funct3 === 3'b001) ? (4'b0011 << {mem_addr[1],1'b0}) : 4'b1111))) begin
                        errors = errors + 1;
                        $display("PROTOCOL_ERROR|write_mask|mask=%h", mem_wstrb);
                    end
                    did_store = 1;
                    store_address_snapshot = mem_addr;
                    store_before_snapshot = dmem[mem_addr[7:2]];
                    stores = stores + 1;
                    $display("STORE|cycle=%0d|addr=%08h|data=%08h", cycle, mem_addr, mem_wdata);
                    $display("WSTORE|cycle=%0d|addr=%08h|mask=%h|data=%08h", cycle, mem_addr, mem_wstrb, mem_wdata);
                    // Actual memory update uses public ports only, not private f3.
                    for (byte_lane = 0; byte_lane < 4; byte_lane = byte_lane + 1)
                        if (mem_wstrb[byte_lane] === 1'b1)
                            dmem[mem_addr[7:2]][byte_lane*8 +: 8] <= mem_wdata[byte_lane*8 +: 8];
                end else if (^mem_rdata === 1'bx) begin
                    errors = errors + 1;
                    $display("PROTOCOL_ERROR|unknown_load_data");
                end
            end
            // Read observation includes loads to x0; no DUT-private result wire required.
            // This is a verification observation, not a public MMIO request/retirement interface.
            if (dut.ex_mem_to_reg === 1'b1 && mem_wren === 1'b0)
                $display("READ|cycle=%0d|rd=%0d|f3=%0d|addr=%08h|raw=%08h",
                         cycle, dut.ex_rd, dut.ex_funct3, mem_addr, mem_rdata);
            if (dut.mem_reg_write === 1'b1 && dut.mem_rd != 0) begin
                $display("WB|cycle=%0d|rd=%0d|data=%08h", cycle, dut.mem_rd, dut.wb_write_data);
                if ((^dut.mem_rd === 1'bx) || (^dut.wb_write_data === 1'bx)) begin
                    errors = errors + 1;
                    $display("PROTOCOL_ERROR|unknown_writeback");
                end
                // Program writes x31=90 using ADDI through all actual pipeline stages.
                if (dut.mem_rd == 31 && dut.wb_write_data === 32'd90 && marker_cycle < 0)
                    marker_cycle = cycle;
            end
            #1;
            $display("EEI|cycle=%0d|valid=%b|kind=%0d|pc=%08h",cycle,eei_stop_valid,eei_stop_kind,eei_stop_pc);
            if (eei_stop_valid !== 1'b0 && eei_stop_valid !== 1'b1) begin
                errors=errors+1; $display("PROTOCOL_ERROR|unknown_EEI_valid");
            end
            if (eei_stop_valid === 1'b1) begin
                if (want_kind==0 || eei_stop_kind !== want_kind[1:0] || eei_stop_pc !== want_pc) begin
                    errors=errors+1; $display("PROTOCOL_ERROR|EEI_payload");
                end
                if (stop_cycle<0) begin
                    stop_cycle=cycle; stopped_fetch_pc=pc;
                    $display("STOP_EVENT|cycle=%0d|kind=%0d|pc=%08h",cycle,eei_stop_kind,eei_stop_pc);
                end
                if (pc !== stopped_fetch_pc || {mem_wren,mem_wstrb,dut.ex_mem_to_reg,dut.mem_reg_write} !== 7'b0) begin
                    errors=errors+1; $display("PROTOCOL_ERROR|side_effect_after_stop");
                end
`ifndef LEGACY_NO_EEI
                if ({dut.if_valid,dut.id_valid,dut.ex_valid,dut.mem_valid} !== 4'b0) begin
                    errors=errors+1; $display("PROTOCOL_ERROR|valid_not_drained");
                end
`endif
            end else if (stop_cycle>=0) begin
                errors=errors+1; $display("PROTOCOL_ERROR|EEI_not_sticky");
            end
            if (did_store)
                $display("APPLY|cycle=%0d|addr=%08h|before=%08h|after=%08h", cycle, store_address_snapshot, store_before_snapshot, observed_store_word);
            if (dut.rf.regs[0] !== 32'd0) begin
                errors = errors + 1;
                $display("PROTOCOL_ERROR|x0_changed|actual=%08h", dut.rf.regs[0]);
            end
            if (stop_cycle>=0 && cycle>=stop_cycle+8) begin
                if (reset_check) begin
                    // External reset only; RF/RAM deliberately are NOT reinitialized.
                    #2 rst_n=0;
                    #1;
                    if ({eei_stop_valid,eei_stop_kind,eei_stop_pc} !== 35'b0) begin
                        errors=errors+1; $display("PROTOCOL_ERROR|reset_EEI_not_cleared");
                    end
                    $display("RESET_CHECK|EEI_cleared|RF_RAM_preserved_checked_below");
                end
                finish_case(0);
            end else if (want_kind==0 && marker_cycle >= 0 && cycle >= marker_cycle + 4)
                finish_case(0);
            else if (cycle >= MAX_CYCLES)
                finish_case(1);
        end
    end
endmodule
