// The meaty test
.include ../_common.asm
.def C0, 0x4000

// Initialize stack ptr
li sp, 0xffff

// Reset everything to zero
li a0, C0
sw zero, 0(a0)
sw zero, 1(a0)
sw zero, 2(a0)
sw zero, 3(a0)
sw zero, 4(a0)

// Address of frame to draw
start:
  li a0, FBUF
  li a1, (FBUF + 96*256)

loop:
  // draw_frame(FBUF)
  call draw_frame
  ecall 1

  // FBUF += 96 (next frame)
  addi a0, a0, 96

  // Are we at the end?
  sub a0, a0, a1
  bp a0, start
  add a0, a0, a1

  j loop

end:
  halt


// Libraries and stuff
.include display_driver.asm

// Frame buffer lives here
// 48x32 is 48x2 words = 96 words
.addr 0x5000
FBUF:
  // .bin bad_apple/badapple.bin
  .bin bad_apple/badapple.bin
