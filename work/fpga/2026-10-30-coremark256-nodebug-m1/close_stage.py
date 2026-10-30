from pathlib import Path
import sys,json,hashlib,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
from stage_budget import check,STAGE_DEADLINE
from host_checks import tree_bytes
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):
 d=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):d.update(b)
 return d.hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf8') as f:json.dump(o,f,ensure_ascii=False,indent=2)
check();result=read(H/'RESULTS.json');assert result['status']=='SOFTWARE_BITSTREAMS_GENERATED_WITH_KNOWN_LIMITS'
protected=read(H/'PROTECTED_INPUTS.json')['files'];assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
frozen=read(H/'FROZEN_INPUTS-r1.json')['files'];assert all(sha(H/x['path'])==x['SHA256'] for x in frozen)
identities=[]
for c in read(H/'PLAN.json')['cases']:
 tid=c['id'];d=H/tid;r=read(d/'AUDIT_RESULT.json');proc=read(d/'BUILD_EXIT_RECEIPT.json')['process']
 assert r['status']=='SOFTWARE_BITSTREAM_GENERATED_WITH_KNOWN_LIMITS' and sha(Path(r['artifact']['path']))==r['artifact']['SHA256']
 assert sha(d/'firmware/program.bin')==c['bin_SHA256'] and sha(d/'firmware/program.elf')==c['ELF_SHA256'] and sha(d/'pds/source/init_tables.svh')==c['init_SHA256']
 assert tree_bytes(d)<=512*1024**2
 identities.append(dict(case=tid,iterations=256,board='MES2L676-100HP',target='PG2L100H-6IFBG676',clock_setting_hz=27000000,measured_clock=False,bin_SHA256=c['bin_SHA256'],ELF_SHA256=c['ELF_SHA256'],INIT_SHA256=c['init_SHA256'],production_memory_SHA256=sha(d/'pds/source/memory_model.sv'),bitstream=r['artifact'],timing=r['timing'],INIT_pieces=r['INIT_pieces'],changed_INIT_count=len(r['changed_INIT_pieces']),seconds=proc['elapsed_seconds'],native_rc=proc['returncode'],shell_peak_bytes=proc['peak_working_set_bytes'],parent_peak_bytes=proc['parent_peak_working_set_bytes'],reported_pool_MB=r['memory_pool_reported_MB'],license_days=r['license_days_remaining'],expected_report_SHA256=sha(P/'work/software/2026-10-29-formal-coremark-m1/oracles-recovery'/tid/'expected-report.txt'),hardware_valid=False,formal_score_valid=False,UART_physical_run='NOT_RUN',long256_DUT='NOT_RUN'))
save('TARGET_IDENTITIES.json',dict(status='SOFTWARE_IDENTITIES_ONLY_NOT_HARDWARE_ACCEPTANCE',cases=identities))
save('POSTFLIGHT.json',dict(status='PROTECTED_AND_FROZEN_INPUTS_UNCHANGED',protected_entries=len(protected),frozen_entries=len(frozen),stage_bytes_before_postflight=tree_bytes(H),deadline_remaining=STAGE_DEADLINE-time.monotonic(),PDS_actual=2,prelaunch_failures=1,original_prelaunch_error='STOPPED.json',GCC=0,DUT=0,hardware='STOPPED',license_days_actual=[4],no_external_send=True))
check();files=sorted(p for p in H.rglob('*') if p.is_file());assert tree_bytes(H)<=2*1024**3
(H/'SHA256SUMS-FINAL.txt').write_text(''.join(sha(p)+'  '+p.relative_to(H).as_posix()+'\n' for p in files),encoding='utf8')
print(json.dumps(dict(status='CLOSED_SOFTWARE_ONLY',protected=len(protected),frozen=len(frozen),files=len(files),bytes=sum(p.stat().st_size for p in files),identities=identities),ensure_ascii=False))
