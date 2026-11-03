OUTPUT_ARCH(riscv)
ENTRY(_start)
MEMORY {
    ROM (rx) : ORIGIN = 0x00000000, LENGTH = 32K
    RAM (rw) : ORIGIN = 0x00010000, LENGTH = 32K
}
SECTIONS {
    .text : { KEEP(*(.text.start)) *(.text .text.*) . = ALIGN(4); } > ROM
    .rodata : ALIGN(4) { *(.rodata .rodata.*) . = ALIGN(4); } > ROM
    .data : ALIGN(4) {
        __data_start = .; *(.sdata .sdata.*) *(.data .data.*) . = ALIGN(4); __data_end = .;
    } > RAM AT> ROM
    __data_load = LOADADDR(.data);
    __global_pointer$ = ORIGIN(RAM) + 0x800;
    .bss (NOLOAD) : ALIGN(4) {
        __bss_start = .; *(.sbss .sbss.*) *(.bss .bss.*) *(COMMON) . = ALIGN(4); __bss_end = .;
    } > RAM
    __stack_top = ORIGIN(RAM) + LENGTH(RAM);
    __stack_bottom = __stack_top - 8192;
    ASSERT(__bss_end<=__stack_bottom,"program RAM overlaps reserved 8K stack")
    ASSERT(LOADADDR(.data)+SIZEOF(.data)<=ORIGIN(ROM)+LENGTH(ROM),"ROM overflow")
    /DISCARD/ : { *(.comment) *(.note.GNU-stack) }
}
