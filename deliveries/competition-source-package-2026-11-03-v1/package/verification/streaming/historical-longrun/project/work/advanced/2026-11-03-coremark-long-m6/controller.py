"""Foreground continuation of the bounded M6 campaign, not a recurring monitor."""
from native import *
from audit_stream import replay
start=json.loads((H/'CAMPAIGN_START.json').read_text())
save(H/'CONTROLLER_ATTEMPT.json',dict(started=time.time(),scope='Wait current on group, full stream audit, bounded same-image off group, full stream audit; no other work',input_sha256={str(p):sha(p)for p in[H/'controller.py',H/'audit_stream.py',H/'audit_raw.exe',H/'engine.hpp',H/'plans/EXECUTION_FROZEN.json']}))
deadline=start['unix']+start['total_wall_limit']
while not(H/'CAMPAIGN_on_EXIT.json').exists():
 if time.time()>min(deadline,start['unix']+start['case_limit']+120):raise SystemExit('Current on campaign exceeded controller bound; no off launch')
 time.sleep(1)
on=json.loads((H/'CAMPAIGN_on_EXIT.json').read_text())
if on['error']or any(x['rc']!=0 or not x['result']or x['result']['status']!='PASS'for x in on['results']):raise SystemExit('on group failed; preserve evidence and stop')
for mode in ['performance','validation']:replay(f'long-{mode}-p1')
if deadline-time.time()<start['case_limit']+120:raise SystemExit('Insufficient campaign budget for off; no launch')
native('campaign-off-controller',[sys.executable,'-X','utf8','-B',H/'campaign.py','off'],limit=start['case_limit']+60)
for mode in ['performance','validation']:replay(f'long-{mode}-p0')
save(H/'CONTROLLER_EXIT.json',dict(status='LONG_RUNS_AND_REPLAYS_PASS',completed=time.time(),wall_seconds=time.time()-start['unix'],hardware_calls=0,PDS_builds=0))
print('All four long runs and full compressed stream replays passed',flush=True)
