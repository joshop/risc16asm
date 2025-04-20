.include _common.asm

// Initialize sp
li sp, 0xffff

// LOAD CONSTANTS
li a0, 10321

call is_prime
halt

// mod(x, y) -> x % y
// a0 <- x
// a1 <- y
// Return x % y in a0
// does NOT modify a1
mod:
  sub a0, a0, a1

  // if (x < 0) x += y; return x;
  bnp a0, mod_end
  
  // else x -= y; loop;
  j mod

  mod_end:
    add a0, a0, a1
    ret

// is_prime(m) -> 1 or 0
/*
  int divisor = 2;
  while (true) {
    if (divisor == m) return 1;
    if (n % divisor == 0) return 0;
  }
*/
is_prime:
  // Save a0 (n) and ra onto the stack
  addi sp, sp, -2
  sw a0, 0(sp)
  sw ra, 1(sp)

  // a1 <- divisor <= 2
  li a1, 2

  is_prime_loop:

    // if (divisor == n) return 1;
    // a2 <- a0 (n) - a1 (divisor)
    sub a2, a0, a1
    bz a2, is_prime_yes

    // if (x % divisor == 0) return 0
    // a0 <- x % divisor
    call mod

    // if (a0 == 0) return 0;
    bz a0, is_prime_no

    // Load n back into a0 (was modified during mod)
    lw a0, 0(sp)

    // else a1 (divisor)++, loop back
    addi a1, a1, 1
    j is_prime_loop

  is_prime_yes:
    li a0, 1
    j is_prime_end
    
  is_prime_no:
    li a0, 0
    j is_prime_end

  is_prime_end:
    lw ra, 1(sp)    // Recover ra
    addi sp, sp, 2  // Reset stack
    ret



halt
