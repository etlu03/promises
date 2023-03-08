###############################################################################
# @file  cotton_integers.py
# @brief The following test cases apply the `promises` package fuzzer againist
#        faulty functions
###############################################################################

from promise import promises

@promises.cotton("0 <= x <= 100")
def f(x: int) -> int:
  if x == 7:
    raise ValueError("f recieved a 7")
  
  if x == 12:
    raise ValueError("f recieved a 12")
  
  if x == 20:
    raise ValueError("f recieved a 99")
  
  if x == 31:
    raise ValueError("f recieved a 99")

  if x == 99:
    raise ValueError("f recieved a 99")
  
  return x

@promises.cotton("x == 1 and 0 < y < 100")
def g(x: int, y: int) -> int:
  if (x + y) % 5 == 0:
    raise ValueError("x + y is a multiple of 5")

  return x + y

@promises.cotton("0 <= x < 7 and 50 < z <= 100 and 10 < y < 12")
def h(x: int, y: int, z: int) -> int:
  if (x + y + z) < 100:
    raise ValueError("x + y is a multiple of 5")
  
  return x - y - z

def main():
  f(); g(); h()

if __name__ == "__main__":
  main()