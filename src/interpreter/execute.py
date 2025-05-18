"""
execute.py

Takes in memory and executes a single instruction in it.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inst_types import iTypeImm, iType
from utils import parse_imm
from interpreter.reg_file import RegFile


def execute(pc: int, rf: RegFile, mem: list[int]):
    """
    Execute a single instruction given pc and internal state.
        pc: address of instruction to fetch
        regfile: register file instance
        mem: all of memory
    """
    assert len(mem) == (1 << 16), "execute: memory must be of size 1<<16"

    if not 0 <= pc < (1 << 16):
        raise IndexError(
            f"execute: pc={pc}, accessed out-of-bounds memory at pc=0x{pc:04x}"
        )

    inst = mem[pc]
    next_pc = pc + 1  # Default next pc

    # Universal: rs, ro, rd
    # TODO: make a Bits class for better indexing
    rs = (inst & (0b111 << 8)) >> 8
    rd = (inst & (0b111 << 5)) >> 5
    ro = (inst & (0b111 << 2)) >> 2

    # Types of opcodes:
    #   op_imm: inst[15:14], for addi and nandi
    #   op5:    inst[15:11], for the rest
    #   op2:    inst[1:0], for alu_al type
    op_imm = (inst & (0b11 << 14)) >> 14
    op5 = (inst & (0b11111 << 11)) >> 11
    op2 = inst & (0b11)

    imm_imm = parse_imm(((inst & (0b111 << 11)) >> 6) + (inst & (0b11111)), 8)
    imm_lui = parse_imm(((inst & (0b111 << 8)) >> 3) + (inst & 0b11111), 8)
    imm_br = parse_imm(inst & 0b11111111, 8)
    imm_load = parse_imm(inst & 0b11111, 5)
    imm_store = parse_imm(((inst & (0b111 << 5)) >> 3) + (inst & 0b11), 5)

    # IMM-TYPE
    if op_imm in [iTypeImm.ADDI, iTypeImm.NANDI]:
        if op_imm == iTypeImm.ADDI:
            # addi
            rf[rd] = (rf[rs] + imm_imm) & 0xFFFF
        elif op_imm == iTypeImm.NANDI:
            # nandi
            rf[rd] = (~(rf[rs] & imm_imm)) & 0xFFFF

        return next_pc

    # Everything else
    match op5:
        case iType.LUI:
            rf[rd] = (imm_lui << 8) & 0xFFFF

        case iType.LOGICAL:
            match op2:
                case 0b00:
                    rf[rd] = (~(rf[rs] & rf[ro])) & 0xFFFF
                case 0b01:
                    rf[rd] = rf[rs] & rf[ro]
                case 0b11:
                    rf[rd] = ~(rf[rs] | rf[ro])
                case 0b10:
                    rf[rd] = rf[rs] | rf[ro]

        case iType.ADDSUB:
            match op2:
                case 0b00 | 0b01:
                    rf[rd] = (rf[rs] + rf[ro]) & 0xFFFF
                case 0b10 | 0b11:
                    # Python magic takes care of this :O
                    rf[rd] = (rf[rs] - rf[ro]) & 0xFFFF

        case iType.XOR:
            rf[rd] = rf[rs] ^ rf[ro]

        case iType.SHIFT:
            shamt = inst & 0b1111
            sd = (inst & (0b1 << 4)) >> 4
            if sd == 0:
                rf[rd] = rf[rs] << shamt
            else:
                rf[rd] = rf[rs] >> shamt

        case iType.JUMP:
            next_pc = rf[rs]
            rf[rd] = pc + 1

        case iType.BR_BZ:
            if rf[rs] == 0:
                next_pc = pc + imm_br
        case iType.BR_BNZ:
            if rf[rs] != 0:
                next_pc = pc + imm_br
        case iType.BR_BP:
            if not (rf[rs] & (1 << 15)):
                next_pc = pc + imm_br
        case iType.BR_BNP:
            if rf[rs] & (1 << 15):
                next_pc = pc + imm_br

        case iType.LOAD:
            rf[rd] = mem[rf[rs] + imm_load]

        case iType.STORE:
            mem[rf[rs] + imm_store] = rf[ro] & 0xFFFF

    return next_pc
