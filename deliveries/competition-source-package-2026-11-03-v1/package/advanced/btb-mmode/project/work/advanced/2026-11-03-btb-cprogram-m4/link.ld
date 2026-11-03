ENTRY(_start)
SECTIONS {
 . = 0; .text : { *(.text.start) *(.text*) *(.rodata*) }
 ASSERT(. < 0x2000,"ROM overflow")
 . = 0x4000; __bss_start = .; .bss (NOLOAD) : { *(.bss*) *(COMMON) } __bss_end = .;
 ASSERT(. < 0x7000,"RAM overflow")
 /DISCARD/ : { *(.comment) *(.riscv.attributes) }
}
