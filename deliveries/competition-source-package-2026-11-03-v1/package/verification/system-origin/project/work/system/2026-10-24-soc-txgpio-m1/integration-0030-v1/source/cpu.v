// =================================================================
// 五级流水线 CPU 顶层模块
// 支持指令: add, sub, and, or, xor, sll, srl, sra, addi, ori, lw, sw, beq, bne, jal, jalr
// 冒险处理: 数据冒险 (load-use 停顿 + 转发) + 控制冒险 (分支冲刷)
// =================================================================
module cpu #(
    parameter integer SYNC_MEMORY = 0
) (
    input wire        clk,
    input wire        rst_n,
    output wire [31:0] pc,
    input wire [31:0] inst,
    output wire [31:0] mem_addr,
    output wire [31:0] mem_wdata,
    output wire        mem_wren,
    output wire [3:0]  mem_wstrb,
    input wire [31:0]  mem_rdata,
    output reg        eei_stop_valid,
    output reg [1:0]  eei_stop_kind,
    output reg [31:0] eei_stop_pc
);
    // Fixed one-edge synchronous memory adapter, single original rising clock.
    // Phase 0: memory samples stable requests; phase 1: pipeline consumes replies.
    // Default 0 preserves the historical combinational-memory timing contract.
    reg memory_phase;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) memory_phase <= 1'b0;
        else memory_phase <= ~memory_phase;
    end
    wire pipeline_advance = (SYNC_MEMORY == 0) || memory_phase;
    wire memory_write_edge = (SYNC_MEMORY == 0) || (rst_n && !memory_phase);
    // ----------------------------------------------
    // 流水线寄存器定义
    // ----------------------------------------------
    // IF/ID
    reg [31:0] if_pc, if_inst;
    // ID/EX
    reg [31:0] id_pc, id_rs1_data, id_rs2_data, id_imm;
    reg [4:0]  id_rs1, id_rs2, id_rd;
    reg        id_reg_write, id_mem_write, id_mem_to_reg, id_alu_src, id_branch, id_jump;
    reg [4:0]  id_alu_ctrl;
    reg [2:0]  id_funct3;
    reg        id_auipc;
    // EX/MEM
    reg [31:0] ex_pc, ex_alu_result, ex_rs2_data;
    reg [4:0]  ex_rd;
    reg        ex_reg_write, ex_mem_write, ex_mem_to_reg, ex_branch, ex_jump;
    reg [2:0]  ex_funct3;
    // MEM/WB
    reg [31:0] mem_alu_result, mem_mem_rdata;
    reg [4:0]  mem_rd;
    reg        mem_reg_write, mem_mem_to_reg;

    wire stall_if, flush_if, flush_id;
    // A-EEI-STOP-0.1: validity is independent of word and side effects.
    reg if_valid, id_valid, ex_valid, mem_valid;
    reg [1:0] id_system_kind;
    localparam EEI_RUN=2'd0, EEI_DRAIN=2'd1, EEI_STOP=2'd2;
    reg [1:0] eei_state;
    wire eei_detect = (eei_state == EEI_RUN) && id_valid && (id_system_kind != 0);
    wire eei_hold = (eei_state != EEI_RUN) || eei_detect;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            if_valid<=0; id_valid<=0; ex_valid<=0; mem_valid<=0;
            id_system_kind<=0; eei_state<=EEI_RUN;
            eei_stop_valid<=0; eei_stop_kind<=0; eei_stop_pc<=0;
        end else if (pipeline_advance) begin
            // Older MEM/WB advance on the detection edge and drain edge.
            mem_valid<=ex_valid;
            ex_valid<=id_valid && !eei_hold;
            if (eei_hold) begin
                if_valid<=0; id_valid<=0; id_system_kind<=0;
            end else begin
                if (flush_if) if_valid<=0;
                else if (!stall_if) if_valid<=1;
                if (flush_id || stall_if) begin id_valid<=0; id_system_kind<=0; end
                else begin
                    id_valid<=if_valid;
                    id_system_kind<=!if_valid ? 2'd0 :
                        (if_inst == 32'h00000073) ? 2'd1 :
                        (if_inst == 32'h00100073) ? 2'd2 :
                        // Local fatal kind3: patterns, unsupported R-type, or nonbase shift-I encoding.
                        ((if_inst[15:0] == 16'h0000) || (if_inst == 32'hffff_ffff) ||
                         ((if_inst[6:0] == 7'b0010011) &&
                          (((if_inst[14:12] == 3'b001) && (if_inst[31:25] != 7'd0)) ||
                           ((if_inst[14:12] == 3'b101) && (if_inst[31:25] != 7'd0) && (if_inst[31:25] != 7'd32)))) ||
                         ((if_inst[6:0] == 7'b0110011) &&
                          ((if_inst[14:12] == 3'b001) || (if_inst[14:12] == 3'b100) ||
                           (if_inst[14:12] == 3'b010) || (if_inst[14:12] == 3'b011) ||
                           (if_inst[14:12] == 3'b110) || (if_inst[14:12] == 3'b111)) &&
                          (if_inst[31:25] != 7'd0)) ||
                         ((if_inst[6:0] == 7'b0110011) &&
                          ((if_inst[14:12] == 3'b000) || (if_inst[14:12] == 3'b101)) &&
                          (if_inst[31:25] != 7'd0) && (if_inst[31:25] != 7'd32))) ? 2'd3 : 2'd0;
                end
            end
            if (eei_state == EEI_RUN && eei_detect) begin
                eei_stop_kind<=id_system_kind; eei_stop_pc<=id_pc;
                eei_state<=EEI_DRAIN;
            end else if (eei_state == EEI_DRAIN) begin
                // No-wait RAM: last older MEM instruction writes RF this edge.
                eei_stop_valid<=1; eei_state<=EEI_STOP;
            end
        end
    end

    // ----------------------------------------------
    // IF 阶段
    // ----------------------------------------------
    reg [31:0] pc_reg;
    assign pc = pc_reg;
    wire [31:0] pc_plus4 = pc_reg + 4;
    wire [31:0] pc_next;

    // 冒险控制信号
    wire        branch_taken;
    wire [31:0] branch_target;
    wire [31:0] jump_target;

    // 缺省下一跳 PC
    assign pc_next = (flush_if) ? (id_jump ? jump_target : branch_target) : 
                     (stall_if) ? pc_reg : pc_plus4;

    // PC 寄存器更新
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) pc_reg <= 32'd0;
        else if (pipeline_advance && !eei_hold) pc_reg <= pc_next;
    end

    // IF/ID 寄存器 (带冲刷和停顿)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            if_pc   <= 32'd0;
            if_inst <= 32'd0;
        end else if (pipeline_advance && (flush_if || eei_hold)) begin
            if_pc   <= 32'd0;
            if_inst <= 32'd0;
        end else if (pipeline_advance && !stall_if) begin
            if_pc   <= pc_reg;
            if_inst <= inst;
        end
    end

    // ----------------------------------------------
    // ID 阶段
    // ----------------------------------------------
    wire [6:0] opcode = if_inst[6:0];
    wire [4:0] rs1 = if_inst[19:15];
    wire [4:0] rs2 = if_inst[24:20];
    wire [4:0] rd  = if_inst[11:7];
    wire [2:0] funct3 = if_inst[14:12];
    wire [6:0] funct7 = if_inst[31:25];

    // 立即数扩展
    reg [31:0] imm_ext;
    always @(*) begin
        case (opcode)
            7'b0010011,7'b0000011,7'b1100111: imm_ext = {{20{if_inst[31]}}, if_inst[31:20]};
            7'b0110111,7'b0010111: imm_ext = {if_inst[31:12], 12'b0};
            7'b0100011: imm_ext = {{20{if_inst[31]}}, if_inst[31:25], if_inst[11:7]};
            7'b1100011: imm_ext = {{20{if_inst[31]}}, if_inst[7], if_inst[30:25], if_inst[11:8], 1'b0};
            7'b1101111: imm_ext = {{12{if_inst[31]}}, if_inst[19:12], if_inst[20], if_inst[30:21], 1'b0};
            default: imm_ext = 32'd0;
        endcase
    end

    // 控制器
    wire        reg_write_id, mem_write_id, branch_id, mem_to_reg_id, alu_src_id, jump_id;
    wire [4:0]  alu_ctrl_id;
    control ctrl (
        .opcode   (opcode),
        .funct3   (funct3),
        .funct7   (funct7),
        .reg_write(reg_write_id),
        .mem_write(mem_write_id),
        .branch   (branch_id),
        .mem_to_reg(mem_to_reg_id),
        .alu_src  (alu_src_id),
        .alu_ctrl (alu_ctrl_id),
        .jump     (jump_id)
    );

    // 寄存器堆 (写端口来自 WB 阶段)
    wire [31:0] rs1_data, rs2_data;
    wire [31:0] wb_write_data;
    regfile rf (
        .clk   (clk),
        .we    (pipeline_advance && mem_valid && mem_reg_write),
        .waddr (mem_rd),
        .wdata (wb_write_data),
        .raddr1(rs1),
        .raddr2(rs2),
        .rdata1(rs1_data),
        .rdata2(rs2_data)
    );

    // Same-edge WB -> ID bypass; keep the register file on its original edge.
    wire [31:0] wb_id_rs1 = (mem_reg_write && (mem_rd != 5'd0) && (mem_rd == rs1))
        ? wb_write_data : rs1_data;
    wire [31:0] wb_id_rs2 = (mem_reg_write && (mem_rd != 5'd0) && (mem_rd == rs2))
        ? wb_write_data : rs2_data;

    // ID/EX 寄存器 (带冲刷)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            id_pc          <= 32'd0;
            id_rs1_data    <= 32'd0;
            id_rs2_data    <= 32'd0;
            id_imm         <= 32'd0;
            id_rs1         <= 5'd0;
            id_rs2         <= 5'd0;
            id_rd          <= 5'd0;
            id_reg_write   <= 1'b0;
            id_mem_write   <= 1'b0;
            id_mem_to_reg  <= 1'b0;
            id_alu_src     <= 1'b0;
            id_branch      <= 1'b0;
            id_jump        <= 1'b0;
            id_alu_ctrl    <= 5'd0;
            id_funct3      <= 3'd0;
            id_auipc       <= 1'b0;
        end else if (pipeline_advance && (flush_id || eei_hold)) begin
            id_auipc       <= 1'b0;
            // 冲刷：清空控制信号，防止错误执行
            id_reg_write   <= 1'b0;
            id_mem_write   <= 1'b0;
            id_branch      <= 1'b0;
            id_jump        <= 1'b0;
            id_mem_to_reg  <= 1'b0;
            // 数据可不清零，但控制信号必须清零
        end else if (pipeline_advance && stall_if) begin
            id_auipc       <= 1'b0;
            // Hold PC/IF-ID, but let the load advance and inject one EX bubble.
            id_reg_write   <= 1'b0;
            id_mem_write   <= 1'b0;
            id_mem_to_reg  <= 1'b0;
            id_branch      <= 1'b0;
            id_jump        <= 1'b0;
        end else if (pipeline_advance) begin
            id_pc          <= if_pc;
            id_rs1_data    <= wb_id_rs1;
            id_rs2_data    <= wb_id_rs2;
            id_imm         <= imm_ext;
            id_rs1         <= rs1;
            id_rs2         <= rs2;
            id_rd          <= rd;
            id_reg_write   <= if_valid && reg_write_id;
            id_mem_write   <= if_valid && mem_write_id;
            id_mem_to_reg  <= if_valid && mem_to_reg_id;
            id_alu_src     <= alu_src_id;
            id_branch      <= if_valid && branch_id;
            id_jump        <= if_valid && jump_id;
            id_alu_ctrl    <= alu_ctrl_id;
            id_funct3      <= funct3;
            id_auipc       <= (opcode == 7'b0010111);
        end
    end

    // ----------------------------------------------
    // EX 阶段
    // ----------------------------------------------
    // EX/MEM has the newest producer. A matching load holds its place but
    // cannot forward its ALU address or fall back to an older WB producer.
    wire ex_match_rs1 = ex_reg_write && (ex_rd != 5'd0) && (ex_rd == id_rs1);
    wire ex_match_rs2 = ex_reg_write && (ex_rd != 5'd0) && (ex_rd == id_rs2);
    wire wb_match_rs1 = mem_reg_write && (mem_rd != 5'd0) && (mem_rd == id_rs1);
    wire wb_match_rs2 = mem_reg_write && (mem_rd != 5'd0) && (mem_rd == id_rs2);
    wire [31:0] forward_rs1 = ex_match_rs1
        ? (ex_mem_to_reg ? id_rs1_data : ex_alu_result)
        : (wb_match_rs1 ? wb_write_data : id_rs1_data);
    wire [31:0] forward_rs2 = ex_match_rs2
        ? (ex_mem_to_reg ? id_rs2_data : ex_alu_result)
        : (wb_match_rs2 ? wb_write_data : id_rs2_data);
    wire [31:0] alu_src1 = id_auipc ? id_pc : forward_rs1;
    wire [31:0] alu_src2 = id_alu_src ? id_imm : forward_rs2;
    wire [31:0] alu_result;
    wire        alu_zero;
    alu alu_inst (
        .a   (alu_src1),
        .b   (alu_src2),
        .ctrl(id_alu_ctrl),
        .result(alu_result),
        .zero(alu_zero)
    );

    // 分支跳转地址计算
    assign branch_target = id_pc + id_imm;
    // For active jumps, control.v maps JAL to alu_src=0 and JALR to 1.
    assign jump_target = id_alu_src
        ? ((forward_rs1 + id_imm) & 32'hffff_fffe) : (id_pc + id_imm);
    // Branch decision: forwarded BLT/BGE signed, BLTU/BGEU unsigned; other paths unchanged.
    assign branch_taken = id_branch &&
        ((id_funct3 == 3'b100)
            ? ($signed(forward_rs1) < $signed(forward_rs2))
            : ((id_funct3 == 3'b101)
                ? ($signed(forward_rs1) >= $signed(forward_rs2))
                : ((id_funct3 == 3'b110)
                    ? ($unsigned(forward_rs1) < $unsigned(forward_rs2))
                    : ((id_funct3 == 3'b111)
                        ? ($unsigned(forward_rs1) >= $unsigned(forward_rs2))
                        : ((id_funct3 == 3'b000) ? alu_zero : ~alu_zero)))));

    // EX/MEM 寄存器
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ex_pc          <= 32'd0;
            ex_alu_result  <= 32'd0;
            ex_rs2_data    <= 32'd0;
            ex_rd          <= 5'd0;
            ex_reg_write   <= 1'b0;
            ex_mem_write   <= 1'b0;
            ex_mem_to_reg  <= 1'b0;
            ex_branch      <= 1'b0;
            ex_jump        <= 1'b0;
            ex_funct3      <= 3'd0;
        end else if (pipeline_advance) begin
            ex_pc          <= id_pc;
            ex_alu_result  <= id_jump ? (id_pc + 32'd4) : alu_result;
            ex_rs2_data    <= forward_rs2;
            ex_rd          <= id_rd;
            ex_reg_write   <= id_valid && !eei_hold && id_reg_write;
            ex_mem_write   <= id_valid && !eei_hold && id_mem_write;
            ex_mem_to_reg  <= id_valid && !eei_hold && id_mem_to_reg;
            ex_branch      <= id_valid && !eei_hold && id_branch;
            ex_jump        <= id_valid && !eei_hold && id_jump;
            ex_funct3      <= id_funct3;
        end
    end

    // ----------------------------------------------
    // MEM 阶段
    // ----------------------------------------------
    assign mem_addr  = ex_alu_result;
    // RAM-WSTRB-0.1: active SB writes only rs2[7:0] into its byte lane.
    assign mem_wdata = (ex_mem_write && (ex_funct3 == 3'b000))
        ? ({24'd0, ex_rs2_data[7:0]} << {ex_alu_result[1:0], 3'b000})
        : (ex_mem_write && (ex_funct3 == 3'b001))
        ? ({16'd0, ex_rs2_data[15:0]} << {ex_alu_result[1], 4'b0000})
        : ex_rs2_data;
    assign mem_wstrb = !mem_wren ? 4'b0000
        : (ex_funct3 == 3'b000) ? (4'b0001 << ex_alu_result[1:0])
        : (ex_funct3 == 3'b001) ? (4'b0011 << {ex_alu_result[1], 1'b0})
        : (ex_funct3 == 3'b010) ? 4'b1111 : 4'b0000;
    assign mem_wren  = ex_mem_write && memory_write_edge;
    // LB/LBU/aligned LH/LHU: external RAM returns the containing aligned word.
    wire [7:0] mem_load_byte = mem_rdata >> {ex_alu_result[1:0], 3'b000};
    wire [15:0] mem_load_half = ex_alu_result[1] ? mem_rdata[31:16] : mem_rdata[15:0];
    wire [31:0] mem_load_data = (ex_funct3 == 3'b100)
        ? {24'd0, mem_load_byte}
        : (ex_funct3 == 3'b000) ? {{24{mem_load_byte[7]}}, mem_load_byte}
        : (ex_funct3 == 3'b101) ? {16'd0, mem_load_half}
        : (ex_funct3 == 3'b001) ? {{16{mem_load_half[15]}}, mem_load_half}
        : mem_rdata;

    // MEM/WB 寄存器
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mem_alu_result <= 32'd0;
            mem_mem_rdata  <= 32'd0;
            mem_rd         <= 5'd0;
            mem_reg_write  <= 1'b0;
            mem_mem_to_reg <= 1'b0;
        end else if (pipeline_advance) begin
            mem_alu_result <= ex_alu_result;
            mem_mem_rdata  <= mem_load_data;
            mem_rd         <= ex_rd;
            mem_reg_write  <= ex_valid && ex_reg_write;
            mem_mem_to_reg <= ex_valid && ex_mem_to_reg;
        end
    end

    // ----------------------------------------------
    // WB 阶段
    // ----------------------------------------------
    assign wb_write_data = mem_mem_to_reg ? mem_mem_rdata : mem_alu_result;

    // ----------------------------------------------
    // 冒险控制单元 (Hazard Detection)
    // ----------------------------------------------
    // Detect an EX load against the actual source operands of the ID instruction.
    wire id_uses_rs1 = (opcode == 7'b0110011) || (opcode == 7'b0010011) ||
                       (opcode == 7'b0000011) || (opcode == 7'b0100011) ||
                       (opcode == 7'b1100011) || (opcode == 7'b1100111);
    wire id_uses_rs2 = (opcode == 7'b0110011) || (opcode == 7'b0100011) ||
                       (opcode == 7'b1100011);
    wire lw_stall = id_reg_write && id_mem_to_reg && (id_rd != 5'd0) &&
                    ((id_uses_rs1 && (id_rd == rs1)) ||
                     (id_uses_rs2 && (id_rd == rs2)));
    // 控制冒险: 分支或跳转在 EX 阶段确定时需要冲刷 IF/ID 和 ID/EX
    wire control_flush = (branch_taken || id_jump);
    assign flush_if = control_flush;
    assign flush_id = control_flush;
    assign stall_if = lw_stall;   // Hold PC/IF-ID; ID/EX receives a side-effect-free bubble.

endmodule
