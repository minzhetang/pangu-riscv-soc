"""Diagnosed fallback: public fixed archive/raw endpoints, no API quota usage."""
import hashlib
import io
import json
import stat
import zipfile
from pathlib import PurePosixPath
from fetch_official import HERE, COMMIT, SELECT, fetch

def main():
    out=HERE/'upstream-direct'
    out.mkdir(exist_ok=False)
    receipt={'commit':COMMIT,'reason':'Original Git tree API returned HTTP403 rate limit; preserve first receipt',
             'status':'STARTED','archive_url':f'https://codeload.github.com/eembc/coremark/zip/{COMMIT}',
             'downloaded_code_executed':False,'published_archive_SHA256':None}
    try:
        data=fetch(receipt['archive_url'],5_000_000)
        (out/'source.zip').write_bytes(data)
        receipt['archive_SHA256']=hashlib.sha256(data).hexdigest().upper()
        z=zipfile.ZipFile(io.BytesIO(data)); entries=z.infolist()
        prefix=f'coremark-{COMMIT}/'
        assert len(entries)<1000 and sum(e.file_size for e in entries)<20_000_000
        for e in entries:
            p=PurePosixPath(e.filename)
            assert e.filename.startswith(prefix) and not p.is_absolute() and '..' not in p.parts
            assert '\\' not in e.filename and ':' not in e.filename
            assert not stat.S_ISLNK(e.external_attr>>16) and e.file_size<=2_000_000
        records=[]
        for name in SELECT+['coremark.md5']:
            content=z.read(prefix+name)
            path=out/'files'/name; path.parent.mkdir(exist_ok=True,parents=True)
            path.write_bytes(content)
            url=f'https://raw.githubusercontent.com/eembc/coremark/{COMMIT}/{name}'
            # Compare exact raw bytes on a different official GitHub endpoint.
            assert content==fetch(url,2_000_000), (name,'raw/archive mismatch; stop and preserve')
            records.append({'name':name,'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest().upper(),'url':url})
        md5=[]
        for line in (out/'files/coremark.md5').read_text().splitlines():
            digest,name=line.split(); name=name.lstrip('*').removeprefix('./')
            if name in SELECT:
                actual=hashlib.md5((out/'files'/name).read_bytes()).hexdigest()
                assert actual==digest, (name,'upstream MD5 mismatch')
                md5.append(name)
        assert all(n in md5 for n in ['core_list_join.c','core_main.c','core_matrix.c','core_state.c','core_util.c','coremark.h'])
        receipt.update(status='VERIFIED_SOURCE_DATA',files=records,archive_entries_checked=len(entries),
                       raw_archive_identical_files=len(records),upstream_MD5_verified=md5,
                       verification='Fixed official commit; TLS archive/raw byte equality; upstream MD5; locally recorded SHA256, not signed release hash')
    except Exception as exc:
        receipt.update(status='FAILED_STOP_NO_EXECUTION',error=repr(exc)); raise
    finally:
        (HERE/'source-receipt-direct.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
