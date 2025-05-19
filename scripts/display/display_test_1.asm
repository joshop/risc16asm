.include ../_common.asm

// Base memory address
li a0, 0x4000

// First column: filled
li a1, 0xffff
sw a1, 0(a0)

// Second column: blank
li a1, 0x0000
sw a1, 1(a0)

// Third column: half fileld
li a1, 0xaaaa
sw a1, 2(a0)

// First row: filled
sw zero, 3(a0)

// Second row: half filled
li a1, 0xf0f0
sw a1, 4(a0)

halt
