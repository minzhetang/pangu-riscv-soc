"""Static bytes/ELF/init/lineage audit only; no tools, models, devices or execution."""
from pathlib import Path
import sys,json,hashlib,re,struct
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
S=P/'work/software/2026-10-29-formal-coremark-m1';F=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 d=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):d.update(b)
 return d.hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf8') as f:json.dump(o,f,ensure_ascii=False,indent=2)
files=sorted((S/'source').glob('*.v'))+sorted((S/'source').glob('*.sv'));assert len(files)==13
assert {p.name for p in files}=={p.name for p in (F/'source-before').iterdir() if p.suffix in ['.sv','.v']}
source=[]
for p in files:
 old=F/'source-before'/p.name;assert sha(p)==sha(old),p.name
 prod=F/'pds/source'/p.name
 exact=sha(p)==sha(prod)
 assert exact or p.name=='memory_model.sv'
 source.append(dict(name=p.name,software_SHA256=sha(p),baseline_source_SHA256=sha(old),production_SHA256=sha(prod),production_exact=exact,transformation='existing audited M0_VERIFY removal and INIT inlining' if not exact else 'none'))
old=read(F/'SUMMARY.json');assert old['functional_RTL13_unchanged'] and old['independent_INIT_pieces']==1792
assert sha(Path(old['bitstream']['path']))==old['bitstream']['SHA256']
assert sha(F/'pds/source/init_tables.svh')==old['image']['init_SHA256']
result=read(S/'RESULTS-M1.json');assert result['status']=='PASS_SCOPED_SOFTWARE_NOT_FORMAL_SCORE'
rows=[]
for tid in ['performance256','validation256']:
 r=next(x for x in result['rows'] if x['id']==tid);b=S/'build'/tid;init=S/'initialization'/(tid+'.svh');text=init.read_text()
 assert r['DUT']=='NOT_RUN' and r['reference']=='PASS_REFERENCE_ONLY'
 assert sha(b/'program.bin')==r['bin_SHA256'] and sha(b/'program.elf')==r['ELF_SHA256']
 image=(b/'program.bin').read_bytes();assert 0<len(image)<=32768 and len(image)%4==0
 def bits(name):
  body=text.split(name+'_BITS = {',1)[1].split('};',1)[0];pieces=re.findall(r"4096'h([0-9a-fA-F]{1024})",body);assert len(pieces)==64
  return bytes.fromhex(''.join(pieces))[::-1]
 rom,ram=bits('ROM'),bits('RAM');assert rom==image+bytes(32768-len(image)) and ram==b'\xa5'*32768
 e=read(S/'oracles-recovery'/tid/'expected.json');sym=e['symbols'];assert sym['__bss_end']<=sym['__stack_bottom'] and sym['__stack_top']==0x18000
 elf=(b/'program.elf').read_bytes();off=struct.unpack_from('<I',elf,28)[0];size,count=struct.unpack_from('<HH',elf,42)
 def initialized_word(addr):
  for i in range(count):
   typ,foff,virt,phys,filesz,memsz,flags,align=struct.unpack_from('<8I',elf,off+i*size)
   if typ==1 and virt<=addr and addr+4<=virt+filesz:return struct.unpack_from('<I',elf,foff+addr-virt)[0]
  raise ValueError('not file backed')
 assert initialized_word(sym['seed4_volatile'])==256 and initialized_word(sym['seed3_volatile'])==0x66
 for n in ['seed1_volatile','seed2_volatile']:
  addr=sym[n];value=0 if sym['__bss_start']<=addr and addr+4<=sym['__bss_end'] else initialized_word(addr)
  assert value==(0 if tid.startswith('performance') else 0x3415)
 rows.append(dict(id=tid,image_bytes=len(image),bin_SHA256=sha(b/'program.bin'),ELF_SHA256=sha(b/'program.elf'),init_SHA256=sha(init),ROM_SHA256=hashlib.sha256(rom).hexdigest().upper(),RAM_SHA256=hashlib.sha256(ram).hexdigest().upper(),seed4=256,steps=e['steps'],raw_ticks=e['raw_ticks'],nominal_seconds=e['raw_ticks']/27000000,crcfinal=e['crcfinal'],build='PASS_PREVIOUS_M1',reference='PASS_PREVIOUS_M1',RTL256='NOT_RUN',PDS256='NOT_RUN',hardware='NOT_RUN',formal_score_valid=False))
constraints=[dict(path=str(F/'pds'/name),SHA256=sha(F/'pds'/name)) for name in ['board_pins.fdc','clock_27mhz.fdc','build.tcl']]
led=read(P/'reports/hardware/2026-10-14-led-volatile-result.json')
assert led['StatusRegister']=='0x081efca0' and led['StatusFlags']['over_temp']==1
save('SAFETY_GATES.json',dict(status='STOPPED_NOT_CLEARED',historical_status=led['StatusRegister'],public_id=led['PublicIdCode'],flags=led['StatusFlags'],temperature_measured=False,pre_configuration_bit27_baseline=False,hardware_queried_this_round=False,source='reports/hardware/2026-10-14-led-volatile-result.json',unknowns=['CFG27 exact validity/polarity/latch-clear relation to ADC OT','actual temperature and time evolution','physical CFG rail endpoint voltage not closed','board power switch complete circuit definition'],no_inference=['software pass/LED/DONE cannot establish safe temperature','ADC OT hysteresis does not define CFG27 clear rules','High Voltage remains engineering decision, not measured supply']))
protected=read(F/'PROTECTED_ORIGINALS.json')['files']+read(S/'PROTECTED_INPUTS.json')
assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
save('SOURCE_AND_IMAGE_IDENTITY.json',dict(status='STATIC_BYTE_AND_LAYOUT_PASS_NOT_NEW_FUNCTIONAL_RUN',source=source,constraints=constraints,old_bitstream=dict(path=old['bitstream']['path'],SHA256=old['bitstream']['SHA256'],iterations=8,not_usable_as_256_image=True),cases=rows))
save('SUMMARY.json',dict(date_client='2026-10-30',status='READINESS_REVIEW_COMPLETE_HARDWARE_STOPPED',protected_entries_verified=len(protected),functional_source_exact_to_baseline=13,production_exact=12,production_memory_binding='reuse existing audited transform, new INIT only',new_C=0,new_reference=0,new_DUT=0,PDS=0,GUI=0,hardware=0,formal_score=False,scope_next='A-BOARD-COREMARK256-NODEBUG-M1 1.0.0 pending approval',debug_export='not prerequisite for nondebug program build; still required evidence before ILA acceptance'))
print('Static lineage13 / production12+binding / two256 INIT+ELF PASS; STOP unchanged; 0 execution')
