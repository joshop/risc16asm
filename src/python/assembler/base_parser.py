"""
parser.py

Parse standalone lines (non-pseudoinstructions, fill directives, etc.)
"""

import re
from utils import parse_const

OPCODE_DICT = {
    "imm": ["addi", "nandi"],
    "lui": ["lui"],
    "alu_al": ["nand", "and", "nor", "or", "add", "sub"],
    "alu_sh": ["sl", "sr", "xor"],
    "jump": ["jalr"],
    "br": ["bz", "bnz", "bp", "bnp"],
    "load": ["lw"],
    "store": ["sw"],
}
BASE_OPCODE = sum(OPCODE_DICT.values(), [])


def base_parse_line(line: str) -> list[int]:
    """
    Method to parse location-independent instructions/directives:
        - .word
        - .dword
        - native opcodes
    """
    # Remove comments
    line = line.split("//", 1)[0]
    if len(line) == 0:
        return []

    # Split line by comma "," followed by whitespace
    try:
        op, args = re.split(r"\s+", line, 1)
        args = re.split(r",\s*", args)[0]
    except Exception as e:
        raise Exception("parse_line: could not parse line in initial split")

    # .word directive
    if op == ".word":
        assert len(args) == 1, "parse_line: expected one arg for .word directive"
        return [parse_const(args[0], 16)]

    # .dword directive
    if op == ".dword":
        assert len(args) == 2, "parse_line: expected one arg for .dword directive"
        dword = parse_const(args[0], 32)
        return [(dword & 0xFFFF0000) >> 16, dword & 0xFFFF]

    # Unmatched .macro (should get caught by program parser)
    if op == ".macro":
        raise SyntaxError("parse_line: .macro does not have matching .endmacro")

    # Regular opcode
    if op in BASE_OPCODE:
        return [parse_base_inst(line)]

    raise Exception(f"parse_line: invalid opcode '{op}'")


def parse_base_inst(s: str) -> int:
    return 0
