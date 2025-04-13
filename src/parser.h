#include "common.h"
#include "utils/split_string.h"

using namespace std;

int parse_line(string line) {
  // Parse a single line of assembly

  vector<string> parts = resplit(line);
  for (string s : parts) {
    cout << s << ", ";
  }
  cout << "\n";

  return 0;
}
