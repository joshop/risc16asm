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

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        exit(1)

    with open(args.input_file) as fin:
        prog_list: bytes = assemble_program(fin.read())
        prog = struct.pack(f"<{len(prog_list)}H", *prog_list)

    print(f"Assembled '{args.input_file}' into machine code with {len(prog)} words")

    interp = Interpreter()
    interp.load_program(prog)

    while not interp.is_halted():
        print(interp.dump_state())
        interp.step()


if __name__ == "__main__":
    main()
