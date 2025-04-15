"""
program_parser.py

Parse a full program into machine code.
"""

from base_inst_parser import base_parse_line


def program_parser(prog: str) -> list[int]:
    """
    Parses a full program and emits the contents of memory.
    """

    mem = [0] * (1 << 16)

    # TODO: Evaluate macros
    pass

    # Store .def directives
    vars = {}

    # Store labels
    labels = {}

    # State
    cur_addr = 0

    # Parse lines one by one
    lines = prog.split("\n")
    for line_idx, line in enumerate(lines):
        try:
            words = base_parse_line(line)
        except Exception as e:
            print(f"Error at line {line_idx}: {e}")
            exit(1)

        # Fill in next memory addresses
        for i, w in enumerate(words):
            if cur_addr + i >= 1 << 16:
                raise IndexError(
                    f"program_parser: could not write to mem addr {cur_addr + i}"
                )
            mem[cur_addr + i] = w

        # Increment current memory address
        cur_addr += len(words)

    return mem


if __name__ == "__main__":
    with open("./scripts/test_1.asm") as fin:
        prog = fin.read()

    mem = program_parser(prog)
