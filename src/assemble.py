"""
assemble.py

Usage:
    python assemble.py <asesmbly_file.asm> [-o <machine_code.asm>]
"""

import sys
import os
import argparse

from assembler.program_parser import assemble_program


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="RISC-16 assembler")
    parser.add_argument("input_file", help="Input assembly file")
    parser.add_argument("-o", "--output", help="Output binary file")

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        exit(1)

    # Determine output file name if not specified
    if args.output is None:
        base_name = os.path.splitext(args.input_file)[0]
        output_file = f"{base_name}.bin"
    else:
        output_file = args.output

    try:
        # Parse the assembly file
        with open(args.input_file) as fin:
            prog = fin.read()
        binary_code = assemble_program(prog)

        # Write the binary code to the output file
        with open(output_file, "wb") as f:
            for word in binary_code:
                f.write(word.to_bytes(2, "little"))

        print(
            f"Successfully assembled {args.input_file} -> {output_file} ({len(binary_code)} words)"
        )

    except Exception as e:
        print(f"Error during assembly: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
