import functools
import re
import inspect
import sys

from typing import Callable

class PreconditionFailure(Exception):
  '''Precondition Unexpectedly Failure'''
  
class PostconditionFailure(Exception):
  '''Postcondition Unexpectedly Failure'''

class IncompleteSignatureError(Exception):
  '''Function signature is not fully typed'''

class ParameterCountError(Exception):
  '''The number of provided parameters is greater than two'''

class InvalidFunctionError(Exception):
  '''The provided parameter is not callable'''

class InvalidContractError(Exception):
  '''Contract is not safe'''

seperators = r"[(,):\->]"
types = frozenset({"int", "float", "complex", "str", "list", "tuple", "range",
                   "bytes", "bytearray", "memoryview", "dict", "bool", "set",
                   "frozenset"})

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
      pass

    return wrapper_cotton
  return decorator_cotton

def retrieve_signature(func, args):
  header = str(inspect.signature(func))
  parameters = ((re.sub(seperators, '', header)).split())[:-1]
  
  signature = {parameters[i]: parameters[i + 1]
               for i in range(0, len(parameters) - 1, 2)}
  
  for i, key in enumerate(signature):
    if signature[key] not in types:
      return None
    else:
      signature[key] = args[i]
      
  return signature

def create_expression(signature, contract):
  for key in signature:
    contract = re.sub(rf"\b{key}\b", stringify(signature[key]), contract)
  
  return contract

def stringify(val):
  if isinstance(val, str):
    val = "'" + val + "'"
  
  return str(val)

def restore(retval):
  if retval[0] == '"' and retval[-1] == '"':
    retval = retval[1: -2]
    return retval

  return eval(retval)