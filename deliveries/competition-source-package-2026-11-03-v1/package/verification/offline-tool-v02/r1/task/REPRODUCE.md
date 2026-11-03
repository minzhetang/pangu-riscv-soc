# A反例复现 / 不改原件

使用已有Python标准库。先将v01的RUN.py、src/worker.py、src/support.py及frozen两文件按原相对路径复制到**全新独立测试副本**。不要在原v01或正式输入包内故意制造输出。

下述 TOOL_COPY/INPUT_PACKAGE/NEW_OUT用本机路径替换并加引号；INPUT_PACKAGE是原mainline-b-verify-offline-m0-2026-10-26-v1，CASE使用本包对应JSON，普通NEW_OUT放在工具和输入包之外，必须不存在：

```text
python -B "TOOL_COPY/RUN.py" --case-file "TASK/C0-default.json" --input-root "INPUT_PACKAGE" --out "NEW_OUT/C0"
python -B "TOOL_COPY/RUN.py" --case-file "TASK/C1-worker-memory.json" --input-root "INPUT_PACKAGE" --out "NEW_OUT/C1"
python -B "TOOL_COPY/RUN.py" --case-file "TASK/C2-result-size.json" --input-root "INPUT_PACKAGE" --out "NEW_OUT/C2"
python -O -B "TOOL_COPY/RUN.py" --case-file "TASK/C3-optimized-protected-output.json" --input-root "INPUT_PACKAGE" --out "TOOL_COPY/forbidden-output-probe"
```

每条记录实际进程rc和新文件大小、内存观测；C3执行前后对复制工具树作清单对照。A实测见COUNTEREXAMPLES。不要只看JSON的native_rc，不能修改预期使旧反例通过。上面没有执行仿真器、编译器或硬件。

新v02用相同输入/预期重跑，C0保持MATCH；C1为LIMIT5；C2为LIMIT5且不写超限文件（容量不足可无结果文件）；C3为INVALID_INPUT3且受保护树不变化。其余矩阵见TASK。
