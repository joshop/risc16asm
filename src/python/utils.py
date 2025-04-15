"""
utils.py

Methods for parsing constants, etc.
"""

import re


def parse_const(s: str, width: int) -> int:
    """
    Convert string constants like "42", "-1", "0xf8", "0b1001"
       to fixed bit-widths.

    1. Excess bits get truncated from the left.
    2. We use stoi, so we stop at invalid chars.
    """
    assert width in [8, 16], "parse_const: bit width must be 8 or 16"
    if width == 8:
        mask = 0xFF
    elif width == 16:
        mask = 0xFFFF

    # Match hexadecimal strings
    hex_match = re.fullmatch(r"(?:0x|\$)([a-fA-F0-9]+)", s)
    if hex_match:
        return int(hex_match.group(1), 16) & mask

    # Match binary strings
    bin_match = re.fullmatch(r"(?:0b|%)([a-fA-F0-9]+)", s)
    if bin_match:
        return int(bin_match, 2) & mask

    # Assume decimal string
    assert re.fullmatch(r"\d+", s), "parse_const: const is not decimal"
    return int(s) & mask


def parse_imm(imm: int, width: int) -> int:
    # Return x as a signed integer with width `width`
    assert imm >= 0, f"parse_imm: expected nonnegative imm, got {imm}"
    assert imm < (1 << width), f"parse_imm: imm {imm} does not fit in {width} bits"

    if imm & (1 << (width - 1)):
        return imm - (1 << width)
    return imm


if __name__ == "__main__":
    # Minimal tests
    assert parse_const("0xbeef", 16) == 0xBEEF
    assert parse_imm(0b11111111, 8) == -1
