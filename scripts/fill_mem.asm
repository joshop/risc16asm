.include _common.asm

li a0, 100
li a1, 0xfff0

loop:
  sw a1, 0(a0)
  addi a0, a0, 1
  j loop

halt
