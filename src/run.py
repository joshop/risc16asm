"""
run.py

Takes an input .asm file, assembles AND runs it.
"""

import os
import argparse
import struct

from assembler.assemble_program import assemble_program
from interpreter.interpreter import Interpreter


def main():
    parser = argparse.ArgumentParser(description="RISC-16 runner")
    parser.add_argument("input_file", help="Input assembly file")
    parser.add_argument(
        "-c",
        "--max-cycles",
        help="Maximum number of cycles to run processor for",
        default=5000,
        type=int,
    )

    args = parser.parse_args()

    # Assemble contents of file
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        exit(1)

    with open(args.input_file) as fin:
        prog_list: bytes = assemble_program(fin.read(), args.input_file)
        prog = struct.pack(f"<{len(prog_list)}H", *prog_list)

    print(f"Assembled '{args.input_file}' into machine code with {len(prog)} words")

    # Make interpreter and start running
    interp = Interpreter()
    interp.load_program(prog)

    while (not interp.is_halted()) and (interp.cycles < args.max_cycles):
        print(interp.dump_state())
        interp.step()

    print(interp.dump_state())


if __name__ == "__main__":
    main()
