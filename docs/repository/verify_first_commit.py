"""Prepare/audit an explicit first-commit allowlist. NEVER stage/commit/push.
Only audit() makes a disposable empty Git repository under ignored tmp/ to ask
Git's own ignore parser which project paths would be eligible. The real project
is not initialized and no source, credentials or global config is changed.
"""
from pathlib import Path
import sys,json,hashlib,re,subprocess,os,shutil
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'docs/repository';BASE='work/system/2026-10-24-timed-coremark-m1'
MANIFEST='docs/repository/first-commit-files.json'
REPORT=ROOT/'reports/repository-preparation-2026-10-24-v1'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest().upper()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,obj):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
def candidates():
    rows=[]
    def add(path,kind,state):rows.append(dict(path=path,category=kind,state=state))
    for n in ['.gitignore','.gitattributes','README.md',MANIFEST,'docs/repository/verify_first_commit.py',
              'docs/repository/FIRST_COMMIT_SCOPE.md','docs/repository/EXTERNAL_DEPENDENCIES.md']:
        add(n,'repository','本轮新准备；尚未暂存/提交/推送')
    for n in ['cpu.v','alu.v','control.v','regfile.v','uart_tx.v','gpio_core.v','local_regif_txgpio_m1.v',
              'memory_model.sv','cycle_counter64.sv','soc_data_adapter.sv','soc_top.sv']:
        add(BASE+'/source/'+n,'rtl','F136有限软件基线；非PDS/FPGA验收；B整包条件保持')
    for n in ['start.S','link.ld','timer.h','timer_smoke.c']:add(BASE+'/firmware/'+n,'firmware','F136关联输入；原件不改')
    for n in ['core_portme.c','core_portme.h']:add(BASE+'/port/'+n,'platform','F136短运行平台适配；非正式成绩')
    for n in ['tb_timer_unit.sv','tb_timer_unit_v2.sv','tb_timed_system.sv']:
        add(BASE+'/tests/'+n,'tests','F136测试源；unit初版保留，v2为增强版')
    for n in ['run_stage.py','cpu_program_reference.py','peripheral_checker.py','check_timed_v2.py',
              'checker_negative_tests_v2.py','unit_boundary.py','wave_review.py','analyze_windows.py']:
        add(BASE+'/'+n,'workflow','原阶段工具；依赖本地历史/模型，未完成干净克隆移植')
    add(BASE+'/manual-plan.json','expectations','执行前冻结计划；不是新测试结果')
    for n in ['postflight.json','unit-v2-result.json','checker-negative-result-v2.json','quality-window-analysis.json']:
        add(BASE+'/'+n,'evidence','F136选定有限证据；本次未重跑')
    for name in ['baseline-N16','baseline-N234','smoke-N16']:
        add(BASE+'/runs/'+name+'/check-result.json','evidence','F136有限PASS；非硬件')
    for name in ['performance-N16','validation-N16']:
        add(BASE+'/runs/'+name+'/check-result-v2.json','evidence','F136最终检查器v2有限PASS；非正式成绩')
        add(BASE+'/runs/'+name+'/ram-output.txt','evidence','实际RAM报告；不足10秒与Errors detected原样保留')
    add(BASE+'/runs/performance-N16/check-result.json','historical-failure','旧检查器漏BSS阶段0导致FAIL；保留，不覆盖v2当前结论')
    for name in ['smoke-N16','performance-N16','validation-N16']:
        add(BASE+'/runs/'+name+'/wave-review.json','evidence','原VCD窗口检查结果；VCD本体不入仓/非ILA')
    for n in ['2026-10-24-timed-coremark-m1.md','2026-10-24-soc-txgpio-m1-system.md']:
        add('reports/verification/'+n,'report','有限软件验收报告；本地引用不代表文件已随仓分发')
    assert len({x['path'] for x in rows})==len(rows)
    return sorted(rows,key=lambda x:x['path'])
def ignore_text(rows):
    tree={}
    for row in rows:
        node=tree
        for bit in row['path'].split('/'):node=node.setdefault(bit,{})
    out=['# First-commit allowlist. Local originals remain untouched.',
         '# New files need review + manifest update; this is not a secret detector.','/*']
    def walk(node,prefix=''):
        for name,children in sorted(node.items()):
            path=prefix+'/'+name
            if children:out.extend(['!'+path+'/',path+'/*']);walk(children,path)
            else:out.append('!'+path)
    walk(tree)
    out.extend(['','# Defense in depth: never admit authorization, keys, tools or large outputs.',
      '**/*.lic','**/*.LIC','**/*.lic.*','**/license.dat','**/LICENSE.DAT','**/*.pem','**/*.key','**/*.pfx','**/*.p12','**/*.jks',
      '**/.env','**/.env.*','**/.git-credentials','**/id_rsa','**/id_ed25519','**/credentials.json',
      '**/.ssh/','**/.aws/','**/.codex/','**/.agents/',
      '**/GTP_*.v','**/GTP_*.sv','**/*.exe','**/*.dll','**/*.msi','**/*.zip','**/*.7z','**/*.rar','**/*.tar','**/*.gz','**/*.xz',
      '**/*.vvp','**/*.vcd','**/*.fst','**/*.wlf','**/*.elf','**/*.bin','**/*.bit','**/*.sbit','**/*.hex','**/*.map',
      '**/*.pyc','**/__pycache__/','**/init_tables.svh',''])
    return '\n'.join(out)
def original_baseline(rows):
    h=ROOT/BASE;summary=read(h/'summary.json')
    assert summary['status']=='FINITE_TIMED_SOFTWARE_SYSTEM_ACCEPTED_NO_FORMAL_SCORE_OR_HARDWARE'
    frozen={}
    for line in (h/'SHA256SUMS.txt').read_text().splitlines():
        digest,rel=line.split('  ',1);frozen[BASE+'/'+rel]=digest
    for row in rows:
        p=ROOT/row['path']
        if row['path'].startswith(BASE+'/'):
            assert row['path'] in frozen and sha(p)==frozen[row['path']],('changed baseline',row['path'])
    receipt=read(ROOT/'reports/verification/2026-10-24-timed-coremark-m1-receipt.json')
    assert sha(ROOT/'reports/verification/2026-10-24-timed-coremark-m1.md')==receipt['report_sha256']
def prepare():
    assert not (ROOT/'.git').exists(),'real repository exists: re-review before preparing'
    rows=candidates();original_baseline(rows)
    assert not (ROOT/'.gitignore').exists() and not (ROOT/MANIFEST).exists() and not (DOC/'FIRST_COMMIT_SCOPE.md').exists()
    with (ROOT/'.gitignore').open('x',encoding='utf-8') as f:f.write(ignore_text(rows))
    lines=['# 首次提交范围（待确认）','','日期：2026-10-24。远端由用户提供：`https://github.com/minzhetang/pangu-riscv-soc`。',
      '用户报告私有空仓库；本轮没有访问验证、登录或关联远端。Git 2.55.0.windows.3可用，项目不是Git仓库，没有可报告的本地分支/提交/暂存区。',
      '',f'拟提交 **{len(rows)}个明确路径**。保留原工作路径，不移动/改写RTL；逐文件原始SHA-256见first-commit-files.json，自清单不自哈希。',
      '', '## 分层状态', '',
      '当前软件依据F136，CPU/B/官方存储模型未改；有限C/计时/双种子短CoreMark及UART通过。非完整RV32I、正式CoreMark、PDS映射或FPGA验收；B整包条件保持。',
      '首次只保存源码/检查器/少量结果，不承诺干净克隆完整SoC可运行。计时单元独立入口见README，未在本轮重跑。',
      '', '## 排除范围', '',
      '- 全部工具、安装包、专有primitive实现、授权/凭据/机器标识、资料压缩包、照片/历史参赛文件和完整队员交付包。',
      '- CoreMark上游源/许可使用说明作为外部依赖，本次不复制；自有平台适配保留。不要把源码版权声明与PDS机器授权混为一谈。',
      '- 本地AGENTS与.project-memory全历史不入首提，避免未审查的历史个人/环境资料；新公开协作规则需另整理，原件仍在本机。',
      '- build/compile/logs/cases/source-before/port-before/models-before/旧工作目录、安装路径清单、完整波形/原始轨迹/镜像/生成初始化常量不入仓。',
      '', '## 逐文件清单', '', '|路径|类别|证据/限制|','|---|---|---|']
    for row in rows:lines.append('|`'+row['path']+'`|'+row['category']+'|'+row['state']+'|')
    lines.extend(['','## 本轮动作边界','',
      '仅准备文件和清单；不在项目根初始化Git，不暂存/提交/设置远端/推送，不读取Git用户名邮箱、凭据库、SSH私钥或授权文件。',
      '审计可在忽略的tmp内创建一次性空Git仓库，只调用Git自身的ignore解析/未跟踪清单，不进行任何网络访问或提交。',
      '首推前重新展示精确暂存范围并由用户确认；禁止git add -f或笼统将整个工作树强行纳入。ignore不保护已经跟踪的文件。',
      '本轮无需登录；未来如GitHub确实要求认证，使用官方交互式登录，由用户在官方页面完成，不向聊天提供密码、令牌或验证码。',
      'over_temp停止保持。'])
    with (DOC/'FIRST_COMMIT_SCOPE.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    for row in rows:
        p=ROOT/row['path']
        if row['path']==MANIFEST:row.update(bytes=None,sha256=None,note='self manifest has no recursive self hash')
        else:row.update(bytes=p.stat().st_size,sha256=sha(p))
    save(ROOT/MANIFEST,dict(version=1,date='2026-10-24',status='PROPOSED_NOT_STAGED_OR_COMMITTED',
      remote_user_provided='https://github.com/minzhetang/pangu-riscv-soc',remote_verified=False,
      source_baseline='F136 finite timed software; no synthesis/hardware acceptance',file_count=len(rows),
      bytes_excluding_manifest=sum(x['bytes'] or 0 for x in rows),files=rows,
      excluded=['authorizations/credentials/machine identifiers','tools and installers','Pango proprietary implementations',
        'CoreMark upstream files external','board/problem/photos/old deliveries','local agent memory/history','large or generated artifacts']))
    print(json.dumps(dict(prepared=len(rows),bytes_excluding_manifest=sum(x['bytes'] or 0 for x in rows),actual_project_git_initialized=False)))
PATTERNS=[('private_key',r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
 ('github_token',r'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{30,})\b'),
 ('credential_url',r'https?://[^\s/@]+:[^\s/@]+@'),
 ('secret_assignment',r'(?im)^\s*["\']?(?:password|passwd|access_token|client_secret|api_key)["\']?\s*[:=]\s*["\'][^"\'\r\n]{12,}["\']'),
 ('machine_MAC',r'\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b'),
 ('machine_identity_value',r'(?im)^\s*(?:HOSTID|MachineGuid|ComputerUUID|machine_code)\s*[:=]\s*\S+'),
 ('authorization_body',r'(?m)^\s*(?:FEATURE|INCREMENT|SERVER|DAEMON)\s+\S+\s+\S+'),
 ('vendor_module_definition',r'(?m)^\s*module\s+(?:GTP_|PANGO_)\w+'),
 ('encrypted_vendor_source',r'(?m)^\s*`pragma\s+protect')]
def audit():
    m=read(ROOT/MANIFEST);rows=m['files'];assert rows==sorted(rows,key=lambda x:x['path'])
    original_baseline(rows);findings=[]
    for row in rows:
        p=ROOT/row['path'];assert p.is_file() and not p.is_symlink()
        if row['sha256']:assert sha(p)==row['sha256'],row['path']
        assert p.stat().st_size<=1024*1024,('too large',row['path'])
        text=p.read_text(encoding='utf-8-sig');assert '\x00' not in text
        for rule,pattern in PATTERNS:
            for hit in re.finditer(pattern,text):findings.append(dict(path=row['path'],line=text.count('\n',0,hit.start())+1,rule=rule))
    REPORT.mkdir(exist_ok=False)
    # Findings contain locations/rules only, NEVER matched secret values.
    save(REPORT/'content-scan.json',dict(heuristic_only=True,selected_files=len(rows),findings=findings))
    if findings:raise RuntimeError('Content scan findings: inspect locations locally; do not stage')
    git=shutil.which('git');assert git
    scratch=ROOT/'tmp/repo-ignore-check-20261024-v1';assert not scratch.exists();scratch.parent.mkdir(exist_ok=True)
    env=os.environ.copy();env.update(GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
    def run(args,input=None):
        p=subprocess.run([git,*args],cwd=ROOT,input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=30)
        assert p.returncode in [0,1],('Git parser failure',p.returncode,p.stderr.decode('utf-8',errors='replace'))
        return p
    run(['-c','init.templateDir=','-c','core.hooksPath=','init','--quiet','--initial-branch=main',str(scratch)])
    prefix=['--git-dir='+str(scratch/'.git'),'--work-tree='+str(ROOT),'-c','core.fsmonitor=false','-c','core.excludesFile='+os.devnull,'-c','core.quotePath=false']
    wanted={x['path'] for x in rows}
    probes=['tools/iverilog/bin/iverilog.exe','modelsim/anything.exe','.project-memory/FACTS.md','AGENTS.md',
      'deliveries/anything.zip','reports/anything.log','work/other/source/cpu.v','README.future.md',
      BASE+'/source/PANGO_LICENSE_FILE.lic',BASE+'/source/license.lic.backup',BASE+'/source/license.dat',
      BASE+'/source/LICENSE.LIC',BASE+'/source/client.key',BASE+'/source/GTP_DRM18K_E1.v',
      BASE+'/source/new_unreviewed_module.sv',BASE+'/source/init_tables.svh',BASE+'/compile/a.vvp',
      BASE+'/runs/performance-N16/wave.vcd',BASE+'/build/program.elf','.env','.git-credentials','credentials.json',
      'photos/board.png','docs/repository/secrets.pem','work/system/2026-10-24-timed-coremark-m1/upstream/core_main.c']
    paths=sorted(wanted)+probes
    proc=run(prefix+['check-ignore','--no-index','-z','--stdin'],('\0'.join(paths)+'\0').encode())
    ignored=set(proc.stdout.decode('utf-8').strip('\0').split('\0')) if proc.stdout else set()
    assert not wanted&ignored,('candidate unexpectedly ignored',sorted(wanted&ignored))
    assert set(probes)<=ignored,('unsafe/unreviewed path visible',sorted(set(probes)-ignored))
    ls=run(prefix+['ls-files','--others','--exclude-standard','-z'])
    visible=set(ls.stdout.decode('utf-8').strip('\0').split('\0')) if ls.stdout else set()
    assert visible==wanted,dict(unexpected=sorted(visible-wanted),missing=sorted(wanted-visible))
    assert not (ROOT/'.git').exists(),'real project Git metadata unexpectedly created'
    result=dict(status='PASS_PREPARATION_ONLY',file_count=len(rows),total_bytes=sum((ROOT/x['path']).stat().st_size for x in rows),
      categories={k:sum(x['category']==k for x in rows) for k in sorted({x['category'] for x in rows})},
      git_visible_set_exact=True,ignore_positive_controls=len(wanted),ignore_negative_controls=len(probes),
      content_scan='heuristic patterns: 0 findings; not a guarantee of absence',
      real_project_git_initialized=False,staged=False,committed=False,remote_accessed=False,pushed=False,
      manifest_sha256=sha(ROOT/MANIFEST),gitignore_sha256=sha(ROOT/'.gitignore'),
      isolated_empty_git_parser=str(scratch.relative_to(ROOT)),hardware='STOP')
    save(REPORT/'audit-result.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');{'prepare':prepare,'audit':audit}[sys.argv[1]]()
