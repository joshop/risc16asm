"""
parser.py

Parse standalone lines (non-pseudoinstructions, fill directives, etc.)
"""

import re
from enum import Enum

from utils import parse_const, encode_const
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


def base_parse_line(line: str, labels: dict, cur_addr: int) -> list[int]:
    """
    Method to parse location-independent instructions/directives:
        - .word
        - .dword
        - native opcodes
    """
    assert isinstance(line, str)
    assert isinstance(labels, dict)
    assert isinstance(cur_addr, int)

    # Remove comments
    line = line.split("//", 1)[0].strip()
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
        raise SyntaxError("parse_line: .macro not closed by matching .endmacro")

    # Regular opcode
    if op in BASE_OPCODES:
        try:
            return [parse_base_inst(op, args, labels, cur_addr)]
        except Exception as e:
            print(f"parse_line: could not parse instruction '{line}':")
            raise e

    raise Exception(f"parse_line: invalid opcode '{op}'")


def reg_idx(reg_name: str):
    reg_names = [f"r{i}" for i in range(8)]
    if not reg_name in reg_names:
        print(f"Invalid register name '{reg_name}'")
    return reg_names.index(reg_name)


def parse_base_inst(op, args, labels: dict, cur_addr: int) -> int:
    """
    Parse a base instruction like addi, lui, sub, sl, bz.
    Branch instructions require special care, hence `labels` and `cur_addr` dicts.
    """
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

            match op:
                case ["nand", "and", "nor", "or"]:
                    inst_bin += iType.LOGICAL << 11
                case ["xor"]:
                    inst_bin += iType.XOR << 11
                case ["add", "sub"]:
                    inst_bin += iType.ADDSUB << 11
                case _:
                    raise SyntaxError(f"Unexpected opcode {op}")
            return inst_bin

        case OPCODES.ALU_SH:
            assert len(args) == 2, f"Expected 3 args for {op} instruction"
            rd, rs = map(reg_idx, args[:2])
            shamt = parse_const(args[2])

            sd = {
                "sl": 0,
                "sr": 1,
            }[op]
            inst_bin = (iType.SHIFT << 11) + (rs << 8) + (rd << 5) + (sd << 4) + shamt
            return inst_bin

        case OPCODES.JUMP:
            return (rs << 8) + (rd << 5)

        case OPCODES.BR:
            assert len(args) == 2, f"Expected 2 args for {op} instruction"
            rs = reg_idx(args[0])
            label = args[1]

            # Figure out the immediate
            if not label in labels:
                raise NameError(f"Label '{label}' not found")

            offset = labels[label] - cur_addr
            imm = encode_const(offset, 8)

            inst_bin = (rs << 8) + imm
            inst_bin += {
                "bz": iType.BR_BZ,
                "bnz": iType.BR_BNZ,
                "bp": iType.BR_BP,
                "bnp": iType.BR_BNP,
            }[op]
            return inst_bin

        case OPCODES.LOAD:
            assert len(args) == 2, f"Expected 2 args for {op} instruction"
            rd = reg_idx(args[0])
            addr = re.match("(.+)\(.+\)")
            offset, rs = parse_const(addr[0]), reg_idx(addr[1])

            imm = encode_const(offset, 5)
            inst_bin = (iType.LOAD << 11) + (rs << 8) + (rd << 5) + imm

        case OPCODES.STORE:
            assert len(args) == 2, f"Expected 2 args for {op} instruction"
            ro = reg_idx(args[0])
            addr = re.match("(.+)\(.+\)")
            offset, rs = parse_const(addr[0]), reg_idx(addr[1])

            imm = encode_const(offset, 5)
            imm_hi = (imm & (0b111 << 2)) >> 2
            imm_lo = imm & 0b11
            inst_bin = (
                (iType.STORE << 11) + (rs << 8) + (imm_hi << 5) + (ro << 2) + imm_lo
            )
            return inst_bin
