from pathlib import Path
import re
def output_size(p):
 try:
   if p.is_file():
    assert not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400,'LINK'
    return p.stat().st_size
 except FileNotFoundError:return 0 # only mutable outputs; protected files checked separately
 return 0
def tree_bytes(root):return sum(output_size(p) for p in Path(root).rglob('*'))
def stages(flow,stdout):
 return dict(compile='Action compile: Real time elapsed' in flow,synthesis='has been successfully synthesized' in flow,mapping='has been successfully mapped' in flow,pnr='has been placed and routed successfully' in flow,timing='Report timing is finished successfully' in flow,bitstream='Generating Programming File done.' in flow and 'Executing : gen_bit_stream -scbv {High Voltage} successfully.' in stdout)
def selftest():
 markers=['Action compile: Real time elapsed','has been successfully synthesized','has been successfully mapped','has been placed and routed successfully','Report timing is finished successfully','Generating Programming File done.']
 out='Executing : gen_bit_stream -scbv {High Voltage} successfully.'
 assert all(stages('\n'.join(markers),out).values())
 for m in markers:assert not all(stages('\n'.join(x for x in markers if x!=m),out).values())
 assert not all(stages('Process "Compile" started.','').values())
 assert not all(stages('Executing : compile','').values())
 # Exercise precisely the FileNotFound branch used by the live walker.
 class Vanished:
  def is_file(self):return True
  def is_symlink(self):return False
  def lstat(self):raise FileNotFoundError()
 assert output_size(Vanished())==0
 class Denied(Vanished):
  def lstat(self):raise PermissionError()
 try:output_size(Denied())
 except PermissionError:pass
 else:raise AssertionError('non-missing error silently ignored')
 return dict(status='PASS_HOST_PREFLIGHT_ONLY',completion_checks=9,mutable_missing_stat_branch='FileNotFoundError only; protected input failures never ignored',native_invocations=0)
