###############################################################################
# @file  promises_strings.py
# @brief The following test cases apply the `promises` package againist
#        function that manipulate strings
###############################################################################

from promise import promises

@promises.ensures("\result[len(s) + 1: len(p)] == from + name")
def reply(s: str, name: str) -> str:
  return s + " from " + name

@promises.ensures("len(s) + len(s) == len(\result)")
@promises.ensures("\result = 2 * s")
def double(s: str) -> str:
  return s + s

@promises.requires("s.isalpha()")
def lower_case(s: str) -> str:
  upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  lower = "abcdefghijklmnopqrstuvwxyz"

  new_string = str()
  for i in range(len(s)):
    ii = upper.index(s[i])
    new_string += lower[ii]
      
  return new_string

def main() -> None:
  s, name = "Hello", "Your Boss"
  email = reply(s, name)
  assert(email == "Hello from Your Boss")

  s, name = "Have a nice weekend", "Your Manager"
  email = reply(s, name)
  assert(email == "Have a nice weekend from Your Manager")

  double_email = double(email)
  assert(double_email == email + email)

  s = "EMAILMENOW"
  lower_s = lower_case(s)
  s = s.lower()
  assert(lower_s == s)

  # testing contract failures
  try:
    lower = lower_case("bad string")
  except:
    pass

  try:
    lower = lower_case("badstring1")
  except:
    pass

  print("No contract fails in promises_strings.py. This is good")

if __name__ == "__main__":
  main()