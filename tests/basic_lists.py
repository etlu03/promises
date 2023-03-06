###############################################################################
# @file  basic_lists.py
# @brief The following test cases apply the `promises` package againist
#        function that manipulate lists
###############################################################################

from promise import promises

@promises.ensures("len(\result) == n")
def generate_list(n: int) -> list:
  A = list()
  for _ in range(n):
    A.append(0)

  return A

@promises.ensures("A == sorted(A)")
def selection_sort(A: list) -> list:
  for i in range(len(A)):
    min_i = i
    for j in range(i + 1, len(A)):
      if A[j] < A[min_i]:
        min_i = j
    A[i], A[min_i] = A[min_i], A[i]

@promises.requires("A == sorted(A)")
def math_range(A: list) -> int:
  return A[len(A) - 1] - A[0]

@promises.requires("0 <= i < len(A)")
@promises.requires("0 <= j < len(A)")
@promises.requires("i <= j")
@promises.ensures("\result == A[i: j]")
def list_splice(A: list, i: int, j: int) -> list:
  B = list()
  for ii in range(len(A)):
    if i <= ii < j:
      B.append(A[ii])
  
  return B

def main() -> None:
  A = generate_list(10)
  A[0: 5 ] = [10, 9, 8, 7, 6]
  A[5: 10] = [ 1, 2, 3, 4, 5]
  selection_sort(A)
  assert(A == list(range(1, 11)))
  
  a = math_range(A)
  b = A.pop(0); c = A.pop(-1)
  assert(a == (c - b))

  B = list_splice(A, 1, 1)
  assert(B == list())

  # testing contract failures
  try:
    C = list_splice(A, -1, 1)
  except:
    pass

  try:
    C = list_splice(A, 1, -1)
  except:
    pass

  try:
    C = list_splice(A, 3, 2)
  except:
    pass

  try:
    C = list_splice(A, 0, len(A))
  except:
    pass
  
  try:
    C = list_splice(A, len(A) + 1, len(A) + 2)
  except:
    pass

  print("No contract fails in basic_lists.py. This is good")
  
if __name__ == "__main__":
  main()