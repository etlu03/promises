###############################################################################
# @file  promises_functions.py
# @brief The following test cases apply the `promises` package againist
#        function that need additional helper functions for verification
###############################################################################

from promise import promises

def is_prime(n: int) -> bool:
  if n <= 2: return True

  for i in range(2, n):
    if n % i == 0:
      return False
  
  return True

@promises.requires("0 < p and 0 < q")
@promises.requires("is_prime(p) and is_prime(q)", is_prime)
def rsa_cipher(p: int, q: int) -> int:
  return p * q

def is_pretend_linked_list(L: list) -> bool:
  for x in L:
    if isinstance(x, list) and len(x) != 1:
      return False
  
  return True

@promises.requires("is_pretend_linked_list(L)", is_pretend_linked_list)
def sum_linked_list(L: list) -> int:
  total = 0
  for x in L:
    total += x[0]
  
  return total

def main():
  p, q = 2, 5
  N = rsa_cipher(p, q)
  assert(N == p * q)

  p, q = 7, 17
  N = rsa_cipher(p, q)
  assert(N == p * q)

  p, q = 101, 71
  N = rsa_cipher(p, q)
  assert(N == p * q)

  linked_list = [[1], [2], [3], [4], [5]]
  s = sum_linked_list(linked_list)
  assert(s == 15)

  # testing contract failures
  try:
    N = rsa_cipher(p, s)
  except:
    pass

  try:
    L = [[1], [1], [1, 2]]
  except:
    pass

  try:
    L = [[1, 2, 3, 4, 5], [1], [1], [1], [1], [1]]
  except:
    pass

  try:
    p, q = 3, 4
    N = rsa_cipher(p, q)
  except:
    pass

  try:
    p = 3
    q = 2 * p
    N = rsa_cipher(p, q)
  except:
    pass

  print("No contract fails in promises_function.py. This is good")

if __name__ == "__main__":
  main()