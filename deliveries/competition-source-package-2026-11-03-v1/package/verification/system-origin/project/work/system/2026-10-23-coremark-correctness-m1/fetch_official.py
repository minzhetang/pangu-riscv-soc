"""Fetch pinned official sources as data only; never execute archive contents."""
import hashlib
import io
import json
import stat
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
COMMIT = '1f483d5b8316753a742cbf5590caf5bd0a4e4777'
SELECT = ['LICENSE.md', 'README.md', 'barebones_porting.md', 'coremark.h',
          'core_list_join.c', 'core_main.c', 'core_matrix.c', 'core_state.c',
          'core_util.c', 'barebones/core_portme.c', 'barebones/core_portme.h']

def fetch(url, limit):
    req = urllib.request.Request(url, headers={'User-Agent':'FPGA-project-source-evidence'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read(limit + 1)
        assert len(data) <= limit, 'download size limit'
        return data

def main():
    target = HERE/'upstream'
    target.mkdir(exist_ok=False)
    record = {'commit':COMMIT,'status':'FETCH_STARTED','exec_downloaded_code':False,
              'tree_url':f'https://api.github.com/repos/eembc/coremark/git/trees/{COMMIT}?recursive=1',
              'archive_url':f'https://codeload.github.com/eembc/coremark/zip/{COMMIT}'}
    try:
        tree_raw = fetch(record['tree_url'], 2_000_000)
        (target/'tree.json').write_bytes(tree_raw)
        tree = json.loads(tree_raw)
        assert not tree.get('truncated')
        archive = fetch(record['archive_url'], 5_000_000)
        (target/'source.zip').write_bytes(archive)
        record['archive_sha256'] = hashlib.sha256(archive).hexdigest().upper()
        blobs = {e['path']:e['sha'] for e in tree['tree'] if e['type']=='blob'}
        z = zipfile.ZipFile(io.BytesIO(archive))
        entries=z.infolist()
        assert len(entries)<1000 and sum(i.file_size for i in entries)<20_000_000
        prefix=f'coremark-{COMMIT}/'
        for info in entries:
            p=PurePosixPath(info.filename)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename
            assert ':' not in info.filename and info.filename.startswith(prefix)
            assert not stat.S_ISLNK(info.external_attr>>16)
            assert info.file_size <= 2_000_000
        records=[]
        for name in SELECT:
            data=z.read(prefix+name)
            git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert git_blob==blobs[name], (name,'Git blob SHA-1 mismatch; preserve and stop')
            path=target/'files'/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
            records.append({'name':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest().upper(),
                            'git_blob_sha1_verified':git_blob,
                            'url':f'https://raw.githubusercontent.com/eembc/coremark/{COMMIT}/{name}'})
        record.update(status='VERIFIED_SOURCE_ONLY',files=records,
                      archive_entries_checked=len(entries),selected_files=len(records),
                      verification='TLS official fixed commit + independent official Git tree blob IDs; no published archive SHA256 claimed')
    except Exception as exc:
        record.update(status='FETCH_OR_VERIFICATION_ERROR',error=repr(exc))
        raise
    finally:
        (HERE/'source-receipt.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps(record,indent=2))

if __name__=='__main__': main()
