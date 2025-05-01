"""
interpret.py

Usage:
    python interpret.py <machine_code.bin>
"""

import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interpreter.interpreter import Interpreter


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="RISC-16 interpreter")
    parser.add_argument("input_file", help="Input binary file")

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        exit(1)

    try:
        # Create interpreter and load program
        interp = Interpreter()
        interp.load_program(args.input_file)

        # Run the program
        cycle = 0

        while True:
            interp.step()
            print(interp.dump_state())
            cycle += 1

            # Break if encounger `bz r0, <zero offset>`
            if interp.mem[interp.pc] == 0b00100_000_00000000:
                break

    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
