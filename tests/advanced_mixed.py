###############################################################################
# @file  advanced_mixed.py
# @brief The following test cases apply the `promises` package againist
#        a mix of function while still ensuring correct behavior
###############################################################################

from promise import promises
import random

@promises.requires("2 <= len(A)")
@promises.ensures("len(\result) == 2")
def double_pop(A: list) -> tuple:
  a, b = A.pop(), A.pop()
  return (b, a)

def has_negatives(A: list) -> bool:
  for x in A:
    if x < 0:
      return False
  
  return True

@promises.ensures("has_negatives(A)", has_negatives)
def remove_negatives(A: list) -> list:
  i, negatives = 0, list()
  while i < len(A):
    if A[i] < 0:
      negatives.append(A.pop(i))
    else:
      i += 1
  
  return negatives

def has_positives(A: list) -> bool:
  for x in A:
    if 0 <= x:
      return False
  
  return True

@promises.ensures("has_positives(A)", has_positives)
def remove_positives(A: list) -> list:
  i, positives = 0, list()
  while i < len(A):
    if A[i] >= 0:
      positives.append(A.pop(i))
    else:
      i += 1
  
  return positives

@promises.ensures("\result == 1")
def f(x: int) -> int:
  return 1

@promises.ensures("\result == 1")
def g(x: int) -> int:
  return 1

@promises.ensures("\result == 2")
def h(x: int) -> int:
  return f(x) + g(x)

@promises.requires("1 + 1 == 2")
@promises.requires("len([1, 2, 3]) == 3")
@promises.requires("len((1, 2, 3)) == 3")
@promises.requires("len({1, 2, 3}) == 3")
@promises.requires("'hello' in 'hello world'")
@promises.ensures("\result == 0")
@promises.ensures("True and True")
@promises.ensures("len((1, 2, 3)) == 3")
@promises.ensures("'goodnight' in 'goodnight moon'")
@promises.ensures("True")
@promises.ensures("True or False")
@promises.ensures("h(x) == 2", h)
def unnecessary_contracts(x: int) -> int:
  return 0

def main() -> None:
  A = [1, 2, 3, 4, 5, 6, 7, 8]
  t = double_pop(A)
  assert(t == (7, 8))

  t = double_pop(A)
  assert(t == (5, 6))

  t = double_pop(A)
  assert(t == (3, 4))

  t = double_pop(A)
  assert(t == (1, 2))

  assert(len(A) == 0)

  try:
    t = double_pop(A)
  except:
    pass

  A = [-1, 0, 1, 2, 3]
  a1 = remove_negatives(A)
  assert(a1 == [-1])

  a2 = remove_positives(A)
  assert(a2 == [0, 1, 2, 3])

  r = random.randint(1, 20)
  for i in range(r):
    b = h(i)
    assert(b == 2 * g(i))

  unnecessary_contracts(0)
  unnecessary_contracts(1)
  unnecessary_contracts(2)
  unnecessary_contracts(3)
  unnecessary_contracts(4)

  print("No contract fails in advanced_mixed.py. This is good")

if __name__ == "__main__":
  main()