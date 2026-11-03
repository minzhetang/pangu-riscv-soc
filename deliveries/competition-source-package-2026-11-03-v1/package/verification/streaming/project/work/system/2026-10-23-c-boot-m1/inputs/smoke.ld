/* Isolated toolchain smoke layout only: no approved SoC/MMIO mapping. */
OUTPUT_ARCH(riscv)
ENTRY(_start)
MEMORY {
    ROM (rx)  : ORIGIN = 0x00000000, LENGTH = 16K
    RAM (rw)  : ORIGIN = 0x00010000, LENGTH = 16K
}
SECTIONS {
    .text : { KEEP(*(.text.start)) *(.text .text.*) *(.rodata .rodata.*) . = ALIGN(4); } > ROM
    .data : ALIGN(4) {
        __data_start = .; *(.sdata .sdata.*) *(.data .data.*) . = ALIGN(4); __data_end = .;
    } > RAM AT> ROM
    __data_load = LOADADDR(.data);
    __global_pointer$ = ORIGIN(RAM) + 0x800;
    .bss (NOLOAD) : ALIGN(4) {
        __bss_start = .; *(.sbss .sbss.*) *(.bss .bss.*) *(COMMON) . = ALIGN(4); __bss_end = .;
    } > RAM
    __stack_top = ORIGIN(RAM) + LENGTH(RAM);
    ASSERT(__bss_end + 1024 < __stack_top, "smoke RAM leaves stack space")
    /DISCARD/ : { *(.comment) *(.note.GNU-stack) }
}
