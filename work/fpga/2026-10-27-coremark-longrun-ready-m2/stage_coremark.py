from pathlib import Path
import json,hashlib,struct
H=Path(__file__).resolve().parent
OLD=H/'UNUSED_BASELINE_NOT_AUTHORIZED'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    d=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):d.update(b)
    return d.hexdigest().upper()
def log(p):
    data=Path(p).read_bytes();assert len(data)<=8*1024*1024
    return data.decode('utf-8-sig').replace('\r\n','\n')

def elf_symbols(p):
    data=Path(p).read_bytes();assert data[:7]==b'\x7fELF\x01\x01\x01'
    fields=struct.unpack_from('<HHIIIIIHHHHHH',data,16);assert fields[1]==243 and fields[3]==0 and fields[6]==0
    sections=[struct.unpack_from('<10I',data,fields[5]+i*fields[10]) for i in range(fields[11])];out={}
    for section in sections:
        if section[1]!=2:continue
        st=sections[section[6]];strings=data[st[4]:st[4]+st[5]]
        for offset in range(section[4],section[4]+section[5],section[9]):
            name,value,size,info,other,index=struct.unpack_from('<IIIBBH',data,offset);text=strings[name:].split(b'\0',1)[0].decode('utf-8')
            if text:out[text]=value
    return out

def initial_word(p,address):
    data=Path(p).read_bytes();off=struct.unpack_from('<I',data,28)[0];size,count=struct.unpack_from('<HH',data,42)
    for i in range(count):
        typ,foff,virt,physical,filesz,memsz,flags,align=struct.unpack_from('<8I',data,off+i*size)
        if typ==1 and virt<=address and address+4<=virt+filesz:return struct.unpack_from('<I',data,foff+address-virt)[0]
    raise AssertionError('no initial word')

def table(image,p):
    assert len(image)%4==0 and len(image)<=32768
    with p.open('x',encoding='ascii') as f:
        for name,data in [('ROM',image+bytes(32768-len(image))),('RAM',bytes([0xa5])*32768)]:
            value=data[::-1].hex();chunks=[value[i:i+1024] for i in range(0,len(value),1024)]
            f.write('localparam [262143:0] '+name+'_BITS = {'+',\n'.join("4096'h"+c for c in chunks)+'};\n')
        f.write('localparam integer ROM_BYTES=32768,RAM_BYTES=32768,RAM_BASE=65536;\n')

def save(p,o):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
