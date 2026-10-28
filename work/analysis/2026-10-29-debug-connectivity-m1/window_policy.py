"""Pure policy: no Windows calls or vendor execution. A missing main window is not an error."""
def decide(request,rows):
 if any(r['role']=='REJECT' for r in rows):return 'STOP_UNKNOWN_DIALOG'
 if request['role']=='main' and any(r['role']=='reminder' for r in rows):return 'WAIT_REMINDER'
 matches=[r for r in rows if r['role']==request['role']]
 if not matches:return 'WAIT_ROLE'
 if len(matches)!=1:return 'STOP_AMBIGUOUS_ROLE'
 row=matches[0]
 if request['op'] in ['click','source','capture'] and row.get('minimized',False):return 'WAIT_RESTORE'
 if request['op'] in ['click','source'] and row['client_size']!=request['expected_client_size']:return 'STOP_GEOMETRY_CHANGED'
 return 'EXECUTE'
