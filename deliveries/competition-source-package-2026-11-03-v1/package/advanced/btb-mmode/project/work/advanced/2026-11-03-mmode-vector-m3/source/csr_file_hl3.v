`timescale 1ns/1ps
// =================================================================
// HL3 privileged CSR file: M/S/U modes, delegation, PMP CSRs,
// S-mode trap state, counters and Sv32 satp.
//
// This is deliberately a separate file from the HL2 M-mode CSR file.
// The HL2 candidate remains the frozen M-mode reference.
// =================================================================
module csr_file_hl3 (
    input  wire        clk,
    input  wire        rst_n,

    // Pipeline commit.  All trap/return/CSR updates are one-shot at this
    // edge so SYNC_MEMORY=1 does not commit the same instruction twice.
    input  wire        commit_enable,

    // CSR instruction access from EX.  The CPU has decoded the instruction;
    // this unit checks address privilege, RO/WO and counter-enable rules.
    input  wire        csr_access,
    input  wire [11:0] csr_addr,
    input  wire        csr_we,
    input  wire [31:0] csr_wdata,
    input  wire        csr_commit,
    input  wire        retire,
    output wire [31:0] csr_rdata,
    output wire        csr_illegal,

    // Current privilege and trap entry/return.
    input  wire [1:0]  current_priv,       // 00=U, 01=S, 11=M
    input  wire        trap_valid,
    input  wire [1:0]  trap_target,         // 01=S, 11=M
    input  wire [31:0] trap_epc,
    input  wire [31:0] trap_cause,
    input  wire [31:0] trap_tval,
    input  wire        mret_valid,
    input  wire        sret_valid,

    // Platform interrupt sources.  M and S sources are separate so the
    // testbench/SoC can exercise delegation independently.
    input  wire        timer_irq,
    input  wire        soft_irq,
    input  wire        ext_irq,
    input  wire        s_timer_irq,
    input  wire        s_soft_irq,
    input  wire        s_ext_irq,

    // Architectural state / observability.
    output wire [1:0]  priv,
    output wire [31:0] mstatus,
    output wire [31:0] sstatus,
    output wire [31:0] mie,
    output wire [31:0] sie,
    output wire [31:0] mip,
    output wire [31:0] sip,
    output wire [31:0] mtvec,
    output wire [31:0] stvec,
    output wire [31:0] mepc,
    output wire [31:0] sepc,
    output wire [31:0] mcause,
    output wire [31:0] scause,
    output wire [31:0] mtval,
    output wire [31:0] stval,
    output wire [31:0] medeleg,
    output wire [31:0] mideleg,
    output wire [31:0] satp,
    output wire [31:0] mscratch,
    output wire [31:0] sscratch,
    output wire [63:0] mcycle,
    output wire [63:0] minstret,
    output wire [127:0] pmp_cfg_flat,      // 16 x 8
    output wire [511:0] pmp_addr_flat      // 16 x 32
);

    // -------------------------------------------------------------
    // Privilege and trap state
    // -------------------------------------------------------------
    reg [1:0]  priv_q;
    reg [31:0] mstatus_q;
    reg [31:0] medeleg_q;
    reg [31:0] mideleg_q;
    reg [31:0] mie_q;
    reg [31:0] mtvec_q;
    reg [31:0] mscratch_q;
    reg [31:0] mepc_q;
    reg [31:0] mcause_q;
    reg [31:0] mtval_q;

    reg [31:0] stvec_q;
    reg [31:0] sscratch_q;
    reg [31:0] sepc_q;
    reg [31:0] scause_q;
    reg [31:0] stval_q;
    reg [31:0] satp_q;

    reg [31:0] mcounteren_q;
    reg [31:0] scounteren_q;

    reg [31:0] mcycle_q;
    reg [31:0] mcycleh_q;
    reg [31:0] minstret_q;
    reg [31:0] minstreth_q;

    reg        ssip_q;
    reg [31:0] pmpcfg0_q;
    reg [31:0] pmpcfg1_q;
    reg [31:0] pmpcfg2_q;
    reg [31:0] pmpcfg3_q;
    reg [511:0] pmpaddr_flat_q;

    localparam [31:0] MISA_VALUE = 32'h4014_0100; // RV32I + S + U
    localparam [31:0] MSTATUS_WMASK = 32'h007E_19AA;
    localparam [31:0] SSTATUS_WMASK = 32'h000C_0122;
    localparam [31:0] MIE_MASK     = 32'h0000_0AAA;
    localparam [31:0] SIE_MASK     = 32'h0000_0222;
    localparam [31:0] MIDELEG_MASK = 32'h0000_0222;
    localparam [31:0] MEDELEG_MASK = 32'h0000_F7FF;
    localparam [31:0] COUNTER_MASK = 32'h0000_0005; // cycle, instret

    assign priv       = priv_q;
    assign mstatus    = mstatus_q;
    assign sstatus    = mstatus_q & SSTATUS_WMASK;
    assign mie        = mie_q;
    assign sie        = mie_q & SIE_MASK;
    assign mtvec      = mtvec_q;
    assign stvec      = stvec_q;
    assign mepc       = mepc_q;
    assign sepc       = sepc_q;
    assign mcause     = mcause_q;
    assign scause     = scause_q;
    assign mtval      = mtval_q;
    assign stval      = stval_q;
    assign medeleg    = medeleg_q;
    assign mideleg    = mideleg_q;
    assign satp       = satp_q;
    assign mscratch   = mscratch_q;
    assign sscratch   = sscratch_q;
    assign mcycle     = {mcycleh_q, mcycle_q};
    assign minstret   = {minstreth_q, minstret_q};

    // S-level pending bits are the low three S interrupt bits of MIP.
    wire [31:0] mip_w = (ssip_q | s_soft_irq) ? 32'h0000_0002 : 32'd0;
    wire [31:0] mip_all = mip_w
        | (soft_irq    ? 32'h0000_0008 : 32'd0)  // MSIP
        | (s_timer_irq ? 32'h0000_0020 : 32'd0)  // STIP
        | (timer_irq   ? 32'h0000_0080 : 32'd0)  // MTIP
        | (s_ext_irq   ? 32'h0000_0200 : 32'd0)  // SEIP
        | (ext_irq     ? 32'h0000_0800 : 32'd0); // MEIP
    assign mip = mip_all;
    assign sip = mip_all & SIE_MASK;

    assign pmp_cfg_flat = {pmpcfg3_q, pmpcfg2_q, pmpcfg1_q, pmpcfg0_q};
    assign pmp_addr_flat = pmpaddr_flat_q;

    // -------------------------------------------------------------
    // CSR address decode / legality
    // -------------------------------------------------------------
    reg csr_known;
    always @(*) begin
        case (csr_addr)
            12'h100, 12'h104, 12'h105, 12'h106,
            12'h140, 12'h141, 12'h142, 12'h143, 12'h144, 12'h180,
            12'h300, 12'h301, 12'h302, 12'h303, 12'h304,
            12'h305, 12'h306, 12'h340, 12'h341, 12'h342,
            12'h343, 12'h344,
            12'h3A0, 12'h3A1, 12'h3A2, 12'h3A3,
            12'hB00, 12'hB02, 12'hB80, 12'hB82,
            12'hC00, 12'hC01, 12'hC02,
            12'hC80, 12'hC81, 12'hC82,
            12'hF11, 12'hF12, 12'hF13, 12'hF14:
                csr_known = 1'b1;
            default:
                csr_known = 1'b0;
        endcase
        // PMP address registers 0x3B0..0x3BF.
        if (csr_addr >= 12'h3B0 && csr_addr <= 12'h3BF)
            csr_known = 1'b1;
    end

    wire [1:0] csr_priv_required = csr_addr[9:8];
    wire csr_read_only_encoding = (csr_addr[11:10] == 2'b11);

    reg csr_read_only_explicit;
    always @(*) begin
        case (csr_addr)
            12'h301, 12'hF11, 12'hF12, 12'hF13, 12'hF14,
            12'hC00, 12'hC01, 12'hC02, 12'hC80, 12'hC81, 12'hC82:
                csr_read_only_explicit = 1'b1;
            default:
                csr_read_only_explicit = 1'b0;
        endcase
    end

    wire csr_read_only = csr_read_only_encoding || csr_read_only_explicit;

    wire priv_ok =
        (csr_priv_required == 2'b00) ||
        (csr_priv_required == 2'b01 && priv_q != 2'b00) ||
        (csr_priv_required == 2'b11 && priv_q == 2'b11);

    // TVM makes satp access illegal in S-mode.
    wire tvm_block = (csr_addr == 12'h180) && (priv_q == 2'b01) && mstatus_q[20];

    // Counter-enable checks (cycle/time/instret).
    reg [2:0] counter_bit;
    reg       counter_block;
    always @(*) begin
        counter_bit = 3'd0;
        counter_block = 1'b0;
        case (csr_addr)
            12'hC00, 12'hC80: counter_bit = 3'd0; // cycle
            12'hC01, 12'hC81: counter_bit = 3'd1; // time
            12'hC02, 12'hC82: counter_bit = 3'd2; // instret
            default: counter_block = 1'b0;
        endcase
        if (counter_bit != 3'd0 || csr_addr == 12'hC00 || csr_addr == 12'hC01 ||
            csr_addr == 12'hC02 || csr_addr == 12'hC80 || csr_addr == 12'hC81 ||
            csr_addr == 12'hC82) begin
            if (priv_q == 2'b00)
                counter_block = !(mcounteren_q[counter_bit] && scounteren_q[counter_bit]);
            else if (priv_q == 2'b01)
                counter_block = !mcounteren_q[counter_bit];
        end
    end

    assign csr_illegal = csr_access &&
        (!csr_known || !priv_ok || tvm_block ||
         (csr_we && csr_read_only) || counter_block);

    // -------------------------------------------------------------
    // CSR read mux
    // -------------------------------------------------------------
    reg [31:0] rdata;
    always @(*) begin
        case (csr_addr)
            12'h100: rdata = mstatus_q & SSTATUS_WMASK;       // sstatus
            12'h104: rdata = mie_q & SIE_MASK;                 // sie
            12'h105: rdata = stvec_q;
            12'h106: rdata = scounteren_q;
            12'h140: rdata = sscratch_q;
            12'h141: rdata = sepc_q;
            12'h142: rdata = scause_q;
            12'h143: rdata = stval_q;
            12'h144: rdata = mip_all & SIE_MASK;               // sip
            12'h180: rdata = satp_q;

            12'h300: rdata = mstatus_q;
            12'h301: rdata = MISA_VALUE;
            12'h302: rdata = medeleg_q;
            12'h303: rdata = mideleg_q;
            12'h304: rdata = mie_q;
            12'h305: rdata = mtvec_q;
            12'h306: rdata = mcounteren_q;
            12'h340: rdata = mscratch_q;
            12'h341: rdata = mepc_q;
            12'h342: rdata = mcause_q;
            12'h343: rdata = mtval_q;
            12'h344: rdata = mip_all;
            12'h3A0: rdata = pmpcfg0_q;
            12'h3A1: rdata = pmpcfg1_q;
            12'h3A2: rdata = pmpcfg2_q;
            12'h3A3: rdata = pmpcfg3_q;

            12'hB00: rdata = mcycle_q;
            12'hB02: rdata = minstret_q;
            12'hB80: rdata = mcycleh_q;
            12'hB82: rdata = minstreth_q;

            12'hC00, 12'hC01: rdata = mcycle_q;
            12'hC02: rdata = minstret_q;
            12'hC80, 12'hC81: rdata = mcycleh_q;
            12'hC82: rdata = minstreth_q;

            12'hF11, 12'hF12, 12'hF13, 12'hF14: rdata = 32'd0;
            default: rdata = 32'd0;
        endcase
        // PMP address registers.
        if (csr_addr >= 12'h3B0 && csr_addr <= 12'h3BF)
            rdata = pmpaddr_flat_q[(csr_addr - 12'h3B0) * 32 +: 32];
    end
    assign csr_rdata = rdata;

    // -------------------------------------------------------------
    // PMP lock helpers
    // -------------------------------------------------------------
    wire pmp_l0  = pmpcfg0_q[7];
    wire pmp_l1  = pmpcfg0_q[15];
    wire pmp_l2  = pmpcfg0_q[23];
    wire pmp_l3  = pmpcfg0_q[31];
    wire pmp_l4  = pmpcfg1_q[7];
    wire pmp_l5  = pmpcfg1_q[15];
    wire pmp_l6  = pmpcfg1_q[23];
    wire pmp_l7  = pmpcfg1_q[31];
    wire pmp_l8  = pmpcfg2_q[7];
    wire pmp_l9  = pmpcfg2_q[15];
    wire pmp_l10 = pmpcfg2_q[23];
    wire pmp_l11 = pmpcfg2_q[31];
    wire pmp_l12 = pmpcfg3_q[7];
    wire pmp_l13 = pmpcfg3_q[15];
    wire pmp_l14 = pmpcfg3_q[23];
    wire pmp_l15 = pmpcfg3_q[31];

    // -------------------------------------------------------------
    // Sequential state
    // -------------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            priv_q        <= 2'b11;
            mstatus_q     <= 32'd0;
            medeleg_q     <= 32'd0;
            mideleg_q     <= 32'd0;
            mie_q         <= 32'd0;
            mtvec_q       <= 32'd0;
            mscratch_q    <= 32'd0;
            mepc_q        <= 32'd0;
            mcause_q      <= 32'd0;
            mtval_q       <= 32'd0;
            stvec_q       <= 32'd0;
            sscratch_q    <= 32'd0;
            sepc_q        <= 32'd0;
            scause_q      <= 32'd0;
            stval_q       <= 32'd0;
            satp_q        <= 32'd0;
            mcounteren_q  <= 32'd0;
            scounteren_q  <= 32'd0;
            mcycle_q      <= 32'd0;
            mcycleh_q     <= 32'd0;
            minstret_q    <= 32'd0;
            minstreth_q   <= 32'd0;
            ssip_q        <= 1'b0;
            pmpcfg0_q     <= 32'd0;
            pmpcfg1_q     <= 32'd0;
            pmpcfg2_q     <= 32'd0;
            pmpcfg3_q     <= 32'd0;
            pmpaddr_flat_q <= 512'd0;
        end else begin
            // Cycle counter increments every clock; instret only retires.
            mcycle_q <= mcycle_q + 32'd1;
            if (mcycle_q == 32'hFFFF_FFFF) begin
                mcycle_q  <= 32'd0;
                mcycleh_q <= mcycleh_q + 32'd1;
            end
            if (commit_enable && retire) begin
                minstret_q <= minstret_q + 32'd1;
                if (minstret_q == 32'hFFFF_FFFF)
                    minstreth_q <= minstreth_q + 32'd1;
            end

            if (commit_enable) begin
                // -------------------------------------------------
                // Trap entry has priority over CSR writes and returns.
                // -------------------------------------------------
                if (trap_valid) begin
                    if (trap_target == 2'b01) begin
                        // Delegated S-mode trap.
                        mstatus_q[5]  <= mstatus_q[1];          // SPIE = SIE
                        mstatus_q[1]  <= 1'b0;                  // SIE = 0
                        mstatus_q[8]  <= priv_q[0];             // SPP = U/S
                        sepc_q        <= {trap_epc[31:2], 2'b00};
                        scause_q      <= trap_cause;
                        stval_q       <= trap_tval;
                        priv_q        <= 2'b01;
                    end else begin
                        // M-mode trap.
                        mstatus_q[7]  <= mstatus_q[3];          // MPIE = MIE
                        mstatus_q[3]  <= 1'b0;                  // MIE = 0
                        mstatus_q[12:11] <= (priv_q == 2'b10) ? 2'b00 : priv_q;
                        mepc_q        <= {trap_epc[31:2], 2'b00};
                        mcause_q      <= trap_cause;
                        mtval_q       <= trap_tval;
                        priv_q        <= 2'b11;
                    end
                end else if (mret_valid) begin
                    mstatus_q[3]     <= mstatus_q[7];           // MIE = MPIE
                    mstatus_q[7]     <= 1'b1;                   // MPIE = 1
                    mstatus_q[12:11] <= 2'b00;                  // MPP = U
                    priv_q           <= (mstatus_q[12:11] == 2'b10) ? 2'b00
                                       : mstatus_q[12:11];
                end else if (sret_valid) begin
                    mstatus_q[1]     <= mstatus_q[5];           // SIE = SPIE
                    mstatus_q[5]     <= 1'b1;                   // SPIE = 1
                    mstatus_q[8]     <= 1'b0;                   // SPP = U
                    priv_q           <= {1'b0, mstatus_q[8]};
                end else if (csr_commit && csr_we && !csr_illegal) begin
                    case (csr_addr)
                        12'h100: begin // sstatus
                            mstatus_q <= (mstatus_q & ~SSTATUS_WMASK) |
                                         (csr_wdata & SSTATUS_WMASK);
                        end
                        12'h104: begin // sie: S bits of mie
                            mie_q <= (mie_q & ~SIE_MASK) |
                                     (csr_wdata & SIE_MASK);
                        end
                        12'h105: begin // stvec
                            stvec_q <= {csr_wdata[31:2],
                                        (csr_wdata[1:0] == 2'b01) ? 2'b01 : 2'b00};
                        end
                        12'h106: scounteren_q <= csr_wdata & COUNTER_MASK;
                        12'h140: sscratch_q <= csr_wdata;
                        12'h141: sepc_q <= {csr_wdata[31:2], 2'b00};
                        12'h142: scause_q <= csr_wdata;
                        12'h143: stval_q <= csr_wdata;
                        12'h144: begin // sip: only SSIP is software-writable
                            ssip_q <= csr_wdata[1];
                        end
                        12'h180: satp_q <= csr_wdata;

                        12'h300: begin // mstatus
                            mstatus_q <= (mstatus_q & ~MSTATUS_WMASK) |
                                         (csr_wdata & MSTATUS_WMASK);
                        end
                        12'h302: medeleg_q <= csr_wdata & MEDELEG_MASK;
                        12'h303: mideleg_q <= csr_wdata & MIDELEG_MASK;
                        12'h304: mie_q <= csr_wdata & MIE_MASK;
                        12'h305: begin // mtvec
                            mtvec_q <= {csr_wdata[31:2],
                                        (csr_wdata[1:0] == 2'b01) ? 2'b01 : 2'b00};
                        end
                        12'h306: mcounteren_q <= csr_wdata & COUNTER_MASK;
                        12'h340: mscratch_q <= csr_wdata;
                        12'h341: mepc_q <= {csr_wdata[31:2], 2'b00};
                        12'h342: mcause_q <= csr_wdata;
                        12'h343: mtval_q <= csr_wdata;
                        12'h344: begin // mip: only SSIP is software-writable
                            ssip_q <= csr_wdata[1];
                        end

                        12'h3A0: begin
                            if (!pmp_l0)  pmpcfg0_q[7:0]   <= csr_wdata[7:0];
                            if (!pmp_l1)  pmpcfg0_q[15:8]  <= csr_wdata[15:8];
                            if (!pmp_l2)  pmpcfg0_q[23:16] <= csr_wdata[23:16];
                            if (!pmp_l3)  pmpcfg0_q[31:24] <= csr_wdata[31:24];
                        end
                        12'h3A1: begin
                            if (!pmp_l4)  pmpcfg1_q[7:0]   <= csr_wdata[7:0];
                            if (!pmp_l5)  pmpcfg1_q[15:8]  <= csr_wdata[15:8];
                            if (!pmp_l6)  pmpcfg1_q[23:16] <= csr_wdata[23:16];
                            if (!pmp_l7)  pmpcfg1_q[31:24] <= csr_wdata[31:24];
                        end
                        12'h3A2: begin
                            if (!pmp_l8)  pmpcfg2_q[7:0]   <= csr_wdata[7:0];
                            if (!pmp_l9)  pmpcfg2_q[15:8]  <= csr_wdata[15:8];
                            if (!pmp_l10) pmpcfg2_q[23:16] <= csr_wdata[23:16];
                            if (!pmp_l11) pmpcfg2_q[31:24] <= csr_wdata[31:24];
                        end
                        12'h3A3: begin
                            if (!pmp_l12) pmpcfg3_q[7:0]   <= csr_wdata[7:0];
                            if (!pmp_l13) pmpcfg3_q[15:8]  <= csr_wdata[15:8];
                            if (!pmp_l14) pmpcfg3_q[23:16] <= csr_wdata[23:16];
                            if (!pmp_l15) pmpcfg3_q[31:24] <= csr_wdata[31:24];
                        end

                        12'hB00: mcycle_q    <= csr_wdata;
                        12'hB02: minstret_q  <= csr_wdata;
                        12'hB80: mcycleh_q   <= csr_wdata;
                        12'hB82: minstreth_q <= csr_wdata;
                        default: begin
                            // PMP address registers.
                            if (csr_addr >= 12'h3B0 && csr_addr <= 12'h3BF) begin
                                case (csr_addr - 12'h3B0)
                                    12'd0:  if (!pmp_l0)  pmpaddr_flat_q[0*32 +: 32]  <= csr_wdata;
                                    12'd1:  if (!pmp_l1)  pmpaddr_flat_q[1*32 +: 32]  <= csr_wdata;
                                    12'd2:  if (!pmp_l2)  pmpaddr_flat_q[2*32 +: 32]  <= csr_wdata;
                                    12'd3:  if (!pmp_l3)  pmpaddr_flat_q[3*32 +: 32]  <= csr_wdata;
                                    12'd4:  if (!pmp_l4)  pmpaddr_flat_q[4*32 +: 32]  <= csr_wdata;
                                    12'd5:  if (!pmp_l5)  pmpaddr_flat_q[5*32 +: 32]  <= csr_wdata;
                                    12'd6:  if (!pmp_l6)  pmpaddr_flat_q[6*32 +: 32]  <= csr_wdata;
                                    12'd7:  if (!pmp_l7)  pmpaddr_flat_q[7*32 +: 32]  <= csr_wdata;
                                    12'd8:  if (!pmp_l8)  pmpaddr_flat_q[8*32 +: 32]  <= csr_wdata;
                                    12'd9:  if (!pmp_l9)  pmpaddr_flat_q[9*32 +: 32]  <= csr_wdata;
                                    12'd10: if (!pmp_l10) pmpaddr_flat_q[10*32 +: 32] <= csr_wdata;
                                    12'd11: if (!pmp_l11) pmpaddr_flat_q[11*32 +: 32] <= csr_wdata;
                                    12'd12: if (!pmp_l12) pmpaddr_flat_q[12*32 +: 32] <= csr_wdata;
                                    12'd13: if (!pmp_l13) pmpaddr_flat_q[13*32 +: 32] <= csr_wdata;
                                    12'd14: if (!pmp_l14) pmpaddr_flat_q[14*32 +: 32] <= csr_wdata;
                                    12'd15: if (!pmp_l15) pmpaddr_flat_q[15*32 +: 32] <= csr_wdata;
                                    default: ;
                                endcase
                            end
                        end
                    endcase
                end
            end

        end
    end

endmodule
