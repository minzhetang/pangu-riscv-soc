"""Software-only startup path bound before first external GPIO_IN read."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
from cpu_program_reference import Reference
h=Path(__file__).resolve().parent
class FirstInputRead(Exception):pass
state={'gpio':0}
def read(pc,address):
    if address==0x2000000c:return state['gpio']
    assert address==0x20000010,('unexpected early IO',pc,address)
    raise FirstInputRead
def write(pc,address,value,mask):
    assert address==0x2000000c and mask==15
    state['gpio']=value&255
r=Reference((h/'build/soc.bin').read_bytes(),read,write)
try:
    while not r.stopped:r.step()
except FirstInputRead:pass
else:raise AssertionError('first input read not reached')
# Pessimistic allowance: each instruction <=1 ordinary+1 load-use+2flush
# logical steps, and2 physical edges per logical step, plus16 fill/drain.
bound=2*(4*r.steps+16)
assert 2*r.steps>18 and bound<4096
out=dict(status='PASS_SOFTWARE_BOUND_NOT_DUT',architectural_steps_to_first_GPIO_IN=r.steps,
    first_input_read_pc=r.pc,pessimistic_physical_bound=bound,GPIO_changes_before_edges=[16,4096],
    assumptions=['CPU is F130 fixed two-edge mode, no variable waits',
        'at most one load-use and two flush bubbles per instruction; fixed fill allowance',
        'no earlier external-dependent IO or interrupt'],DUT_runs=0,
    note='timing plan frozen before DUT; unexpected dynamic behavior must fail, not retime stimulus to fit')
with (h/'gpio-stimulus-bound.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps(out))
