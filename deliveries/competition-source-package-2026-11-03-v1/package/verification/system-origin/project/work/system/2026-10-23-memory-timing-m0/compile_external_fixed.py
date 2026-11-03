"""Permission-gated batch: exactly two frozen compile commands, no simulation."""
from pathlib import Path
import datetime, json, sys
sys.stdout.reconfigure(encoding='utf-8')
import run as m

m.verify()
out=m.ROOT/'external-compile'
out.mkdir(exist_ok=False)
result=dict(scope='two fixed non-admin compiles only; no VVP execution',compiles=[])
for target in m.read(m.ROOT/'commands.json')['targets']:
    argv=target['argv'].copy()
    output=out/(target['id']+'.vvp')
    argv[argv.index('-o')+1]=str(output)
    r=m.bounded(argv,m.ROOT,'external-compile-'+target['id'],60)
    r.update(target=target['id'],output=str(output))
    result['compiles'].append(r)
    if r['returncode']!=0 or r['timeout'] or r['log_cap']:
        result['status']='TOOL_ERROR'; break
    if not output.is_file() or output.stat().st_size==0:
        result['status']='NO_NEW_OUTPUT'; break
else: result['status']='COMPILED_NOT_SIMULATED'
result['date_beijing']=datetime.datetime.now().astimezone().isoformat()
result['postflight']=m.verify()
m.save(out/'result.json',result)
print(json.dumps(result,ensure_ascii=False))
