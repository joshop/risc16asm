"""
parser.py

Parse standalone lines (non-pseudoinstructions, fill directives, etc.)
"""

import re
from enum import Enum

from utils import parse_const
from inst_types import iType, iTypeImm


class OPCODES(Enum):
    IMM = ["addi", "nandi"]
    LUI = ["lui"]
    ALU_AL = ["nand", "and", "nor", "or", "add", "sub"]
    ALU_SH = ["sl", "sr", "xor"]
    JUMP = ["jalr"]
    BR = ["bz", "bnz", "bp", "bnp"]
    LOAD = ["lw"]
    STORE = ["sw"]


OPCODE_DICT = {
    "imm": OPCODES.IMM,
    "lui": OPCODES.LUI,
    "alu_al": OPCODES.ALU_AL,
    "alu_sh": OPCODES.ALU_SH,
    "jump": OPCODES.JUMP,
    "br": OPCODES.BR,
    "load": OPCODES.LOAD,
    "store": OPCODES.STORE,
}
BASE_OPCODES = sum(OPCODE_DICT.values(), [])


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

    # Split line by comma whitespace
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
    if op in BASE_OPCODES:
        try:
            return [parse_base_inst(op, args)]
        except Exception as e:
            print(f"parse_line: could not parse instruction '{line}':")
            raise e

    raise Exception(f"parse_line: invalid opcode '{op}'")


def reg_idx(reg_name: str):
    reg_names = [f"r{i}" for i in range(8)]
    if not reg_name in reg_names:
        print(f"Invalid register name '{reg_name}'")
    return reg_names.index(reg_name)


def parse_base_inst(op, args) -> int:
    match op:
        case OPCODES.IMM:
            assert len(args) == 3, f"Expected 3 args for {op} instruction"
            rd, rs = map(reg_idx, args[:2])
            imm = parse_const(args[2], 8)

            # Instruction, encoded as binary
            inst_bin = (rs << 8) + (rd << 5) + imm
            if op == "addi":
                inst_bin += iTypeImm.ADDI << 14
            elif op == "nandi":
                inst_bin += iTypeImm.NANDI << 14

            return inst_bin

        case OPCODES.LUI:
            assert len(args) == 2, f"Expected 2 args for {op} instruction"
            rd = reg_idx(args[0])
            imm = parse_const(args[1], 8)

            imm_hi = imm & (0b111 << 5)
            imm_lo = imm & (0b11111)
            inst_bin = (iType.LUI << 11) + (imm_hi << 8) + (rd << 5) + (imm_lo)
            return inst_bin

        case OPCODES.ALU_AL:
            assert len(args) == 3, f"Expected 3 args for {op} instruction"
            rs, rd, ro = map(reg_idx, args)

            op2 = {
                "nand": 0b00,
                "and": 0b01,
                "nor": 0b11,
                "or": 0b10,
                "xor": 0b00,  # doesn't matter
                "add": 0b00,  # or 0b01
                "sub": 0b10,  # or 0b11
            }[op]
            inst_bin = (rs << 8) + (rd << 5) + (ro << 2) + op2
            if op in ["nand", "and", "nor", "or"]:
                inst_bin += iType.LOGICAL << 11
            elif op in ["xor"]:
                inst_bin += iType.XOR << 11
            elif op in ["add", "sub"]:
                inst_bin += iType.ADDSUB << 11
            else:
                raise SyntaxError(f"Unexpected opcode {op}")

        case OPCODES.ALU_SH:
            assert len(args) == 2, f"Expected 3 args for {op} instruction"
            rd, rs = map(reg_idx, args[:2])
            shamt = parse_const(args[2])

            if op == "sl":
                sd = 0
            elif op == "sr":
                sd = 1
            else:
                raise SyntaxError(f"Unexpected opcode {op}")

            inst_bin = (iType.SHIFT << 11) + (rs << 8) + (rd << 5) + (sd << 4) + shamt
