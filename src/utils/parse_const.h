/*
  Utility methods for:
    1. converting string constants like "42", "-1", "0xf8", "0b1001"
       to fixed bit-widths
*/

#include "../common.h"

using namespace std;

// Convert constant to integer of fixed bit width.
//    1. Excess bits get truncated from the left.
//    2. We use stoi, so we stop at invalid chars.

int parse_const(string s) {
  // Detect hex values
  regex hex_pattern("0x([0-9a-fA-F]+)");
  smatch hex_match;
  if (regex_search(s, hex_match, hex_pattern)) {
    string hex_string = hex_match[1].str();
    return stoi(hex_string, NULL, 16);
  }

  // Detect binary values
  regex bin_pattern("^(?:%|0b)([01]+)$");
  smatch bin_match;
  if (regex_search(s, bin_match, bin_pattern)) {
    string bin_string = bin_match[1].str();
    return stoi(bin_string, NULL, 2);
  }

  // Assume decimal value
  return stoi(s, NULL, 10);
}
