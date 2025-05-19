// No-op
.macro nop
addi r0, r0, 0
.endmacro

// Move
.macro mv (\w+), (\w+)
add \1, r0, \2
.endmacro

// Load immediate
.macro li (\w+), (.+)
lui \1, (((\2) >> 8) + ((\2 & 0xff) >> 7)) & 0xff
addi \1, \1, (\2) & 0xff
.endmacro

// Logical things
// Not (flip all bits)
.macro not (\w+), (\w+)
nand \1, \2, \2
.endmacro

// And immediate
.macro andi (\w+), (\w+), (.+)
nandi \1, \2, \3
neg \1, \1
.endmacro

// And register
.macro and (\w+), (\w+), (\w+)
nand \1, \2, \3
neg \1
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
