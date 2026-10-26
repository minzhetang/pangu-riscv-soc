"""Bounded live capture. Only closed, verified new spool files may be removed."""
from pathlib import Path
import sys,json,time
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from stage_coremark import read,sha
from stream_io import Archiver,save,require
from host_supervisor import bounded,peak
from compile_once import protect
import shutil

def spool_budget(run):
    spool=Path(run)/'spool';total=0
    for p in spool.iterdir():
        require(p.is_file() and not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400,'unknown spool file/link')
        total+=p.stat().st_size
    require(total<=32*1024*1024,'UNARCHIVED_SPOOL_CAP')
    return total

if __name__=='__main__':
    assert not sys.flags.optimize;protect()
    for row in read(H/'frozen-live-inputs.json')['files']:assert sha(row['path'])==row['SHA256'],row['path']
    comp=read(H/'compile-result.json');assert comp['status']=='PASS_COMPILE_ONLY_NOT_DUT'
    image=comp['rows'][0];assert sha(image['output'])==image['SHA256']
    save(H/'DUT-attempt.json',dict(maximum=1,used=1,stage='D156',physical_limit=8000000,host_seconds=600,program='performance',iterations=2,CPU_RTL_changes=False,hardware='STOPPED'))
    run=H/'runs/performance-N234';run.mkdir(exist_ok=False);(run/'spool').mkdir();arch=Archiver(run)
    state=dict(offset=0,pending=b'',peak_spool=0,peak_parent=0,ready_events=0,parse_lines=0)
    def collect(logdir,exitcode):
        state['peak_spool']=max(state['peak_spool'],spool_budget(run));state['peak_parent']=max(state['peak_parent'],peak(__import__('os').getpid()) or 0)
        require(state['peak_parent']<=512*1024*1024,'PARENT_WORKING_SET_CAP')
        wave=run/'wave.vcd';pins=run/'uart-pins.log'
        require(not wave.exists() or wave.stat().st_size<=256*1024*1024,'VCD_CAP')
        require(not pins.exists() or pins.stat().st_size<=8*1024*1024,'PIN_LOG_CAP')
        p=logdir/'stdout.log'
        with p.open('rb') as f:f.seek(state['offset']);data=f.read(8*1024*1024+1)
        state['offset']+=len(data);state['pending']+=data
        require(len(state['pending'])<=8*1024*1024,'STDOUT_BOUND')
        parts=state['pending'].split(b'\n');state['pending']=parts.pop()
        for line in parts:
            state['parse_lines']+=1;line=line.rstrip(b'\r').decode('utf-8-sig')
            if line.startswith(('SEGMENT|','END_STREAM|')):
                arch.consume(line);state['ready_events']+=line.startswith('SEGMENT|')
        state['peak_spool']=max(state['peak_spool'],spool_budget(run))
        if exitcode is not None:require(not state['pending'],'truncated stdout')
    lib=H.parents[2]/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/lib/ivl';vvp=lib.parents[1]/'bin/vvp.exe'
    r=bounded([vvp,'-N','-M-','-M'+str(lib),image['output'],'+MAX_CYCLES=8000000'],run,'run-performance-N234',600,while_running=collect)
    specs=arch.finish();save(run/'process.json',r);shutil.copyfile(r['stdout'],run/'stdout.log')
    save(run/'capture-result.json',dict(status='ARCHIVE_CAPTURE_COMPLETE_NOT_FUNCTIONAL_PASS',supervisor={k:v for k,v in state.items() if k!='pending'},process=r,streams=specs,source_protected=protect(),new_DUT=1))
    print(json.dumps(dict(status='NEW_DUT_CAPTURE_COMPLETE_NOT_FUNCTIONAL_PASS',spool_peak=state['peak_spool'],parent_peak=state['peak_parent'],archived_events=state['ready_events']),ensure_ascii=False))
