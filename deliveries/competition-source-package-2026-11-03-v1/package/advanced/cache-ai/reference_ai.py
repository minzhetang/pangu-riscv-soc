"""Independent scalar math reference: no RTL shared implementation or model library."""
import hashlib,json,math,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
def nearest(x): return math.floor(x+.5) if x>=0 else -math.floor(-x+.5)
def clip(x,lo,hi):return max(lo,min(hi,x))
def quant(x):return clip(nearest(x*64),-128,127)
def result(x,w,b):
    raw=[b[r]+sum(x[k]*w[r][k] for k in range(16)) for r in range(8)]
    # Division/remainder, independent of RTL's magnitude arithmetic and bit shift.
    y=[]
    for s in raw:
        a,rem=divmod(abs(s),64);a+=rem>=32
        y.append(clip(a if s>=0 else -a,-128,127))
    return raw,y
def generate():
    cases=[]
    for seed in [1,7,19]:
        xf=[math.sin((i+1)*(seed+1))*.7 for i in range(16)]
        wf=[[math.cos((r+2)*(k+1)+seed)*.35 for k in range(16)] for r in range(8)]
        bf=[math.sin(r+seed)*.1 for r in range(8)]
        x=list(map(quant,xf));w=[list(map(quant,row)) for row in wf];b=[nearest(v*4096) for v in bf]
        raw,y=result(x,w,b);fp=[bf[r]+sum(xf[k]*wf[r][k] for k in range(16)) for r in range(8)]
        cases.append(dict(name=f'non_grid_{seed}',x=x,w=w,b=b,raw=raw,y=y,float_reference=fp,
            float_inputs=xf,float_weights=wf,float_bias=bf,
            pre_output_quantization_error=[raw[r]/4096-fp[r] for r in range(8)],
            final_quantization_error=[y[r]/64-fp[r] for r in range(8)]))
    specs=[('zero',[0]*16,[[0]*16 for _ in range(8)],[0]*8),
      ('extrema',[-128,127]*8,[[(-128 if (k+r)%2 else 127) for k in range(16)] for r in range(8)],[0]*8),
      ('bias_limits',[127]*16,[[127 if r%2 else -128 for k in range(16)] for r in range(8)],[2147483647 if r%2 else -2147483648 for r in range(8)]),
      ('rounding',[0]*16,[[0]*16 for _ in range(8)],[32,-32,96,-96,31,-31,97,-97]),
      ('saturation',[0]*16,[[0]*16 for _ in range(8)],[8095,8096,8192,-8191,-8192,-8224,8128,-8256])]
    for name,x,w,b in specs:
        raw,y=result(x,w,b);fp=[v/4096 for v in raw]
        cases.append(dict(name=name,x=x,w=w,b=b,raw=raw,y=y,float_reference=fp,pre_output_quantization_error=[0]*8,final_quantization_error=[y[r]/64-fp[r] for r in range(8)]))
    d=ROOT/'ai_vectors';d.mkdir(exist_ok=True)
    for idx,c in enumerate(cases):
        values=c['x']+sum(c['w'],[])+c['b']+sum(([c['raw'][r],c['y'][r]] for r in range(8)),[])
        (d/f'{idx}.txt').write_text('\n'.join(str(v) for v in values)+'\n')
    lines=(d/'0.txt').read_text().splitlines();lines[-1]=str(int(lines[-1])+1)
    (d/'negative.txt').write_text('\n'.join(lines)+'\n')
    (d/'cases.json').write_text(json.dumps(cases,indent=2))
    files=[ROOT/'ai_plan.md',ROOT/'reference_ai.py',*sorted(d.glob('*'))]
    (ROOT/'AI_FROZEN_SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n' for p in files))
def run_ai(bounded,tools):
    # Keep this routine frozen too: matrix/thresholds cannot change after observing RTL.
    from run import verify
    verify('AI_FROZEN_SHA256.txt')
    bounded('ai_compile_v1',[tools/'iverilog.exe','-g2012','-Wall','-s','ai_tb','-o','ai.vvp','fc.sv','ai_tb.sv'])
    cases=json.loads((ROOT/'ai_vectors/cases.json').read_text());results=[]
    for idx,c in enumerate(cases):
        for stalls in [0,1]:
            args=[tools/'vvp.exe','ai.vvp',f'+VEC=ai_vectors/{idx}.txt',f'+STALL={stalls}']
            if idx==6 and stalls:args+=['+WAVE=ai_rounding.vcd']
            raw=bounded(f'ai_{idx}_s{stalls}_v1',args)
            vals=[list(map(int,m)) for m in re.findall(r'OUTPUT row=(\d+) raw=(-?\d+) y=(-?\d+)',raw)]
            assert vals==[[r,c['raw'][r],c['y'][r]] for r in range(8)],(idx,vals)
            m=re.search(r'AI_METRIC cycles=(\d+) config_cycles=(\d+)',raw);assert m and 'PASS ai' in raw
            cyc,cc=map(int,m.groups());assert cyc==(148 if stalls else 136),(cyc,stalls)
            results.append(dict(case=c['name'],stalls=stalls,compute_cycles=cyc,config_cycles=cc,outputs=vals,status='PASS'))
    raw=bounded('ai_reset_protocol_v1',[tools/'vvp.exe','ai.vvp','+VEC=ai_vectors/0.txt','+MODE=1','+WAVE=ai_reset.vcd']);assert 'PROTOCOL_PASS' in raw
    raw=bounded('ai_negative_v1',[tools/'vvp.exe','ai.vvp','+VEC=ai_vectors/negative.txt'],expected_exit=1);assert 'mismatch' in raw
    (ROOT/'AI_RESULTS.json').write_text(json.dumps(results,indent=2));verify('AI_FROZEN_SHA256.txt')
    print('PASS AI: 8 cases x 2 stall patterns, reset/protocol and negative rejection; SYNTHETIC ONLY')
if __name__=='__main__':generate()
