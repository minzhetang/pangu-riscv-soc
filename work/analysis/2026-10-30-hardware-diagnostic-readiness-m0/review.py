"""Read-only PDF/history evidence; no FPGA tools or hardware operations."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
from pypdf import PdfReader
H=Path(__file__).resolve().parent;P=H.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
cases=[('UG040005_Logos2_Configuration_V1.3_EN.pdf','326794CD880EA789CC3BB2FD5D8369E59A7BEA508B1D7B10BA16E064CCCB6C27',[59]),('UG040009_Logos2_ADC_V1.6_EN.pdf','43A0A99BF004AA721418A140D82F183B209B7C7559327299E693CD60F646F10B',[15,29])]
out=[]
for name,want,pages in cases:
 p=P/'reports/hardware/2026-10-14-over-temp-evidence'/name;assert sha(p)==want
 r=PdfReader(p)
 for page in pages:
  text=r.pages[page-1].extract_text()
  (H/(name.split('_')[0]+'-p'+str(page)+'.txt')).write_text(text,encoding='utf8')
  out.append(dict(path=str(p),SHA256=want,actual_pdf_page=page,printed_page=page-1,read='text and fresh rendered full page visually checked',key='STATUSR27 row lacks complete mapping/clear rules' if page==59 else 'temperature conversion/OT hysteresis' if page==15 else 'unconfigured ADC power-up still outputs OT'))
p=P/'reports/hardware/2026-10-14-led-volatile-result.json';j=json.loads(p.read_text(encoding='utf-8-sig'));assert j['StatusRegister']=='0x081efca0' and ((int(j['StatusRegister'],16)>>27)&1)==1
log=P/'work/pds-jtag/2026-10-14-led-volatile/configuration_tcl.log';lines=log.read_text(encoding='utf-8-sig').splitlines();assert sum('cfg_program succeed' in s for s in lines)==1
result=dict(date='2026-10-30',status='NO_HARDWARE_CLEARANCE',PDF_rows=out,old_state=dict(source=str(p),SHA256=sha(p),STATUSR=j['StatusRegister'],bit27=1),configuration_log=dict(SHA256=sha(log),commands=len(lines),new_execution=False),equipment_user_report=dict(multimeter_basic_voltage_current_resistance_continuity=True,temperature_capability=False,brand_model='UNKNOWN',independently_verified=False,source='2026-10-30 user replies'),rendering='three pdftoppm page renders; missing Symbol/ArialUnicode font warnings retained in tool output; critical rows/text readable by visual inspection',new_temperature_measurement=False,new_voltage_measurement=False,PDS=0,simulation=0,hardware=0,decision='D202',next='resolve measurement conditions before drafting any powered test; continue independent report/analysis tasks')
with (H/'REVIEW_RESULT.json').open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print('Three PDF pages and unchanged historical register rechecked; basic multimeter only (user report); hardware STOP unchanged')
