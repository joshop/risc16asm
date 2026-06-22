.include _common.asm

start:
  li a0, 0xf000

loop:
  // Flip the bits
  li a2, 0xffff

  sw a2, 0(a0)

  addi a0, a0, 1

  // Have we gone too far?
  bz a0, start

  j loop

halt
