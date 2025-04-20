// No-op
.macro nop
addi r0, r0, 0
.endmacro

// Load immediate
.macro li (\w+), (\w+)
lui \1, ((\2) >> 8) + ((\2 & 0xff) >> 7)
addi \1, \1, (\2) & 0xff
.endmacro

// Jump unconditionally
.macro j (\w+)
bz r0, \1
.endmacro

// Jump and link
.macro jal|call (\w+)
li ra, \1
jalr ra, ra
.endmacro

// Return to ra
.macro ret
jalr r0, ra
.endmacro

// Halt
.macro halt
.word 0b00100_000_00000000
.endmacro
