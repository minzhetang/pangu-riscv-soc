/* Standalone tool smoke linker layout; not a mainline SoC memory map. */
.section .text.start,"ax",@progbits
.globl _start
.type _start,@function
_start:
    .option push
    .option norelax
    la sp, __stack_top
    la gp, __global_pointer$
    la a0, __data_load
    la a1, __data_start
    la a2, __data_end
    .option pop
1:  bgeu a1, a2, 2f
    lw t0, 0(a0)
    sw t0, 0(a1)
    addi a0, a0, 4
    addi a1, a1, 4
    jal zero, 1b
2:  .option push
    .option norelax
    la a1, __bss_start
    la a2, __bss_end
    .option pop
3:  bgeu a1, a2, 4f
    sw zero, 0(a1)
    addi a1, a1, 4
    jal zero, 3b
4:  call main
    ebreak
5:  jal zero, 5b
.size _start, .-_start
