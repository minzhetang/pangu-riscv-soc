"""Read-only verdict. Normal Python, without -O. No simulation launch."""
import pathlib,hashlib,json,re
R=pathlib.Path(__file__).resolve().parent
FIELDS=['requests','cycles','hits','transactions','bytes','mmio']
def hashes(root,name):
    for line in (root/name).read_text().splitlines():
        sha,path=line.split('  ',1);assert hashlib.sha256((root/path).read_bytes()).hexdigest()==sha,path
def parse(raw):
    m=re.search(r'METRIC requests=(\d+) cycles=(\d+) hits=(\d+) transactions=(\d+) bytes=(\d+) mmio=(\d+)',raw)
    assert m and 'PASS cache' in raw
    return dict(zip(FIELDS,map(int,m.groups())))
def main():
    for f in ['FROZEN_SHA256.txt','EXECUTION_SHA256.txt']:hashes(R,f)
    ex=json.loads((R/'EXPECTED.json').read_text());rows=json.loads((R/'RESULTS.json').read_text())
    assert len(rows)==184 and {(r['key'],r['policy'],r['delay']) for r in rows}=={(k,p,d) for k in ex for p in ex[k] for d in [0,3]}
    for r in rows:
        got=parse((R/'logs'/f"{r['key']}_{r['policy']}_d{r['delay']}.log").read_text())
        assert got=={k:r[k] for k in FIELDS}
        for k in FIELDS:
            if k!='cycles':assert r[k]==ex[r['key']][r['policy']][k]
    for mode in [1,2,3,4]:
        assert {1:'RESET_CONCURRENT_PASS',2:'HELD_VALID_PASS',3:'ADMISSION_RESET_PASS',4:'TWO_GHOST_RESET_PASS'}[mode] in (R/'logs'/f'protocol_m2_{mode}.log').read_text()
    assert 'data ch' in (R/'logs/negative_data.log').read_text()
    got=parse((R/'logs/negative_stats.log').read_text());n=json.loads((R/'NEGATIVE_STATS.json').read_text())
    assert got==n['actual'] and n['expected_rejection'] and n['correct_data']
    assert any(got[k]!=ex['0_adverse']['m2'][k] for k in FIELDS if k!='cycles')
    assert n['expected_m2']==ex['0_adverse']['m2']
    targets=json.loads((R/'TARGETS.json').read_text());assert len(targets)==16 and all(t['passed'] for t in targets)
    ix={(r['key'],r['policy'],r['delay']):r for r in rows}
    for ro in [0,1]:
        for d in [0,3]:
            get=lambda n,p:ix[(f'{ro}_{n}',p,d)]
            assert get('stream','m2')['bytes']==get('stream','bypass')['bytes'] and get('stream','m2')['cycles']==get('stream','bypass')['cycles']
            assert get('adverse','m2')['cycles']<=.65*get('adverse','m1')['cycles'] and get('adverse','m2')['cycles']<=1.15*get('adverse','m0')['cycles']
            for n in ['locality','pollution']:assert get(n,'m2')['cycles']<=1.05*get(n,'m1')['cycles']
    receipts=list((R/'logs').glob('*.json'));assert len(receipts)==193
    for p in receipts:
        r=json.loads(p.read_text());assert r['exit']==int(p.stem=='negative_data') and r['reason'] is None
        assert r['priority']=='BELOW_NORMAL' and r['seconds']<20
    for old in [R.parent,R.parent/'cache-m1-admission']:hashes(old,'SHA256SUMS.txt')
    assert (R/'baseline.sv').read_bytes()==(R.parent/'cache.sv').read_bytes()
    assert (R/'m1.sv').read_bytes()==(R.parent/'cache-m1-admission/candidate.sv').read_bytes()
    if (R/'SHA256SUMS.txt').exists():hashes(R,'SHA256SUMS.txt')
    print('PASS M2 audit:184 configs/4 protocols/2 negatives/16 targets;193 bounded process receipts;M0/M1 preserved')
if __name__=='__main__':main()
