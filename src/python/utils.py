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
    assert width in [8, 16], "Width must be 8 or 16"
    if width == 8:
        mask = 0xFF
    elif width == 16:
        mask = 0xFFFF

    # Match hexadecimal strings
    hex_match = re.match(r"(?:0x|\$)([a-fA-F0-9]+)", s)
    if hex_match:
        return int(hex_match.group(1), 16) & mask

    # Match binary strings
    bin_match = re.match(r"(?:0b|%)([a-fA-F0-9]+)", s)
    if bin_match:
        return int(bin_match, 2) & mask

    # Assume decimal string
    return int(s) & mask
