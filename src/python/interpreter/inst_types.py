from enum import Enum


class iTypeImm:
    """
    Enum for inst[15:14] to detect imm-type instructions
    """

    ADDI = 0b10
    NANDI = 0b11


class iType:
    """
    Enum for inst[15:11] to detect most other instructions
    """

    LUI = 0b01000
    LOGICAL = 0b01001
    ADDSUB = 0b01100
    SHIFT = 0b01010
    XOR = 0b01101

    JUMP = 0b00000

    BR_BZ = 0b00100
    BR_BNZ = 0b00101
    BR_BP = 0b00110
    BR_BNP = 0b00111

    LOAD = 0b00010
    STORE = 0b00011
