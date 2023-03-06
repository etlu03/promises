## Abstract
Contracts are program annotations that spell out what the code is supposed to do. They assist software designers in making connecting their algorithmic to their implementation as programs. The main purpose of contract programming is to ensure all that components of a software system agrees on how to interact with each other. Contracts aim to guarantee the correctness and safety of each isolated component before they are meshed together into a large system.

Since that Python does not natively support contracts as a language feature, programmers have created various libraries to implement contracts on Python's behalf. However, most of the existing libraries do not implement contracts in a Pythonic way. For example, the `pcd` library chose to specify functions used in the pre- and post-conditions with a lambda function which clutters the decorators with unnecessary information.

The `promises` package is a port of the pre- and post-conditions utilized in `c0`, the programming language used in CS 15-122: Principles of Imperative Computation at Carnegie Mellon University. We are able to more cleanly represent pre-conditions with the `requires` decorator and post-conditions with the `ensures` decorator.

## Documentation
The `promises` package defines the following functions:
```python
requires(expected_args=[contract: str, function: func or None])
```
The `contract` should be a valid pre-condition of the decorated function. <br />
The `supplement` should be additional function that will be referenced by the pre-condition. <br />
```python
ensures(expected_args=[contract: str, function: func or None])
```
The `contract` should be a valid post-condition of the decorated function. <br />
The `supplement` should be additional function that will be referenced by the post-condition. <br />

## Comparison
A code snippet utilizing `pcd` (directly from the `pcd` README.rst):
```python
from pcd import contract

@contract(post=lambda r: isinstance(r, dict))
def get_user_input():
    input = {}
    while True:
        try:
            key, value = raw_input('<key>,<value> or <return>: ').split(',')
            input[key] = value
        except ValueError:
            break
    return process_input(input)

@contract(pre=lambda: isinstance(input, dict),
          post=lambda r: isinstance(r, dict))
def process_input(input):
    cleaned = {}
    for key, value in input.items():
        cleaned[clean_value(key)] = clean_value(value)
    return cleaned

@contract(pre=lambda: isinstance(value, str) or
                      isinstance(value, unicode))
def clean_value(value):
    return value.strip()
```
The same code snippet as above rewritten with `promises` contracts:
```python
from promises import promise

@promise.ensures("isinstance(result, dict)")
def get_user_input():
    input = {}
    while True:
        try:
            key, value = raw_input('<key>,<value> or <return>: ').split(',')
            input[key] = value
        except ValueError:
            break
    return process_input(input)

@promise.requires("isinstance(input, dict)")
@promise.ensures("isinstance(result, dict)")
def process_input(input):
    cleaned = {}
    for key, value in input.items():
        cleaned[clean_value(key)] = clean_value(value)
    return cleaned

@promise.requires("isinstance(value, str) or
                   isinstance(value, unicode)")
def clean_value(value):
    return value.strip()
```
Contracts written with `promises` are simpler and less abrasive. Designers do not need to fiddle around with a lambda functions to write good contracts. In addition, `promises` supports passing in an addition function to with its contracts. The following example will illustrate how a helper function as be used with a `requires` decorator.
```python
from promises import promise
def is_prime(x):
  if x < 2:
    return False
  
  for i in range(2, int(x ** 0.5) + 1):
    if x % i == 0:
      return False
  
  return True

@promise.requires("is_prime(x) and is_prime(y)",
                   is_prime)
def rsa_encryption(x, y):
    return x * y
```
## Installation
The `promises` package can be installed by cloning this repository into your working directory and running the following command:
```
> python setup.py install
```
From there, the package can be imported into your working file with the following import statement:
```python
from promises import promise
```
## Shortcomings
The `promises` package does not come without its shortcomings.
### Security
There is a critical security flaw within the implementation of the `promises` package. The `promises` package use `eval()` to parse contracts. Malicious users can use the `promises` package as a mechanism to execute malicious scripts on other machines. A common attack will utilize the `os` module. <br />
**DO NOT RUN CODE YOU DO NOT UNDERSTAND!!!**
### Classes
As of version 1.0.0, the `promises` package can not be utilized to ensure the correctness and safety of functions within classes.
### Other Packages and Modules
As of version 1.0.0, the user will need to explicitly write import statements in `promises/promise.py` if they wish to have contracts that utilize functions from other packages and modules. Please check `promises/promise.py` for more about this.
