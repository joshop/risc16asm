"""
assemble.py

Usage:
    python assemble.py <asesmbly_file.asm> [-o <machine_code.asm>]
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

import argparse

from assembler.assemble_program import assemble_program


def assemble(input_file: str, output_file: str):
    """
    input_file: file containing assembly code
    output: file to write to containing machine code
    """
    # Parse the assembly file
    # Exceptions will pass through
    with open(input_file) as fin:
        prog = fin.read()
    binary_code = assemble_program(prog)

    # Write the binary code to the output file
    with open(output_file, "wb") as f:
        for word in binary_code:
            f.write(word.to_bytes(2, "little"))

    print(
        f"Successfully assembled {input_file} -> {output_file} ({len(binary_code)} words)"
    )


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

    return assemble(args.input_file, output_file)


if __name__ == "__main__":
    main()
