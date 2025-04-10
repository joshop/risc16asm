# Assembly Format
A program consists of a sequence of the following:
- Instructions of the form `op field, ...`, which emit their opcode
- Labels of the form `lab: `, which defines `lab` to be the current address
- Comments of the form `%comment text... %`
- Whitespace (which is ignored)
- Assembler directives
- Macros (previously defined)
Assembler directives include the following:
- `.byte X` emits a single byte, `X`
- `.word X` emits a single word (16 bits), `X`
- `.dword X` emits a double word (32 bits), `X`
- `.def Y X` defines a constant with value `X` called `Y`
- `.addr X` defines the current address to be `X`
- `.bin filename` emits all of the bytes in `filename`
- `.
- `.macro "pattern" "replacement"` defines a macro that translates
