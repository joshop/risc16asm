.include _common.asm

// a4 <- end address
li a4, (-(0x4007) & 0xffff)

// a1 <- mask
li a1, 0xffff

start:
  // Start address
  li a0, 0x4000

loop:

  // Flip the bits
  lw a2, 0(a0)
  // xor a2, a2, a1
  // addi a2, a2, 1
  xor a2, a2, a0
  addi a2, a2, 1

  sw a2, 0(a0)

  addi a0, a0, 1

  // Have we gone too far?
  add a3, a0, a4
  bz a3, start

  j loop

halt
