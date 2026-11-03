.section .text.start,"ax"
.globl _start
_start:
 lui sp,8
 la t0,__bss_start
 la t1,__bss_end
1: bgeu t0,t1,2f
 sw zero,0(t0)
 addi t0,t0,4
 j 1b
2: call main
 lui t0,3
 sw a0,28(t0)
 lui t1,0x600d6
 addi t1,t1,13
 sw t1,32(t0)
3: j 3b
