import json,pathlib,re
from run import bounded,TOOLS,verify
R=pathlib.Path(__file__).resolve().parent
FIELDS=['requests','cycles','hits','transactions','bytes','mmio']
def parse(raw):
    m=re.search(r'METRIC requests=(\d+) cycles=(\d+) hits=(\d+) transactions=(\d+) bytes=(\d+) mmio=(\d+)',raw)
    assert m and 'PASS cache' in raw
    return dict(zip(FIELDS,map(int,m.groups())))
def match(got,expected):
    return all(got[k]==expected[k] for k in FIELDS if k!='cycles')
def main():
    verify('FROZEN_SHA256.txt');verify('EXECUTION_SHA256.txt')
    ex=json.loads((R/'EXPECTED.json').read_text());results=[]
    for name,source,defines in [('m0','baseline.sv',[]),('m1','m1.sv',['-DADMISSION_M1']),('m2','candidate.sv',['-DADMISSION_M1','-DTWO_GHOST'])]:
        bounded('compile_'+name,[TOOLS/'iverilog.exe',*defines,'-g2012','-Wall','-s','cache_tb','-o',name+'.vvp',source,'backend.sv','cache_tb.sv'])
    for key,policies in ex.items():
        for p,expected in policies.items():
            for delay in [0,3]:
                image='m0' if p=='bypass' else p
                args=[TOOLS/'vvp.exe',image+'.vvp',f'+RO={key[0]}',f'+BYPASS={int(p=="bypass")}',f'+DELAY={delay}',f'+VEC=vectors/{key}.txt']
                if key=='0_adverse' and p=='m2' and delay==3:args+=['+WAVE=m2_adverse.vcd']
                got=parse(bounded(f'{key}_{p}_d{delay}',args));assert match(got,expected),(key,p,got,expected)
                results.append(dict(key=key,policy=p,delay=delay,**got,eligible_reads=expected['eligible_reads']))
    for mode in [1,2,3,4]:
        raw=bounded(f'protocol_m2_{mode}',[TOOLS/'vvp.exe','m2.vvp',f'+MODE={mode}','+DELAY=3',f'+WAVE=protocol_{mode}.vcd'])
        assert {1:'RESET_CONCURRENT_PASS',2:'HELD_VALID_PASS',3:'ADMISSION_RESET_PASS',4:'TWO_GHOST_RESET_PASS'}[mode] in raw
    raw=bounded('negative_data',[TOOLS/'vvp.exe','m2.vvp','+RO=0','+VEC=negative.txt'],expected_exit=1);assert 'data ch' in raw
    # Actual M1 execution returns correct data but wrong statistics for M2.
    raw=bounded('negative_stats',[TOOLS/'vvp.exe','m1.vvp','+RO=0','+DELAY=3','+VEC=vectors/0_adverse.txt'])
    got=parse(raw);assert not match(got,ex['0_adverse']['m2'])
    (R/'NEGATIVE_STATS.json').write_text(json.dumps(dict(expected_rejection=True,correct_data=True,actual=got,expected_m2=ex['0_adverse']['m2']),indent=2))
    ix={(r['key'],r['policy'],r['delay']):r for r in results};checks=[]
    for ro in [0,1]:
        for d in [0,3]:
            get=lambda name,p:ix[(f'{ro}_{name}',p,d)]
            checks += [dict(channel=ro,delay=d,test='stream',passed=get('stream','m2')['bytes']==get('stream','bypass')['bytes'] and get('stream','m2')['cycles']==get('stream','bypass')['cycles']),
                dict(channel=ro,delay=d,test='adverse',passed=get('adverse','m2')['cycles']<=.65*get('adverse','m1')['cycles'] and get('adverse','m2')['cycles']<=1.15*get('adverse','m0')['cycles'])]
            for name in ['locality','pollution']:checks.append(dict(channel=ro,delay=d,test=name,passed=get(name,'m2')['cycles']<=1.05*get(name,'m1')['cycles']))
    (R/'RESULTS.json').write_text(json.dumps(results,indent=2));(R/'TARGETS.json').write_text(json.dumps(checks,indent=2))
    verify('FROZEN_SHA256.txt');verify('EXECUTION_SHA256.txt')
    print(f'PASS correctness: {len(results)} configs +4 protocols +2 negative checks; targets {sum(c["passed"] for c in checks)}/{len(checks)}')
if __name__=='__main__':main()
