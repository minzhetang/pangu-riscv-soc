"""Ordinary simulations can follow individually FINISHED fixed compilation jobs.
Never executes a target while its compile process is incomplete. Final batch
acceptance remains conditional on the complete compile-result and postflight.
"""
import sys,time
sys.dont_write_bytecode=True
import run_m2 as m
assert m.read(m.H/'selftest-result.json')['status']=='PASS'
targets={t['id']:t for t in m.read(m.H/'compile-plan.json')['targets']}
rows=[];start=time.monotonic()
for name in m.names:
    marker=m.H/'logs'/('compile-'+name)/'process.json'
    while not marker.exists():
        if (m.H/'compile-result.json').exists():
            batch=m.read(m.H/'compile-result.json')
            assert batch['status']=='ALL_COMPILED_NOT_SIMULATED','compile batch stopped before this target'
        assert time.monotonic()-start<900,'waiting for fixed compile batch exceeded bound'
        time.sleep(.2)
    process=m.read(marker)
    assert process['returncode']==0 and not process['timed_out'],'completed compile target failed'
    path=targets[name]['output'];before=m.s.sha(path)
    m.check_frozen()
    r=m.s.generic(name,1,{'generic-1':path})
    assert m.s.sha(path)==before
    rows.append(dict(id=name,compiled_output_sha256=before,**r))
    print(name+': '+r['status']+' '+str(r.get('errors')),flush=True)
    if r['status']!='PASS':break
m.save(m.H/'programs-result.json',dict(status='PASS' if len(rows)==9 and all(r['status']=='PASS' for r in rows) else 'NOT_ACCEPTED',
    cases=rows,protected=m.check_frozen(),note='per-target compile rc/hash checked; full compile batch must also pass before stage acceptance'))
