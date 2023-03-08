###############################################################################
# @file  cotton_integers.py
# @brief The following test cases apply the `promises` package fuzzer againist
#        faulty functions
###############################################################################

from promise import promises

@promises.cotton("0 < x")
def f(x: int) -> int:
  if x == 10:
    raise ValueError("f caught a 10")

  return x

@promises.cotton("x <= 100")
def g(x: int) -> int:
  if x == 100:
    raise ValueError("g caught a 100")

  return x

@promises.cotton("x > 100")
def h(x: int) -> int:
  if x == 101:
    raise ValueError("h caught a 101")

  return x

@promises.cotton("x >= 100")
def i(x: int) -> int:
  if x == 102:
    raise ValueError("i caught a 102")

  return x

@promises.cotton("8 < x < 10")
def j(x: int) -> int:
  if x == 9:
    raise ValueError("j caught a 9")

  return x

@promises.cotton("10 <= x < 100")
def k(x: int) -> int:
  if x == 33:
    raise ValueError("k caught a 33")

  return x

@promises.cotton("10 <= x <= 100")
def l(x: int) -> int:
  if x == 32:
    raise ValueError("l caught a 32")

  return x

@promises.cotton("10 < x <= 50")
def m(x: int) -> int:
  if x == 50:
    raise ValueError("m caught a 50")

  return x

@promises.cotton("60 > x > 40")
def n(x: int) -> int:
  if x == 50:
    raise ValueError("n caught a 50")

  return x

@promises.cotton("11 > x >= 9")
def o(x: int) -> int:
  if x == 9:
    raise ValueError("o caught a 9")

  return x

@promises.cotton("11 >= x >= 9")
def p(x: int) -> int:
  if x == 11:
    raise ValueError("p caught a 11")

  return x

@promises.cotton("11 >= x > 10")
def q(x: int) -> int:
  if x == 11:
    raise ValueError("q caught a 11")

  return x

@promises.cotton("x == 10")
def r(x: int) -> int:
  if x == 10:
    raise ValueError("r caught a 10")

  return x

def main():
  f(); g(); h();
  i(); j(); k();
  l(); m(); n();
  o(); p(); q();
  r();

if __name__ == "__main__":
  main()