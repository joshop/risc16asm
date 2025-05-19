.macro li (r[0-7]), (\w+)
lui \1, (\2) >> 8
addi \1, \1, (\2) & 0xff
.endmacro

.macro halt
.word 0b00100_000_00000000
.endmacro

.addr 0
main:
  li r3, myfunction
  jalr r0, r3

.addr 0x1234
myfunction:
  .word 0b00100_000_00000000
