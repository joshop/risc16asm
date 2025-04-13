/*
  Assembler for our 16-bit risc-based assembly
*/

#include "parser.h"

using namespace std;

int main() {
  string s = "addi x0, x0, x0";
  parse_line(s);

  return 0;
}
