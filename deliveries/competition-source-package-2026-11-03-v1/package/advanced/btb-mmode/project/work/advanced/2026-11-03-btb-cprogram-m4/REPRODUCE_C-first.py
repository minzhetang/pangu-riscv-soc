from pathlib import Path
import argparse,shutil,subprocess,sys,json
H=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--iverilog-root',required=True);p.add_argument('--output',required=True);args=p.parse_args()
tool=Path(args.iverilog_root).resolve();out=Path(args.output).resolve()
if not (tool/'bin/iverilog.exe').is_file() or not (tool/'bin/vvp.exe').is_file():raise SystemExit('Existing legal Windows Icarus root required')
if out.exists() or out.is_relative_to(H):raise SystemExit('Output must be a new directory outside the package')
src=H/'work/advanced/2026-11-03-btb-cprogram-m4'
if not src.is_dir():raise SystemExit('Run this entry from the delivery root')
out.mkdir(parents=True);dest=out/'work/advanced'/src.name;dest.mkdir(parents=True)
for name in ['source','expected']:shutil.copytree(src/name,dest/name)
for name in ['execute.py','run.py','reference.py','tb.sv','program.bin','program.hex','FROZEN_REFERENCE.json']:shutil.copyfile(src/name,dest/name)
helper=Path('work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py');(out/helper).parent.mkdir(parents=True);shutil.copyfile(H/helper,out/helper)
code=(dest/'execute.py').read_text();start=next(line for line in code.splitlines() if line.startswith('I=R/'));code=code.replace(start,'I=Path('+repr(str(tool))+'); jobs=[]');(dest/'execute.py').write_text(code)
r=subprocess.run([sys.executable,'-X','utf8','-B',str(dest/'run.py'),'package-repro'],cwd=dest,timeout=600)
result=dict(rc=r.returncode,stage=str(dest),results=str(dest/'package-repro-RESULTS.json'),scope='New CPU simulation of the frozen C binary, not a formal CoreMark or hardware acceptance')
(out/'REPRO_RESULT.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));raise SystemExit(r.returncode)
