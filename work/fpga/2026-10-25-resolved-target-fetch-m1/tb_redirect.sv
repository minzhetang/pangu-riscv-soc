`timescale 1ns/1ps
module tb_redirect #(parameter integer PF=0);
    reg clk=0,rst_n=0;
    wire [31:0] pc,addr,wdata,stop_pc; reg [31:0] inst=0,rdata=0;
    wire wren,stopped;wire [3:0] strobe;wire [1:0] stop_kind;
    reg [31:0] rom[0:8191],ram[0:8191];reg [4095:0] image_path,data_path;
    integer physical=0,advances=0,stall=0,flush=0,tail=0,limit=4000;
    integer trace_fd,fetch_fd,rf_fd,ram_fd,i,j,requests=0,hits=0,applies=0,cancels=0;
    integer ex_count=0,wb_count=0,store_count=0,reset_pending=0,did_reset=0;
    reg pre_request,pre_hit,pre_redirect;reg [31:0] pre_target,pre_id_pc,pre_pc;
    reg [1023:0] held;
    cpu #(.SYNC_MEMORY(1),.RESOLVED_TARGET_FETCH(PF)) dut(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),
        .mem_addr(addr),.mem_wdata(wdata),.mem_wren(wren),.mem_wstrb(strobe),.mem_rdata(rdata),
        .eei_stop_valid(stopped),.eei_stop_kind(stop_kind),.eei_stop_pc(stop_pc));
    wire [1023:0] architectural_state={dut.pc_reg,dut.if_pc,dut.if_inst,dut.if_valid,
        dut.id_pc,dut.id_rs1_data,dut.id_rs2_data,dut.id_imm,dut.id_rs1,dut.id_rs2,dut.id_rd,
        dut.id_reg_write,dut.id_mem_write,dut.id_mem_to_reg,dut.id_alu_src,dut.id_branch,dut.id_jump,dut.id_auipc,dut.id_alu_ctrl,dut.id_funct3,dut.id_valid,
        dut.ex_pc,dut.ex_alu_result,dut.ex_rs2_data,dut.ex_rd,dut.ex_reg_write,dut.ex_mem_write,dut.ex_mem_to_reg,dut.ex_branch,dut.ex_jump,dut.ex_funct3,dut.ex_valid,
        dut.mem_alu_result,dut.mem_mem_rdata,dut.mem_rd,dut.mem_reg_write,dut.mem_mem_to_reg,dut.mem_valid,
        dut.id_system_kind,dut.eei_state,dut.eei_stop_valid,dut.eei_stop_kind,dut.eei_stop_pc};
    always #5 clk=~clk;
    // A one-edge verification memory, same frozen 32K ROM/32K RAM protocol.
    // No CPU state forcing or final-result initialization.
    always @(posedge clk)begin
        inst <= pc<32768 ? rom[pc>>2] : 32'd0;
        rdata <= addr<32768 ? rom[addr>>2] : ((addr>=65536&&addr<98304)?ram[(addr-65536)>>2]:32'd0);
        if(rst_n&&wren)begin
            if(addr<65536||addr>=98304||strobe==0)$fatal(1,"MEMORY_PROTOCOL");
            for(j=0;j<4;j=j+1)if(strobe[j])ram[(addr-65536)>>2][j*8+:8]<=wdata[j*8+:8];
        end
    end
    initial begin
        if(!$value$plusargs("IMAGE=%s",image_path)||!$value$plusargs("DATA=%s",data_path))$fatal(1,"INPUT_PATH");
        if(!$value$plusargs("MAX_CYCLES=%d",limit))limit=4000;
        if(limit<1||limit>4000)$fatal(1,"LIMIT");
        if($test$plusargs("RESET_PENDING"))reset_pending=1;
        if(reset_pending&&PF!=1)$fatal(1,"RESET_CASE_REQUIRES_PF1");
        for(i=0;i<8192;i=i+1)begin rom[i]=0;ram[i]=32'ha5a5a5a5;end
        $readmemh(image_path,rom);$readmemh(data_path,ram);
        trace_fd=$fopen("trace.log","w");fetch_fd=$fopen("fetch.log","w");
        if(!trace_fd||!fetch_fd)$fatal(1,"LOG_OPEN");
        $dumpfile("wave.vcd");$dumpvars(0,dut);$dumpvars(1,tb_redirect);
        repeat(4)@(negedge clk);rst_n=1;
    end
    always @(posedge clk)begin
        if(!rst_n)begin physical=0;advances=0;stall=0;flush=0;ex_count=0;wb_count=0;store_count=0;end
        else begin
            physical=physical+1;if(physical>limit)$fatal(1,"SYSTEM_TIMEOUT");
            if((^{dut.pipeline_advance,dut.id_valid,dut.ex_valid,dut.mem_valid,dut.eei_hold,
                dut.redirect_request,dut.redirect_fetch_hit,dut.fetch_redirect_valid,wren,stopped})===1'bx)$fatal(1,"UNKNOWN_CONTROL");
            pre_request=dut.redirect_request;pre_hit=dut.redirect_fetch_hit;pre_target=dut.redirect_target;pre_id_pc=dut.id_pc;pre_pc=pc;
            pre_redirect=dut.pipeline_advance&&dut.id_valid&&!dut.eei_hold&&dut.control_flush;
            if(dut.pipeline_advance)begin
                advances=advances+1;if(dut.stall_if)stall=stall+1;if(dut.flush_if)flush=flush+1;
                if(dut.id_valid&&!dut.eei_hold)begin $fdisplay(trace_fd,"EX|%0d|%08x",physical,dut.id_pc);ex_count=ex_count+1;end
                if(dut.ex_valid&&dut.ex_mem_to_reg)$fdisplay(trace_fd,"READ|%0d|%08x|%08x|%08x|%08x",physical,dut.ex_pc,addr,rdata,dut.mem_load_data);
                if(!dut.flush_if&&!dut.stall_if&&!dut.eei_hold&&inst!==(dut.pc_reg<32768?rom[dut.pc_reg>>2]:32'd0))$fatal(1,"FETCH_RESPONSE");
            end
            if(dut.rf.we&&dut.mem_rd!=0)begin $fdisplay(trace_fd,"WB|%0d|%0d|%08x",physical,dut.mem_rd,dut.wb_write_data);wb_count=wb_count+1;end
            if(wren)begin
                if(dut.pipeline_advance||!dut.ex_valid)$fatal(1,"STORE_PHASE");
                $fdisplay(trace_fd,"STORE|%0d|%08x|%08x|%08x|%01x",physical,dut.ex_pc,addr,wdata,strobe);store_count=store_count+1;
            end
            if(!wren&&strobe!==0)$fatal(1,"IDLE_STROBE");
            if(!dut.pipeline_advance&&dut.rf.we)$fatal(1,"HOLD_WB");
            if(stopped&&(wren||(dut.rf.we&&dut.mem_rd!=0)))$fatal(1,"STOP_SIDE_EFFECT");
            if(!dut.pipeline_advance&&pre_request)begin
                requests=requests+1;$fdisplay(fetch_fd,"REQ|%0d|%08x|%08x",physical,pre_id_pc,pre_pc);
            end
            if(pre_redirect)begin
                applies=applies+1;if(pre_hit)hits=hits+1;
                $fdisplay(fetch_fd,"REDIR|%0d|%08x|%08x|%0d|%08x|%08x",physical,pre_id_pc,pre_target,pre_hit,dut.fetch_redirect_pc,inst);
            end
            held=architectural_state;
            #1;
            if(!dut.pipeline_advance)begin end // phase toggles after the edge: use physical parity below.
            if(physical%2==1)begin
                if(held!==architectural_state)$fatal(1,"HOLD_ARCHITECTURAL_STATE");
                if(dut.fetch_redirect_valid!==pre_request)$fatal(1,"REQUEST_VALID_CAPTURE");
                if(pre_request)begin
                    if(dut.fetch_redirect_pc!==pre_pc)$fatal(1,"REQUEST_TAG_CAPTURE");
                    $fdisplay(fetch_fd,"SAMPLE|%0d|%08x|%08x|%08x",physical,pre_id_pc,dut.fetch_redirect_pc,inst);
                end
            end
            if(pre_redirect)$fdisplay(fetch_fd,"APPLY|%0d|%08x|%0d|%08x|%08x|%0d|%08x|%08x|%0d",physical,pre_id_pc,pre_hit,pre_target,dut.pc_reg,dut.if_valid,dut.if_pc,dut.if_inst,dut.id_valid);
        end
    end
    // Reset once after an actual request but before its apply edge.
    // The first attempt has no executed instruction or WB/STORE to discard.
    always @(negedge clk)if(rst_n&&reset_pending&&!did_reset&&dut.fetch_redirect_valid)begin
        if(ex_count!=0||wb_count!=0||store_count!=0)$fatal(1,"RESET_PREFIX_NOT_EMPTY");
        $fdisplay(fetch_fd,"RESET|%0d|%08x",physical,dut.fetch_redirect_pc);cancels=cancels+1;
        rst_n=0;did_reset=1;#1;if(dut.fetch_redirect_valid!==0||stopped!==0)$fatal(1,"RESET_LEAK");
        repeat(2)@(negedge clk);rst_n=1;
    end
    always @(negedge clk)begin
        if(!rst_n)tail=0;
        else if(stopped)begin
            tail=tail+1;if(tail==8)begin
                if(reset_pending&&did_reset!=1)$fatal(1,"RESET_NOT_EXERCISED");
                rf_fd=$fopen("registers.hex","w");ram_fd=$fopen("ram.hex","w");if(!rf_fd||!ram_fd)$fatal(1,"OUTPUT_OPEN");
                for(i=0;i<32;i=i+1)$fdisplay(rf_fd,"%08x",dut.rf.regs[i]);
                for(i=0;i<32768;i=i+1)$fdisplay(ram_fd,"%02x",(ram[i>>2]>>((i%4)*8))&255);
                $fclose(rf_fd);$fclose(ram_fd);$fclose(trace_fd);$fclose(fetch_fd);
                $display("METRICS|physical=%0d|advances=%0d|stall=%0d|flush=%0d|tail=%0d|requests=%0d|hits=%0d|applies=%0d|cancels=%0d",physical,advances,stall,flush,tail,requests,hits,applies,cancels);
                $display("STOP|%0d|%08x",stop_kind,stop_pc);$display("SYSTEM_ENDED_NOT_FUNCTIONAL_PASS");$finish;
            end
        end
    end
endmodule
