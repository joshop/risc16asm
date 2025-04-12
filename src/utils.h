/*
  Utility methods for:
    1. converting string constants like "42", "-1", "0xf8", "0b1001"
       to fixed bit-widths
*/

#include "common.h"

using namespace std;

// Convert constant to integer of fixed bit width.
//    1. Excess bits get truncated from the left.
//    2. We use stoi, so we stop at invalid chars.

template <size_t N>
bitset<N> parse_const(string s) {
  // Detect hex values
  string hex_value = "";
  if (s.substr(0, 1) == "$") hex_value = s.substr(1);
  if (s.substr(0, 2) == "0x") hex_value = s.substr(2);
  if (hex_value != "") {
    return bitset<N>(stoi(hex_value, NULL, 16));
  }

  // Detect binary values
  string bin_value = "";
  if (s.substr(0, 1) == "%") bin_value = s.substr(1);
  if (s.substr(0, 2) == "0b") bin_value = s.substr(2);
  if (bin_value != "") {
    return bitset<N>(stoi(bin_value, NULL, 2));
  }

  // Assume decimal value
  return bitset<N>(stoi(s, NULL, 1));
}
