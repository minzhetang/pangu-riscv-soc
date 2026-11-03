from pathlib import Path
import shutil,json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[2]
B=R/'deliveries/task2-review-20261101-v01/extracted/HANDOFF_TASK2_DYNAMIC_PREDICTION_TRAPS_20261101_v01/final_hl4/pds100_hl4'
C=R/'work/advanced/2026-11-03-coremark-strict-m5'
for pred in [0,1]:
 d=H/f'pred{pred}';d.mkdir(exist_ok=False);shutil.copytree(B/'source',d/'source')
 for p in (C/'source').glob('*.v'):shutil.copyfile(p,d/'source'/p.name)
 # Apply the already verified preservation annotations to the independent
 # wrapper copy, not the original B or production core.
 for name in ['board_reset_sync.sv','gpio_core.v']:shutil.copyfile(R/'work/fpga/2026-11-03-event-recorder-m3/build/source'/name,d/'source'/name)
 p=d/'source/board_top_hl4.sv';p.write_text(p.read_text().replace('.BTB_ENABLE     (1)',f'.BTB_ENABLE     ({pred})'))
 # Same newly compiled program image on both sides; not an accepted board image.
 image=(C/'build/performance/program.bin').read_bytes();rom=image+b'\0'*(32768-len(image));ram=b'\0'*32768
 def const(data):return '{'+','.join("4096'h"+data[i:i+512][::-1].hex() for i in range(len(data)-512,-1,-512))+'}'
 (d/'source/init_tables.svh').write_text('localparam [262143:0] ROM_BITS = '+const(rom)+';\nlocalparam [262143:0] RAM_BITS = '+const(ram)+';\nlocalparam ROM_BYTES=32768, RAM_BYTES=32768;\nlocalparam [31:0] RAM_BASE=32\'h00010000;\n')
 for name in ['board_pins.fdc','clock_27mhz.fdc']:shutil.copyfile(B/name,d/name)
 shutil.copyfile(R/'work/fpga/2026-11-03-event-recorder-m3/build/closure_io.fdc',d/'closure_io.fdc')
 flow=(B/'build.tcl').read_text().replace('io_timing.fdc','closure_io.fdc')
 if 'gen_bit' in flow:raise RuntimeError('Unexpected bitstream operation')
 (d/'flow.tcl').write_text(flow)
 code=(H/'build-template.py').read_text()
 code=code.replace("H=Path(__file__).resolve().parent;R=H.parents[2]","H=Path(__file__).resolve().parent;R=H.parents[2]")
 code=code.replace("H/'build/source'",f"H/'pred{pred}/source'").replace("H/'build/generate_bitstream'",f"H/'pred{pred}/generate_bitstream'").replace("H/'build/flow.tcl'",f"H/'pred{pred}/flow.tcl'").replace("H/'build'",f"H/'pred{pred}'")
 code=code.replace("H/'PROTECTED_INPUTS.json'","H/'PROTECTED_INPUTS.json'").replace("H/n).open('x'",f"H/('pred{pred}-'+n)).open('x'")
 code=code.replace("H/'ATTEMPT.json'",f"H/'pred{pred}-ATTEMPT.json'").replace("H/'native-sanitized.log'",f"H/'pred{pred}-native-sanitized.log'")
 code=code.replace("'board_pins.fdc','clock_27mhz.fdc','closure_io.fdc'","'board_pins.fdc','clock_27mhz.fdc','closure_io.fdc'")
 (H/f'build-pred{pred}.py').write_text(code)
shutil.copyfile(R/'work/fpga/2026-11-03-event-recorder-m3/PROTECTED_INPUTS.json',H/'PROTECTED_INPUTS.json')
inputs=[dict(path=p.relative_to(H).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for d in ['pred0','pred1'] for p in sorted((H/d).rglob('*')) if p.is_file()]
(H/'INPUTS.json').write_text(json.dumps(inputs,indent=2))
(H/'SCOPE.json').write_text(json.dumps(dict(date='2026-11-03',purpose='User requested no-board CoreMark/frequency/resource comparison',runs=2,device='PG2L100H-6IFBG676',clock_MHz=27,flow='compile/synthesize/dev_map/pnr/report_timing; NO bitstream',comparison='Only BTB_ENABLE differs; same wrappers/constraints/image',hardware_calls=0,license_environment_changes=False,limitations='No claim of physical frequency, IO/CDC signoff or correct full HL4; synthetic timing mock applies to simulation only, PDS wrapper has native timer'),indent=2))
print('Prepared paired independent offline flows, no bitstream/hardware')
