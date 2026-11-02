"""Validate full report; compute exact nominal ratios, never certify target scores."""
import re
from fractions import Fraction
def parse(text,expected,flags):
 if len(text.encode('ascii'))>4096:raise ValueError('report cap')
 def one(pattern):
  m=re.findall(pattern,text,re.M)
  if len(m)!=1:raise ValueError('missing/duplicate field '+pattern)
  return m[0]
 def raw(label):
  hi,lo=one('^'+re.escape(label)+r'\s*:\s*([0-9a-f]{8}) ([0-9a-f]{8})$')
  return (int(hi,16)<<32)|int(lo,16)
 iterations=int(one(r'^Iterations\s*:\s*(\d+)\s*$'))
 if iterations!=expected['iterations']:raise ValueError('iterations')
 crc=[]
 for field in ['seedcrc','[0]crclist','[0]crcmatrix','[0]crcstate']:
  crc.append(int(one('^'+re.escape(field)+r'\s*:\s*0x([0-9a-f]{4})\s*$'),16))
 if crc!=expected['standard_CRC']:raise ValueError('CRC')
 final=one(r'^\[0\]crcfinal\s*:\s*0x([0-9a-f]{4})\s*$')
 if final!=expected['crcfinal']:raise ValueError('crcfinal')
 if one(r'^Compiler flags\s*:\s*(.+)$')!=flags:raise ValueError('flags')
 start=raw('Raw start hi/lo');end=raw('Raw end hi/lo');delta=raw('Raw delta hi/lo')
 if not 0<delta<=0xffffffff or end<=start or end-start!=delta:raise ValueError('raw timing')
 if int(one(r'^Total ticks\s*:\s*(\d+)\s*$'))!=delta:raise ValueError('ticks disagree')
 hz=int(one(r'^Timer Hz set\s*:\s*(\d+); MEASUREMENT CANDIDATE; TARGET EVIDENCE REQUIRED$'))
 if hz!=27000000:raise ValueError('frequency setting')
 short=delta<10*hz
 header='2K '+expected['seed']+' run parameters for coremark.'
 if text.splitlines().count(header)!=1:raise ValueError('mode header')
 if int(one(r'^CoreMark Size\s*:\s*(\d+)\s*$'))!=666:raise ValueError('data size')
 if one(r'^Compiler version\s*:\s*(.+)$')!='GCC 15.2.0':raise ValueError('compiler')
 if one(r'^Memory location\s*:\s*(.+)$')!='Code in on-chip ROM; data in static on-chip RAM; clock ratio 1:1':raise ValueError('memory declaration')
 seconds=int(one(r'^Total time \(secs\)\s*:\s*(\d+)\s*$'))
 if seconds!=delta//hz:raise ValueError('integer seconds')
 if seconds:
  if int(one(r'^Iterations/Sec\s*:\s*(\d+)\s*$'))!=iterations//seconds:raise ValueError('legacy integer rate')
 elif re.search(r'^Iterations/Sec',text,re.M):raise ValueError('unexpected rate')
 for label,want in [('Errors detected',int(short)),('Correct operation validated. See README.md for run and reporting rules.',int(not short)),('ERROR! Must execute for at least 10 secs for a valid result!',int(short))]:
  if text.splitlines().count(label)!=want:raise ValueError('missing/duplicate status')
 prefixes=('CoreMark Size','Total ticks','Total time (secs)','Iterations/Sec','Iterations ','Compiler version','Compiler flags','Memory location','seedcrc','[0]crclist','[0]crcmatrix','[0]crcstate','[0]crcfinal','Raw start hi/lo','Raw end hi/lo','Raw delta hi/lo','Timer Hz set','Errors detected','Correct operation validated.','ERROR! Must execute for at least 10 secs')
 if any(line!=header and not line.startswith(prefixes) for line in text.splitlines()):raise ValueError('unexpected output')
 if ('Must execute for at least 10 secs' in text)!=short or ('Errors detected' in text)!=short or ('Correct operation validated.' in text)==short:raise ValueError('validation/error markers')
 if re.search(r'(?i)(?:overflow|unavailable|port error)',text):raise ValueError('error marker')
 return dict(status='SHORT_FUNCTIONAL_ONLY' if short else 'SOFTWARE_MEASUREMENT_CANDIDATE',iterations=iterations,delta=delta,nominal_hz=hz,seconds_fraction=str(Fraction(delta,hz)),nominal_iterations_per_second_fraction=str(Fraction(iterations*hz,delta)),hardware_valid=False,formal_score_valid=False,requires='matching target program identity, real clock evidence, both seeds >=10s and repeated target runs, A review')
