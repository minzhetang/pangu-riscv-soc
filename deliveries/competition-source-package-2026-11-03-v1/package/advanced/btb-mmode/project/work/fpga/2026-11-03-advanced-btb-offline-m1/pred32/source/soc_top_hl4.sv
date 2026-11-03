`timescale 1ns/1ps
// HL4 SoC: five-stage CPU with BTB + M/S/U privilege, PMP, traps and Sv32.
//
// Address map (same byte windows as the frozen baseline):
//   0x00000000..0x00007fff  ROM / instruction memory
//   0x00010000..0x00017fff  RAM / data memory
//   0x00020000..0x00021fff  page-table RAM (root + leaf, 8 KiB)
//   0x20000000..0x200000ff  local IO (TX, GPIO, MTIMECMP, MSIP)
//   0x20000100              mtime low  (read-only)
//   0x20000104              mtime high (read-only)
//
// Page-table RAM is a separate simple dual-port array: CPU stores use the
// write port while the Sv32 walker uses the read port.  Keeping it apart from
// the program/data RAM makes the walker timing independent of the normal
// load/store port.
module soc_top_hl4 #(
    parameter integer CLKS_PER_BIT  = 16,
    parameter integer BTB_INDEX_BITS = 6,
    parameter integer BTB_ENABLE     = 1,
    parameter integer SYNC_MEMORY    = 1
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire [7:0]  gpio_in_async,
    output wire        uart_tx,
    output wire [7:0]  gpio_out,
    output wire        write_error,

    // Interrupt/debug observability (also useful for ILA bring-up).
    output wire        timer_irq,
    output wire        soft_irq,
    output wire [31:0] dbg_mepc,
    output wire [31:0] dbg_mcause,
    output wire [31:0] dbg_mtval,
    output wire [31:0] dbg_mstatus,
    output wire        dbg_trap,
    output wire [31:0] dbg_trap_pc,
    output wire [31:0] dbg_sepc,
    output wire [31:0] dbg_scause,
    output wire [31:0] dbg_stval,
    output wire [31:0] dbg_sstatus,
    output wire [1:0]  dbg_priv
);

    wire [31:0] pc, pc_phys, inst, address, wdata, rdata, mem_rdata, io_rdata, io_wdata;
    wire [31:0] pt_addr, pt_rdata, mmu_pt_wdata;
    wire        mmu_pt_we;
    wire [31:0] ex_addr;
    wire        ex_is_store;
    wire        wren, ram_we, io_sel, io_we, io_error, invalid_write;
    wire [63:0] timer_ticks;
    wire [63:0] mtimecmp;
    wire [31:0] msip;
    wire [3:0]  wstrb, ram_strobe, io_strobe;
    wire [7:0]  io_addr;
    wire        mem_fault, inst_fault;
    wire        addr_pt;
    wire        pt_we;

    cycle_counter64 timer (
        .clk(clk), .rst_n(rst_n), .ticks(timer_ticks)
    );

    // Level-sensitive platform interrupt sources.  MSIP bit 0 is the
    // machine software interrupt; MTIP is the 64-bit compare match.
    assign timer_irq = (timer_ticks >= mtimecmp);
    assign soft_irq  = msip[0];

    cpu_hl4 #(
        .SYNC_MEMORY   (SYNC_MEMORY),
        .BTB_INDEX_BITS(BTB_INDEX_BITS),
        .BTB_ENABLE    (BTB_ENABLE)
    ) cpu_core (
        .clk(clk), .rst_n(rst_n),
        .pc(pc), .pc_phys(pc_phys), .inst(inst),
        .pt_addr(pt_addr), .pt_rdata(pt_rdata),
        .pt_we(mmu_pt_we), .pt_wdata(mmu_pt_wdata),
        .mem_addr(address), .mem_wdata(wdata),
        .mem_wren(wren), .mem_wstrb(wstrb), .mem_rdata(rdata),
        .ex_addr(ex_addr), .ex_is_store(ex_is_store),
        .mem_fault(mem_fault), .inst_fault(inst_fault),
        .timer_irq(timer_irq), .soft_irq(soft_irq), .ext_irq(1'b0),
        .s_timer_irq(1'b0), .s_soft_irq(1'b0), .s_ext_irq(1'b0),
        .dbg_mepc(dbg_mepc), .dbg_mcause(dbg_mcause),
        .dbg_mtval(dbg_mtval), .dbg_mstatus(dbg_mstatus),
        .dbg_trap(dbg_trap), .dbg_trap_pc(dbg_trap_pc),
        .dbg_sepc(dbg_sepc), .dbg_scause(dbg_scause),
        .dbg_stval(dbg_stval), .dbg_sstatus(dbg_sstatus),
        .dbg_priv(dbg_priv)
    );

    // Page-table RAM: 8 KiB, enough for a 4 KiB root and one 4 KiB leaf
    // table.  CPU stores use the write port; the Sv32 walker owns the read
    // port.  A normal CPU data access to this window temporarily shares the
    // read port when the walker is idle.
    reg [31:0] pt_ram [0:2047];
    reg [31:0] pt_rdata_q;
    wire       pt_walk_read = (pt_addr >= 32'h0002_0000) &&
                              (pt_addr <  32'h0002_2000);
    wire [10:0] pt_index = pt_walk_read ? pt_addr[12:2] : address[12:2];

    assign addr_pt = (address >= 32'h0002_0000) &&
                     (address <  32'h0002_2000);
    assign pt_we = wren && addr_pt;
    assign pt_rdata = pt_rdata_q;

    // The page-table RAM is deliberately not initialized in RTL.  Software
    // writes every PTE before enabling Sv32, and leaving it uninitialized lets
    // PDS infer block RAM instead of 65k initialized flip-flops.

    wire       pt_walk_write = rst_n && mmu_pt_we && pt_walk_read;
    wire       pt_cpu_write  = rst_n && pt_we;
    wire       pt_write      = pt_walk_write | pt_cpu_write;
    wire [10:0] pt_waddr     = pt_walk_write ? pt_addr[12:2] : address[12:2];
    wire [31:0] pt_wdata     = pt_walk_write ? mmu_pt_wdata : wdata;
    wire [3:0]  pt_wstrb     = pt_walk_write ? 4'hf : wstrb;

    always @(posedge clk) begin
        if (!rst_n)
            pt_rdata_q <= 32'd0;
        else
            pt_rdata_q <= pt_ram[pt_index];

        // A single write port keeps PDS/BRAM inference happy.  The walker's
        // hardware A/D update has priority over a CPU PTE store.
        if (pt_write) begin
            if (pt_wstrb[0]) pt_ram[pt_waddr][7:0]   <= pt_wdata[7:0];
            if (pt_wstrb[1]) pt_ram[pt_waddr][15:8]  <= pt_wdata[15:8];
            if (pt_wstrb[2]) pt_ram[pt_waddr][23:16] <= pt_wdata[23:16];
            if (pt_wstrb[3]) pt_ram[pt_waddr][31:24] <= pt_wdata[31:24];
        end
    end

    wire [31:0] rdata_raw;
    wire        ram_we_raw;
    wire [3:0]  ram_strobe_raw;
    wire        write_error_raw;
    assign ram_we = ram_we_raw && !addr_pt;
    assign ram_strobe = ram_strobe_raw & {4{!addr_pt}};
    assign rdata = addr_pt ? pt_rdata : rdata_raw;
    assign write_error = write_error_raw && !addr_pt;

    memory_model #(.LATENCY(1), .CASE(0)) storage (
        .clk(clk), .rst_n(rst_n),
        .pc(pc_phys), .inst(inst),
        .addr(address), .wdata(wdata),
        .wren(ram_we), .wstrb(ram_strobe), .rdata(mem_rdata)
    );

    soc_data_adapter route (
        .address(address), .write_data(wdata),
        .write_enable(wren), .write_strobe(wstrb),
        .memory_read_data(mem_rdata), .io_read_data(io_rdata),
        .timer_ticks(timer_ticks),
        .io_write_error(io_error), .cpu_read_data(rdata_raw),
        .memory_write_enable(ram_we_raw), .memory_write_strobe(ram_strobe_raw),
        .io_select(io_sel), .io_write_enable(io_we),
        .io_address(io_addr), .io_write_data(io_wdata),
        .io_write_strobe(io_strobe),
        .invalid_write(invalid_write), .write_error(write_error_raw)
    );

    local_regif_hl2 #(.CLKS_PER_BIT(CLKS_PER_BIT)) peripherals (
        .clk(clk), .rst_n(rst_n),
        .io_sel(io_sel), .io_wr_en(io_we),
        .io_addr(io_addr), .io_wdata(io_wdata),
        .io_wstrb(io_strobe), .gpio_in_async(gpio_in_async),
        .io_rdata(io_rdata), .io_wr_error(io_error),
        .uart_tx(uart_tx), .gpio_out(gpio_out),
        .mtimecmp(mtimecmp), .msip(msip)
    );

    // Access-fault decode.  Decode the current EX-stage ALU result, not the
    // older EX/MEM address, so a load/store is checked in its own cycle.
    // The CPU only uses mem_fault for valid loads and stores, so a
    // non-memory ALU result on ex_addr does not create a trap.
    wire addr_rom   = (ex_addr < 32'h00008000);
    wire addr_ram   = (ex_addr >= 32'h00010000) && (ex_addr < 32'h00018000);
    wire addr_pt_ex = (ex_addr >= 32'h00020000) && (ex_addr < 32'h00022000);
    wire addr_io    = (ex_addr[31:8] == 24'h200000);
    wire addr_timer = (ex_addr == 32'h20000100) || (ex_addr == 32'h20000104);

    // Only RAM and the writable local-IO registers accept stores.  ROM,
    // timer, and reserved IO writes are precise store access faults.
    wire io_store_ok =
        (ex_addr == 32'h2000_0000) ||   // TXDATA
        (ex_addr == 32'h2000_000c) ||   // GPIO_OUT
        (ex_addr == 32'h2000_0014) ||   // MTIMECMP_LO
        (ex_addr == 32'h2000_0018) ||   // MTIMECMP_HI
        (ex_addr == 32'h2000_001c);     // MSIP
    wire io_load_ok =
        (ex_addr == 32'h2000_0000) ||   // TXDATA
        (ex_addr == 32'h2000_0008) ||   // STATUS
        (ex_addr == 32'h2000_000c) ||   // GPIO_OUT
        (ex_addr == 32'h2000_0010) ||   // GPIO_IN
        (ex_addr == 32'h2000_0014) ||   // MTIMECMP_LO
        (ex_addr == 32'h2000_0018) ||   // MTIMECMP_HI
        (ex_addr == 32'h2000_001c);     // MSIP
    wire load_ok  = addr_rom || addr_ram || addr_pt_ex ||
                    (addr_io && io_load_ok) || addr_timer;
    wire store_ok = addr_ram || addr_pt_ex || (addr_io && io_store_ok);
    assign mem_fault = ex_is_store ? !store_ok : !load_ok;

    // Only the ROM is executable, using the translated physical PC.
    assign inst_fault = (pc_phys >= 32'h00008000);

endmodule
