"""Record hashes and finite post-loop quality metrics from existing results only."""
import json
from prepare_and_build import HERE,ROOT,item,save,verify
from check_and_run import frozen_verify

def main():
    verify(); original=json.loads((HERE/'result.json').read_text())
    revised=json.loads((HERE/'wave-v2-result.json').read_text())
    assert original['status']==revised['status']=='PASS'
    metrics={}
    for case,result in original['cases'].items():
        m=result['metrics']; ex=result['actual_streams']['counts']['EX']
        cycles=int(m['cycles']); flush=int(m['flush']); stall=int(m['stall'])
        assert cycles==ex+2*flush+stall+7
        metrics[case]={'active_cycles':cycles,'EX_non_EBREAK':ex,'redirect_bubbles_model_accounting':2*flush,
                       'load_use_stalls':stall,'initial_fill_and_EEI_observation':7,
                       'EX_slot_utilization':ex/cycles,'cycles_per_EX_NOT_retirement_CPI':cycles/ex,
                       'scope':'Whole startup+benchmark+RAM formatting, NOT timed CoreMark kernel or FPGA performance'}
    save(HERE/'quality-metrics.json',metrics)
    records=[]
    for p in HERE.rglob('*'):
        if p.is_file() and p.name not in ['SHA256SUMS.json','handoff-result.json']:
            records.append(item(p))
    save(HERE/'SHA256SUMS.json',records)
    save(HERE/'handoff-result.json',{
        'stage':'A-COREMARK-CORRECTNESS-M1','status':'FINITE_CRC_AND_TRACE_PASS',
        'two_original_parameter_runs':'result.json','original_wave_window_gap':'wave-window-review.json',
        'capture_only_corrected_performance_run':'wave-v2-result.json','quality':'quality-metrics.json',
        'CPU_RTL_changes':0,'frozen_input_checks':frozen_verify(),'protected_upstream_and_prior_M1_records':33,
        'source_and_old_evidence_changes':[],'new_firmware_images':2,'ordinary_vvp_runs':3,
        'external_compile_permissions_consumed':2,'normal_Icarus_compile_fault_root_cause':'UNRESOLVED',
        'formal_CoreMark_score':'NOT_MEASURED_TIMER_UNAVAILABLE','system_integration':'NOT_RUN','FPGA':'NOT_RUN',
        'over_temp_hardware_stop':'UNCHANGED','hardware_operations':0,
        'limits':['fixed initial RF zeros','zero-wait behavioral ROM/RAM, not FPGA BRAM',
                  'no true retirement PC','separate WB vs memory streams, no unified commit order',
                  'VCD startup + performance stop windows; not full kernel waveform or ILA',
                  'validation stop wave not re-run; functional stop guards and full streams matched',
                  'timer unavailable, upstream minimum-duration error intentionally retained']})
    print(json.dumps(json.loads((HERE/'handoff-result.json').read_text()),indent=2))

if __name__=='__main__': main()
