"""Single approved non-admin CLI context comparison after WinError 623.

No retry loop, GUI, bitstream, hardware, license or environment changes.
"""
import ctypes
import importlib.util
from pathlib import Path

root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('m0stage', root / 'stage.py')
stage = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = stage
spec.loader.exec_module(stage)
assert not ctypes.windll.shell32.IsUserAnAdmin()
assert stage.read(root / 'simulation-result.json')['status'] == 'PASS'
stage.protect()
assert not (root / 'pds-external-process.json').exists()
assert not any((root / 'pds' / n).exists() for n in
               ['compile', 'synthesize', 'device_map', 'place_route', 'report_timing'])
result = stage.bounded([stage.PDS, '-file', root / 'pds/build.tcl'],
                       root / 'pds', 'pds-flow-external-01', 1200)
stage.save(root / 'pds-external-process.json', result)
print('PDS_PROCESS_EXITED', result['returncode_hex'],
      'inspect fresh reports; NOT success claim', flush=True)
