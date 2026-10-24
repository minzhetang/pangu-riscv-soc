        // synthesis translate_off
        for(w=0;w<1024;w=w+1) begin:observe
            assign rom[b*1024+w]=ROM_BITS[(b*1024+w)*32+:32];
            assign ram[b*1024+w]={
                halfword[1].ram_block.mem[w*2+1][7:0],halfword[1].ram_block.mem[w*2][7:0],
                halfword[0].ram_block.mem[w*2+1][7:0],halfword[0].ram_block.mem[w*2][7:0]};
        end
        // synthesis translate_on
