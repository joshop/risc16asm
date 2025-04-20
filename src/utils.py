def parse_const(s: str, width: int, labels: dict = {}, vars: dict = {}) -> int:
    """
    Convert string constants like "42", "-1", "0xf8", "0b1001"
       to fixed bit-widths.

    1. Excess bits get truncated from the left.
    2. `labels` and `vars` allow us to eval things
    """
    # Select lowest `width` bits
    mask = (1 << width) - 1

    value = eval(s, {"__builtins__": None, **labels, **vars})

    assert (
        -(1 << width) <= value < (1 << width)
    ), f"parse_const: Value {value} does not fit in {width} bits"
    return value & mask


def encode_const(imm: int, width: int) -> int:
    # Encode x as a signed integer with width `width`
    # Used by assembler
    assert width > 0, "encode_const: width must be positive"
    assert (
        -(1 << (width - 1)) <= imm < (1 << (width - 1))
    ), f"encode_const: imm {imm} does not fit in {width} bits"
    return imm & ((1 << width) - 1)


def parse_imm(imm: int, width: int) -> int:
    # Parse x as a signed integer with width `width`
    # Used by interpreter
    assert width > 0, f"encode_imm: nonzero width {width}"
    assert imm >= 0, f"parse_imm: expected nonnegative imm, got {imm}"
    assert imm < (1 << width), f"parse_imm: imm {imm} does not fit in {width} bits"

    if imm & (1 << (width - 1)):
        return imm - (1 << width)
    return imm


def format_const(x: int, base: int):
    """
    Format an integer as fixed width
    """
    assert base in [2, 10, 16], f"Base {base} not one of 2, 10, 16"
    assert x >= 0, f"Constant {x} not nonnegative integer"

    # Check that it fits within `width` digits
    width = {2: 16, 10: 5, 16: 4}[base]
    if width > 0:
        assert x < pow(
            base, width
        ), f"Constant {x} does not fit in {width} base-{base} digits"

    match base:
        case 2:
            return "b'" + f"{x:b}".zfill(width)
        case 10:
            return "" + f"{x:d}".rjust(width)
        case 16:
            return "h'" + f"{x:x}".zfill(width)


if __name__ == "__main__":
    # Minimal tests
    assert parse_const("0xbeef", 16) == 0xBEEF
    assert parse_imm(0b11111111, 8) == -1
