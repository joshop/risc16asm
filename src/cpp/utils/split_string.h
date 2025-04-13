#include "../common.h"

using namespace std;

std::vector<std::string> resplit(
    const std::string &s,
    const std::regex &sep_regex = std::regex{"\\s+"}) {
  std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
  std::sregex_token_iterator end;
  return {iter, end};
}
