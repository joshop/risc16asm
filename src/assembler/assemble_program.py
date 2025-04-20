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


def assemble_program(prog: str, filepath: str | None = None) -> list[int]:
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
    macros = {}  # match macros to their expanded forms
    base_insts = []  # store (op, args, line_idx, addr)

    line_idx = 0

    while line_idx < len(lines):
        # Remove comments
        line = lines[line_idx].split("//", 1)[0].strip()
        if len(line) == 0:
            line_idx += 1
            continue

        # Handle multiline comments
        if line.startswith("/*"):
            while not "*/" in lines[line_idx]:
                line_idx += 1
            line_idx += 1
            continue

        print(f"LINE_IDX={line_idx}, line={line}")

        try:
            # Is it a label?
            label_match = re.fullmatch("(\w+):", line)
            if label_match:
                label = label_match.group(1)

                # No duplicate labels
                if label in labels:
                    raise SyntaxError(f"Duplicate label '{label}' on line {line_idx}")

                labels[label] = cur_addr
                line_idx += 1
                continue

            else:
                # Handle macros
                is_macro = False
                for macro_pattern, repl_pattern in macros.items():
                    if re.fullmatch(macro_pattern, line):
                        replacement_lines = re.sub(macro_pattern, repl_pattern, line)
                        is_macro = True
                        break

                if is_macro:
                    for line in replacement_lines.split("\n"):
                        op, args = re.split(r"\s+", line, 1)
                        args = re.split(r",\s*", args)
                        base_insts.append([op, args, line_idx, cur_addr])
                        cur_addr += 1

                    line_idx += 1
                    continue

                # Regular instruction (not a macro)
                op, args = re.split(r"\s+", line, 1)
                args = re.split(r",\s*", args)

                match op:
                    case ".include":
                        assert (
                            len(args) == 1
                        ), f"Expeced 1 arg for .include directive, got {len(args)}"

                        # Read contents of .include and assemble it
                        # .include is relative to the program's file path, if it exists
                        raw_path = os.path.join(os.path.dirname(filepath), args[0])
                        with open(raw_path) as fin:
                            subprog_asm = fin.read()
                            lines[line_idx + 1 : line_idx + 1] = subprog_asm.split("\n")

                    case ".word":
                        assert (
                            len(args) == 1
                        ), f"Expected 1 arg for .word directive, got {len(args)}"
                        base_insts.append([op, args, line_idx, cur_addr])
                        cur_addr += 1

                    case ".dword":
                        assert (
                            len(args) == 1
                        ), f"Expected 1 arg for .dword directive, got {len(args)}"
                        base_insts.append([op, args, line_idx, cur_addr])
                        cur_addr += 2

                    case ".def":
                        assert (
                            len(args) == 2
                        ), f"Expected 2 args for .def directive, got {len(args)}"
                        Y, X = args[0], parse_const(args[1], 16)
                        vars[Y] = X

                    case ".addr":
                        assert (
                            len(args) == 1
                        ), f"Expected 1 args for .addr directive, got {len(args)}"
                        X = parse_const(args[0], 16)
                        cur_addr = X

                    case ".bin":
                        # TODO
                        pass

                    case ".include":
                        # TODO
                        pass

                    case ".macro":
                        # Read the entire macro
                        og_line_idx = line_idx
                        macro_pattern = line.split(" ", 1)[1]

                        # No duplicate macros
                        if macro_pattern in macros:
                            raise SyntaxError(
                                f"Duplicate macro '{macro_pattern}' on line {og_line_idx}"
                            )

                        # Get all contents before .endmacro
                        replacement_lines = []
                        line_idx += 1
                        while line_idx < len(lines) and lines[line_idx] != ".endmacro":
                            replacement_lines.append(lines[line_idx])
                            line_idx += 1

                        # Reached end of file and have not yet found
                        if line_idx == len(lines):
                            raise SyntaxError(
                                f"No matching .endmacro found for .macro directive on line {og_line_idx}"
                            )

                        # Save this macro
                        macros[macro_pattern] = "\n".join(replacement_lines)

                    case _:
                        # Standard instruction
                        base_insts.append([op, args, line_idx, cur_addr])
                        cur_addr += 1

            # Next line
            line_idx += 1

        except Exception as e:
            raise SyntaxError(
                f"Could not parse line '{lines[line_idx]}' at line {line_idx+1}: {e}"
            )

    # Pass 2: assemble each line
    for op, args, line_idx, addr in base_insts:
        try:
            if op == ".bin":
                # Include raw binary, treat as a bunch of .word directives
                words = args
            else:
                # Parse as usual instruction
                words = base_parse_line(op, args, labels, addr)

        except Exception as e:
            print(f"Error assembling '{op} {', '.join(args)}' at line {line_idx+1}")
            raise e

        print(
            f"line {line_idx+1:>5} | addr h'{addr:04x} | op {op:>8} | {', '.join(args):<28} | "
            f"h'{words[0]:04x}"
            # f"b'{words[0]:016b}"
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
