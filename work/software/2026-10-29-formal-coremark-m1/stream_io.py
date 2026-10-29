"""A production-adapter candidate: bounded closed segments, no ISA semantics."""
from pathlib import Path
import hashlib,json,time
from stage_budget import check,json_read,deadline as make_deadline
import block_codec
H=Path(__file__).resolve().parent
LINE=256;RECORDS=32768;RAW_CAP=16*1024**3;ARCHIVE_CAP=4*1024**3
INDEX_CAP=16*1024**2;SEGMENT_CAP=16384;RECORD_CAP=500000000

def require(ok,text):
    if not ok:raise ValueError(text)

def sha(path):
    check();d=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):check();d.update(b)
    return d.hexdigest().upper()

def save(path,value):
    with Path(path).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')

def bounded_lines(block):
    for line in block.splitlines(keepends=True):
        require(0<len(line)<=LINE and line.endswith(b'\n'),'line too long or incomplete')
        yield line

def open_stream(directory,kind):
    check();d=Path(directory);spec=json_read(d/'streams.json',65536)[kind]
    mode=spec['mode'];path=Path(spec['path']);total=count=0;whole=hashlib.sha256()
    if mode=='raw':
        require(path.is_file() and path.stat().st_size<=RAW_CAP,'raw input bound')
        with path.open('rb') as f:
            while True:
                line=f.readline(LINE+1)
                if not line:break
                for row in bounded_lines(line):
                    total+=len(row);count+=1;whole.update(row)
                    yield row.decode('ascii')
        require(spec.get('complete') is True,'raw snapshot incomplete')
        return
    if mode=='f153':
        iterator=block_codec.decode(path,spec['index_SHA256'])
        for block in iterator:
            check()
            for row in bounded_lines(block):
                total+=len(row);count+=1;require(total<=RAW_CAP,'raw cap');whole.update(row)
                yield row.decode('ascii')
        return
    require(mode=='segments','stream format')
    require(path.is_dir() and not path.is_symlink(),'archive path')
    index=path/'stream-index.json';require(index.stat().st_size<=INDEX_CAP and sha(index)==spec['index_SHA256'],'global index identity')
    meta=json_read(index,INDEX_CAP);require(meta['format']=='CLOSED-SEGMENTS-1' and meta['complete'] is True and meta['kind']==kind,'incomplete stream')
    require(len(meta['segments'])<=SEGMENT_CAP and 0<meta['raw_bytes']<=RAW_CAP and meta['packed_bytes']<=ARCHIVE_CAP,'stream bounds')
    for number,seg in enumerate(meta['segments']):
        check()
        require(seg['seq']==number and seg['folder']==f'{number:06d}' and 0<seg['records']<=RECORDS,'segment order/count')
        folder=path/seg['folder'];require(not folder.is_symlink(),'segment link')
        got_n=got_b=0
        for block in block_codec.decode(folder,seg['index_SHA256']):
            check()
            for row in bounded_lines(block):
                got_n+=1;got_b+=len(row);count+=1;total+=len(row)
                require(total<=RAW_CAP and count<=RECORD_CAP,'stream record/raw cap');whole.update(row)
                yield row.decode('ascii')
        require((got_n,got_b)==(seg['records'],seg['raw_bytes']),'segment totals')
    require((total,count,whole.hexdigest().upper())==(meta['raw_bytes'],meta['records'],meta['raw_SHA256']),'whole stream totals')

class Archiver:
    """Only this newly created run's closed spool paths can be removed."""
    def __init__(self,run,deadline=None,poll=None):
        self.deadline=make_deadline(900) if deadline is None else deadline;self.poll=poll
        self.timings=dict(encode_s=0.0,decode_verify_s=0.0,source_verify_delete_s=0.0)
        self.run=Path(run).resolve();self.spool=(self.run/'spool').resolve(strict=True)
        self.root=self.run/'archive';self.root.mkdir(exist_ok=False)
        self.rows={k:[] for k in ['trace','bus']};self.hashes={k:hashlib.sha256() for k in self.rows}
        self.closed={};self.raw_total={k:0 for k in self.rows};self.packed=0;self.deleted=[]
        for k in self.rows:(self.root/k).mkdir()
    def checkpoint(self):
        check(self.deadline)
        if self.poll is not None:self.poll()
    def consume(self,line):
        self.checkpoint()
        a=line.strip().split('|')
        if a[0]=='END_STREAM':
            require(len(a)==4 and a[1] in self.rows and a[1] not in self.closed,'bad/duplicate end marker')
            k=a[1];require((int(a[2]),int(a[3]))==(len(self.rows[k]),sum(r['records'] for r in self.rows[k])),'end count')
            self.closed[k]=True;return
        require(len(a)==5 and a[0]=='SEGMENT' and a[1] in self.rows,'ready event')
        k=a[1];seq,n=int(a[2]),int(a[3]);require(seq<SEGMENT_CAP,'SEGMENT_CAP');require(k not in self.closed and seq==len(self.rows[k]) and 0<n<=RECORDS,'ready order/count')
        expected=f'spool/{k}-{seq:06d}.log';require(a[4]==expected,'ready path')
        path=self.run/expected;resolved=path.resolve(strict=True)
        require(resolved.parent==self.spool and not path.is_symlink() and not getattr(path.lstat(),'st_file_attributes',0)&0x400,'spool containment/link')
        require(0<path.stat().st_size<=RECORDS*LINE,'closed segment size')
        raw=path.read_bytes();lines=list(bounded_lines(raw));require(len(lines)==n,'ready record count')
        total=self.raw_total[k]+len(raw);require(total<=RAW_CAP,'total raw budget')
        require(sum(r['records'] for r in self.rows[k])+n<=RECORD_CAP,'RECORD_CAP')
        dst=self.root/k/f'{seq:06d}';started=time.monotonic();self.checkpoint();meta=block_codec.encode(path,dst,min(self.deadline,time.monotonic()+15));self.timings['encode_s']+=time.monotonic()-started
        self.checkpoint();started=time.monotonic()
        ih=sha(dst/'index.json');offset=0
        for block in block_codec.decode(dst,ih):
            self.checkpoint()
            require(block==raw[offset:offset+len(block)],'byte-for-byte archive recovery');offset+=len(block)
        require(offset==len(raw) and meta['lines']==n and meta['SHA256']==hashlib.sha256(raw).hexdigest().upper(),'closed byte/SHA/count')
        self.timings['decode_verify_s']+=time.monotonic()-started
        packed=sum(x.stat().st_size for x in dst.iterdir() if x.is_file());self.packed+=packed
        require(self.packed<=ARCHIVE_CAP,'archive total budget')
        row=dict(seq=seq,folder=f'{seq:06d}',records=n,raw_bytes=len(raw),raw_SHA256=meta['SHA256'],index_SHA256=ih,packed_bytes=packed,source_closed=True,byte_for_byte_verified=True)
        self.rows[k].append(row);self.hashes[k].update(raw);self.raw_total[k]=total
        # No recursive deletion, and no unverified/history path can reach here.
        self.checkpoint();started=time.monotonic()
        require(path.resolve(strict=True)==resolved and sha(path)==meta['SHA256'],'source changed before cleanup')
        path.unlink();self.timings['source_verify_delete_s']+=time.monotonic()-started;self.deleted.append(dict(path=expected,SHA256=meta['SHA256'],verified_before_delete=True))
    def finish(self):
        self.checkpoint()
        require(set(self.closed)==set(self.rows),'missing END_STREAM receipt')
        require(not list(self.spool.iterdir()),'unaccounted raw segment')
        specs={}
        for k,rows in self.rows.items():
            value=dict(format='CLOSED-SEGMENTS-1',kind=k,complete=True,segments=rows,raw_bytes=self.raw_total[k],records=sum(r['records'] for r in rows),raw_SHA256=self.hashes[k].hexdigest().upper(),packed_bytes=sum(r['packed_bytes'] for r in rows))
            idx=self.root/k/'stream-index.json';require(len(json.dumps(value,indent=2).encode('utf-8'))+1<=INDEX_CAP,'GLOBAL_INDEX_CAP');save(idx,value)
            specs[k]=dict(mode='segments',path=str(self.root/k),index_SHA256=sha(idx))
        save(self.run/'streams.json',specs)
        save(self.run/'archive-receipt.json',dict(status='COMPLETE_ARCHIVE_NOT_FUNCTIONAL_PASS',packed_bytes=self.packed,timings=self.timings,deleted=self.deleted,per_stream={k:dict(segments=len(v),raw_bytes=self.raw_total[k],records=sum(x['records'] for x in v),raw_SHA256=self.hashes[k].hexdigest().upper()) for k,v in self.rows.items()}))
        require(sum(q.stat().st_size for q in self.root.rglob('*') if q.is_file())<=ARCHIVE_CAP,'ARCHIVE_META_CAP')
        self.checkpoint();return specs
