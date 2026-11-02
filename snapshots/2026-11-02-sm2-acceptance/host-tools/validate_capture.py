"""Strict serial/report validation; no serial, PDS, compiler, or hardware imports."""
import importlib.util
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_report_parser',HERE/'measurement_report_frozen.py')
parser=importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

def require(ok, message):
    if not ok: raise ValueError(message)

def validate(raw, serial, expected, flags):
    require(0 < len(raw) <= 65536,'raw byte bound')
    require(serial.get('opened') is True and serial.get('closed') is True,'open/close')
    require(serial.get('write_calls')==0 and serial.get('bytes')==len(raw),'I/O accounting')
    require(serial.get('error_events')==[],'serial error or absent error ledger')
    require(not any(serial.get(k) for k in ['error','close_error','event_collection_error']),'capture exception')
    require(serial.get('state') in ['DATA_CAPTURED_THEN_QUIET','END_MARKER_THEN_QUIET'],'capture termination')
    require(serial.get('end_marker_seen') is True,'end marker state')
    if serial.get('schema')==2:
        require(serial.get('transport_clean') is True,'new receiver clean flag')
        offset=0;last=-1.0
        require(isinstance(serial.get('chunks'),list) and 0<len(serial['chunks'])<=2048,'chunk ledger')
        for chunk in serial['chunks']:
            require(chunk['offset']==offset and 0<chunk['bytes']<=8192,'chunk coverage')
            require(chunk['elapsed_seconds']>=last,'chunk monotonic time')
            offset+=chunk['bytes'];last=chunk['elapsed_seconds']
        require(offset==len(raw),'chunk total')
    text=raw.decode('ascii').replace('\r\n','\n')
    require('\r' not in text,'stray CR')
    header='2K '+expected['seed']+' run parameters for coremark.'
    require(text.count(header)==1,'report count/mode')
    prefix,core=text.split(header)
    marker='BOARD_QA_M2 END LED=000000a5\n'
    require(core.endswith(marker) and core.count(marker)==1,'end marker/trailing bytes')
    core=header+core[:-len(marker)]
    lines=prefix.splitlines()
    fixed=['BOARD_QA_M2 BOOT','RAMTEST PASS wstrb/sign/zero','MULTEST PASS 80']
    fixed += [f'LED {i:08x} WRITE {1<<i:08x} READ {1<<i:08x}' for i in range(8)]
    fixed += ['GPIO_INPUT_READY KEY1..4 press/release;120s limit']
    require(lines[:len(fixed)]==fixed,'QA fixed sequence')
    tail=lines[len(fixed):]
    statuses=['GPIO_INPUT PASS press=0000000f release=0000000f','GPIO_INPUT TIMEOUT']
    require(tail and tail[-1] in statuses,'GPIO outcome')
    inputs=[]
    for line in tail[:-1]:
        if line=='GPIO_WAIT':continue
        require(re.fullmatch(r'INPUT [0-9a-f]{8}',line) is not None,'unexpected/duplicate QA output')
        value=int(line[6:],16)
        require(value in [0,1,2,4,8],'unexpected GPIO value');inputs.append(value)
    require(inputs and inputs[0]==0,'GPIO initial state')
    gpio_pass=tail[-1]==statuses[0]
    if gpio_pass:
        wanted=[0,1,0,2,0,4,0,8,0];index=0
        for value in inputs:
            if index<len(wanted) and value==wanted[index]:index+=1
        require(index==len(wanted),'GPIO PASS without full ordered evidence')
    parsed=parser.parse(core,expected,flags)
    require(parsed['delta']>=270000000,'short benchmark')
    return {'status':'CAPTURE_REPORT_CHECKS_PASS','ticks':parsed['delta'],
            'nominal_seconds':parsed['delta']/27000000,
            'GPIO_this_capture':'ORDERED_INPUT_PASS' if gpio_pass else 'TIMEOUT_NOT_RETESTED',
            'GPIO_previous_acceptance_separate':True,'LED_optical_check':'NOT_OBSERVED_BY_HOST',
            'target_image_identity':'REQUIRES_SEPARATE_CONFIGURATION_BINDING',
            'hardware_adopted':False,'formal_score_certified':False}
