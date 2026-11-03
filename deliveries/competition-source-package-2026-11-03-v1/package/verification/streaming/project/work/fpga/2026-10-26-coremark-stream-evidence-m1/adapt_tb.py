from pathlib import Path
import re,difflib,json
H=Path('D:/A_FPGA_Comp/work/fpga/2026-10-26-coremark-stream-evidence-m1')
s=(H/'before/tb_board_coremark.sv').read_text(encoding='utf-8-sig')
s=s.replace('integer advances=0,stall=0,flush=0,wave_until=1024;', 'integer trace_seq=0,bus_seq=0,trace_count=0,bus_count=0,trace_total=0,bus_total=0;\n    string trace_name,bus_name;\n    integer advances=0,stall=0,flush=0,wave_until=1024;')
tasks='''    // Only the logging enclosure rotates; event predicates, fields and sampled edges stay unchanged.
    task open_trace;
        begin
            trace_name=$sformatf("spool/trace-%06d.log",trace_seq);
            events_fd=$fopen(trace_name,"w");if(!events_fd)$fatal(1,"TRACE_SEGMENT_OPEN");
        end
    endtask
    task open_bus;
        begin
            bus_name=$sformatf("spool/bus-%06d.log",bus_seq);
            bus_fd=$fopen(bus_name,"w");if(!bus_fd)$fatal(1,"BUS_SEGMENT_OPEN");
        end
    endtask
    task close_trace;
        begin
            if(events_fd)begin
                $fclose(events_fd);events_fd=0;
                $display("SEGMENT|trace|%0d|%0d|%s",trace_seq,trace_count,trace_name);$fflush();
                trace_seq=trace_seq+1;trace_count=0;
            end
        end
    endtask
    task close_bus;
        begin
            if(bus_fd)begin
                $fclose(bus_fd);bus_fd=0;
                $display("SEGMENT|bus|%0d|%0d|%s",bus_seq,bus_count,bus_name);$fflush();
                bus_seq=bus_seq+1;bus_count=0;
            end
        end
    endtask
'''
s=s.replace('    initial begin\n',tasks+'    initial begin\n',1)
s=s.replace('events_fd=$fopen("trace.log","w");bus_fd=$fopen("bus.log","w");', 'open_trace();open_bus();')
for fd,kind in [('events_fd','trace'),('bus_fd','bus')]:
    pattern=r'\$fdisplay\('+fd+r',.*?\);'
    hits=re.findall(pattern,s,re.S);assert len(hits)==(4 if kind=='trace' else 1),(kind,len(hits))
    def wrap(m):
        return 'begin if(!'+fd+')open_'+kind+'();'+m.group(0)+f'{kind}_count={kind}_count+1;{kind}_total={kind}_total+1;if({kind}_count==32768)close_{kind}();end'
    s=re.sub(pattern,wrap,s,flags=re.S)
s=s.replace('$fclose(rf_fd);$fclose(ram_fd);$fclose(events_fd);$fclose(bus_fd);$fclose(serial_fd);', '''$fclose(rf_fd);$fclose(ram_fd);close_trace();close_bus();$fclose(serial_fd);
            $display("END_STREAM|trace|%0d|%0d",trace_seq,trace_total);
            $display("END_STREAM|bus|%0d|%0d",bus_seq,bus_total);$fflush();''')
assert 'trace.log' not in s and 'bus.log' not in s
(H/'tests/tb_board_coremark.sv').write_text(s,encoding='utf-8',newline='\n')
(H/'TB_DIFF.patch').write_text(''.join(difflib.unified_diff((H/'before/tb_board_coremark.sv').read_text(encoding='utf-8-sig').splitlines(True),s.splitlines(True),fromfile='before/tb_board_coremark.sv',tofile='tests/tb_board_coremark.sv')),encoding='utf-8')
B=H.parent/'2026-10-25-coremark-iter2-m1';plan=json.loads((B/'compile-plan.json').read_text(encoding='utf-8-sig'));row=next(r for r in plan['targets'] if r['id']=='performance-N234')
for k,v in list(row.items()):
    if isinstance(v,str):row[k]=v.replace(str(B),str(H))
    elif isinstance(v,list):row[k]=[str(x).replace(str(B),str(H)) for x in v]
with (H/'compile-plan.json').open('x',encoding='utf-8') as f:json.dump(dict(maximum=1,targets=[row]),f,indent=2);f.write('\n')
print('Logging-only TB diff and exact single-target compiler plan ready; compiler not executed')
