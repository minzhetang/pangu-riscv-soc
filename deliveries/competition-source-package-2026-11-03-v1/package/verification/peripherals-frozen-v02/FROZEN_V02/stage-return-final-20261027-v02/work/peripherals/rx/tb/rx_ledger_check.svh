// Shared ordered ledger comparator macro used by the formal RX TB and the
// negative extra-event proof.  It compares type and data in order.
// The including scope must declare the arrays/counters named below and an
// integer loop variable named ledger_i.
`ifndef RX_LEDGER_CHECK_SVH
`define RX_LEDGER_CHECK_SVH
`define RX_LEDGER_COMPARE(ERR) \
    begin \
        ERR = 0; \
        if (exp_ledger_count != act_ledger_count) \
            ERR = ERR + 1; \
        else begin \
            for (ledger_i = 0; ledger_i < exp_ledger_count; ledger_i = ledger_i + 1) begin \
                if ((exp_ledger_type[ledger_i] !== act_ledger_type[ledger_i]) || \
                    (exp_ledger_data[ledger_i] !== act_ledger_data[ledger_i])) \
                    ERR = ERR + 1; \
            end \
        end \
    end
`endif
