`timescale 1ns/1ps
module tb_mem_adapt #(parameter integer SYNC=0);
    reg clk=0,rst_n=0;
    wire [31:0] pc,inst,addr,wdata,rdata,stop_pc;
    wire wren,stopped;wire [3:0] wstrb;wire [1:0] stop_kind;
    integer physical=0,advances=0,memory_holds=0,stall=0,flush=0,raw_stall=0,raw_flush=0;
    integer tail=0,limit=4000,trace_fd,rf_fd,ram_fd,i,ram_bytes=256;
    reg [31:0] held_state[0:27];
    reg last_hold=0;
    cpu #(.SYNC_MEMORY(SYNC)) dut(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),
        .mem_addr(addr),.mem_wdata(wdata),.mem_wren(wren),.mem_wstrb(wstrb),.mem_rdata(rdata),
        .eei_stop_valid(stopped),.eei_stop_kind(stop_kind),.eei_stop_pc(stop_pc));
    memory_model #(.LATENCY(SYNC)) memory(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),
        .addr(addr),.wdata(wdata),.wren(wren),.wstrb(wstrb),.rdata(rdata));
    always #5 clk=~clk;
    initial begin
        if(!$value$plusargs("MAX_CYCLES=%d",limit)) limit=4000;
        if(!$value$plusargs("RAM_BYTES=%d",ram_bytes)) ram_bytes=256;
        if(limit<1 || limit>20000000) $fatal(1,"INPUT cycle limit");
        trace_fd=$fopen("trace.log","w");if(!trace_fd) $fatal(1,"trace open");
        $dumpfile("wave.vcd");$dumpvars(0,dut);$dumpvars(1,tb_mem_adapt);$dumpvars(1,memory);
        repeat(4) @(negedge clk);rst_n=1;
    end
    // No force/initialization of CPU registers. All images traverse normal CPU paths.
    always @(posedge clk) if(rst_n) begin
        physical=physical+1;
        if(physical>limit) $fatal(1,"TIMEOUT physical cycle limit");
        if(physical==4096) $dumpoff;
        if(physical%500000==0) $display("PROGRESS physical=%0d advances=%0d",physical,advances);
        if((^{dut.pipeline_advance,dut.memory_phase,dut.id_valid,dut.ex_valid,dut.mem_valid,
              dut.mem_reg_write,wren,dut.stall_if,dut.flush_if,stopped})===1'bx) $fatal(1,"UNKNOWN control");
        if(dut.stall_if) raw_stall=raw_stall+1;
        if(dut.flush_if) raw_flush=raw_flush+1;
        if(dut.pipeline_advance) begin
            advances=advances+1;
            if(dut.stall_if) stall=stall+1;
            if(dut.flush_if) flush=flush+1;
            if(dut.id_valid && !dut.eei_hold) begin
                if((^{dut.id_pc,dut.forward_rs1,dut.forward_rs2,dut.id_alu_ctrl})===1'bx) $fatal(1,"UNKNOWN EX");
                $fdisplay(trace_fd,"EX|%08x",dut.id_pc);
            end
            if(dut.ex_valid && dut.ex_mem_to_reg) begin
                if((^{addr,rdata,dut.mem_load_data,dut.ex_pc})===1'bx) $fatal(1,"UNKNOWN READ");
                $fdisplay(trace_fd,"READ|%08x|%08x|%08x|%08x",dut.ex_pc,addr,rdata,dut.mem_load_data);
            end
            if(!dut.flush_if && !dut.stall_if && !dut.eei_hold && inst!==memory.rom[pc>>2])
                $fatal(1,"FETCH_RESPONSE wrong PC/word");
        end else memory_holds=memory_holds+1;
        // Observe the actual RF write enable, not a held pipeline WB intent.
        if(dut.rf.we && dut.mem_rd!=0) begin
            if((^{dut.mem_rd,dut.wb_write_data})===1'bx) $fatal(1,"UNKNOWN WB");
            $fdisplay(trace_fd,"WB|%0d|%08x",dut.mem_rd,dut.wb_write_data);
        end
        if(wren) begin
            if(!dut.ex_valid || (SYNC && dut.pipeline_advance)) $fatal(1,"STORE wrong phase/valid");
            if((^{dut.ex_pc,addr,wdata,wstrb})===1'bx) $fatal(1,"UNKNOWN STORE");
            $fdisplay(trace_fd,"STORE|%08x|%08x|%08x|%01x",dut.ex_pc,addr,wdata,wstrb);
        end
        if(!wren && wstrb!==0) $fatal(1,"IDLE nonzero write mask");
        if(SYNC && !dut.pipeline_advance && dut.rf.we) $fatal(1,"WB during hold");
        if(stopped && (wren || (dut.rf.we && dut.mem_rd!=0))) $fatal(1,"STOP side effect");
        if(stopped) $dumpon;
        if(!dut.pipeline_advance) begin
            held_state[0]=dut.pc_reg;held_state[1]=dut.if_pc;held_state[2]=dut.if_inst;
            held_state[3]=dut.id_pc;held_state[4]=dut.id_rs1_data;held_state[5]=dut.id_rs2_data;held_state[6]=dut.id_imm;
            held_state[7]={dut.id_rs1,dut.id_rs2,dut.id_rd};
            held_state[8]={dut.id_reg_write,dut.id_mem_write,dut.id_mem_to_reg,dut.id_alu_src,dut.id_branch,dut.id_jump,dut.id_auipc,dut.id_alu_ctrl,dut.id_funct3};
            held_state[9]=dut.ex_pc;held_state[10]=dut.ex_alu_result;held_state[11]=dut.ex_rs2_data;
            held_state[12]={dut.ex_rd,dut.ex_reg_write,dut.ex_mem_write,dut.ex_mem_to_reg,dut.ex_branch,dut.ex_jump,dut.ex_funct3};
            held_state[13]=dut.mem_alu_result;held_state[14]=dut.mem_mem_rdata;
            held_state[15]={dut.mem_rd,dut.mem_reg_write,dut.mem_mem_to_reg};
            held_state[16]={dut.if_valid,dut.id_valid,dut.ex_valid,dut.mem_valid,dut.id_system_kind,dut.eei_state,dut.eei_stop_valid,dut.eei_stop_kind};
            held_state[17]=dut.eei_stop_pc;
            #1;
            if(held_state[0]!==dut.pc_reg || held_state[1]!==dut.if_pc || held_state[2]!==dut.if_inst ||
               held_state[3]!==dut.id_pc || held_state[4]!==dut.id_rs1_data || held_state[5]!==dut.id_rs2_data || held_state[6]!==dut.id_imm ||
               held_state[7]!=={17'd0,dut.id_rs1,dut.id_rs2,dut.id_rd} ||
               held_state[8]!=={17'd0,dut.id_reg_write,dut.id_mem_write,dut.id_mem_to_reg,dut.id_alu_src,dut.id_branch,dut.id_jump,dut.id_auipc,dut.id_alu_ctrl,dut.id_funct3} ||
               held_state[9]!==dut.ex_pc || held_state[10]!==dut.ex_alu_result || held_state[11]!==dut.ex_rs2_data ||
               held_state[12]!=={19'd0,dut.ex_rd,dut.ex_reg_write,dut.ex_mem_write,dut.ex_mem_to_reg,dut.ex_branch,dut.ex_jump,dut.ex_funct3} ||
               held_state[13]!==dut.mem_alu_result || held_state[14]!==dut.mem_mem_rdata ||
               held_state[15]!=={25'd0,dut.mem_rd,dut.mem_reg_write,dut.mem_mem_to_reg} ||
               held_state[16]!=={21'd0,dut.if_valid,dut.id_valid,dut.ex_valid,dut.mem_valid,dut.id_system_kind,dut.eei_state,dut.eei_stop_valid,dut.eei_stop_kind} ||
               held_state[17]!==dut.eei_stop_pc) $fatal(1,"HOLD_STATE changed");
        end
    end
    always @(negedge clk) if(rst_n && stopped) begin
        tail=tail+1;
        if(tail==(SYNC?8:4)) begin
            rf_fd=$fopen("registers.hex","w");ram_fd=$fopen("ram.hex","w");
            if(!rf_fd || !ram_fd) $fatal(1,"output open");
            for(i=0;i<32;i=i+1) $fdisplay(rf_fd,"%08x",dut.rf.regs[i]);
            for(i=0;i<ram_bytes;i=i+1) $fdisplay(ram_fd,"%02x",(memory.ram[i>>2]>>((i%4)*8))&255);
            $fclose(rf_fd);$fclose(ram_fd);$fclose(trace_fd);
            $display("METRICS|physical=%0d|advances=%0d|memory_holds=%0d|stall=%0d|flush=%0d|raw_stall=%0d|raw_flush=%0d|tail=%0d|time_ps=%0t",physical,advances,memory_holds,stall,flush,raw_stall,raw_flush,tail,$time);
            $display("STOP|%0d|%08x",stop_kind,stop_pc);
            $display("SIMULATION_ENDED_NOT_FUNCTIONAL_PASS");$finish;
        end
    end
endmodule
