"""Render measured CSV samples with Pillow; no synthetic/simulated waveform data."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, json, hashlib

F = Path(__file__).resolve().parent
PC='soc/cpu_core/id_pc'; ADV='soc/cpu_core/pipeline_advance'; VALID='soc/cpu_core/id_valid'
fontpath=Path('C:/Windows/Fonts/consola.ttf')
font=ImageFont.truetype(str(fontpath),17)
small=ImageFont.truetype(str(fontpath),14)
titlefont=ImageFont.truetype(str(fontpath),23)
tracks=[('advance',ADV),('EX valid',VALID),('load-use','soc/cpu_core/stall_if'),('redirect','soc/cpu_core/flush_id'),('branch taken','soc/cpu_core/branch_taken')]

def render(case):
    d=F/'qualified-windows'/case
    a=json.loads((d/(case+'.analysis.json')).read_text())
    assert hashlib.sha256((d/(case+'.wdf')).read_bytes()).hexdigest().upper()==a['wdf_sha256']
    rows=[{k:int(v) for k,v in r.items()} for r in csv.DictReader((d/(case+'.csv')).open())]
    assert len(rows)==1024 and [r['sample'] for r in rows]==list(range(1024))
    panels=[('Frozen entry trigger',512)]
    load=next((e for e in a['load_use_events'] if e['fully_observed'] and (case!='state' or 0x1ee0<=e['pc']<0x21c8)),None)
    flow=next((e for e in a['control_flow_events'] if e['fully_observed'] and e['kind']!='jalr'),None)
    if load:panels.append(('Qualified load-use: rd=x%d -> PC %04x'%(load['rd'],load['consumer_pc']),load['sample']))
    if flow:panels.append(('Qualified '+flow['kind']+' redirect: PC %04x -> %04x'%(flow['pc'],flow['next_valid_pc']),flow['sample']))
    w=2150; ph=340; image=Image.new('RGB',(w,155+ph*len(panels)), 'white');dr=ImageDraw.Draw(image)
    dr.text((25,16),case+' | real FPGA capture | 1024 samples, 140 binary channels',font=titlefont,fill='#12283c')
    dr.text((25,52),'Timed EX events/slots: %d/%d = %.3f%%; stalls=%d; redirects=%d'%(a['active_EX_events'],a['logical_slots'],100*a['EX_events_per_logical_slot'],a['qualified_load_use_stalls'],a['qualified_control_flushes']),font=font,fill='#12283c')
    dr.text((25,79),'Green=qualified EX event; amber=invalid advance slot. Sampled before edge. Not retirement IPC.',font=small,fill='#465362')
    for panel,(label,anchor) in enumerate(panels):
        top=110+panel*ph;lo=max(0,min(960,anchor-16));hi=lo+64;x0=185;dx=30
        dr.text((25,top),label+' | physical sample indices %d..%d'%(lo,hi-1),font=font,fill='#12283c')
        for i in range(lo,hi):
            x=x0+(i-lo)*dx
            if rows[i][ADV]:dr.rectangle((x,top+44,x+dx,top+290),fill='#e7f6ed' if rows[i][VALID] else '#fff0d5')
            if i%4==0:
                dr.line((x,top+35,x,top+290),fill='#cbd3dc');dr.text((x,top+20),str(i),font=small,fill='#546475')
        for ti,(name,col) in enumerate(tracks):
            y=top+58+ti*36;dr.text((20,y-12),name,font=font,fill='#294355');pts=[]
            for i in range(lo,hi):
                assert rows[i][col] in (0,1)
                x=x0+(i-lo)*dx;level=y+(0 if rows[i][col] else 17);pts.extend([(x,level),(x+dx,level)])
            dr.line(pts,fill='#155ba8' if ti<2 else '#ab3c18',width=2)
        y=top+248;dr.text((20,y-6),'EX PC bus',font=font,fill='#294355');i=lo
        while i<hi:
            j=i+1
            while j<hi and rows[j][PC]==rows[i][PC]:j+=1
            x=x0+(i-lo)*dx;end=x0+(j-lo)*dx
            dr.rectangle((x,y-5,end,y+20),outline='#526678')
            if end-x>=50:dr.text((x+4,y-4),'%04x'%rows[i][PC],font=small,fill='#12283c')
            i=j
        x=x0+(anchor-lo)*dx;dr.line((x,top+35,x,top+285),fill='#8b32a8',width=2)
        dr.text((x+4,top+286),'trigger' if anchor==512 else 'event',font=small,fill='#8b32a8')
    dr.text((25,image.height-34),'WDF SHA256 '+a['wdf_sha256']+' | full CSV/JSON retained; displayed subset only',font=small,fill='#465362')
    dest=d/(case+'-waveform.png');assert not dest.exists();image.save(dest)
    return dict(case=case,path=str(dest.relative_to(F)),sha256=hashlib.sha256(dest.read_bytes()).hexdigest().upper(),panels=panels,source_sha256=a['wdf_sha256'],samples_drawn_per_panel=64,clock_scale='Physical sampled clock indices; no independent frequency claim')

if __name__=='__main__':
    results=[render(c) for c in ['list','matrix','state','matrix_repeat']]
    with (F/'WAVEFORM_FIGURES.json').open('x') as f:json.dump(results,f,indent=2)
    print(json.dumps(results,indent=2))
