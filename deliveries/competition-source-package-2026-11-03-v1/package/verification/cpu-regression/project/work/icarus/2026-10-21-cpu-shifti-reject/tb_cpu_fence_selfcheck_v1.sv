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

    // Observer-only dynamic instruction identity. No DUT state is written/forced.
    reg obs_if_valid=0, obs_ex_valid=0, obs_mem_valid=0, obs_wb_valid=0;
    reg [31:0] obs_if_pc=0, obs_ex_pc=0, obs_mem_pc=0, obs_wb_pc=0;
    reg [31:0] obs_if_word=0, obs_ex_word=0, obs_mem_word=0, obs_wb_word=0;
    integer obs_cycle=0;
    reg [7:0] obs_kind=0;
    reg [31:0] obs_addr=0, obs_data=0, obs_after=0, obs_event_pc=0, obs_event_word=0;
    reg [3:0] obs_mask=0;
    wire [31:0] obs_written_word=dmem[obs_addr[7:2]];

    task observer_error(input string why);
        begin
            // Fatal is deliberate: observer and RAM process do not race on errors.
            $display("PROTOCOL_ERROR|fence_observer|%s",why);
            $fatal(1,"RAM-FENCE observer mismatch");
        end
    endtask
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            obs_if_valid<=0; obs_ex_valid<=0; obs_mem_valid<=0; obs_wb_valid<=0;
            obs_cycle=0;
        end else begin
            obs_cycle=obs_cycle+1;
            // These tokens model actual IF/ID accepts, stalls, bubbles and flushes.
            if (obs_if_valid && (dut.if_pc !== obs_if_pc || dut.if_inst !== obs_if_word)) observer_error("IF identity");
            if (obs_ex_valid && dut.id_pc !== obs_ex_pc) observer_error("EX identity");
            if (obs_mem_valid && dut.ex_pc !== obs_mem_pc) observer_error("MEM identity");
            if (obs_ex_valid && obs_ex_word[6:0]==7'h0f) begin
                if (obs_ex_word[14:12] !== 3'b000 ||
                    {dut.id_reg_write,dut.id_mem_write,dut.id_mem_to_reg,dut.id_branch,dut.id_jump,dut.flush_if} !== 6'b0)
                    observer_error("active FENCE EX control");
            end
            if (obs_wb_valid && obs_wb_word[6:0]==7'h0f && dut.mem_reg_write !== 1'b0) observer_error("FENCE WB");
            obs_kind=0; obs_addr=0; obs_data=0; obs_after=0; obs_mask=0;
            obs_event_pc=obs_mem_pc; obs_event_word=obs_mem_word;
            if (obs_mem_valid && obs_mem_word[6:0]==7'h0f) begin
                if ({dut.ex_reg_write,mem_wren,dut.ex_mem_to_reg,dut.ex_branch,dut.ex_jump,mem_wstrb} !== 9'b0)
                    observer_error("active FENCE MEM control");
                obs_kind="F";
            end else if (mem_wren === 1'b1) begin
                if (!obs_mem_valid || obs_mem_word[6:0]!==7'h23) observer_error("unidentified store");
                obs_kind="W"; obs_addr=mem_addr; obs_data=mem_wdata; obs_mask=mem_wstrb;
            end else if (dut.ex_mem_to_reg === 1'b1) begin
                if (!obs_mem_valid || obs_mem_word[6:0]!==7'h03) observer_error("unidentified load");
                obs_kind="R"; obs_addr=mem_addr; obs_data=dut.mem_load_data; obs_after=mem_rdata;
            end
            obs_wb_valid<=obs_mem_valid; obs_wb_pc<=obs_mem_pc; obs_wb_word<=obs_mem_word;
            obs_mem_valid<=obs_ex_valid; obs_mem_pc<=obs_ex_pc; obs_mem_word<=obs_ex_word;
            obs_ex_valid<=obs_if_valid && !dut.flush_id && !dut.stall_if;
            obs_ex_pc<=obs_if_pc; obs_ex_word<=obs_if_word;
            if (dut.flush_if) obs_if_valid<=0;
            else if (!dut.stall_if) begin obs_if_valid<=1; obs_if_pc<=pc; obs_if_word<=inst; end
            #1;
            if (obs_kind=="W") obs_after=obs_written_word;
            if (obs_kind!=0) begin
                if (^{obs_event_pc,obs_event_word,obs_addr,obs_data,obs_mask,obs_after}===1'bx) observer_error("active event X/Z");
                $display("RAM|cycle=%0d|kind=%s|pc=%08h|word=%08h|addr=%08h|data=%08h|mask=%h|after=%08h",
                    obs_cycle,obs_kind,obs_event_pc,obs_event_word,obs_addr,obs_data,obs_mask,obs_after);
            end
        end
    end

    cpu dut(.clk(clk), .rst_n(rst_n), .pc(pc), .inst(inst),
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
            if (did_store)
                $display("APPLY|cycle=%0d|addr=%08h|before=%08h|after=%08h", cycle, store_address_snapshot, store_before_snapshot, observed_store_word);
            if (dut.rf.regs[0] !== 32'd0) begin
                errors = errors + 1;
                $display("PROTOCOL_ERROR|x0_changed|actual=%08h", dut.rf.regs[0]);
            end
            if (marker_cycle >= 0 && cycle >= marker_cycle + 4)
                finish_case(0);
            else if (cycle >= MAX_CYCLES)
                finish_case(1);
        end
    end
endmodule
