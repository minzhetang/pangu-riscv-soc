"""Correlate every actual request/tag/apply with independent architectural redirects."""
from check_redirect_v2 import fetch_ledger
def audit_core(path,expected,image,trace,stop_pc):
    ledger=fetch_ledger(path,expected,image,1,False);actions=ledger['actions'];index=0;previous=None;gaps={};examples={}
    def check_pair(current,nxt):
        nonlocal index
        if index>=len(actions) or actions[index]['cycle']!=current[0]:return
        a=actions[index];assert current[1]==a['pc']
        if nxt is None:assert a['target']==stop_pc
        else:
            gap=nxt[0]-current[0];assert nxt[1]==a['target'] and gap==(4 if a['hit'] else 6)
            key=str(gap);gaps[key]=gaps.get(key,0)+1
            if len(examples)<12:examples.setdefault(f'{a["pc"]:08x}',dict(cycle=current[0],target_cycle=nxt[0],target=f'{nxt[1]:08x}',gap=gap))
        index+=1
    with trace.open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split('|')
            if a[0]!='EX':continue
            current=(int(a[1]),int(a[2],16))
            if previous is not None:check_pair(previous,current)
            previous=current
    check_pair(previous,None);assert index==len(actions)
    return {**{k:v for k,v in ledger.items() if k!='actions'},'successor_EX_gaps':gaps,'examples':examples,'all_redirects_correlated':index}
