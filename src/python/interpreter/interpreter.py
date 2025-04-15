"""
interpreter.py

Takes in memory and executes it.
"""

from inst_types import iTypeImm, iType
from utils import parse_imm


class RegFile:
    def __init__(self):
        """
        Create a new register file class instance.
          - Writing to 0 register does nothing
          - Reading from 0 register always returns 0
          - Set values are anded with 0xFFFF to ensure it fits in 16 bits
        """
        self.regs = [0] * 8

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def get(self, reg_idx: int):
        assert 0 <= reg_idx < 8, f"RegFile.get: reg_idx {reg_idx} not between 0 and 7"
        if reg_idx == 0:
            return 0

        return self.regs[reg_idx]

    def set(self, reg_idx: int, value: int):
        assert 0 <= reg_idx < 8, f"RegFile.set: reg_idx {reg_idx} not between 0 and 7"
        if reg_idx == 0:
            return

        assert 0 <= value < (1 << 16), f"RegFile.set: value {value} not in range"
        self.regs[reg_idx] = value & 0xFFFF


def execute(pc: int, rf: RegFile, mem: list[int]):
    """
    Execute a single instruction given pc and internal state.
        pc: address of instruction to fetch
        regfile: register file instance
        mem: all of memory
    """
    assert len(mem) == (1 << 16), "execute: memory must be of size 1<<16"

    if not 0 <= pc < (1 << 16):
        print(f"execute: accessed out-of-bounds memory at pc=0x{pc:04x}")

    inst = mem[pc]
    next_pc = pc  # Default next pc

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

    imm_imm = ((inst & (0b111 << 11)) >> 6) + (inst & (0b11111))
    imm_lui = ((inst & (0b111 << 8)) >> 3) + (inst & 0b11111)
    imm_br = inst & 0b11111111
    imm_load = inst & 0b11111
    imm_store = ((inst & (0b111 << 5)) >> 3) + (inst & 0b11)

    # IMM-TYPE
    if op_imm in [iTypeImm.ADDI, iTypeImm.NANDI]:
        if op_imm == iTypeImm.ADDI:
            # addi
            rf[rd] = rf[rs] + imm_imm
        elif op_imm == iTypeImm.NANDI:
            # nandi
            rf[rd] = ~(rf[rs] & imm_imm)
        return

    # Everything else
    match op5:
        case iType.LUI:
            rf[rd] = imm_lui << 8

        case iType.LOGICAL:
            match op2:
                case 0b00:
                    rf[rd] = ~(rf[rs] & rf[ro])
                case 0b11:
                    rf[rd] = rf[rs] & rf[ro]
                case 0b11:
                    rf[rd] = ~(rf[rs] | rf[ro])
                case 0b10:
                    rf[rd] = rf[rs] | rf[ro]

        case iType.ADDSUB:
            match op2:
                case 0b00, 0b01:
                    rf[rd] = rf[rs] + rf[ro]
                case 0b10, 0b11:
                    # Python magic takes care of this :O
                    rf[rd] = rf[rs] - rf[ro]

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
            rf[rd] = pc + 1
            next_pc = rf[rs]

        case iType.BR_BZ:
            if rf[rs] == 0:
                next_pc = pc + imm_br
        case iType.BR_BNZ:
            if rf[rs] != 0:
                next_pc = pc + imm_br
        case iType.BR_BP:
            if rf[rs] > 0:
                next_pc = pc + imm_br
        case iType.BR_BNP:
            if rf[rs] <= 0:
                next_pc = pc + imm_br

        case iType.LOAD:
            rf[rd] = mem[rf[rs] + imm_load]

        case iType.STORE:
            mem[rs + imm_store] = rf[rd] & 0xFFFF

    return next_pc
