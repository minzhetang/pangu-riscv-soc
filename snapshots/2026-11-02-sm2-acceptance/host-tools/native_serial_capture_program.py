"""Independent Win32 read-only UART capture. No .NET, serial writes, purge or PDS.
Default is an offline structure/mask check; --run requires a fresh stage/gate.
"""
import ctypes as c
from ctypes import wintypes as w
import datetime,json,time,sys
from pathlib import Path

class DCB(c.Structure):
    _fields_=[('DCBlength',w.DWORD),('BaudRate',w.DWORD),('flags',w.DWORD),
              ('wReserved',w.WORD),('XonLim',w.WORD),('XoffLim',w.WORD),
              ('ByteSize',w.BYTE),('Parity',w.BYTE),('StopBits',w.BYTE),
              ('XonChar',c.c_char),('XoffChar',c.c_char),('ErrorChar',c.c_char),
              ('EofChar',c.c_char),('EvtChar',c.c_char),('wReserved1',w.WORD)]
class COMSTAT(c.Structure):
    _fields_=[('flags',w.DWORD),('cbInQue',w.DWORD),('cbOutQue',w.DWORD)]
class TIMEOUTS(c.Structure):
    _fields_=[(n,w.DWORD) for n in ['interval','read_multiplier','read_constant','write_multiplier','write_constant']]
ERRORS={1:'RXOver',2:'Overrun',4:'RXParity',8:'Frame',16:'Break',256:'TXFull',1024:'PTO',2048:'IOE',4096:'DNS',32768:'OOP',65536:'Mode'}
def names(bits):return [name for bit,name in ERRORS.items() if bits&bit]
def stamp():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def need(ok,why):
    if not ok:raise RuntimeError(why)
def settings(d):return dict(baud=d.BaudRate,data_bits=d.ByteSize,parity=d.Parity,stop_bits=d.StopBits,flags_hex=f'0x{d.flags:08x}')
def offline():
    need(c.sizeof(DCB)==28 and c.sizeof(COMSTAT)==12 and c.sizeof(TIMEOUTS)==20,'Win32 structure sizes')
    need(DCB.ByteSize.offset==18 and DCB.flags.offset==8,'DCB offsets')
    need(names(0)==[] and names(1)==['RXOver'] and names(2)==['Overrun'] and names(3)==['RXOver','Overrun'],'Distinct error decoding')
    print(json.dumps(dict(kind='OFFLINE_WIN32_LAYOUT_AND_MASK_CHECK',PASS=True,serial_opens=0,DCB_bytes=c.sizeof(DCB),COMSTAT_bytes=c.sizeof(COMSTAT),TIMEOUTS_bytes=c.sizeof(TIMEOUTS))))

def run(H):
    gate=json.loads((H/'LIVE_GATE.json').read_text())
    need(gate['approved'] is True and gate['hardware_ready'] is True and gate['phase']=='D294_SM2_RESUME','Fresh live gate')
    need(datetime.datetime.fromisoformat(gate['expires_at'])>datetime.datetime.now(datetime.timezone.utc),'Expired gate')
    need(not (H/'SERIAL_ATTEMPT.json').exists(),'Already attempted')
    k=c.WinDLL('kernel32',use_last_error=True)
    k.CreateFileW.argtypes=[w.LPCWSTR,w.DWORD,w.DWORD,c.c_void_p,w.DWORD,w.DWORD,w.HANDLE];k.CreateFileW.restype=w.HANDLE
    for n,types in [('GetCommState',[w.HANDLE,c.POINTER(DCB)]),('SetCommState',[w.HANDLE,c.POINTER(DCB)]),('SetupComm',[w.HANDLE,w.DWORD,w.DWORD]),('SetCommTimeouts',[w.HANDLE,c.POINTER(TIMEOUTS)]),('GetCommTimeouts',[w.HANDLE,c.POINTER(TIMEOUTS)]),('ClearCommError',[w.HANDLE,c.POINTER(w.DWORD),c.POINTER(COMSTAT)]),('ReadFile',[w.HANDLE,c.c_void_p,w.DWORD,c.POINTER(w.DWORD),c.c_void_p]),('CloseHandle',[w.HANDLE])]:
        fn=getattr(k,n);fn.argtypes=types;fn.restype=w.BOOL
    def api(ok):
        if not ok:raise c.WinError(c.get_last_error())
    def save(name,obj):
        with (H/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
    result=dict(schema=2,transport='WIN32_READFILE',run_id=gate['run_id'],started=stamp(),port='COM22',baud=115200,opened=False,closed=False,write_calls=0,program_calls=0,pds_calls=0,bytes=0,error_events=[],chunks=[],queue_observations=[],read_calls=0,max_seconds=900,max_bytes=65536,end_marker_seen=False)
    save('SERIAL_ATTEMPT.json',result)
    handle=None;start=time.monotonic();last=0;tail=b''
    try:
        handle=k.CreateFileW('\\\\.\\COM22',0xC0000000,0,None,3,0,None)
        need(handle not in [None,c.c_void_p(-1).value],'Open COM22 failed, WinError '+str(c.get_last_error()))
        result['opened']=True
        d=DCB();d.DCBlength=c.sizeof(d);api(k.GetCommState(handle,c.byref(d)));result['initial_settings']=settings(d)
        api(k.SetupComm(handle,4096,4096))
        d.BaudRate=115200;d.flags=1;d.ByteSize=8;d.Parity=0;d.StopBits=0
        api(k.SetCommState(handle,c.byref(d)));api(k.GetCommState(handle,c.byref(d)));result['effective_settings']=settings(d)
        need(d.BaudRate==115200 and d.ByteSize==8 and d.Parity==0 and d.StopBits==0 and d.flags==1,'Serial settings readback mismatch')
        timeout=TIMEOUTS(0xFFFFFFFF,0,50,0,150);api(k.SetCommTimeouts(handle,c.byref(timeout)))
        check_timeout=TIMEOUTS();api(k.GetCommTimeouts(handle,c.byref(check_timeout)))
        result['timeout_readback']={n:getattr(check_timeout,n) for n,_ in TIMEOUTS._fields_}
        need(check_timeout.interval==0xFFFFFFFF and check_timeout.read_constant==50,'Timeout readback')
        save('SERIAL_ARMED.json',dict(run_id=gate['run_id'],state='COM_OPEN_CAPTURE_ARMED',armed_at=stamp(),port='COM22',baud=115200,transport='WIN32_READFILE'))
        save('RESET_REQUEST.json',dict(request_at=time.time(),deadline=time.time()+480,action='KEY0 then KEY1..4, same CPU image',program_calls=0))
        print('ARMED_NATIVE_WIN32_KEY0_CAPTURE',flush=True)
        buf=c.create_string_buffer(8192)
        with (H/'uart-raw.bin').open('xb') as f:
            while time.monotonic()-start<900:
                if (H/'STOP_SERIAL').exists():result['state']='CONTROLLER_STOP';break
                flags=w.DWORD();stat=COMSTAT();api(k.ClearCommError(handle,c.byref(flags),c.byref(stat)))
                elapsed=time.monotonic()-start
                if flags.value:
                    need(len(result['error_events'])<128,'error event bound')
                    result['error_events'].append(dict(type='|'.join(names(flags.value)) or 'Unknown',mask=flags.value,observed_at=stamp(),elapsed_seconds=elapsed,bytes_recorded=f.tell(),input_queue=stat.cbInQue))
                if flags.value or stat.cbInQue:
                    need(len(result['queue_observations'])<2048,'queue observation bound')
                    result['queue_observations'].append(dict(elapsed_seconds=elapsed,input_bytes=stat.cbInQue,output_bytes=stat.cbOutQue,comm_flags=stat.flags))
                available=65536-f.tell()
                if available<=0:result['state']='BYTE_LIMIT';break
                n=w.DWORD();api(k.ReadFile(handle,buf,min(8192,available),c.byref(n),None));result['read_calls']+=1
                if n.value:
                    need(len(result['chunks'])<2048,'chunk bound')
                    data=buf.raw[:n.value];offset=f.tell();f.write(data);f.flush();result['bytes']=f.tell()
                    last=time.monotonic()-start;tail=(tail+data)[-256:]
                    result['chunks'].append(dict(offset=offset,bytes=n.value,elapsed_seconds=last,observed_at=stamp(),pending_before_read=stat.cbInQue))
                    if b'BOARD_QA_M2 END LED=000000a5' in tail:result['end_marker_seen']=True
                elif result['end_marker_seen'] and time.monotonic()-start-last>=2:
                    result['state']='END_MARKER_THEN_QUIET';break
            else:result['state']='TIME_LIMIT'
        flags=w.DWORD();stat=COMSTAT();api(k.ClearCommError(handle,c.byref(flags),c.byref(stat)))
        if flags.value:result['error_events'].append(dict(type='|'.join(names(flags.value)) or 'Unknown',mask=flags.value,observed_at=stamp(),elapsed_seconds=time.monotonic()-start,bytes_recorded=result['bytes'],input_queue=stat.cbInQue,phase='final_readback'))
    except BaseException as e:result.update(state='SERIAL_CAPTURE_ERROR',error=type(e).__name__+': '+str(e))
    finally:
        if handle not in [None,c.c_void_p(-1).value]:
            if k.CloseHandle(handle):result['closed']=True
            else:result['close_error']='WinError '+str(c.get_last_error())
        result['total_seconds']=time.monotonic()-start;result['finished']=stamp()
        result['transport_clean']=result['opened'] and result['closed'] and not result['error_events'] and not result.get('error') and not result.get('close_error') and result.get('state')=='END_MARKER_THEN_QUIET'
        save('SERIAL_RESULT.json',result)
    print(json.dumps({k:result.get(k) for k in ['state','bytes','transport_clean','error','initial_settings','effective_settings','read_calls']}),flush=True)
    return 0 if result['transport_clean'] else 2

if __name__=='__main__':
    if len(sys.argv)==1 or sys.argv[1:]==['--selftest']:offline()
    elif len(sys.argv)==3 and sys.argv[1]=='--run':raise SystemExit(run(Path(sys.argv[2])))
    else:raise SystemExit('Use --selftest or --run FRESH_STAGE')
