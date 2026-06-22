.include ../_common.asm

// Display driver
// Read from frame buffer and manipulate IO to make image
// args:
//    a0: address of frame buffer

.def C0, 0x4000

draw_frame:
  // Save registers onto stack
  addi sp, sp, -6
  sw ra, 0(sp)
  sw a0, 1(sp)
  sw a1, 2(sp)
  sw a2, 3(sp)
  sw a3, 4(sp)
  sw a4, 5(sp)

  mv a4, a0               // a4 <- frame buffer base address
  li a1, 93
  add a1, a1, a4          // a1 <- current frame buffer word
  
  li a0, C0               // a0 <- C0 (IO base)
  li a3, C0 + 4           // a3 <- Rx (row memory base)

  // Initialize row outputs
  li a2, 0xffff           // top half blank
  sw a2, 3(a0)
  li a2, 0x7fff           // a2 <- row word
  sw a2, 4(a0)

  // Neg version woohoo
  not a2, a2

  // Go through the pixels backwards
  dd_loop_outer:
    li a4, 0xffff
    sw a4, 0(a3)

    // COL WORD 2
    lw a4, 2(a1)
    sw a4, 2(a0)

    // COL WORD 1
    lw a4, 1(a1)
    sw a4, 1(a0)

    // COL WORD 0
    lw a4, 0(a1)
    sw a4, 0(a0)

    // Move buffer index
    addi a1, a1, -3
    
    // Shift to previous row
    dd_shift_row:
      sr a2, a2, 1
      not a2, a2
      sw a2, 0(a3)        // Write to row word
      not a2, a2

    // If index == 0, end
    // a4 <- FBUF (saved at 1(sp))
    lw a4, 1(sp)
    sub a1, a1, a4
    bz a1, dd_end
    add a1, a1, a4

    // Are we good? (i.e. didn't shift out of range)
    bnz a2, dd_loop_outer

    // Shifted out of range (set previous row)
    // ASSERTION: this executes only when we get to the upper half of display
    li a2, 0xffff
    sw a2, 4(a0)          // Reset lower half of screen
    li a2, 0x7fff
    sw a2, 3(a0)          // Reset upper half of screen
    not a2, a2            // Reset to negated version
    addi a3, a0, 3        // Reset row address to write to to be 3(C0)

    j dd_loop_outer

  dd_end:
    // Pop back from stack and return
    lw ra, 0(sp)
    lw a0, 1(sp)
    lw a1, 2(sp)
    lw a2, 3(sp)
    lw a3, 4(sp)
    lw a4, 5(sp)
    addi sp, sp, 6

    ret
