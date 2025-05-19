.include _common.asm

nop
nop
nop

// Initialize sp
li sp, 0xffff

// LOAD CONSTANTS
li a0, 50

call nth_prime
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


// nth_prime(n) -> nth prime number
// a0 <- n
nth_prime:
  // a1 <- alleged nth prime
  li a1, 2

  // a2 <- counter (starts at n)
  mv a2, a0

  // store ra, n on stack
  addi sp, sp, -4
  sw a0, 0(sp)
  sw ra, 1(sp)
  sw a1, 3(sp)  // alleged prime

  // loop
  nth_prime_loop:
    // save counter, alleged prime to stack
    sw a2, 2(sp)
    sw a1, 3(sp)

    lw a0, 3(sp)   // a0 <- alleged nth prime
    call is_prime

    // decrement count by primality
    lw a2, 2(sp)
    sub a2, a2, a0

    // are we done?
    bz a2, nth_prime_end

    // if not, go back
    lw a1, 3(sp)
    addi a1, a1, 1
    j nth_prime_loop

  nth_prime_end:
    // reset the stack and put ra back
    lw ra, 1(sp)
    addi sp, sp, 2
    ret


// is_prime(n) -> 1 or 0
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
  
  // if even return 0
  // check if last bit is a 1
  andi a3, a0, 1
  bz a3, is_prime_no

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
