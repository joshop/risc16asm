This is the working doc for the design of a transistorized computer.

Every instruction needs two cycles: fetch and execute.

There is a single multi-byte instruction type, called LI ("load immediate").

This machine is intentionally small: the zero page will act as working
registers, for the most part. The compiler will emit something very small and we
will translate it through very inefficient code to this assembly.

## ISA

### Registers

- A ..... 8 bits, accumulator
- IR .... 8 bits, instruction register
- ADL .. 8 bits, memory address register low
- ADH .. 8 bits, memory address register high
- PCL ... 8 bits, program counter low
- PCH ... 8 bits, program counter high
- C ..... 1 bit, carry flag

### States

- Fetch: Load mem[PC] into IR, increment PC
- Exec: read/write from mem, arithmetic, etc. Usually don't increment PC here
  unless LI or BZ

### Instructions

Arithmetic

- LI ............ A <- imm
- ADD ........... A <- A + mem[MAR]
- ADDC .......... {C, A} <- A + mem[MAR] + C
- NAND .......... A <- A NAND mem[MAR]

Carry control

- CLRC .......... clear carry
- SETC .......... set carry

Transfers

- TAL ........... ADL <- A
- TAH ........... ADH <- A
- TLA ........... A <- ADL
- THA ........... A <- ADH

Memory

- STA ........... mem[MAR] <- A
- LDA ........... A <- mem[MAR]

Control flow

- JMP ........... PC <- MAR
- JZ ............ PC <- MAR if (A == 0)
- JNZ ........... PC <- MAR if (A != 0)

## Hardware

Memory:

- ROM:
  [AT28C256-15PU](https://www.digikey.com/en/products/detail/microchip-technology/AT28C256-15PU/1008506)
  (32 KiB EEPROM)
- RAM:
  [AS6C62256](https://www.alliancememory.com/wp-content/uploads/AS6C62256-23-March-2016-rev1.2.pdf)
  (32 KiB RAM)

Transistors:

- NMOS: BSS123
- PMOS: BSS84
