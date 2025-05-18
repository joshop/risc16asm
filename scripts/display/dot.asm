// Make a thing move across the screen
.include ../_common.asm

.def C0, 0x4000
.def C1, 0x4001
.def C2, 0x4002
.def R0, 0x4003
.def R1, 0x4004

// Reset everything to zero
li a0, C0
sw zero, 0(a0)
sw zero, 1(a0)
sw zero, 2(a0)
sw zero, 3(a0)
sw zero, 4(a0)
sw zero, 5(a0)

halt
