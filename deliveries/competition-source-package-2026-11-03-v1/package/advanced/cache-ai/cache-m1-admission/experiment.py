import json,re,pathlib,sys,csv,hashlib
from run import bounded,TOOLS,verify
R=pathlib.Path(__file__).resolve().parent
def run():
    verify('FROZEN_SHA256.txt');verify('EXECUTION_SHA256.txt')
    ex=json.loads((R/'EXPECTED.json').read_text());results=[]
    for name in ['baseline','admission']:
        source='baseline.sv' if name=='baseline' else 'candidate.sv'
        args=[TOOLS/'iverilog.exe','-g2012','-Wall','-s','cache_tb','-o',name+'.vvp',source,'backend.sv','execution_tb.sv']
        if name=='admission':args.insert(1,'-DADMISSION_M1')
        bounded('compile_'+name,args)
    for key,policies in ex.items():
        ro,workload=key.split('_')
        for p,expected in policies.items():
            image='baseline' if p in ['baseline','bypass'] else 'admission'
            for delay in [0,3]:
                args=[TOOLS/'vvp.exe',image+'.vvp',f'+RO={ro}',f'+BYPASS={int(p=="bypass")}',f'+DELAY={delay}',f'+VEC=vectors/{key}.txt']
                if key=='0_stream' and delay==3 and p=='admission':args+=['+WAVE=admission_stream.vcd']
                raw=bounded(f'{key}_{p}_d{delay}',args)
                m=re.search(r'METRIC requests=(\d+) cycles=(\d+) hits=(\d+) transactions=(\d+) bytes=(\d+) mmio=(\d+)',raw)
                assert m and 'PASS cache' in raw
                got=dict(zip(['requests','cycles','hits','transactions','bytes','mmio'],map(int,m.groups())))
                for k in got.keys()-{'cycles'}:assert got[k]==expected[k],(key,p,k,got,expected)
                results.append(dict(key=key,policy=p,delay=delay,**got,eligible_reads=expected['eligible_reads']))
    for p in ['baseline','admission']:
        for mode in [1,2]+([3] if p=='admission' else []):
            raw=bounded(f'protocol_{p}_{mode}',[TOOLS/'vvp.exe',p+'.vvp',f'+MODE={mode}','+DELAY=3',f'+WAVE=protocol_{p}_{mode}.vcd'])
            marker={1:'RESET_CONCURRENT_PASS',2:'HELD_VALID_PASS',3:'ADMISSION_RESET_PASS'}[mode];assert marker in raw
    raw=bounded('negative_admission',[TOOLS/'vvp.exe','admission.vvp','+RO=0','+VEC=old_vectors/negative.txt'],expected_exit=1)
    assert 'data ch' in raw
    # Freeze target evaluated from actual data; failure does not become automatic adoption.
    lookup={(r['key'],r['policy'],r['delay']):r for r in results}
    for ro in [0,1]:
        for delay in [0,3]:
            a=lookup[(f'{ro}_stream','admission',delay)];b=lookup[(f'{ro}_stream','bypass',delay)]
            assert a['bytes']==b['bytes'] and a['cycles']<=b['cycles']*1.05
            assert lookup[(f'{ro}_locality','admission',delay)]['cycles']<lookup[(f'{ro}_locality','bypass',delay)]['cycles']
    (R/'RESULTS.json').write_text(json.dumps(results,indent=2));verify('FROZEN_SHA256.txt');verify('EXECUTION_SHA256.txt')
    print(f'PASS {len(results)} trace configurations, 5 protocol/reset tests, negative rejection; target met')
if __name__=='__main__':run()
