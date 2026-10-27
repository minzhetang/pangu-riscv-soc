from pathlib import Path
import re,json,difflib
P=Path('D:/A_FPGA_Comp');B=P/'队员成果接收/B-VERIFY-OFFLINE-M0-return-v02';V=B.with_name('B-VERIFY-OFFLINE-M0-return-v01');H=P/'work/analysis/2026-10-27-b-offline-r1-review'
lines=(B/'DIFF.patch').read_text(encoding='utf-8-sig').splitlines();starts=[i for i,x in enumerate(lines) if x.startswith('diff --git ')]+[len(lines)];rows=[]
for index in range(len(starts)-1):
 section=lines[starts[index]:starts[index+1]];match=re.fullmatch(r'diff --git a/(.+) b/(.+)',section[0]);name=match[1];old=(V/name).read_text(encoding='utf-8-sig').splitlines() if (V/name).is_file() else [];new=(B/name).read_text(encoding='utf-8-sig').splitlines() if (B/name).is_file() else [];out=[];cursor=0;i=1;error=None
 try:
  while i<len(section):
   line=section[i]
   if not line.startswith('@@ '):i+=1;continue
   m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',line);target=max(0,int(m[1])-1);assert target>=cursor;out+=old[cursor:target];cursor=target;i+=1
   while i<len(section) and not section[i].startswith('@@ '):
    line=section[i];i+=1
    if line.startswith('\\ No newline'):continue
    assert line and line[0] in ' +-',repr(line)
    if line[0] in ' -':assert cursor<len(old) and old[cursor]==line[1:],(cursor,line[:80]);cursor+=1
    if line[0] in ' +':out.append(line[1:])
  out+=old[cursor:];assert out==new,'applied output differs'
 except Exception as exc:error=str(exc)[:200]
 rows.append(dict(path=name,status='APPLIED_EXACT_LINES' if error is None else 'MISMATCH',error=error))
(H/'PATCH_CHECK.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
diff=[]
for name in ['RUN.py','src/support.py','src/worker.py','tests/run_suite.py']:
 diff += difflib.unified_diff((V/name).read_text(encoding='utf-8-sig').splitlines(True),(B/name).read_text(encoding='utf-8-sig').splitlines(True),fromfile='v01/'+name,tofile='v02/'+name)
(H/'CODE_DIFF.patch').write_text(''.join(diff),encoding='utf-8');print(json.dumps(dict(sections=len(rows),exact=sum(x['status']=='APPLIED_EXACT_LINES' for x in rows),mismatches=[x for x in rows if x['error']]),ensure_ascii=False))
