"""Read existing R4 reports only. Never launch PDS, GUI, simulator or hardware tools."""
from pathlib import Path
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parents[3]
H = Path(__file__).resolve().parent
R = P / 'work/fpga/2026-10-28-local-debug-insert-m1-r4'
PDF = Path('D:/PDS/PDS_2022.2-SP6.4/doc')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def save(name, obj):
    with (H / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

names = ['build/report_timing/rtr.db', 'build/place_route/board_top_pnr.netlist',
         'build/place_route/clock_utilization.txt', 'build/place_route/run.log',
         'build/device_map/board_top.dmr', 'build/device_map/dmr.db',
         'build/place_route/prr.db', 'build/synthesize/board_top_syn.vm',
         'debug.fic', 'NET_MAPPING.json', 'WARNINGS_AUDIT.json',
         'DANGLING_REVIEW.json', 'SOURCE_RECEIPTS.json', 'POSTFLIGHT.json',
         'SUMMARY.json', 'build/generate_bitstream/board_top.sbit']
paths = [R / name for name in names]
paths += [PDF / n for n in ['User_Constraint_Editor_User_Guide.pdf',
          'Pango_Design_Suite_User_Guide.pdf', 'Fabric_Inserter_User_Guide.pdf',
          'Design_Editor_User_Guide.pdf']]
protected = json.loads((R / 'PROTECTED_ORIGINALS.json').read_text())['files']
frozen = []
for phase in ['pre', 'build']:
    frozen += [dict(path=str(R / row['path']), SHA256=row['SHA256'])
               for row in json.loads((R / (phase + '-FROZEN_INPUTS.json')).read_text())['files']]
receipts = [dict(path=str(p), SHA256=sha(p), bytes=p.stat().st_size) for p in paths]
save('INPUTS.json', receipts)

root = ET.parse(R / 'build/report_timing/rtr.db').getroot()
clock_evidence = {}
for corner in ['slow', 'fast']:
    table = root.find("table[@id='report_clock_network_" + corner + "']")
    assert table is not None
    found = {}
    def visit(row, domain, path):
        label = row.findtext('data') or ''
        path = path + [label]
        m = re.search(r'u_CORES/u_debug_core_0/trig0_d1\[(\d+)\]/[^ ]+/CLK(?: |$)', label)
        if m:
            bit = int(m[1])
            assert bit not in found, ('duplicate sampling clock endpoint', corner, bit)
            found[bit] = dict(domain=domain, path=path)
        for child in row.findall('row'):
            visit(child, domain, path)
    for row in table.findall('row'):
        visit(row, row.findtext('data').split(' (', 1)[0], [])
    assert set(found) == set(range(140))
    assert all(e['domain'] == 'clk_27mhz' for e in found.values())
    assert all(any('clkbufg_3/gopclkbufg/CLKOUT' in n for n in e['path']) for e in found.values())
    clock_evidence[corner] = {str(k): found[k] for k in sorted(found)}
save('SAMPLER_CLOCKS.json', dict(status='140_OF_140_BOTH_CORNERS_USER_CLOCK',
     evidence=clock_evidence, data_pin_connections_verified=False,
     limitation='Native clock-network report proves reported CLK ancestry, not D pin source, CDC correctness or physical capture'))

def rows(tid):
    t = root.find("table[@id='" + tid + "']")
    headers = [e.text or '' for e in t.find('column_headers').findall('data')]
    return [dict(zip(headers, [e.text or '' for e in row.findall('data')])) for row in t.findall('row')]
interactions = rows('report_clock_interaction')
async_rows = [r for r in interactions if r['Inter-Clock Constrains'] == 'Asynchronous Groups']
assert len(async_rows) == 3
assert {(r['Launch Clock'], r['Capture Clock']) for r in async_rows} == {
    ('DebugCore_JCLK', 'clk_27mhz'), ('DebugCore_CAPTURE', 'clk_27mhz'), ('clk_27mhz', 'DebugCore_JCLK')}
save('CLOCK_INTERACTIONS.json', dict(status='ASYNC_RELATIONSHIPS_DOCUMENTED_NOT_CDC_VALIDATED',
     declared_clocks=rows('report_timing_clock_summary'), interactions=interactions,
     explicit_limit='Declared 20/10MHz debug clocks are not measured cable clocks. Asynchronous Groups has no setup/hold result for these relationships; endpoint counts are native report counts, not unique CDC crossing counts.'))

flow = (R / 'build/place_route/run.log').read_text(errors='replace')
crit = [line for line in flow.splitlines() if line.startswith('C:')]
assert len(crit) == 4 and sum('Place-2028' in s for s in crit) == 1
assert sum('Route-2036' in s for s in crit) == 3
assert all('u_CORES/' in s for s in crit)
dmr = (R / 'build/device_map/board_top.dmr').read_text()
assert re.search(r'n:u_CORES/drck_o\s*\|\s*PAP_CLOCK_DEDICATED_ROUTE\s*\|\s*FALSE', dmr)
save('WARNING_FINDINGS.json', dict(status='FOUR_CRITICAL_REMAIN_OPEN', messages=crit,
     generated_attribute='u_CORES/drck_o PAP_CLOCK_DEDICATED_ROUTE=FALSE',
     manual_basis=[dict(file=str(PDF / 'User_Constraint_Editor_User_Guide.pdf'), version='1.7',
                        PDF_pages=[97,98], section='2.3.4.9', finding='FALSE permits SRB interconnect and may downgrade Place-0084 to Place-2028; not a waiver'),
                   dict(file=str(PDF / 'Pango_Design_Suite_User_Guide.pdf'), version='1.5',
                        PDF_pages=[115], finding='Check Clock Net Routing Path reports Route-2036 for non-clock-tree routing')],
     no_rebuild=True, warning_waived=False))

# The text inventory contains direction/type declarations but no net-to-pin edges.
inventory = (R / 'build/place_route/board_top_pnr.netlist').read_text()
sections = re.split(r'(?m)^(Port|Inst|Pin|Net|Clock)\s*$', inventory)
unknown = []
counts = {}
for i in range(1, len(sections), 2):
    kind, body = sections[i], sections[i+1]
    entries = [s.strip() for s in body.splitlines() if s.strip()]
    counts[kind] = counts.get(kind, 0) + len(entries)
    for entry in entries:
        assert ';' in entry, (kind, entry[:120])
        if kind in ['Port','Inst','Pin','Clock']:
            assert len(entry.split(';')) == 2
        elif kind == 'Net':
            assert entry.endswith(';') and len(entry.split(';')) == 2 and entry.split(';')[1] == ''
mapping = json.loads((R / 'NET_MAPPING.json').read_text())
selected = [s for p in mapping['probes'] for s in p['selected'] if s['channel'] >= 136]
assert [s['channel'] for s in selected] == [136,137,138,139]
vm = (R / 'build/synthesize/board_top_syn.vm').read_text(encoding='utf-8-sig')
assert re.search(r'\.eei_stop_valid\s*\(stopped\)', vm)
assert re.search(r'\.eei_stop_kind\s*\(stop_kind\)', vm)
assert re.search(r'\.write_error\s*\(write_error\)', vm)
assert re.search(r'\.stopped\s*\(stopped\)', vm)
save('DATA_SOURCE_LIMITS.json', dict(status='PREINSERTION_ALIAS_SUPPORTED_POSTROUTE_D_INPUT_UNRESOLVED',
     risk_channels=selected, preinsertion_named_port_connections=True,
     inventory_entries=counts, inventory_has_net_to_pin_edges=False,
     XML_reports_checked=['device_map/dmr.db','place_route/prr.db','report_timing/rtr.db'],
     no_binary_ADF_decoding=True,
     remaining='Need native post-route driver/load report or editor observation to establish D pin -> mapped source driver, especially channels136-139; cell and net names alone are insufficient.'))

assert all(sha(Path(row['path'])) == row['SHA256'] for row in protected + frozen)
assert all(sha(Path(row['path'])) == row['SHA256'] for row in receipts)
summary = dict(date='2026-10-29', status='READONLY_DIAGNOSIS_COMPLETE_WITH_NATIVE_CONNECTIVITY_GAP',
     critical_open=4, sampler_clock_endpoints_both_corners=140,
     main_sampling_clock='clk_27mhz via clkbufg_3', async_relationships_not_CDC_validated=3,
     full_data_pin_connectivity_verified=False, protected_entries=len(protected),
     frozen_entries=len(frozen), inputs_unchanged=True,
     PDS_builds=0, GUI=0, new_DUT=0, hardware='STOPPED',
     next='Request one bounded native Design Editor read-only session on copied existing routed DB; no rebuild or constraint change')
save('SUMMARY.json', summary)
print(json.dumps(summary))
