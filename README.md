# RISC-16

Assembler and emulator for a custom 16-bit instruction set.

## Usage

### Assembly

Suppose we have assembly code in `scripts/test_1.asm`. To assemble it into machine code:

```sh
python src/assemble.py scripts/test_1.asm [-o <output_file>]
```

If no output file is specified, it will default to `<basename>.bin`.

### Emulation

If the machine code is in `scripts/test_1.bin`, emulate it using

```sh
python src/interpret.py scripts/test_1.bin
```

### All-in-one

To do it all in one step, run

```sh
python src/run.py scripts/test_1.asm
```

## Assembly format

A program consists of a sequence of the following separated by newlines:

- Instructions of the form `op field, ...`, which emit their opcode
- Labels of the form `lab: `, which defines `lab` to be the current address
- Comments of the form `// comment text ended by a newline`
- Whitespace (which is ignored)
- Assembler directives
- Macros (previously defined)

Assembler directives include the following:

- `.word X` emits a single word (16 bits), `X`
- `.dword X` emits a double word (32 bits), `X`
- `.def Y X` defines a constant with value `X` called `Y`
- `.addr X` defines the current address to be `X`
- `.bin filename` emits all of the bytes in `filename`
- `.include filename` causes the assembler to process `filename`'s contents as if it was inserted into the file directly.
- `.macro pattern` defines a macro that translates any statement matched by the regex `pattern`. Statements until `.endmacro` are considered part of the macro.

When instructions are assembled, immediates can be expressions with any of the following components:

- Constants in decimal, hexadecimal (`$` or `0x`) prefix, binary (`%` or `0b` prefix)
- Constants defined with `.def`
- Addresses of labels within the program
- `+`, `-`, `&`, `|`, `^`, `~`, `>>`, `<<` operators
  Example:

```
.macro li (r[0-7]), ([0-9]+)
lui \1, (\2) >> 8
addi \1, \1, (\2) & $ff
.endmacro
.addr 0
main:
  li r3, myfunction
  jalr r0, r3
.addr $1234
myfunction:
  // ... do something
```
