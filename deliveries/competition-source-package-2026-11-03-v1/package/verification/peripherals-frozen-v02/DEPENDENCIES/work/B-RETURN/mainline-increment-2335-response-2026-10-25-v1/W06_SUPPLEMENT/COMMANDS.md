# A主线W06补证，B无需重复开发或重跑

本目录已提供原合同N16/N234的主线实际新波形、原生运行日志和结果；tb_w06_boundary_v2.sv是A自写的独立验证，不修改B原TB/RTL。主线使用Icarus/vvp13.0显式路径、-B和VPI库，编译每项60s、运行30s，TB最多12000物理沿。完整实跑argv/cwd/rc/耗时在RESULTS.json两配置compile_process/run_process；外部权限仅当时本批有效，不随文件转授权。

输入沿用已收wrapper/TX/GPIO SHA：5C81EE8F...64FA / 21044928...988C / 03380919...F95E。两次试验分别验证：完成沿E+10N沿前ready仍0→拒绝一次脉冲且不排队；另一轮在E+10N+1接受新请求。每配置4次TX接受/2次拒绝/0GPIO副作用，连续引脚与独立合同模型均一致。

如果未来另获执行许可需复现，参数顺序必须将所有选项置于源文件前：iverilog -B <ivl-lib> -g2012 -Wall -s tb_w06_boundary -DCLKS_PER_BIT=<16或234> -o <新输出.vvp> <已核wrapper.v> <已核uart_tx.v> <已核gpio_core.v> <本目录TB.sv>；vvp -N -M- -M<ivl-lib> <新输出.vvp> +WAVE_FILE=<新输出.vcd>。现阶段B只需在最终coverage_map中引用本补证ID/版本/SHA，不追改其旧1.0.3计划或声称其原run已覆盖。
