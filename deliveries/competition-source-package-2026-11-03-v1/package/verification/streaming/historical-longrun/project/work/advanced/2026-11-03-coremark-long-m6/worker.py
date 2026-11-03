from run_fast import *
capture=json.loads((H/'plans/TERMINAL_CAPTURE.json').read_text())
for rel,digest in capture['sha256'].items():
 if sha(H/rel)!=digest:raise RuntimeError('Terminal-capture input changed')
run_case(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
