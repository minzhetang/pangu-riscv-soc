from pathlib import Path
import hashlib,json,shutil,time,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent; P=H.parents[2]
R=P/'work/fpga/2026-10-28-local-debug-insert-m1-r4'
S=P/'deliveries/mainline-debug-connectivity-scope-2026-10-29-v1/IMPLEMENTATION_SCOPE.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
assert sha(S)=='50B7C10E6A2F0D3C433AF05E90D3605FD60BF84CC56ACB5D6E0CF6CF3D5C882E'
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
start=time.monotonic();save('STAGE_CLOCK.json',dict(date='2026-10-29',start=start,deadline_monotonic=start+1200))
save('APPROVAL.json',dict(stage='A-DEBUG-CONNECTIVITY-M1',version='1.0.0',decision='D182',scope_SHA256=sha(S),GUI_limit=1,GUI_seconds=600,help_limit=6,PDS_builds=0,hardware='STOPPED'))
for d in ['inputs','scripts','gui-commands']: (H/d).mkdir(exist_ok=False)
paths=[R/'build/place_route/board_top_pnr.adf',R/'build/report_timing/rtr.db']
paths+=list((R/'build/report_timing').glob('*.adf'))
rows=[]
for p in paths:
 q=H/'inputs'/p.name;shutil.copyfile(p,q);assert sha(p)==sha(q)
 rows.append(dict(source=str(p),copy=str(q),SHA256=sha(p),bytes=p.stat().st_size))
save('COPY_RECEIPT.json',rows)
protected=json.loads((R/'PROTECTED_ORIGINALS.json').read_text())['files']
for ph in ['pre','build']:
 protected += [dict(path=str(R/x['path']),SHA256=x['SHA256']) for x in json.loads((R/(ph+'-FROZEN_INPUTS.json')).read_text())['files']]
protected += [dict(path=str(p),SHA256=sha(p)) for p in paths+[S,R/'debug.fic',R/'build/generate_bitstream/board_top.sbit']]
save('PROTECTED_INPUTS.json',protected)
s=(R/'gui_control.py').read_text(encoding='utf-8')
s=s.replace("r'^Fabric Inserter 2022\\.2-SP6\\.4(?: - .+)? \\(on [^)]+\\)$'", "r'^Design Editor(?: .*|)$'")
s=s.replace("if title=='Expiration Reminder':return 'reminder'", "if title=='Expiration Reminder':return 'reminder'\n if title=='Select DB File':return 'load'")
a=s.index('def selfcheck():');b=s.index("if __name__=='__main__'",a)
s=s[:a]+'''def selfcheck():
 for title,role in [('Design Editor 2022.2-SP6.4 - View Only Mode','main'),('Expiration Reminder','reminder'),('Select DB File','load'),('License Finder','REJECT')]:
  assert classify(title,'Qt5152QWindowIcon',7,7)==role
 assert classify('Design Editor','Qt5152QWindowIcon',8,7)=='REJECT'
 print('5 owned-role policy cases passed; no vendor process')
'''+s[b:]
s=s.replace(" from process_guard import verify_completed_synthesis\n verify_completed_synthesis(H)", " rows=json.loads((H/'COPY_RECEIPT.json').read_text())\n assert all(hashlib.sha256(Path(x['copy']).read_bytes()).hexdigest().upper()==x['SHA256'] for x in rows)")
s=s.replace("bin/cdt_ins.exe", "bin/de.exe")
a=s.index(' assert hashlib.sha256(exe.read_bytes())');b=s.index('\n stage=',a)
s=s[:a]+" save('EXE_RECEIPT.json',dict(path=str(exe),SHA256=hashlib.sha256(exe.read_bytes()).hexdigest().upper()))"+s[b:]
s=s.replace(" if role=='REJECT':safe='[UNRECOGNIZED_OWN_WINDOW_TITLE_NOT_RECORDED]'", " if role=='REJECT':safe='[UNRECOGNIZED_OWN_WINDOW_TITLE_NOT_RECORDED]'")
s=s.replace(".replace('unused','unused')", "")
with (H/'gui_control.py').open('x',encoding='utf-8') as f:f.write(s)
shutil.copyfile(R/'window_policy.py',H/'window_policy.py')
save('PREPARATION.json',dict(copies=len(rows),scope_verified=True,protected_entries=len(protected),native_started=False))
print('Prepared',len(rows),'same-byte native DB copies; no GUI launched')
