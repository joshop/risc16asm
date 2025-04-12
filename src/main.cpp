/*
  Assembler for our 16-bit risc-based assembly
*/

#include "common.h"
#include "types.h"
#include "utils.h"

using namespace std;

int main() {
  string s = "0b101010";
  Word x = parse_const<16>(s);

  cout << x << "\n";

  return 0;
}
