        // synthesis translate_off
        if(rst_n && wren && ((^{addr,wdata,wstrb})===1'bx || !data_ram || wstrb==0))
            $fatal(1,"MEMORY_PROTOCOL store outside RAM/zero-mask/unknown");
        if(rst_n && !wren && wstrb!==0) $fatal(1,"MEMORY_PROTOCOL idle strobe");
        // synthesis translate_on
