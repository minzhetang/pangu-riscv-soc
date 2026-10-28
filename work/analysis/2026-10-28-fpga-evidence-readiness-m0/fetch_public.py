from pathlib import Path
import hashlib,json,re,sys,time,urllib.request,urllib.parse
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
URLS=[('remote_manual','https://szlogicmatrix.com/wp-content/uploads/2026/03/'+urllib.parse.quote('FPGA远程实验室用户使用手册-开发者版-4.pdf')),('portal','http://www.logicmatrixsemi.com:5174/')]
rows=[]
for name,url in URLS:
    start=time.monotonic();row=dict(name=name,url=url,cap_bytes=8388608,timeout_seconds=20)
    try:
        with urllib.request.urlopen(url,timeout=20) as r:
            row.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
            if r.headers.get('Content-Length'):
                if int(r.headers['Content-Length'])>8388608:raise ValueError('SIZE_CAP')
            b=r.read(8388609)
            if len(b)>8388608:raise ValueError('SIZE_CAP')
            row.update(bytes=len(b),SHA256=hashlib.sha256(b).hexdigest().upper())
            if name=='remote_manual':
                if not b.startswith(b'%PDF-'):raise ValueError('NOT_PDF')
                with (H/'remote_lab_developer_manual.pdf').open('xb') as f:f.write(b)
                row['saved']='remote_lab_developer_manual.pdf'
            else:
                s=b.decode('utf-8','replace');m=re.search(r'<title[^>]*>(.*?)</title>',s,re.S|re.I)
                row.update(title=m.group(1).strip() if m else None,html_shell_only=True,JS_executed=False)
    except Exception as e:
        row.update(status='ACCESS_FAILED',error_type=type(e).__name__,error=str(e)[:200])
    row['elapsed_seconds']=round(time.monotonic()-start,3);rows.append(row)
with (H/'HTTP_RESULTS_EXTERNAL.json').open('x',encoding='utf-8') as f:json.dump(rows,f,ensure_ascii=False,indent=2)
print(json.dumps(rows,ensure_ascii=False))
