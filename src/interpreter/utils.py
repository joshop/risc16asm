def parse_imm(imm: int, width: int) -> int:
    # Parse x as a signed integer with width `width`
    # Used by interpreter
    assert width > 0, f"encode_imm: nonzero width {width}"
    assert imm >= 0, f"parse_imm: expected nonnegative imm, got {imm}"
    assert imm < (1 << width), f"parse_imm: imm {imm} does not fit in {width} bits"

    if imm & (1 << (width - 1)):
        return imm - (1 << width)
    return imm


if __name__ == "__main__":
    # Minimal tests
    assert parse_imm(0b11111111, 8) == -1
