"""Extra EX/edge evidence only; no new native or sequential-model execution."""
import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(r'D:\A_FPGA_Comp');D=ROOT/'work/icarus/2026-10-21-cpu-shifti-reject';P='tb_cpu_selfcheck_v1.dut.';T='tb_cpu_selfcheck_v1.'
sp=importlib.util.spec_from_file_location('shift_ex_vcd',ROOT/'scripts/verification/cpu_bgeu_evidence.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
    assert not (D/'runs-v2/EX-review.json').exists()
    p=read(D/'validation-v2/plan.json');r=read(D/'runs-v2/result.json')
    old={c['id'].replace('SC','SM',1):c for c in read(ROOT/'work/icarus/2026-10-21-shifti-v0/manual-plan.json')['cases']}
    rows=[]
    for c,row in zip(p['cases'][717:],r['cases'][717:]):
        assert c['id']==row['id'];wave=Path(row['wave']['path']);assert v.sha(wave)==row['wave']['sha256']
        edges,n,last=v.vcd_edges(wave);words={i['pc']:int(i['word'],16) for i in c['instructions']};hits=[];candidate=[];branch=[]
        for cy,(tick,pre,post) in enumerate(edges,1):
            if not n(pre,P+'id_valid'):continue
            pc=n(pre,P+'id_pc');word=words[pc];op=word&127;f3=(word>>12)&7;f7=word>>25
            shift_bad=op==0x13 and ((f3==1 and f7!=0) or (f3==5 and f7 not in (0,32)))
            if shift_bad:
                s=dict(cycle=cy,EX_pc=pc,word=f'{word:08x}',high7=f7,funct3=f3,
                    tag=n(pre,P+'id_system_kind'),detect=n(pre,P+'eei_detect'),ctrl=n(pre,P+'id_alu_ctrl'),
                    a=n(pre,P+'alu_src1'),b=n(pre,P+'alu_src2'),result=n(pre,P+'alu_result'),zero=n(pre,P+'alu_zero'),
                    post_ex_valid=n(post,P+'ex_valid'),post_ex_reg_write=n(post,P+'ex_reg_write'),post_ex_mem_write=n(post,P+'ex_mem_write'))
                assert s['tag']==3 and s['detect']==1 and s['ctrl']==0
                assert s['zero']==int(s['result']==0) and s['post_ex_valid']==s['post_ex_reg_write']==s['post_ex_mem_write']==0
                assert c['expected_stop']==dict(pc=pc,kind=3)
                hits.append(s)
            if c['id'] in old and pc==old[c['id']]['candidate_pc']:
                original=old[c['id']]
                assert word==int(original['candidate_word'],16)
                s=dict(cycle=cy,pc=pc,word=f'{word:08x}',a=n(pre,P+'alu_src1'),b=n(pre,P+'alu_src2'),result=n(pre,P+'alu_result'),ctrl=n(pre,P+'id_alu_ctrl'))
                assert s['a']==int(original['expected_a'],16) and s['b']==int(original['expected_b'],16)
                assert s['result']==int(original['manual_expected_ALU'],16) and s['ctrl']==original['expected_ctrl']
                if original['category']=='LEGAL_CONTROL':assert n(pre,P+'id_system_kind')==n(pre,P+'eei_detect')==0
                candidate.append(s)
            if c['id']=='SM13_wrongpath' and pc==8:
                assert n(pre,P+'branch_taken')==n(pre,P+'flush_if')==1
                assert n(pre,P+'branch_target')==n(post,T+'pc')==20
                assert n(post,P+'id_reg_write')==n(post,P+'if_valid')==n(post,P+'id_valid')==0
                branch.append(dict(cycle=cy,EX_pc=8,target=20,post_pc=20))
        stop=c['expected_stop'];event_word=words[stop['pc']] if stop else None
        bad_stop=event_word is not None and event_word&127==0x13 and (event_word>>12)&7 in (1,5)
        assert len(hits)==int(bad_stop)
        if c['id'] in old:assert len(candidate)==old[c['id']]['candidate_expected_EX']
        if c['id']=='SM13_wrongpath':assert len(branch)==1
        rows.append(dict(id=c['id'],status='PASS_FINITE_EX_CHECK',nonbase_hits=hits,F107_same_word_EX=candidate,branch=branch))
    out=dict(date='2026-10-21',reference='F-108/D-095',status='PASS_FINITE_SHIFTI_TAG_AND_KILL',new_cases=46,
        rows=rows,nonbase_detects=sum(len(c['nonbase_hits']) for c in rows),F107_same_words_checked=13,
        native_or_model_calls=0,not_all_253_fields=True,ALU_control_codes_unchanged=True,hardware_stop_unchanged=True)
    with (D/'runs-v2/EX-review.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
    print('EX PASS',out['nonbase_detects'],'nonbase detection/kill samples;13 F107 contexts;no new DUT/model calls')
if __name__=='__main__':main()
