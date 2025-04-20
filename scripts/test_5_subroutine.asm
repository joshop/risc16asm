.include ./_common.asm

// Add a bunch of numbers
li a0, 100
li a1, 200
call add

halt

nop

add:
  // a0 <- x
  // a1 <- y
  add a0, a0, a1
  ret
