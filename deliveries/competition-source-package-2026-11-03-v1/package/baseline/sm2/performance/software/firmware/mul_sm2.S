.section .text.__mulsi3,"ax",@progbits
.align 2
.globl __mulsi3
.type __mulsi3,@function
__mulsi3:
    srai a3,a1,31
    xor a1,a1,a3
    sub a1,a1,a3
    addi a2,a0,0
    addi a0,zero,0
1:
    andi a4,a1,1
    beq a4,zero,2f
    add a0,a0,a2
2:
    srli a1,a1,1
    slli a2,a2,1
    andi a4,a1,1
    beq a4,zero,3f
    add a0,a0,a2
3:
    srli a1,a1,1
    slli a2,a2,1
    bne a1,zero,1b
    xor a0,a0,a3
    sub a0,a0,a3
    jalr zero,0(ra)
.size __mulsi3,.-__mulsi3
