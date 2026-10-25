# 本轮执行与复现入口

2026-10-25，D137只读分析。没有iverilog/vvp、GCC、PDS或硬件命令；0新DUT，0顺序模型重放。解析器5正/3负合成检查不计CPU用例。

实际统计入口（普通用户PowerShell，不改PATH）：

```powershell
& 'C:\Users\tamii\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'D:\A_FPGA_Comp\work\analysis\2026-10-25-control-flow-quality-m0\analyze.py'
```

程序原生rc=0；27个输入前后SHA核同，摘要/逐PC表已生成。程序用exclusive create保护历史结果，不能在同目录盲重跑；复现应使用独立新分析目录并保留基线绝对路径。没有运行旧产物冒充新执行。

`SUMMARY.json`存旧DUT再分析结果，`INPUTS.json`存所有统计输入/大小/SHA，两个`*-by-pc.json`存223个控制流地址的编码/函数/次数/实际后继/间隔。

另一次普通Python只读核对，rc=0：两个反汇编用正则逐项取出`address: word`和函数头，与原bin的little-endian机器字及`build-result.json/artifacts/symbols`核对，并核逐PC表的executions/taken之和等于摘要。各3454个机器字、46个标签通过；结果为`disassembly-check.json`，0编译/模型/DUT。该核对不是新的CPU验证。

核对核心逻辑：

```python
words = re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+', disassembly, re.M)
assert all(int.from_bytes(image[int(pc,16):int(pc,16)+4], 'little') == int(word,16)
           for pc, word in words)
labels = re.findall(r'^([0-9a-f]+) <([^>]+)>:', disassembly, re.M)
assert all(symbols[fn] == int(pc,16) for pc, fn in labels)
assert sum(r['executions'] for r in by_pc.values()) == counts['controls']
assert sum(r['taken'] for r in by_pc.values()) == counts['redirects']
```

源码行号/时序推演见报告，候选实施仅在`NEXT_IMPLEMENTATION_SCOPE.md`列范围，未执行。原始证据、CPU/TB/模型/镜像/预期及B包没有写操作；没有新位流、波形采集、设备/服务器或许可证动作。
