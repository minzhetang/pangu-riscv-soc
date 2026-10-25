"""Boolean input sensitivity for the actually encountered LUTs, not DUT execution.
Equations transcribed from locally installed official primitive models; sources
and hashes are recorded by netlist_graph. No vendor source is redistributed.
"""
import re,itertools
def literal(t):
    assert len(t)==1,t
    m=re.fullmatch(r"(\d+)'([bBdDhH])([0-9a-fA-F_]+)",t[0]);assert m,t
    return int(m[3].replace('_',''),dict(b=2,d=10,h=16)[m[2].lower()])&((1<<int(m[1]))-1)
def value(typ,params,port,v):
    if typ in ['GTP_INBUF','GTP_OUTBUF']:return v['I']
    if typ=='GTP_INV':return v['I']^1
    if typ.startswith('GTP_MUX2LUT'):return v['I1'] if v['S'] else v['I0']
    init=literal(params['INIT']) if 'INIT' in params else 0
    n=int(typ[-1]) if re.fullmatch('GTP_LUT[1-6]',typ) else 6
    index=sum(v['I'+str(i)]<<i for i in range(min(n,5)))
    low=(init>>index)&1;high=(init>>(index+32))&1
    if typ=='GTP_LUT6CARRY':
        carry=params.get('I5_TO_CARRY',['"TRUE"']);lut=params.get('I5_TO_LUT',['"FALSE"'])
        assert carry in [['"TRUE"'],['"FALSE"']] and lut in [['"TRUE"'],['"FALSE"']]
        ci=v['I5'] if carry==['"TRUE"'] else high
        select=v['I5'] if lut==['"TRUE"'] else v['CIN']
        if port=='Z':return high if select else low
        assert port=='COUT';return v['CIN'] if low else ci
    if typ=='GTP_LUT6D' and port=='Z5':return low
    if n==6:return high if v['I5'] else low
    return low
def dependencies(typ,params,inputs,output,fixed=None):
    fixed=fixed or {};free=[p for p in inputs if p not in fixed]
    if not free:return []
    values={}
    for bits in itertools.product([0,1],repeat=len(free)):
        values[bits]=value(typ,params,output,dict(zip(free,bits))|fixed)
    return [p for i,p in enumerate(free) if any(values[b]!=values[b[:i]+(1-b[i],)+b[i+1:]] for b in values)]
def selftest():
    six=['I'+str(i) for i in range(6)]
    p={'INIT':["64'hAAAAAAAAAAAAAAAA"]}
    assert dependencies('GTP_LUT6',p,six,'Z')==['I0']
    p={'INIT':["64'hFFFFFFFF00000000"]}
    assert dependencies('GTP_LUT6',p,six,'Z')==['I5']
    assert dependencies('GTP_LUT6D',p,six,'Z5')==[]
    assert dependencies('GTP_LUT6D',p,six,'Z',{'I5':1})==[]
    assert dependencies('GTP_LUT6D',{'INIT':["64'hFFFFFFFFFFFFFFFF"]},six,'Z')==[]
    assert set(dependencies('GTP_MUX2LUT7',{},['I0','I1','S'],'Z'))=={'I0','I1','S'}
    # Independent direct INIT indexing vs low/high decomposition.
    checks=0
    for n in range(1,7):
        init=(0x8739BCAE6F051D42&((1<<(1<<n))-1))
        for bits in itertools.product([0,1],repeat=n):
            index=sum(x<<i for i,x in enumerate(bits))
            assert value('GTP_LUT'+str(n),{'INIT':[str(1<<n)+"'h"+format(init,'x')]},'Z',dict(zip(six,bits)))==((init>>index)&1);checks+=1
    # Carry output tested for both parameter switches and every seven-bit input.
    for carry,lut in itertools.product([False,True],repeat=2):
        params={'INIT':["64'h8739BCAE6F051D42"],'I5_TO_CARRY':['"TRUE"' if carry else '"FALSE"'],'I5_TO_LUT':['"TRUE"' if lut else '"FALSE"']}
        for bits in itertools.product([0,1],repeat=7):
            v=dict(zip(six+['CIN'],bits));idx=sum(v['I'+str(i)]<<i for i in range(5));lo=(0x8739BCAE6F051D42>>idx)&1;hi=(0x8739BCAE6F051D42>>(32+idx))&1
            a=v['I5'] if carry else hi;s=v['I5'] if lut else v['CIN']
            assert value('GTP_LUT6CARRY',params,'COUT',v)==((lo&v['CIN'])|((lo^1)&a))
            assert value('GTP_LUT6CARRY',params,'Z',v)==((s&hi)|((s^1)&lo));checks+=2
    return dict(status='PASS',direct_index_or_boolean_product_checks=checks,sensitivity_checks=6,new_DUT_runs=0)
