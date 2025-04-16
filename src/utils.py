import re


def parse_imm(imm: int, width: int) -> int:
    # Parse x as a signed integer with width `width`
    # Used by interpreter
    assert width > 0, f"encode_imm: nonzero width {width}"
    assert imm >= 0, f"parse_imm: expected nonnegative imm, got {imm}"
    assert imm < (1 << width), f"parse_imm: imm {imm} does not fit in {width} bits"

    if imm & (1 << (width - 1)):
        return imm - (1 << width)
    return imm


def parse_const(s: str, width: int) -> int:
    """
    Convert string constants like "42", "-1", "0xf8", "0b1001"
       to fixed bit-widths.

    1. Excess bits get truncated from the left.
    2. We use stoi, so we stop at invalid chars.
    """
    # Select lowest `width` bits
    mask = (1 << width) - 1

    # Match hexadecimal strings
    hex_match = re.fullmatch(r"(?:0x|\$)([a-fA-F0-9_]+)", s)
    if hex_match:
        return int(hex_match.group(1).replace("_", ""), 16) & mask

    # Match binary strings
    bin_match = re.fullmatch(r"(?:0b|%)([a-fA-F0-9_]+)", s)
    if bin_match:
        return int(bin_match.group(1).replace("_", ""), 2) & mask

    # Assume decimal string
    assert re.fullmatch(r"\d+", s), "parse_const: const is not decimal"
    return int(s.replace("_", "")) & mask


def encode_const(imm: int, width: int) -> int:
    # Encode x as a signed integer with width `width`
    # Used by assembler
    assert width > 0, "encode_const: width must be positive"
    assert (
        -(1 << (width - 1)) <= imm < (1 << (width - 1))
    ), f"encode_const: imm {imm} does not fit in {width} bits"
    return imm & ((1 << width) - 1)


if __name__ == "__main__":
    # Minimal tests
    assert parse_const("0xbeef", 16) == 0xBEEF
    assert parse_imm(0b11111111, 8) == -1
