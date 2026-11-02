"""Current-stage strict checker. No device/tool invocation."""
from pathlib import Path
import json,sys,hashlib,importlib.util
R=Path('D:/A_FPGA_Comp');P=R/'work/quality/2026-11-02-offline-resume-prep-v1'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def need(ok,why):
    if not ok:raise ValueError(why)
H=Path(sys.argv[1]);mode=sys.argv[2]
need(mode in ['performance','validation'],'Mode')
spec=importlib.util.spec_from_file_location('current_checker',P/'validate_capture.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
identity=load(P/'INPUT_IDENTITY.json')[mode]
result={'status':'FAIL','mode':mode,'new_target_capture':True,'error':None}
try:
    raw=(H/'uart-raw.bin').read_bytes();s=load(H/'SERIAL_RESULT.json');execution=load(H/'RESULT.json')
    need(execution['error'] is None,'controller error')
    need(execution['cleanup'] and all(x['job_empty'] and not x['forced_cleanup'] and x['root_exit_code']==0 for x in execution['cleanup']),'native exit/cleanup')
    if execution['full_svf_configuration_dispatches']==1:
        program=execution;binding=H
    else:
        need(execution['full_svf_configuration_dispatches']==0,'unexpected program count')
        binding=Path(load(H/'PROGRAM_BINDING.json')['source_stage']);program=load(binding/'RESULT.json')
    need(program['error'] is None and program['full_svf_configuration_dispatches']==1 and program['native_full_svf_configuration_executions']==1,'configuration binding')
    bit=binding/'inputs/board_top.sbit'
    need(hashlib.sha256(bit.read_bytes()).hexdigest().upper()==identity['bit_sha256'],'bit identity')
    after=[x for x in program['samples'] if x['phase'].startswith('after')]
    need(len(after)==2,'two post configuration samples required')
    need(all(x['flags']['done']==1 and x['flags']['done_i']==1 and x['gouten']==1 and not any(x['flags'][k] for k in ['timeout','rbcrc_err','aut_err','crc_err','id_err']) for x in after),'post configuration status')
    checked=C.validate(raw,s,identity['expected'],identity['flags'])
    result.update(checked,status='FINITE_TARGET_REPORT_PASS',capture_stage=str(H.relative_to(R)),program_binding=str(binding.relative_to(R)),bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest().upper(),bit_sha256=identity['bit_sha256'],serial_errors=s['error_events'],clock_independently_measured=False,full_architectural_trace=False,formal_score_certified=False)
except (ValueError,KeyError,UnicodeError,OSError,TypeError) as e:result['error']=type(e).__name__+': '+str(e)
with (H/'CAPTURE_CHECK.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result['status']=='FINITE_TARGET_REPORT_PASS' else 2)
