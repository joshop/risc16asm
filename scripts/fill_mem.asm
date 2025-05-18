.include _common.asm


// a1 <- mask
li a1, 0xf0f0

start:
  // Start address
  li a0, 0xfff0

loop:

  // Flip the bits
  lw a2, 0(a0)
  xor a2, a2, a1

  sw a2, 0(a0)

  addi a0, a0, 1

  // Have we gone too far?
  bz a0, start

  j loop

halt
