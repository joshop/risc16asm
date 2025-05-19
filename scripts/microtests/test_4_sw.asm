.macro halt
.word 0b00100_000_00000000
.endmacro

addi sp, r0, -1
addi sp, sp, -16

addi a0, r0, 1
sw a0, 4(sp)

addi a0, r0, 0xff
lw a0, 4(sp)

.word 0b00100_000_00000000
