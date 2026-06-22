/*
  Parse immediate value as a signed integer with specified width
  Used by interpreter for sign extension
 */
export function parseImm(imm, width) {
  // Check assertions
  if (width <= 0) {
    throw new Error(`parseImm: nonzero width ${width}`);
  }
  if (imm < 0) {
    throw new Error(`parseImm: expected nonnegative imm, got ${imm}`);
  }
  if (imm >= 1 << width) {
    throw new Error(`parseImm: imm ${imm} does not fit in ${width} bits`);
  }

  // Sign extend if MSB is set
  if (imm & (1 << (width - 1))) {
    return imm - (1 << width);
  }
  return imm;
}

// Format integer as 16-bit hex string
export function fmtHex(x) {
  return `h'${x.toString(16).padStart(4, '0')}`;
}
