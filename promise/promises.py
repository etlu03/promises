import functools
import re
import inspect
import sys
import random

from typing import Callable

class PreconditionFailure(Exception):
  '''Precondition unexpectedly failed'''
  
class PostconditionFailure(Exception):
  '''Postcondition unexpectedly failed'''

class CottonFailure(Exception):
  '''Fuzzer has crashed'''

class IncompleteSignatureError(Exception):
  '''Function signature is not fully typed'''

class ParameterCountError(Exception):
  '''The number of provided parameters is greater than two'''

class InvalidFunctionError(Exception):
  '''The provided parameter is not callable'''

class UnsupportedTypeError(Exception):
  '''`cotton()` recieved an unsupported type'''

class InvalidContractError(Exception):
  '''Contract is not safe'''

seperators = r"[(,):\->]"
types = frozenset({"int", "float", "complex", "str", "list", "tuple", "range",
                   "bytes", "bytearray", "memoryview", "dict", "bool", "set",
                   "frozenset"})
cotton_types = frozenset({"int", "str"})

def requires(*expected_args):
  def decorator_requires(func):
    @functools.wraps(func)
    def wrapper_requires(*args, **kwargs):
      if 2 < len(expected_args):
        raise ParameterCountError("`requires()` only takes up to one additional parameter")

      signature = retrieve_signature(func, args)
      if signature is None:
        raise IncompleteSignatureError("The `requires()` function header has type-defined inputs")
      
      contract = create_expression(signature, expected_args[0])

      if len(expected_args) == 2:
        helper = expected_args[1]
        if isinstance(helper, Callable):
          namespace = helper.__name__
          contract = re.sub(rf"\b{namespace}\b", "helper", contract)
        else:
          raise InvalidFunctionError("The provided parameter is not callable")

      if not eval(contract):
        raise PreconditionFailure("A Precondition unexpectly failed")
            
      retval = func(*args, **kwargs)
      return retval
    return wrapper_requires
  return decorator_requires

def ensures(*expected_args):
  def decorator_ensures(func):
    @functools.wraps(func)
    def wrapper_ensures(*args, **kwargs):
      if 2 < len(expected_args):
        raise ParameterCountError("`ensures()` only takes up to one additional parameter")
      
      signature = retrieve_signature(func, args)
      if signature is None:
        raise IncompleteSignatureError("The `ensures()` function header has type-defined inputs")
      
      retval = stringify(func(*args, **kwargs))

      contract = re.sub("\\result", retval, expected_args[0])
      contract = create_expression(signature, contract)

      if len(expected_args) == 2:
        helper = expected_args[1]
        if isinstance(helper, Callable):
          namespace = helper.__name__
          contract = re.sub(rf"\b{namespace}\b", "helper", contract)
        else:
          raise InvalidFunctionError("The provided parameter is not callable")
      
        if not eval(contract):
          raise PostconditionFailure("A Postcondition unexpectly failed")
      
      return restore(retval)

    return wrapper_ensures
  return decorator_ensures

def cotton(*expected_args):
  def decorator_cotton(func):
    @functools.wraps(func)
    def wrapper_cotton(*args, **kwargs):
      if 1 < len(expected_args):
        raise ParameterCountError("`cotton()` only takes to one parameter")
      
      signature = parse_signature(func)
      if signature is None:
        raise IncompleteSignatureError("The `ensures()` function header has type-defined inputs")
      
      testbench = create_testbench(signature, expected_args[0])
      if testbench is None:
        raise UnsupportedTypeError("`cotton()` recieved an unsupported type")
      
      errors = list()
      for test in testbench:
        test = tuple(test)
        try:
          func(*test, **kwargs)
        except:
          errors.append(f"{func.__name__} failed on *arg={test}")

      if len(errors) != 0:
        raise CottonFailure("Fuzzer has crashed")

      return None

    return wrapper_cotton
  return decorator_cotton

def retrieve_signature(func, args):
  signature = parse_signature(func)
  
  for i, key in enumerate(signature):
    if signature[key] not in types:
      return None
    else:
      signature[key] = args[i]
      
  return signature

def parse_signature(func):
  header = str(inspect.signature(func))
  parameters = ((re.sub(seperators, '', header)).split())[:-1]

  signature = {parameters[i]: parameters[i + 1]
               for i in range(0, len(parameters) - 1, 2)}

  return signature

def create_expression(signature, contract):
  for key in signature:
    contract = re.sub(rf"\b{key}\b", stringify(signature[key]), contract)
  
  return contract
  
def int_precondition(testbench, invariant):
  lowerbound, upperbound = -sys.maxsize - 1, sys.maxsize
  if invariant[2] is None:
    for i in range(len(testbench)):
      testbench[i].append(random.randint(lowerbound, upperbound))
    return
    
  if re.search(r"==", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r"==", invariant[2])]
    if tokens[0].isdigit():
      lowerbound = upperbound = int(tokens[0])
    elif tokens[-1].isdigit():
      lowerbound = upperbound = int(tokens[-1])
  
  elif re.search(r"<=.*<=", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<=.*<=", invariant[2])

    lowerbound = int(lowerbound.strip())
    upperbound = int(upperbound.strip())
  
  elif re.search(r">=.*>=", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">=.*>=", invariant[2])

    upperbound = int(upperbound.strip())
    lowerbound = int(lowerbound.strip())
  
  elif re.search(r"<.*<=", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<.*<=", invariant[2])

    lowerbound = int(lowerbound.strip()) + 1
    upperbound = int(upperbound.strip())
  
  elif re.search(r"<=.*<", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<=.*<", invariant[2])

    lowerbound = int(lowerbound.strip())
    upperbound = int(upperbound.strip()) - 1
  
  elif re.search(r">=.*>", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">=.*>", invariant[2])

    upperbound = int(upperbound.strip())
    lowerbound = int(lowerbound.strip()) - 1
  
  elif re.search(r">.*>=", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">.*>=", invariant[2])

    upperbound = int(upperbound.strip()) + 1
    lowerbound = int(lowerbound.strip())

  elif re.search(r"<.*<", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<.*<", invariant[2])

    lowerbound = int(lowerbound.strip()) + 1
    upperbound = int(upperbound.strip()) - 1
        
  elif re.search(r">.*>", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">.*>", invariant[2])

    upperbound = int(upperbound.strip()) + 1
    lowerbound = int(lowerbound.strip()) - 1
      
  elif re.search(r"<=", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r"<=", invariant[2])]
    print(tokens)
    if tokens[0].isdigit():
      lowerbound = int(tokens[0])
    elif tokens[-1].isdigit():
      upperbound = int(tokens[-1])
  
  elif re.search(r">=", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r">=", invariant[2])]
    if tokens[0].isdigit():
      upperbound = int(tokens[0])
    elif tokens[-1].isdigit():
      lowerbound = int(tokens[-1])

  elif re.search(r"<", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r"<", invariant[2])]
    if tokens[0].isdigit():
      lowerbound = int(tokens[0]) + 1
    elif tokens[-1].isdigit():
      upperbound = int(tokens[-1]) - 1
    
  elif re.search(r">", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r">", invariant[2])]
    if tokens[0].isdigit():
      upperbound = int(tokens[0]) - 1
    elif tokens[-1].isdigit():
      lowerbound = int(tokens[-1]) + 1

  for i in range(len(testbench)):
    testbench[i].append(random.randint(lowerbound, upperbound))
  
def str_precondition(testbench, invariant):
  lowerbound, upperbound = 0, 1000
  if invariant[2] is None:
    for i in range(len(testbench)):
      testbench[i].append(random.randint(lowerbound, upperbound))
    return
    
  if re.search(r"==", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r"==", invariant[2])]
    if tokens[0].isdigit():
      lowerbound = upperbound = int(tokens[0])
    elif tokens[-1].isdigit():
      lowerbound = upperbound = int(tokens[-1])
  
  elif re.search(r"<=.*<=", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<=.*<=", invariant[2])

    lowerbound = int(lowerbound.strip())
    upperbound = int(upperbound.strip())
  
  elif re.search(r">=.*>=", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">=.*>=", invariant[2])

    upperbound = int(upperbound.strip())
    lowerbound = int(lowerbound.strip())
  
  elif re.search(r"<.*<=", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<.*<=", invariant[2])

    lowerbound = int(lowerbound.strip()) + 1
    upperbound = int(upperbound.strip())
  
  elif re.search(r"<=.*<", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<=.*<", invariant[2])

    lowerbound = int(lowerbound.strip())
    upperbound = int(upperbound.strip()) - 1
  
  elif re.search(r">=.*>", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">=.*>", invariant[2])

    upperbound = int(upperbound.strip())
    lowerbound = int(lowerbound.strip()) - 1
  
  elif re.search(r">.*>=", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">.*>=", invariant[2])

    upperbound = int(upperbound.strip()) + 1
    lowerbound = int(lowerbound.strip())

  elif re.search(r"<.*<", invariant[2]) is not None:
    lowerbound, upperbound = re.split(r"<.*<", invariant[2])

    lowerbound = int(lowerbound.strip()) + 1
    upperbound = int(upperbound.strip()) - 1
        
  elif re.search(r">.*>", invariant[2]) is not None:
    upperbound, lowerbound = re.split(r">.*>", invariant[2])

    upperbound = int(upperbound.strip()) + 1
    lowerbound = int(lowerbound.strip()) - 1
      
  elif re.search(r"<=", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r"<=", invariant[2])]
    print(tokens)
    if tokens[0].isdigit():
      lowerbound = int(tokens[0])
    elif tokens[-1].isdigit():
      upperbound = int(tokens[-1])
  
  elif re.search(r">=", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r">=", invariant[2])]
    if tokens[0].isdigit():
      upperbound = int(tokens[0])
    elif tokens[-1].isdigit():
      lowerbound = int(tokens[-1])

  elif re.search(r"<", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r"<", invariant[2])]
    if tokens[0].isdigit():
      lowerbound = int(tokens[0]) + 1
    elif tokens[-1].isdigit():
      upperbound = int(tokens[-1]) - 1
    
  elif re.search(r">", invariant[2]) is not None:
    tokens = [tok.strip() for tok in re.split(r">", invariant[2])]
    if tokens[0].isdigit():
      upperbound = int(tokens[0]) - 1
    elif tokens[-1].isdigit():
      lowerbound = int(tokens[-1]) + 1
  
  for i in range(len(testbench)):
    string = str()
    length = random.randint(lowerbound, upperbound)
    for _ in range(length):
      lower = random.randint(0, 1)
      if lower == 0:
        string += chr(random.randint(65, 90))
      else:
        string += chr(random.randint(97, 122))
    testbench[i].append(string)
  
  print(testbench)

def create_testbench(signature, contract):
  testbench = [[] for _ in range(100)]
  for var in signature:
    if signature[var] not in cotton_types:
      return None
    
  preconditions = [condition.strip() for condition in re.split(r"\bor\b|\band\b", contract)]
  variables = list()
  for var in signature:
    for invariant in preconditions:
      if var in invariant:
        variables.append((var, signature[var], invariant))
        break
    else:
      variables.append((var, signature[var], None))
  
  for invariant in variables:
    if invariant[1] == "int":
      int_precondition(testbench, invariant)
    elif invariant[1] == "str":
      str_precondition(testbench, invariant)
    
  return testbench

def stringify(val):
  if isinstance(val, str):
    val = "'" + val + "'"
  
  return str(val)

def restore(retval):
  if retval[0] == '"' and retval[-1] == '"':
    retval = retval[1: -2]
    return retval

  return eval(retval)

@cotton("0 < len(s) < 2")
def f(s: str) -> str:
  return s

f("hello")