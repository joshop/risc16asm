"""
program_parser.py

Parse a full program into machine code.
"""

import re
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import parse_const
from assembler.base_inst_parser import base_parse_line


def assemble_program(prog: str) -> list[int]:
    """
    Parses a full program and emits the contents of memory.
        prog: assembly program
    """
    mem = [0] * (1 << 16)

    # Parse lines one by one
    lines = prog.split("\n")

    # Pass 1: find label addresses
    #   - remove comments
    #   - expand macros
    #   - figure out instruction widths

    cur_addr = 0
    max_addr = 0
    vars = {}  # figure out label addresses
    labels = {}  # store .def directives
    base_insts = []  # store (op, args, line_idx, addr)

    line_idx = 0

    while line_idx < len(lines):
        # Remove comments
        line = lines[line_idx].split("//", 1)[0].strip()
        if len(line) == 0:
            line_idx += 1
            continue

        # Split line
        try:
            # Is it a label?
            label_match = re.fullmatch("(\w+):", line)
            if label_match:
                label = label_match.group(1)
                labels[label] = cur_addr
                line_idx += 1
                continue

            else:
                # Regular instruction
                op, args = re.split(r"\s+", line, 1)
                args = re.split(r",\s*", args)

        except Exception as e:
            raise SyntaxError(
                f"Could not parse line '{lines[line_idx]}' at line {line_idx}: {e}"
            )

        match op:
            case ".word":
                assert len(args) == 1, "Expected 1 arg for .word directive"
                base_insts.append([op, args, line_idx, cur_addr])
                cur_addr += 1

            case ".dword":
                assert len(args) == 1, "Expected 1 arg for .dword directive"
                base_insts.append([op, args, line_idx, cur_addr])
                cur_addr += 2

            case ".def":
                assert len(args) == 2, f"Expected 2 args for .def directive"
                Y, X = args[0], parse_const(args[1], 16)
                vars[Y] = X

            case ".addr":
                assert len(args) == 1, f"Expected 1 arg for .addr directive"
                X = parse_const(args[1], 16)
                cur_addr = X

            case ".bin":
                # TODO
                pass

            case ".include":
                # TODO
                pass

            case ".macro":
                # Read the entire macro
                # TODO
                pass

            case _:
                base_insts.append([op, args, line_idx, cur_addr])
                cur_addr += 1

        # Next line
        line_idx += 1

    # Pass 2: assemble each line
    for op, args, line_idx, addr in base_insts:
        try:
            words = base_parse_line(op, args, labels, addr)
        except Exception as e:
            print(f"Error assembling '{lines[line_idx]}' at line {line_idx}")
            raise e

        print(
            f"line {line_idx:>5} | addr 0x{addr:04x} | op {op:>8} | {', '.join(args):>20} | {words[0]:04x}"
        )
        max_addr = max(max_addr, addr)

        # Fill in next memory addresses
        for i, w in enumerate(words):
            assert isinstance(w, int), f"Returned invalid word '{w}'"
            if addr + i >= 1 << 16:
                raise IndexError(f"Could not write to mem addr {addr + i}")
            mem[addr + i] = w

    return mem[: (max_addr + 1)]


if __name__ == "__main__":
    with open("./scripts/test_1.asm") as fin:
        prog = fin.read()

    mem = assemble_program(prog)
    for word in mem:
        print(f"{word:016b}")

        if word == 0:
            break
