.macro li (r[0-7]), (\w+)
lui \1, (\2) >> 8
addi \1, \1, (\2) & 0xff
.endmacro

.macro halt
.word 0b00100_000_00000000
.endmacro

.addr 0
li r3, 3
