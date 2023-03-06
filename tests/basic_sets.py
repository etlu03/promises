###############################################################################
# @file  basic_sets.py
# @brief The following test cases apply the `promises` package againist
#        function that manipulate sets and dictionaries
###############################################################################

from promise import promises
from collections import Counter

@promises.ensures("len(\result) <= len(A) \
                  and len(\result) <= len(B)")
@promises.ensures("\result == (A & B)")
def set_intersection(A: set, B: set) -> set:
  C = set()
  for x in A:
    if x in B:
      C.add(x)
    
  return C

@promises.ensures("len(A) <= len(\result) and len(B) <= len(\result)")
@promises.ensures("\result == (A | B)")
def set_addition(A: set, B: set) -> set:
  C = set()
  for x in A:
    C.add(x)

  for y in B:
    C.add(y)
  
  return C

@promises.requires("0 < len(A)")
@promises.ensures("len(A) == len(\result)")
def set_double(A: set) -> set:
  return A | A

@promises.ensures("len(A) == 0")
def clear_set(A: set) -> set:
  B = list(A)
  for x in B:
    A.remove(x)

@promises.ensures("len(\result) <= len(s)")
def frequency(s: str) -> dict:
  D = dict()
  for c in s:
    if c in D:
      D[c] += 1
    else:
      D[c] = 1
  
  return D

# helper function
def is_cleared(D: dict) -> bool:
  for key in D:
    if D[key] != 0:
      return False
  
  return True

@promises.ensures("is_cleared(D)", is_cleared)
def clear_dict(D: dict) -> None:
  for key in D:
    D[key] = 0;

def main() -> None:
  A, B = {1, 2}, {2, 3}
  C = set_intersection(A, B)
  assert(C == {2})

  C = set_addition(A, C)
  assert(A == C)

  C = set_addition(B, C)
  assert(C == (A | B))

  D = set_double(C)
  assert(D == C)

  D = set_double(D)
  D = set_double(D)
  assert(D == C)

  clear_set(A)
  clear_set(B)
  clear_set(C)
  clear_set(D)
  assert(A == B and B == C and C == D)

  s = "hello"
  f = frequency(s)
  assert(f == Counter(s))

  s = "hello world"
  f = frequency(s)
  assert(f == Counter(s))

  s = "good night moon"
  f = frequency(s)
  assert(f == Counter(s))

  print("No contract fails in basic_set.py. This is good")

if __name__ == "__main__":
  main()