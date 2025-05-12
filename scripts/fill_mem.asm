.include _common.asm

li a0, 0xfff0

// a1 <- mask
li a1, 0xf0f0

loop:
  // Flip the bits
  lw a2, 0(a0)
  // xor a2, a2, a1
  addi a2, a2, 1

  sw a2, 0(a0)

  addi a0, a0, 1
  j loop

halt
