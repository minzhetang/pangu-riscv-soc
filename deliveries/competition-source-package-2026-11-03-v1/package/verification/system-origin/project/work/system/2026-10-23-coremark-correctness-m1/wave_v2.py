"""Wave capture-only correction; frozen original testbench/results remain intact."""
import argparse
import ctypes
import json
import subprocess
import time
from pathlib import Path
from prepare_and_build import HERE,save,item,sha
from check_and_run import TOOLS,frozen_verify,compare
from review_windows import review

def prepare():
    original=(HERE/'tb_coremark.sv').read_text()
    revised=(HERE/'tb_coremark_wave_v2.sv').read_text()
    assert revised.replace('            // The first stopped negedge has already incremented holds to1.\n            if(holds<=1) $dumpon;',
                           '            if(holds==0) $dumpon;')==original
    files=[HERE/'source'/n for n in ['alu.v','control.v','regfile.v','cpu.v']]
    files += [HERE/'memory_model.sv',HERE/'tb_coremark_wave_v2.sv',HERE/'wave_v2.py']
    files += [HERE/'performance'/n for n in ['coremark.elf','image.hex','expected.json']]
    assert not (HERE/'wave-v2-frozen.json').exists()
    save(HERE/'wave-v2-frozen.json',{'purpose':'Only fix $dumpon condition after first stop negedge. No DUT/input/expected changes.',
        'source_diff':'- if(holds==0) $dumpon;\n+ // first stopped negedge has incremented holds\n+ if(holds<=1) $dumpon;',
        'original_results':'result.json remains original two-case functional verdict',
        'files':[item(p) for p in files],'run_cases':['performance'],'requires_new_external_compile_permission':True})

def verify():
    frozen_verify()
    records=json.loads((HERE/'wave-v2-frozen.json').read_text())['files']
    assert all(sha(Path(r['path']))==r['sha256'] for r in records)

def compile_external():
    verify(); assert not ctypes.windll.shell32.IsUserAnAdmin()
    directory=HERE/'compile-wave-v2-external-01'; directory.mkdir(exist_ok=False)
    argv=[str(TOOLS/'bin/iverilog.exe'),'-B',str(TOOLS/'lib/ivl'),'-g2012','-Wall','-s','tb_coremark','-o',str(directory/'coremark.vvp')]
    argv += [str(HERE/'source'/n) for n in ['alu.v','control.v','regfile.v','cpu.v']]
    argv += [str(HERE/'memory_model.sv'),str(HERE/'tb_coremark_wave_v2.sv')]
    save(directory/'request.json',{'argv':argv,'cwd':str(HERE),'timeout_seconds':60,'IsUserAnAdmin':False,'compile_only':True})
    start=time.monotonic()
    try:
        p=subprocess.run(argv,cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        stdout,stderr=p.stdout,p.stderr; result={'exit_code':p.returncode,'timed_out':False}
    except subprocess.TimeoutExpired as exc:
        stdout,stderr=exc.stdout or b'',exc.stderr or b''; result={'exit_code':None,'timed_out':True}
    (directory/'stdout.log').write_bytes(stdout); (directory/'stderr.log').write_bytes(stderr)
    result.update(elapsed_seconds=round(time.monotonic()-start,6),
                  VVP=item(directory/'coremark.vvp') if (directory/'coremark.vvp').exists() else None)
    save(directory/'process.json',result); verify(); print(json.dumps(result,indent=2))

def run():
    verify(); compile_dir=HERE/'compile-wave-v2-external-01'
    proc=json.loads((compile_dir/'process.json').read_text()); vvp=compile_dir/'coremark.vvp'
    assert proc['exit_code']==0 and not proc['timed_out'] and sha(vvp)==proc['VVP']['sha256']
    directory=HERE/'performance/dut-wave-v2-01'; directory.mkdir(exist_ok=False)
    logs=directory/'run'; logs.mkdir()
    words=json.loads((HERE/'performance/image-receipt.json').read_text())['words']
    argv=[str(TOOLS/'bin/vvp.exe'),'-N','-M-','-M'+str(TOOLS/'lib/ivl'),str(vvp),'+IMAGE=../image.hex',f'+WORDS={words}']
    save(logs/'request.json',{'argv':argv,'cwd':str(directory),'timeout_seconds':180,'ordinary':True,'VVP_SHA256':sha(vvp)})
    start=time.monotonic()
    try:
        p=subprocess.run(argv,cwd=directory,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        stdout,stderr=p.stdout,p.stderr; process={'exit_code':p.returncode,'timed_out':False}
    except subprocess.TimeoutExpired as exc:
        stdout,stderr=exc.stdout or b'',exc.stderr or b''; process={'exit_code':None,'timed_out':True}
    (logs/'stdout.log').write_bytes(stdout); (logs/'stderr.log').write_bytes(stderr)
    process['elapsed_seconds']=round(time.monotonic()-start,6); save(logs/'process.json',process)
    result={'status':'TIMEOUT' if process['timed_out'] else 'RUN_FAILURE','process':process}
    if process['exit_code']==0 and not process['timed_out']:
        result['functional']=compare('performance',directory)
        result['wave']=review('performance','dut-wave-v2-01')
        result['status']='PASS' if result['functional']['status']==result['wave']['status']=='PASS' else 'NOT_ACCEPTED'
    save(HERE/'wave-v2-result.json',result); verify(); print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['prepare','compile-external','run'])
    {'prepare':prepare,'compile-external':compile_external,'run':run}[p.parse_args().action]()
