###############################################################################
# @file  basic_math.py
# @brief The following test cases apply the `promises` package againist
#        function with simple contracts
###############################################################################

from promise import promises

@promises.requires("0 < L and 0 < H")
@promises.ensures("0 < \result")
def area_of_rectangle(L: int, H: int) -> int:
  return L * H

@promises.requires("0 < L and 0 < H and 0 < W")
@promises.ensures("0 < \result")
def volume(L: int, H: int, W: int) -> int:
  return L * H * W

@promises.requires("0 < A")
def is_square(A: int) -> bool:
  side = int(A ** 0.5)
  return (side ** 2) == A

@promises.requires("0 < n")
@promises.ensures("n + n == \result")
def double(n: int) -> int:
  return n << 1

@promises.requires("0 < n")
@promises.ensures("n // 2 == \result")
def half(n: int) -> int:
  return n >> 1

def main() -> None:
  L, H, W = 3, 3, 3
  A = area_of_rectangle(L, W)
  assert(A == L * W)

  V = volume(L, H, W)
  assert(V == L * H * W)
  
  square = is_square(A)
  assert(square)

  L, H, W = 3, 4, 5
  A = area_of_rectangle(L, W)
  assert(A == L * W)

  V = volume(L, H, W)
  assert(V == L * H * W)
  
  square = is_square(A)
  assert(not square)

  B = double(A)
  assert(B == 2 * A)

  B = half(B)
  assert(A == B)

  A = double(A)
  A = double(A)
  B = double(B)

  assert(half(A) == B)
  assert(A == double(B))

  B = double(B)
  assert(A == B)

  # testing post-condition failures
  try:
    C = double(-1)
  except:
    pass

  try:
    D = half(0)
  except:
    pass

  try:
    C = double(10)
    D = half(C)
    D = double(D)
    assert(D == C)
    E = double(-C)
  except:
    pass

  print("No contract fails in basic_math.py. This is good")

if __name__ == "__main__":
  main()