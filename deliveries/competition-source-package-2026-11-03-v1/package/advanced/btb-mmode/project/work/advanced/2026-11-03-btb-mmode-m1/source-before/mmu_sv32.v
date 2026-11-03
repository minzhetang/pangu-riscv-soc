`timescale 1ns/1ps
// =================================================================
// Sv32 TLB + hardware page-table walker for the HL4 candidate.
//
// This is a compact 32-entry direct-mapped I/D TLB pair with a shared
// two-level Sv32 page-table walker.  The page-table port is separate from
// the normal data port; the SoC/testbench supplies a read port into the
// same physical RAM.
//
// Supported:
//   - 4 KiB pages
//   - 4 MiB superpages (root-level leaf PTE)
//   - U/S permission checks, SUM and MXR
//   - satp ASID is not tagged; software must flush on ASID changes
//   - hardware A/D updates on successful leaf translations
// =================================================================
module mmu_sv32 (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        step,          // pipeline advance

    input  wire [31:0] satp,
    input  wire [1:0]  priv,           // current fetch privilege
    input  wire        sum,
    input  wire        mxr,
    input  wire        flush,

    // Instruction translation port.
    input  wire [31:0] i_va,
    input  wire        i_req,
    output wire [31:0] i_pa,
    output wire        i_hit,
    output wire        i_fault,

    // Data translation port.  d_priv is the MPRV-resolved privilege.
    input  wire [31:0] d_va,
    input  wire        d_req,
    input  wire        d_store,
    input  wire [1:0]  d_priv,
    output wire [31:0] d_pa,
    output wire        d_hit,
    output wire        d_fault,

    // Physical page-table port.  The read address must remain stable until
    // the next walker step; pt_we/pt_wdata update the A/D bits of a
    // successfully translated leaf PTE.
    output wire [31:0] pt_addr,
    input  wire [31:0] pt_rdata,
    output wire        pt_we,
    output wire [31:0] pt_wdata,

    output wire        busy
);
    localparam integer TLB_ENTRIES = 32;

    localparam [2:0] ST_IDLE      = 3'd0,
                     ST_ROOT_REQ  = 3'd1,
                     ST_ROOT_WAIT = 3'd2,
                     ST_LEAF_REQ  = 3'd3,
                     ST_LEAF_WAIT = 3'd4,
                     ST_DONE      = 3'd5,
                     ST_FAULT     = 3'd6;

    reg        i_valid [0:TLB_ENTRIES-1];
    reg [31:0] i_tag   [0:TLB_ENTRIES-1];
    reg [21:0] i_ppn   [0:TLB_ENTRIES-1];
    reg [3:0]  i_perm  [0:TLB_ENTRIES-1]; // {U,X,W,R}
    reg        i_super [0:TLB_ENTRIES-1];

    reg        d_valid [0:TLB_ENTRIES-1];
    reg [31:0] d_tag   [0:TLB_ENTRIES-1];
    reg [21:0] d_ppn   [0:TLB_ENTRIES-1];
    reg [3:0]  d_perm  [0:TLB_ENTRIES-1];
    reg        d_super [0:TLB_ENTRIES-1];
    reg        d_dirty [0:TLB_ENTRIES-1];

    reg [2:0]  state;
    reg [31:0] req_va;
    reg        req_data;
    reg        req_store;
    reg [1:0]  req_priv;
    reg        req_sum;
    reg        req_mxr;
    reg [31:0] root_addr_q;
    reg [31:0] leaf_addr_q;
    reg [31:0] pte1_q;

    reg        i_fault_q;
    reg        d_fault_q;
    reg [31:0] i_fault_va;
    reg [31:0] d_fault_va;

    wire satp_active = satp[31];
    wire i_translate = i_req && satp_active && (priv != 2'b11);
    wire d_translate = d_req && satp_active && (d_priv != 2'b11);

    wire [4:0] i_idx = i_va[16:12];
    wire [4:0] d_idx = d_va[16:12];

    wire i_tag_match = i_valid[i_idx] &&
        (i_super[i_idx] ? (i_tag[i_idx][31:22] == i_va[31:22])
                        : (i_tag[i_idx][31:12] == i_va[31:12]));
    wire d_tag_match = d_valid[d_idx] &&
        (d_super[d_idx] ? (d_tag[d_idx][31:22] == d_va[31:22])
                        : (d_tag[d_idx][31:12] == d_va[31:12]));

    function automatic perm_ok;
        input [3:0]  p;       // {U,X,W,R}
        input [1:0]  mode;
        input        is_store;
        input        is_fetch;
        input        use_sum;
        input        use_mxr;
        begin
            // Keep this as one continuous expression.  PDS 2022.2 mis-handles
            // the intermediate "ok" variable in this automatic function.
            perm_ok =
                (mode == 2'b11) ? 1'b1 :
                (mode == 2'b00) ?
                    (!p[3] ? 1'b0 :
                     is_fetch ? p[2] :
                     is_store ? p[1] :
                     (p[0] || (use_mxr && p[2]))) :
                    ((p[3] && (is_fetch || !use_sum)) ? 1'b0 :
                     is_fetch ? p[2] :
                     is_store ? p[1] :
                     (p[0] || (use_mxr && p[2])));
        end
    endfunction

    wire i_tlb_ok = i_tag_match &&
        perm_ok(i_perm[i_idx], priv, 1'b0, 1'b1, sum, mxr);
    wire d_tlb_ok = d_tag_match &&
        perm_ok(d_perm[d_idx], d_priv, d_store, 1'b0, sum, mxr);

    wire i_fault_match = i_tag_match && !i_tlb_ok;
    wire d_fault_match = d_tag_match && !d_tlb_ok;

    wire i_walk_fault = i_fault_q && (i_va == i_fault_va);
    wire d_walk_fault = d_fault_q && (d_va == d_fault_va);

    // A store hit in a TLB entry installed by a load still needs the PTE D
    // bit updated.  Treat that case as a walk so the shared A/D write-back
    // path handles it, then install the entry with dirty=1.
    wire d_ad_miss = d_translate && d_tag_match && d_tlb_ok &&
                     d_store && !d_dirty[d_idx];

    wire i_miss = i_translate && !i_tag_match && !i_walk_fault;
    wire d_miss = d_translate &&
                  ((!d_tag_match && !d_walk_fault) || d_ad_miss);

    assign i_hit = !i_translate || i_tlb_ok;
    assign d_hit = !d_translate || (d_tlb_ok && !d_ad_miss);
    assign i_fault = i_translate && (i_fault_match || i_walk_fault);
    assign d_fault = d_translate && (d_fault_match || d_walk_fault);

    assign i_pa = !i_translate ? i_va :
                  (i_super[i_idx] ? {i_ppn[i_idx][19:10], i_va[21:0]}
                                  : {i_ppn[i_idx][19:0], i_va[11:0]});
    assign d_pa = !d_translate ? d_va :
                  (d_super[d_idx] ? {d_ppn[d_idx][19:10], d_va[21:0]}
                                  : {d_ppn[d_idx][19:0], d_va[11:0]});

    assign busy = (state != ST_IDLE);
    assign pt_addr = (state == ST_ROOT_REQ || state == ST_ROOT_WAIT)
                   ? root_addr_q
                   : (state == ST_LEAF_REQ || state == ST_LEAF_WAIT)
                   ? leaf_addr_q : 32'd0;

    // Hardware A/D update.  A translation that succeeds sets A (and D for a
    // store) in the leaf PTE.  The write is issued on the walker's final
    // WAIT step, at the same time the TLB entry is installed.
    wire root_leaf_ok =
        (pt_rdata[0] && (pt_rdata[1] || pt_rdata[3]) &&
         !(pt_rdata[1] == 1'b0 && pt_rdata[2] == 1'b1) &&
         (pt_rdata[19:10] == 10'd0) &&
         perm_ok({pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]},
                 req_priv, req_store, !req_data, req_sum, req_mxr));
    wire leaf_ok =
        pt_rdata[0] && (pt_rdata[1] || pt_rdata[3]) &&
        !(pt_rdata[1] == 1'b0 && pt_rdata[2] == 1'b1) &&
        perm_ok({pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]},
                req_priv, req_store, !req_data, req_sum, req_mxr);
    wire ad_needed = !pt_rdata[6] || (req_store && !pt_rdata[7]);
    assign pt_we = step && !flush && ad_needed &&
        ((state == ST_ROOT_WAIT && root_leaf_ok) ||
         (state == ST_LEAF_WAIT && leaf_ok));
    assign pt_wdata = pt_rdata | 32'h0000_0040 |
                      (req_store ? 32'h0000_0080 : 32'd0);

    // Choose a new walk only when the walker is idle.  Data has priority.
    wire start_walk = (state == ST_IDLE) && (d_miss || i_miss);
    wire start_data = d_miss;

    integer j;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state       <= ST_IDLE;
            req_va      <= 32'd0;
            req_data    <= 1'b0;
            req_store   <= 1'b0;
            req_priv    <= 2'b11;
            req_sum     <= 1'b0;
            req_mxr     <= 1'b0;
            root_addr_q <= 32'd0;
            leaf_addr_q <= 32'd0;
            pte1_q      <= 32'd0;
            i_fault_q   <= 1'b0;
            d_fault_q   <= 1'b0;
            i_fault_va  <= 32'd0;
            d_fault_va  <= 32'd0;
            for (j = 0; j < TLB_ENTRIES; j = j + 1) begin
                i_valid[j] <= 1'b0;
                d_valid[j] <= 1'b0;
                d_dirty[j] <= 1'b0;
            end
        end else if (flush) begin
            state <= ST_IDLE;
            for (j = 0; j < TLB_ENTRIES; j = j + 1) begin
                i_valid[j] <= 1'b0;
                d_valid[j] <= 1'b0;
                d_dirty[j] <= 1'b0;
            end
            i_fault_q <= 1'b0;
            d_fault_q <= 1'b0;
        end else if (step) begin
            // Clear a sticky walk fault once the offending request leaves.
            if (i_fault_q && (i_va != i_fault_va)) i_fault_q <= 1'b0;
            if (d_fault_q && (d_va != d_fault_va)) d_fault_q <= 1'b0;

            case (state)
                ST_IDLE: begin
                    if (start_walk) begin
                        req_va    <= start_data ? d_va : i_va;
                        req_data  <= start_data;
                        req_store <= start_data ? d_store : 1'b0;
                        req_priv  <= start_data ? d_priv : priv;
                        req_sum   <= sum;
                        req_mxr   <= mxr;
                        root_addr_q <= {satp[19:0], 12'b0} +
                                       (start_data ? {20'd0, d_va[31:22], 2'b00}
                                                   : {20'd0, i_va[31:22], 2'b00});
                        state <= ST_ROOT_REQ;
                    end
                end

                ST_ROOT_REQ: begin
                    state <= ST_ROOT_WAIT;
                end

                ST_ROOT_WAIT: begin
                    pte1_q <= pt_rdata;
                    if (!pt_rdata[0]) begin
                        // Invalid PTE.
                        if (req_data) begin
                            d_fault_q  <= 1'b1;
                            d_fault_va <= req_va;
                        end else begin
                            i_fault_q  <= 1'b1;
                            i_fault_va <= req_va;
                        end
                        state <= ST_IDLE;
                    end else if (pt_rdata[1] || pt_rdata[3]) begin
                        // Root-level leaf: 4 MiB superpage.  PPN[9:0] must be
                        // zero for the superpage to be aligned, and W=1/R=0 is
                        // a reserved encoding.
                        if ((pt_rdata[1] == 1'b0 && pt_rdata[2] == 1'b1) ||
                            (pt_rdata[19:10] != 10'd0) ||
                            !perm_ok({pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]},
                                     req_priv, req_store, !req_data, req_sum, req_mxr)) begin
                            if (req_data) begin
                                d_fault_q  <= 1'b1;
                                d_fault_va <= req_va;
                            end else begin
                                i_fault_q  <= 1'b1;
                                i_fault_va <= req_va;
                            end
                        end else begin
                            if (req_data) begin
                                d_valid[req_va[16:12]] <= 1'b1;
                                d_tag[req_va[16:12]]   <= req_va;
                                d_ppn[req_va[16:12]]   <= pt_rdata[31:10];
                                d_perm[req_va[16:12]]  <= {pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]};
                                d_super[req_va[16:12]] <= 1'b1;
                                d_dirty[req_va[16:12]] <= pt_rdata[7] || req_store;
                            end else begin
                                i_valid[req_va[16:12]] <= 1'b1;
                                i_tag[req_va[16:12]]   <= req_va;
                                i_ppn[req_va[16:12]]   <= pt_rdata[31:10];
                                i_perm[req_va[16:12]]  <= {pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]};
                                i_super[req_va[16:12]] <= 1'b1;
                            end
                        end
                        state <= ST_DONE;
                    end else begin
                        // Pointer to the second level.  A reserved R=0,W=1
                        // encoding is invalid.
                        if (pt_rdata[2]) begin
                            if (req_data) begin
                                d_fault_q  <= 1'b1;
                                d_fault_va <= req_va;
                            end else begin
                                i_fault_q  <= 1'b1;
                                i_fault_va <= req_va;
                            end
                            state <= ST_IDLE;
                        end else begin
                            leaf_addr_q <= {pt_rdata[29:10], 12'b0} +
                                           (req_data ? {20'd0, req_va[21:12], 2'b00}
                                                     : {20'd0, req_va[21:12], 2'b00});
                            state <= ST_LEAF_REQ;
                        end
                    end
                end

                ST_LEAF_REQ: begin
                    state <= ST_LEAF_WAIT;
                end

                ST_LEAF_WAIT: begin
                    if (!pt_rdata[0] || (!pt_rdata[1] && !pt_rdata[3]) ||
                        (pt_rdata[1] == 1'b0 && pt_rdata[2] == 1'b1)) begin
                        if (req_data) begin
                            d_fault_q  <= 1'b1;
                            d_fault_va <= req_va;
                        end else begin
                            i_fault_q  <= 1'b1;
                            i_fault_va <= req_va;
                        end
                        state <= ST_IDLE;
                    end else if (!perm_ok({pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]},
                                          req_priv, req_store, !req_data, req_sum, req_mxr)) begin
                        if (req_data) begin
                            d_fault_q  <= 1'b1;
                            d_fault_va <= req_va;
                        end else begin
                            i_fault_q  <= 1'b1;
                            i_fault_va <= req_va;
                        end
                        state <= ST_IDLE;
                    end else begin
                        if (req_data) begin
                            d_valid[req_va[16:12]] <= 1'b1;
                            d_tag[req_va[16:12]]   <= req_va;
                            d_ppn[req_va[16:12]]   <= pt_rdata[31:10];
                            d_perm[req_va[16:12]]  <= {pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]};
                            d_super[req_va[16:12]] <= 1'b0;
                            d_dirty[req_va[16:12]] <= pt_rdata[7] || req_store;
                        end else begin
                            i_valid[req_va[16:12]] <= 1'b1;
                            i_tag[req_va[16:12]]   <= req_va;
                            i_ppn[req_va[16:12]]   <= pt_rdata[31:10];
                            i_perm[req_va[16:12]]  <= {pt_rdata[4], pt_rdata[3], pt_rdata[2], pt_rdata[1]};
                            i_super[req_va[16:12]] <= 1'b0;
                        end
                        state <= ST_DONE;
                    end
                end

                ST_DONE: begin
                    state <= ST_IDLE;
                end

                ST_FAULT: begin
                    state <= ST_IDLE;
                end

                default: state <= ST_IDLE;
            endcase
        end
    end
endmodule
