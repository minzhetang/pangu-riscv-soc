"""Read-only pre-edge/post-edge VCD crosscheck; no simulation or expected changes."""
import json
from pathlib import Path
from run_c_boot import HERE, save, sha, verify

def main():
    path=HERE/"ordinary-run-01/runs/wave.vcd"
    lines=path.read_text(encoding="utf-8").splitlines()
    stack=[]; names={}; end=None
    for i,line in enumerate(lines):
        f=line.split()
        if not f: continue
        if f[0]=="$scope": stack.append(f[2])
        elif f[0]=="$upscope": stack.pop()
        elif f[0]=="$var": names[".".join(stack+[f[4]])]=f[3]
        elif f[0]=="$enddefinitions": end=i+1; break
    assert "$timescale\n\t1ps\n$end" in "\n".join(lines[:20])
    prefix="tb_c_boot.dut."
    def val(state,n):
        raw=state.get(names[prefix+n],"x")
        assert not any(c in raw.lower() for c in "xz"), (n,raw)
        return int(raw,2)
    def h(state,n): return f"{val(state,n):08x}"
    state={}; changes={}; timestamp=0
    wb=[]; events=[]; ex=[]; stall=0; flush=0; active=0
    detected=[]; published=[]; poststop=[]
    def group(t, updates):
        nonlocal stall,flush,active
        before=state.copy()
        state.update(updates)
        clock=names[prefix+"clk"]
        if before.get(clock)!="0" or state.get(clock)!="1": return
        if before.get(names[prefix+"rst_n"])!="1": return
        active+=1
        stall+=val(before,"stall_if"); flush+=val(before,"control_flush")
        wb_active=val(before,"mem_valid") and val(before,"mem_reg_write")
        if wb_active and val(before,"mem_rd"):
            wb.append([str(val(before,"mem_rd")),h(before,"wb_write_data")])
        if val(before,"id_valid") and not val(before,"eei_hold"):
            ex.append(h(before,"id_pc"))
        if val(before,"ex_valid") and val(before,"ex_mem_to_reg"):
            events.append(["READ",h(before,"ex_pc"),h(before,"mem_addr"),h(before,"mem_rdata"),h(before,"mem_load_data")])
        if val(before,"mem_wren"):
            events.append(["STORE",h(before,"ex_pc"),h(before,"mem_addr"),h(before,"mem_wdata"),f"{val(before,'mem_wstrb'):x}"])
        if val(before,"eei_detect"):
            detected.append({"time_ps":t,"valid_EX_pc":h(before,"id_pc"),
                             "kind":val(before,"id_system_kind")})
        if val(state,"eei_stop_valid") and not val(before,"eei_stop_valid"):
            published.append({"time_ps":t,"pc":h(state,"eei_stop_pc"),"kind":val(state,"eei_stop_kind")})
        if val(before,"eei_stop_valid"):
            assert not wb_active and not val(before,"mem_wren")
            poststop.append(t)
    for line in lines[end:]:
        if line.startswith("#"):
            group(timestamp,changes); changes={}; timestamp=int(line[1:])
        elif line and line[0] in "bB":
            bits,code=line[1:].split(); changes[code]=bits
        elif line and line[0] in "01xXzZ": changes[line[1:]]=line[0].lower()
    group(timestamp,changes)
    expected=json.loads((HERE/"expected.json").read_text(encoding="utf-8"))
    assert wb==expected["writebacks"]
    assert events==expected["memory_events"]
    assert ex==expected["execution_PC_not_retirement"]
    assert stall==expected["stall_model_expected"] and flush==expected["flush_model_expected"]
    assert len(detected)==len(published)==1
    assert detected[0]["valid_EX_pc"]==published[0]["pc"]=="00000068"
    assert detected[0]["kind"]==published[0]["kind"]==2
    assert len(poststop)>=3
    result={"status":"PASS_FINITE_VCD_CROSSCHECK","VCD":str(path),"sha256":sha(path),
            "pre_edge_observations":{"WB":len(wb),"READ":sum(e[0]=="READ" for e in events),
            "STORE":sum(e[0]=="STORE" for e in events),"valid_EX_PC_not_retirement":len(ex),
            "active_clock_edges":active,"stall":stall,"flush":flush},
            "EEI_detect_before_edge":detected,"EEI_publish_after_edge":published,
            "poststop_no_side_effect_edges":len(poststop),"timescale":"1ps",
            "last_tick_ps":timestamp,"whole_simulation_time_ns":timestamp/1000,
            "raw_stdout_time_ns_field_is_actually_ps_ticks":True,
            "protected_records_after":verify(),"new_simulation_calls":0}
    save(HERE/"wave-review.json",result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
