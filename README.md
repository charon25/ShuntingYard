# Shuting-yard algorithm

This repo is a Python (>= 3.9) module containing an implementation of the [Shunting-yard algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm), which converts any "regular" mathematical expression into its [Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation) equivalent, and then can evaluate it.

# Installation

To install it, just run :

```bash
pip install <TODO> --user
```

Or alternatively you can use :

```bash
git clone https://github.com/charon25/ShuntingYard.git
cd ShuntingYard
python setup.py install --user
```

# Usage

Either use it directly in a command line interface with :

```bash
python -m shunting_yard <expression>
```

For instance :

```bash
>>> python -m shunting_yard "1 + cos(pi)"

1 + cos(pi) = 0.0
```

Or you can use it in a Python script with :

```python
import shunting_yard as sy

print(sy.compute("2^32 - sqrt(tan(42))"))
```

## Allowed functions

By default, the module can process the 5 basic operations (`+`, `-`, `*`, `/`, `^`) as well as those functions :
 - sqrt
 - sin, cos, tan
 - min, max (with 2 arguments)
 - abs

As well as the constants `pi` and `e`.

These operations and functions can be mixed however you want.

Furthermore, you can add more functions with the optional parameters `additional_functions` of the `sy.compute` function. It should be a dictionary whose keys are string, and values are a tuple containing first the number of expected argument to the function, and then the function itself. For example :

```python
import math

additional_functions = {
    'gamma': (0, lambda:0.5772156649015329), # create new constant
    'inc': (1, lambda x:x + 1), # using lambda
    'exp': (1, math.exp), # using already existing functino
    'gcd3': (3, math.gcd) # 3 parameters
}
```

## Additional features

Instead of just calling the `sy.compute` function, you can break it into its parts :
 - `sy.shunting_yard` will return the RPN equivalent expression of the given mathematical expression ;
 - `sy.compute_rpn` will use this expression and compute its value (use the `additional_functions` parameters here).

Furthermore, you can just use the `sy.tokenize` function to transform a mathematical expression into its base components (returns a generator).

Examples :

```python
import shunting_yard as sy

print(sy.shunting_yard('2 * sin(5/2)'))
# 2 5 2 / sin *

print(sy.compute_rpn('pi 2 / sin'))
# 1.0

print(sy.compute_rpn('3 inc', {'inc': (1, lambda x:x + 1)}))
# 4

print(list(sy.tokenize('1+(2 * 3) - 4 * (2 / 3)')))
# ['1', '+', '(', '2', '*', '3', ')', '-', '4', '*', '(', '2', '/', '3', ')']

```
