`timescale 1ns/1ps
// =================================================================
// HL4 candidate: HL3 privilege support plus Sv32 address translation.
//
//   - direct-mapped BTB + 2-bit direction predictor (same as HL2)
//   - M/S/U privilege modes and S-mode trap state
//   - exception/interrupt delegation (medeleg/mideleg)
//   - PMP (16 entries, TOR/NA4/NAPOT, locked entries)
//   - Sv32 TLB + hardware page-table walker (4 KiB/4 MiB pages)
//   - M/S/U CSR access checks, SRET/MRET, WFI and SFENCE.VMA
//
// The page-table port is separate from the normal data port.  A real SoC
// must provide a read port into the physical page-table memory.
// =================================================================
module cpu_hl4 #(
    parameter integer SYNC_MEMORY    = 0,
    parameter integer BTB_INDEX_BITS = 6,
    parameter integer BTB_ENABLE     = 1
) (
    input  wire        clk,
    input  wire        rst_n,

    output wire [31:0] pc,          // virtual PC (EPC/debug)
    output wire [31:0] pc_phys,     // translated instruction address
    input  wire [31:0] inst,

    // Sv32 page-table read port and A/D write-back port.
    output wire [31:0] pt_addr,
    input  wire [31:0] pt_rdata,
    output wire        pt_we,
    output wire [31:0] pt_wdata,

    output wire [31:0] mem_addr,
    output wire [31:0] mem_wdata,
    output wire        mem_wren,
    output wire [3:0]  mem_wstrb,
    input  wire [31:0] mem_rdata,

    // Current EX-stage data address and store qualifier.  A platform must
    // decode these for load/store access faults; mem_addr is the older
    // EX/MEM address.
    output wire [31:0] ex_addr,
    output wire        ex_is_store,

    // Platform fault/interrupt inputs.  Tie low when unused.
    input  wire        mem_fault,
    input  wire        inst_fault,
    input  wire        timer_irq,
    input  wire        soft_irq,
    input  wire        ext_irq,
    input  wire        s_timer_irq,
    input  wire        s_soft_irq,
    input  wire        s_ext_irq,

    // Debug/verification observability.
    output wire [31:0] dbg_mepc,
    output wire [31:0] dbg_mcause,
    output wire [31:0] dbg_mtval,
    output wire [31:0] dbg_mstatus,
    output wire [31:0] dbg_sepc,
    output wire [31:0] dbg_scause,
    output wire [31:0] dbg_stval,
    output wire [31:0] dbg_sstatus,
    output wire [1:0]  dbg_priv,
    output wire        dbg_trap,
    output wire [31:0] dbg_trap_pc
);
    // -------------------------------------------------------------
    // Fixed one-edge synchronous memory adapter.
    // Phase 0: memory samples stable requests; phase 1: pipeline consumes.
    // -------------------------------------------------------------
    reg memory_phase;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) memory_phase <= 1'b0;
        else        memory_phase <= ~memory_phase;
    end
    wire pipeline_advance   = (SYNC_MEMORY == 0) || memory_phase;
    wire memory_write_edge  = (SYNC_MEMORY == 0) || (rst_n && !memory_phase);

    // -------------------------------------------------------------
    // Pipeline registers
    // -------------------------------------------------------------
    // IF/ID
    reg [31:0] if_pc, if_inst;
    reg        if_pred_taken, if_pred_valid, if_inst_fault;
    reg [31:0] if_pred_target;

    // ID/EX
    reg [31:0] id_pc, id_inst;
    reg [31:0] id_rs1_data, id_rs2_data, id_imm;
    reg [4:0]  id_rs1, id_rs2, id_rd;
    reg        id_reg_write, id_mem_write, id_mem_to_reg, id_alu_src;
    reg        id_branch, id_jump;
    reg [4:0]  id_alu_ctrl;
    reg [2:0]  id_funct3;
    reg        id_auipc;
    reg        id_pred_taken, id_pred_valid, id_inst_fault;
    reg [31:0] id_pred_target;

    // EX/MEM
    reg [31:0] ex_alu_result, ex_rs2_data;
    reg [4:0]  ex_rd;
    reg        ex_reg_write, ex_mem_write, ex_mem_to_reg;
    reg [2:0]  ex_mem_funct3;

    // MEM/WB
    reg [31:0] mem_alu_result, mem_mem_rdata;
    reg [4:0]  mem_rd;
    reg        mem_reg_write, mem_mem_to_reg;

    // Validity travels with the pipeline.
    reg if_valid, id_valid, ex_valid, mem_valid;

    // -------------------------------------------------------------
    // BTB / CSR / trap control wires (declared before use)
    // -------------------------------------------------------------
    wire        btb_hit, btb_taken;
    wire [31:0] btb_target;
    wire        btb_update_valid, btb_update_is_jump, btb_update_taken;
    wire [31:0] btb_update_pc, btb_update_target;

    wire [31:0] csr_rdata, mtvec, mepc, mcause, mtval, mstatus, mie, mip, mscratch;
    wire [31:0] sstatus, sie, sip, stvec, sepc, scause, stval;
    wire [31:0] medeleg, mideleg, satp, sscratch;
    wire [63:0] mcycle, minstret;
    wire [127:0] pmp_cfg_flat;
    wire [511:0] pmp_addr_flat;
    wire        pmp_if_allow, pmp_data_allow;
    wire [1:0]  priv, trap_target, int_target, data_priv;
    wire        csr_illegal;
    wire        csr_access, csr_commit, csr_we;
    wire [11:0] ex_csr_addr;
    wire [31:0] ex_csr_wdata;

    wire [31:0] pc_plus4, pc_pred, pc_next, redirect_pc;
    wire        redirect, flush_if, flush_id, stall_if;
    wire        ex_exception, ex_btb_mispredict, ex_mret_valid, ex_sret_valid;
    wire        interrupt_taken;
    wire [31:0] ex_cause, ex_tval, trap_cause, trap_tval, trap_epc, trap_vector;
    wire        trap_valid, trap_is_interrupt;
    wire [3:0]  int_code;
    wire        int_request, if_is_mret, if_is_sret, ex_suppress_int;
    wire [31:0] ex_actual_target;
    wire        ex_actual_taken;
    wire        ex_is_sret, ex_is_wfi, ex_is_sfence;
    wire        ex_is_load;
    wire        ex_load_fault, ex_store_fault, ex_pmp_fault;
    wire [3:0]  exc_code_w;
    wire        retire;
    wire        if_inst_fault_pmp;

    // Sv32 MMU / stall control.
    wire [31:0] i_pa, d_pa, mmu_pt_addr, mmu_pt_wdata;
    wire        i_hit, i_fault, d_hit, d_fault, mmu_busy, mmu_pt_we;
    wire        d_req, d_store;
    wire [31:0] ex_data_phys;
    wire        stall_all;
    wire        ex_page_fault, ex_inst_page_fault;
    wire [31:0] ex_phys_addr;
    reg         if_page_fault, id_page_fault;

    // -------------------------------------------------------------
    // IF stage
    // -------------------------------------------------------------
    reg [31:0] pc_reg;
    assign pc = pc_reg;
    assign pc_phys = i_pa;
    assign pt_addr = mmu_pt_addr;
    assign pt_we = mmu_pt_we;
    assign pt_wdata = mmu_pt_wdata;
    assign pc_plus4 = pc_reg + 32'd4;

    // Instruction-fetch PMP check.  The same configuration is also used
    // by the data-side checker below; two instances keep the two address
    // paths independent.
    pmp u_pmp_if (
        .priv      (priv),
        .addr      (pc_phys),
        .access    (2'd0),
        .size      (4'd4),
        .cfg_flat  (pmp_cfg_flat),
        .addr_flat (pmp_addr_flat),
        .allow     (pmp_if_allow),
        .matched   ()
    );
    assign if_inst_fault_pmp = !pmp_if_allow;

    btb #(.INDEX_BITS(BTB_INDEX_BITS)) u_btb (
        .clk            (clk),
        .rst_n          (rst_n),
        .lookup_pc      (pc_reg),
        .lookup_hit     (btb_hit),
        .lookup_taken   (btb_taken),
        .lookup_target  (btb_target),
        .update_valid   (btb_update_valid && pipeline_advance),
        .update_is_jump (btb_update_is_jump),
        .update_taken   (btb_update_taken),
        .update_pc      (btb_update_pc),
        .update_target  (btb_update_target)
    );

    assign pc_pred = ((BTB_ENABLE != 0) && btb_taken) ? btb_target : pc_plus4;
    assign pc_next = redirect ? redirect_pc :
                     ((stall_if || stall_all) ? pc_reg : pc_pred);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) pc_reg <= 32'd0;
        else if (pipeline_advance && (!stall_all || redirect)) pc_reg <= pc_next;
    end

    // IF/ID holds the instruction and the prediction made for that PC.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            if_pc          <= 32'd0;
            if_inst        <= 32'd0;
            if_pred_taken  <= 1'b0;
            if_pred_target <= 32'd0;
            if_pred_valid  <= 1'b0;
            if_inst_fault  <= 1'b0;
            if_page_fault  <= 1'b0;
        end else if (pipeline_advance && flush_if) begin
            if_pc          <= 32'd0;
            if_inst        <= 32'd0;
            if_pred_taken  <= 1'b0;
            if_pred_target <= 32'd0;
            if_pred_valid  <= 1'b0;
            if_inst_fault  <= 1'b0;
            if_page_fault  <= 1'b0;
        end else if (pipeline_advance && !stall_if && !stall_all) begin
            if_pc          <= pc_reg;
            if_inst        <= inst;
            if_pred_taken  <= (BTB_ENABLE != 0) ? btb_taken : 1'b0;
            if_pred_target <= btb_target;
            if_pred_valid  <= (BTB_ENABLE != 0) ? btb_hit : 1'b0;
            if_inst_fault  <= inst_fault || if_inst_fault_pmp;
            if_page_fault  <= i_fault;
        end
    end

    // -------------------------------------------------------------
    // ID stage
    // -------------------------------------------------------------
    wire [6:0] opcode = if_inst[6:0];
    wire [4:0] rs1 = if_inst[19:15];
    wire [4:0] rs2 = if_inst[24:20];
    wire [4:0] rd  = if_inst[11:7];
    wire [2:0] funct3 = if_inst[14:12];
    wire [6:0] funct7 = if_inst[31:25];

    reg [31:0] imm_ext;
    always @(*) begin
        case (opcode)
            7'b0010011, 7'b0000011, 7'b1100111:
                imm_ext = {{20{if_inst[31]}}, if_inst[31:20]};
            7'b0110111, 7'b0010111:
                imm_ext = {if_inst[31:12], 12'b0};
            7'b0100011:
                imm_ext = {{20{if_inst[31]}}, if_inst[31:25], if_inst[11:7]};
            7'b1100011:
                imm_ext = {{20{if_inst[31]}}, if_inst[7], if_inst[30:25], if_inst[11:8], 1'b0};
            7'b1101111:
                imm_ext = {{12{if_inst[31]}}, if_inst[19:12], if_inst[20], if_inst[30:21], 1'b0};
            default:
                imm_ext = 32'd0;
        endcase
    end

    wire        reg_write_id, mem_write_id, branch_id, mem_to_reg_id, alu_src_id, jump_id;
    wire [4:0]  alu_ctrl_id;
    control ctrl (
        .opcode    (opcode),
        .funct3    (funct3),
        .funct7    (funct7),
        .reg_write (reg_write_id),
        .mem_write (mem_write_id),
        .branch    (branch_id),
        .mem_to_reg(mem_to_reg_id),
        .alu_src   (alu_src_id),
        .alu_ctrl  (alu_ctrl_id),
        .jump      (jump_id)
    );

    // Register file write port is driven by WB.
    wire [31:0] rs1_data, rs2_data;
    wire [31:0] wb_write_data;
    regfile rf (
        .clk   (clk),
        .we    (pipeline_advance && !stall_all && mem_valid && mem_reg_write),
        .waddr (mem_rd),
        .wdata (wb_write_data),
        .raddr1(rs1),
        .raddr2(rs2),
        .rdata1(rs1_data),
        .rdata2(rs2_data)
    );

    // Same-edge WB -> ID bypass, preserving the original F behaviour.
    wire [31:0] wb_id_rs1 = (mem_reg_write && (mem_rd != 5'd0) && (mem_rd == rs1))
        ? wb_write_data : rs1_data;
    wire [31:0] wb_id_rs2 = (mem_reg_write && (mem_rd != 5'd0) && (mem_rd == rs2))
        ? wb_write_data : rs2_data;

    // ID/EX capture.  On flush/stall the control side is cleared.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            id_pc          <= 32'd0;
            id_inst        <= 32'd0;
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
            id_pred_taken  <= 1'b0;
            id_pred_target <= 32'd0;
            id_pred_valid  <= 1'b0;
            id_inst_fault  <= 1'b0;
            id_page_fault  <= 1'b0;
        end else if (pipeline_advance && (flush_id || (stall_if && !stall_all))) begin
            id_pc          <= 32'd0;
            id_inst        <= 32'd0;
            id_reg_write   <= 1'b0;
            id_mem_write   <= 1'b0;
            id_mem_to_reg  <= 1'b0;
            id_branch      <= 1'b0;
            id_jump        <= 1'b0;
            id_alu_src     <= 1'b0;
            id_auipc       <= 1'b0;
            id_pred_taken  <= 1'b0;
            id_pred_target <= 32'd0;
            id_pred_valid  <= 1'b0;
            id_inst_fault  <= 1'b0;
            id_page_fault  <= 1'b0;
        end else if (pipeline_advance && !stall_all) begin
            id_pc          <= if_pc;
            id_inst        <= if_inst;
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
            id_pred_taken  <= if_pred_taken;
            id_pred_target <= if_pred_target;
            id_pred_valid  <= if_pred_valid;
            id_inst_fault  <= if_inst_fault;
            id_page_fault  <= if_page_fault;
        end
    end

    // -------------------------------------------------------------
    // EX stage: forwarding, branch resolution, CSR, exceptions
    // -------------------------------------------------------------
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
    wire [31:0] branch_target;
    wire [31:0] jump_target;
    wire        branch_taken;
    assign ex_is_store = id_mem_write;
    assign ex_phys_addr = (ex_is_load || ex_is_store) ? d_pa : alu_result;
    assign ex_addr = ex_phys_addr;
    alu alu_inst (
        .a     (alu_src1),
        .b     (alu_src2),
        .ctrl  (id_alu_ctrl),
        .result(alu_result),
        .zero  (alu_zero)
    );

    assign branch_target = id_pc + id_imm;
    assign jump_target = id_alu_src
        ? ((forward_rs1 + id_imm) & 32'hffff_fffe)
        : (id_pc + id_imm);
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

    // Decode the instruction in EX from the carried instruction word.
    wire [6:0]  ex_opcode     = id_inst[6:0];
    wire [2:0]  ex_funct3     = id_inst[14:12];
    wire [6:0]  ex_funct7     = id_inst[31:25];
    wire [4:0]  ex_rs1_field  = id_inst[19:15];
    wire [11:0] ex_csr_addr_w = id_inst[31:20];

    assign ex_csr_addr = ex_csr_addr_w;

    wire ex_is_csr    = (ex_opcode == 7'b1110011) && (ex_funct3 != 3'b000);
    wire ex_is_ecall  = (id_inst == 32'h00000073);
    wire ex_is_ebreak = (id_inst == 32'h00100073);
    wire ex_is_mret   = (id_inst == 32'h30200073);
    assign ex_is_sret   = (id_inst == 32'h10200073);
    assign ex_is_wfi    = (id_inst == 32'h10500073);
    assign ex_is_sfence =
        (ex_opcode == 7'b1110011) && (ex_funct3 == 3'b000) &&
        (ex_funct7 == 7'b0001001); // SFENCE.VMA

    // Privileged instructions have mode-dependent legality.
    wire ex_priv_illegal =
        (ex_is_mret   && (priv != 2'b11)) ||
        (ex_is_sret   && ((priv == 2'b00) || ((priv == 2'b01) && mstatus[22]))) ||
        (ex_is_sfence && ((priv == 2'b00) || ((priv == 2'b01) && mstatus[20]))) ||
        (ex_is_wfi    && (priv != 2'b11) && mstatus[21]);

    wire ex_csr_op_ok = (ex_funct3 == 3'b001) || (ex_funct3 == 3'b010) ||
                        (ex_funct3 == 3'b011) || (ex_funct3 == 3'b101) ||
                        (ex_funct3 == 3'b110) || (ex_funct3 == 3'b111);

    wire ex_csr_we = ex_is_csr && ex_csr_op_ok &&
        ((ex_funct3 == 3'b001) || (ex_funct3 == 3'b101) ||
         (((ex_funct3 == 3'b010) || (ex_funct3 == 3'b110) ||
           (ex_funct3 == 3'b011) || (ex_funct3 == 3'b111)) &&
          (ex_rs1_field != 5'd0)));

    // CSRRW/CSRRWI write the source; CSRRS/CSRRC combine with the old value.
    wire [31:0] ex_inst_zimm = {27'd0, ex_rs1_field};
    wire [31:0] ex_csr_operand = ex_funct3[2] ? ex_inst_zimm : forward_rs1;
    wire [31:0] ex_csr_value =
        ((ex_funct3 == 3'b001) || (ex_funct3 == 3'b101)) ? ex_csr_operand :
        ((ex_funct3 == 3'b010) || (ex_funct3 == 3'b110)) ? (csr_rdata | ex_csr_operand) :
        ((ex_funct3 == 3'b011) || (ex_funct3 == 3'b111)) ? (csr_rdata & ~ex_csr_operand) :
        csr_rdata;
    assign ex_csr_wdata = ex_csr_value;

    // Comprehensive illegal-instruction decoder for the supported RV32I subset.
    reg ex_illegal_dec;
    always @(*) begin
        ex_illegal_dec = 1'b1;
        case (ex_opcode)
            7'b0110011: begin // R-type
                case (ex_funct3)
                    3'b000, 3'b101:
                        ex_illegal_dec = !((ex_funct7 == 7'b0000000) || (ex_funct7 == 7'b0100000));
                    3'b001, 3'b010, 3'b011, 3'b100, 3'b110, 3'b111:
                        ex_illegal_dec = (ex_funct7 != 7'b0000000);
                    default: ex_illegal_dec = 1'b1;
                endcase
            end
            7'b0010011: begin // I-type ALU
                case (ex_funct3)
                    3'b001: ex_illegal_dec = (ex_funct7 != 7'b0000000);
                    3'b101: ex_illegal_dec = !((ex_funct7 == 7'b0000000) || (ex_funct7 == 7'b0100000));
                    3'b000, 3'b010, 3'b011, 3'b100, 3'b110, 3'b111:
                        ex_illegal_dec = 1'b0;
                    default: ex_illegal_dec = 1'b1;
                endcase
            end
            7'b0110111, 7'b0010111: ex_illegal_dec = 1'b0; // LUI, AUIPC
            7'b0000011: begin // loads
                case (ex_funct3)
                    3'b000, 3'b001, 3'b010, 3'b100, 3'b101: ex_illegal_dec = 1'b0;
                    default: ex_illegal_dec = 1'b1;
                endcase
            end
            7'b0100011: begin // stores
                case (ex_funct3)
                    3'b000, 3'b001, 3'b010: ex_illegal_dec = 1'b0;
                    default: ex_illegal_dec = 1'b1;
                endcase
            end
            7'b1100011: begin // branches
                case (ex_funct3)
                    3'b000, 3'b001, 3'b100, 3'b101, 3'b110, 3'b111: ex_illegal_dec = 1'b0;
                    default: ex_illegal_dec = 1'b1;
                endcase
            end
            7'b1101111: ex_illegal_dec = 1'b0; // JAL; bits 14:12 are immediate bits
            7'b1100111: ex_illegal_dec = (ex_funct3 != 3'b000); // JALR
            7'b0001111: begin // FENCE / FENCE.I
                ex_illegal_dec = !((ex_funct3 == 3'b000) || (ex_funct3 == 3'b001));
            end
            7'b1110011: begin // SYSTEM
                if (ex_funct3 == 3'b000) begin
                    ex_illegal_dec = !(ex_is_ecall || ex_is_ebreak || ex_is_mret ||
                                       ex_is_sret || ex_is_wfi || ex_is_sfence);
                end else begin
                    ex_illegal_dec = !ex_csr_op_ok;
                end
            end
            default: ex_illegal_dec = 1'b1;
        endcase
    end

    assign csr_access = id_valid && ex_is_csr;
    assign csr_commit = id_valid && ex_is_csr && !ex_exception;
    wire csr_commit_eff = csr_commit && !stall_all;
    assign csr_we = ex_csr_we;

    // Address and access checks for the current EX instruction.
    wire [31:0] ex_mem_addr = alu_result;
    assign ex_is_load = id_mem_to_reg;

    wire ex_load_misaligned =
        id_valid && ex_is_load &&
        (((ex_funct3 == 3'b010) && (ex_mem_addr[1:0] != 2'b00)) ||
         (((ex_funct3 == 3'b001) || (ex_funct3 == 3'b101)) && ex_mem_addr[0]));
    wire ex_store_misaligned =
        id_valid && ex_is_store &&
        (((ex_funct3 == 3'b010) && (ex_mem_addr[1:0] != 2'b00)) ||
         ((ex_funct3 == 3'b001) && ex_mem_addr[0]));

    // MPRV makes data accesses use MPP as the effective privilege.
    assign data_priv = (mstatus[17] && (priv == 2'b11)) ? mstatus[12:11] : priv;

    // Sv32 translation and pipeline-wide stalls.
    assign d_req   = id_valid && (ex_is_load || ex_is_store);
    assign d_store = ex_is_store;
    assign stall_all = mmu_busy ||
        (1'b1 && !i_hit && !i_fault) ||
        (d_req && !d_hit && !d_fault);

    wire mmu_flush =
        (csr_commit_eff && (ex_csr_addr == 12'h180)) ||
        (id_valid && ex_is_sfence && !ex_exception && !stall_all);

    mmu_sv32 u_mmu (
        .clk       (clk),
        .rst_n     (rst_n),
        .step      (pipeline_advance),
        .satp      (satp),
        .priv      (priv),
        .sum       (mstatus[18]),
        .mxr       (mstatus[19]),
        .flush     (mmu_flush),
        .i_va      (pc_reg),
        .i_req     (1'b1),
        .i_pa      (i_pa),
        .i_hit     (i_hit),
        .i_fault   (i_fault),
        .d_va      (ex_mem_addr),
        .d_req     (d_req),
        .d_store   (d_store),
        .d_priv    (data_priv),
        .d_pa      (d_pa),
        .d_hit     (d_hit),
        .d_fault   (d_fault),
        .pt_addr   (mmu_pt_addr),
        .pt_rdata  (pt_rdata),
        .pt_we     (mmu_pt_we),
        .pt_wdata  (mmu_pt_wdata),
        .busy      (mmu_busy)
    );
    assign ex_data_phys = d_pa;

    reg [3:0] ex_access_size;
    always @(*) begin
        ex_access_size = 4'd4;
        case (ex_funct3)
            3'b000: ex_access_size = 4'd1;
            3'b001, 3'b101: ex_access_size = 4'd2;
            default: ex_access_size = 4'd4;
        endcase
    end

    pmp u_pmp_data (
        .priv      (data_priv),
        .addr      (d_pa),
        .access    (ex_is_store ? 2'd2 : 2'd1),
        .size      (ex_access_size),
        .cfg_flat  (pmp_cfg_flat),
        .addr_flat (pmp_addr_flat),
        .allow     (pmp_data_allow),
        .matched   ()
    );
    assign ex_pmp_fault = d_hit && (ex_is_load || ex_is_store) && !pmp_data_allow;

    assign ex_load_fault  = id_valid && ex_is_load  && d_hit && !d_fault &&
                            (mem_fault || ex_pmp_fault);
    assign ex_store_fault = id_valid && ex_is_store && d_hit && !d_fault &&
                            (mem_fault || ex_pmp_fault);

    wire ex_pc_misaligned = id_valid && (id_pc[1:0] != 2'b00);
    assign ex_inst_page_fault = id_valid && id_page_fault;
    wire ex_inst_fault_ok = id_valid && id_inst_fault;
    wire ex_illegal = id_valid && (ex_illegal_dec || ex_priv_illegal ||
                                   (ex_is_csr && csr_illegal));
    assign ex_page_fault = id_valid && d_fault && (ex_is_load || ex_is_store);
    wire ex_ebreak = id_valid && ex_is_ebreak;
    wire ex_ecall  = id_valid && ex_is_ecall;
    wire [3:0] ex_ecall_code = (priv == 2'b00) ? 4'd8 :
                               (priv == 2'b01) ? 4'd9 : 4'd11;

    reg        exc_valid;
    reg [3:0]  exc_code;
    reg [31:0] exc_tval;
    always @(*) begin
        exc_valid = 1'b1;
        exc_code  = 4'd0;
        exc_tval  = 32'd0;
        if (ex_pc_misaligned) begin
            exc_code = 4'd0;  exc_tval = id_pc;
        end else if (ex_inst_page_fault) begin
            exc_code = 4'd12; exc_tval = id_pc;
        end else if (ex_inst_fault_ok) begin
            exc_code = 4'd1;  exc_tval = id_pc;
        end else if (ex_illegal) begin
            exc_code = 4'd2;  exc_tval = id_inst;
        end else if (ex_ebreak) begin
            exc_code = 4'd3;  exc_tval = id_pc;
        end else if (ex_page_fault) begin
            exc_code = ex_is_store ? 4'd15 : 4'd13;
            exc_tval = ex_mem_addr;
        end else if (ex_load_misaligned) begin
            exc_code = 4'd4;  exc_tval = ex_mem_addr;
        end else if (ex_load_fault) begin
            exc_code = 4'd5;  exc_tval = ex_mem_addr;
        end else if (ex_store_misaligned) begin
            exc_code = 4'd6;  exc_tval = ex_mem_addr;
        end else if (ex_store_fault) begin
            exc_code = 4'd7;  exc_tval = ex_mem_addr;
        end else if (ex_ecall) begin
            exc_code = ex_ecall_code; exc_tval = 32'd0;
        end else begin
            exc_valid = 1'b0;
        end
    end

    assign ex_exception = id_valid && exc_valid;
    assign ex_cause  = {28'd0, exc_code};
    assign ex_tval   = exc_tval;

    // Branch/jump prediction comparison and BTB update.
    assign ex_actual_taken  = id_jump || branch_taken;
    assign ex_actual_target = id_jump ? jump_target : branch_target;

    assign ex_btb_mispredict =
        id_valid && (id_branch || id_jump) && !ex_exception &&
        ((ex_actual_taken != id_pred_taken) ||
         (ex_actual_taken && (!id_pred_valid || (ex_actual_target != id_pred_target))));

    assign btb_update_valid   = id_valid && (id_branch || id_jump) && !ex_exception;
    assign btb_update_is_jump = id_jump;
    assign btb_update_taken   = ex_actual_taken;
    assign btb_update_pc      = id_pc;
    assign btb_update_target  = ex_actual_target;

    // MRET/SRET are control transfers and must not commit a register write.
    assign ex_mret_valid = id_valid && ex_is_mret && !ex_exception;
    assign ex_sret_valid = id_valid && ex_is_sret && !ex_exception;

    // -------------------------------------------------------------
    // Interrupt selection with M/S delegation.
    //
    // In M-mode all pending interrupts are taken in M.  In S/U mode,
    // mideleg selects S-level interrupts; M-level interrupts remain
    // enabled regardless of mstatus.MIE (MIE only gates M-mode execution).
    // -------------------------------------------------------------
    wire [31:0] m_pending = mip & mie &
        ((priv == 2'b11) ? 32'hFFFF_FFFF : ~mideleg);
    wire [31:0] s_pending = mip & mie & mideleg;
    wire m_any = m_pending[11] || m_pending[3] || m_pending[7];
    wire s_any = s_pending[9] || s_pending[1] || s_pending[5];
    wire m_enable = (priv == 2'b11) ? mstatus[3] : 1'b1;
    wire s_enable = (priv != 2'b11) && mstatus[1];

    wire [3:0] m_int_code = m_pending[11] ? 4'd11 :
                            m_pending[3]  ? 4'd3  :
                            m_pending[7]  ? 4'd7  : 4'd0;
    wire [3:0] s_int_code = s_pending[9]  ? 4'd9  :
                            s_pending[1]  ? 4'd1  :
                            s_pending[5]  ? 4'd5  : 4'd0;

    assign int_request = (m_enable && m_any) || (s_enable && s_any);
    assign int_target  = (m_enable && m_any) ? 2'b11 : 2'b01;
    assign int_code    = (m_enable && m_any) ? m_int_code : s_int_code;

    // Take an interrupt before the instruction currently in ID.  Suppress it
    // while EX contains a control/CSR/RET instruction or an exception.
    assign if_is_mret = (if_inst == 32'h30200073);
    assign if_is_sret = (if_inst == 32'h10200073);
    assign ex_suppress_int = id_valid &&
        (id_branch || id_jump || ex_is_csr || ex_is_mret || ex_is_sret ||
         ex_is_sfence);
    assign interrupt_taken = int_request && if_valid && !stall_all &&
        !ex_exception && !ex_suppress_int && !if_is_mret && !if_is_sret;

    // Exception delegation is valid only when the trap came from S/U.
    wire exception_to_s = (priv != 2'b11) && medeleg[exc_code];

    assign trap_valid = ex_exception || interrupt_taken;
    assign trap_is_interrupt = !ex_exception && interrupt_taken;
    assign trap_target = trap_is_interrupt ? int_target :
                         (exception_to_s ? 2'b01 : 2'b11);
    assign trap_cause = ex_exception ? ex_cause :
                        {1'b1, 27'd0, int_code};
    assign trap_tval = ex_exception ? ex_tval : 32'd0;
    assign trap_epc = ex_exception ? id_pc :
                      (if_valid ? if_pc : pc_reg);

    // Direct mode: base.  Vectored mode: base + 4*cause (interrupts only).
    wire [31:0] trap_base = (trap_target == 2'b01) ? stvec : mtvec;
    assign trap_vector = (trap_is_interrupt && (trap_base[1:0] == 2'b01))
        ? ({trap_base[31:2], 2'b00} + {26'd0, int_code, 2'b00})
        : {trap_base[31:2], 2'b00};

    assign redirect = trap_valid || ex_mret_valid || ex_sret_valid ||
                      ex_btb_mispredict;
    assign redirect_pc = trap_valid ? trap_vector :
                         (ex_mret_valid ? mepc :
                          (ex_sret_valid ? sepc :
                           (ex_btb_mispredict
                              ? (ex_actual_taken ? ex_actual_target : (id_pc + 32'd4))
                              : pc_plus4)));

    assign flush_if = redirect;
    assign flush_id = redirect;

    // Load-use hazard detection (same contract as F, with CSR rs1 added).
    wire id_uses_rs1 = (opcode == 7'b0110011) || (opcode == 7'b0010011) ||
                       (opcode == 7'b0000011) || (opcode == 7'b0100011) ||
                       (opcode == 7'b1100011) || (opcode == 7'b1100111) ||
                       ((opcode == 7'b1110011) && (funct3 != 3'b000) && !funct3[2]);
    wire id_uses_rs2 = (opcode == 7'b0110011) || (opcode == 7'b0100011) ||
                       (opcode == 7'b1100011);
    wire lw_stall = id_reg_write && id_mem_to_reg && (id_rd != 5'd0) &&
                    ((id_uses_rs1 && (id_rd == rs1)) ||
                     (id_uses_rs2 && (id_rd == rs2)));
    assign stall_if = lw_stall;

    // -------------------------------------------------------------
    // EX/MEM
    // -------------------------------------------------------------
    wire ex_reg_write_final = (ex_is_csr ? 1'b1 : id_reg_write) && !ex_exception;
    wire [31:0] ex_alu_result_final = ex_is_csr
        ? csr_rdata
        : (id_jump ? (id_pc + 32'd4)
                   : ((id_mem_to_reg || id_mem_write) ? d_pa : alu_result));
    wire ex_mem_to_reg_final = ex_is_csr ? 1'b0 : id_mem_to_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ex_alu_result  <= 32'd0;
            ex_rs2_data    <= 32'd0;
            ex_rd          <= 5'd0;
            ex_reg_write   <= 1'b0;
            ex_mem_write   <= 1'b0;
            ex_mem_to_reg  <= 1'b0;
            ex_mem_funct3  <= 3'd0;
        end else if (pipeline_advance && !stall_all) begin
            ex_alu_result  <= ex_alu_result_final;
            ex_rs2_data    <= forward_rs2;
            ex_rd          <= id_rd;
            ex_reg_write   <= id_valid && !ex_exception && ex_reg_write_final;
            ex_mem_write   <= id_valid && !ex_exception && id_mem_write;
            ex_mem_to_reg  <= id_valid && !ex_exception && ex_mem_to_reg_final;
            ex_mem_funct3  <= id_funct3;
        end
    end

    // -------------------------------------------------------------
    // MEM stage
    // -------------------------------------------------------------
    assign mem_addr  = ex_alu_result;
    assign mem_wdata = (ex_mem_write && (ex_mem_funct3 == 3'b000))
        ? ({24'd0, ex_rs2_data[7:0]} << {ex_alu_result[1:0], 3'b000})
        : (ex_mem_write && (ex_mem_funct3 == 3'b001))
        ? ({16'd0, ex_rs2_data[15:0]} << {ex_alu_result[1], 4'b0000})
        : ex_rs2_data;
    assign mem_wstrb = !mem_wren ? 4'b0000
        : (ex_mem_funct3 == 3'b000) ? (4'b0001 << ex_alu_result[1:0])
        : (ex_mem_funct3 == 3'b001) ? (4'b0011 << {ex_alu_result[1], 1'b0})
        : (ex_mem_funct3 == 3'b010) ? 4'b1111 : 4'b0000;
    assign mem_wren = ex_mem_write && memory_write_edge;

    wire [7:0] mem_load_byte = mem_rdata >> {ex_alu_result[1:0], 3'b000};
    wire [15:0] mem_load_half = ex_alu_result[1] ? mem_rdata[31:16] : mem_rdata[15:0];
    wire [31:0] mem_load_data = (ex_mem_funct3 == 3'b100)
        ? {24'd0, mem_load_byte}
        : (ex_mem_funct3 == 3'b000) ? {{24{mem_load_byte[7]}}, mem_load_byte}
        : (ex_mem_funct3 == 3'b101) ? {16'd0, mem_load_half}
        : (ex_mem_funct3 == 3'b001) ? {{16{mem_load_half[15]}}, mem_load_half}
        : mem_rdata;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mem_alu_result <= 32'd0;
            mem_mem_rdata  <= 32'd0;
            mem_rd         <= 5'd0;
            mem_reg_write  <= 1'b0;
            mem_mem_to_reg <= 1'b0;
        end else if (pipeline_advance && !stall_all) begin
            mem_alu_result <= ex_alu_result;
            mem_mem_rdata  <= mem_load_data;
            mem_rd         <= ex_rd;
            mem_reg_write  <= ex_valid && ex_reg_write;
            mem_mem_to_reg <= ex_valid && ex_mem_to_reg;
        end
    end

    // -------------------------------------------------------------
    // WB
    // -------------------------------------------------------------
    assign wb_write_data = mem_mem_to_reg ? mem_mem_rdata : mem_alu_result;

    // -------------------------------------------------------------
    // Validity pipeline
    // -------------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            if_valid <= 1'b0;
            id_valid <= 1'b0;
            ex_valid <= 1'b0;
            mem_valid <= 1'b0;
        end else if (pipeline_advance) begin
            if (flush_if || flush_id) begin
                // A trap/redirect must take priority over an MMU stall.  If
                // the stall is only an instruction-fetch miss, keep the older
                // EX/MEM instruction so it can retire after the redirect.
                if_valid <= 1'b0;
                id_valid <= 1'b0;
                if (!stall_all) begin
                    mem_valid <= ex_valid;
                    ex_valid  <= id_valid && !ex_exception;
                end
            end else if (!stall_all) begin
                mem_valid <= ex_valid;
                ex_valid  <= id_valid && !ex_exception;
                if (!stall_if) if_valid <= 1'b1;
                if (stall_if) id_valid <= 1'b0;
                else id_valid <= if_valid;
            end
        end
    end

    // -------------------------------------------------------------
    // CSR file
    // -------------------------------------------------------------
    assign retire = mem_valid && !stall_all;

    csr_file_hl3 u_csr (
        .clk           (clk),
        .rst_n         (rst_n),
        .commit_enable (pipeline_advance),
        .csr_access    (csr_access),
        .csr_addr      (ex_csr_addr),
        .csr_we        (csr_we),
        .csr_wdata     (ex_csr_wdata),
        .csr_commit    (csr_commit_eff),
        .retire        (retire),
        .csr_rdata     (csr_rdata),
        .csr_illegal   (csr_illegal),
        .current_priv  (priv),
        .trap_valid    (trap_valid),
        .trap_target   (trap_target),
        .trap_epc      (trap_epc),
        .trap_cause    (trap_cause),
        .trap_tval     (trap_tval),
        .mret_valid    (ex_mret_valid),
        .sret_valid    (ex_sret_valid),
        .timer_irq     (timer_irq),
        .soft_irq      (soft_irq),
        .ext_irq       (ext_irq),
        .s_timer_irq   (s_timer_irq),
        .s_soft_irq    (s_soft_irq),
        .s_ext_irq     (s_ext_irq),
        .priv          (priv),
        .mstatus       (mstatus),
        .sstatus       (sstatus),
        .mie           (mie),
        .sie           (sie),
        .mip           (mip),
        .sip           (sip),
        .mtvec         (mtvec),
        .stvec         (stvec),
        .mepc          (mepc),
        .sepc          (sepc),
        .mcause        (mcause),
        .scause        (scause),
        .mtval         (mtval),
        .stval         (stval),
        .medeleg       (medeleg),
        .mideleg       (mideleg),
        .satp          (satp),
        .mscratch      (mscratch),
        .sscratch      (sscratch),
        .mcycle        (mcycle),
        .minstret      (minstret),
        .pmp_cfg_flat  (pmp_cfg_flat),
        .pmp_addr_flat (pmp_addr_flat)
    );

    // -------------------------------------------------------------
    // Debug observability
    // -------------------------------------------------------------
    assign dbg_mepc    = mepc;
    assign dbg_mcause  = mcause;
    assign dbg_mtval   = mtval;
    assign dbg_mstatus = mstatus;
    assign dbg_sepc    = sepc;
    assign dbg_scause  = scause;
    assign dbg_stval   = stval;
    assign dbg_sstatus = sstatus;
    assign dbg_priv    = priv;
    assign dbg_trap    = trap_valid;
    assign dbg_trap_pc = trap_epc;

    // Keep intentionally unused decoded signals visible for lint tools.
    wire unused_ex_wfi   = ex_is_wfi;
    wire unused_ex_sfence = ex_is_sfence;
    wire unused_mscratch = |mscratch;
    wire unused_mcycle   = |mcycle;
    wire unused_minstret = |minstret;
    wire unused_sie      = |sie;
    wire unused_sip      = |sip;
    wire unused_sscratch = |sscratch;
    wire unused_satp     = |satp;
    wire [31:0] unused_btb_hit = {31'd0, btb_hit};
endmodule
