import math
from operator import add, mul, sub, truediv
from typing import Any, Callable, Optional, Union

from shunting_yard.constants import NUMBER_CHARS


class WrongExpressionError(Exception):
    pass


Number = Union[int, float]
FunctionDictionary = dict[str, tuple[int, Callable[[Any], Number]]]

FUNCTIONS: FunctionDictionary = {
    '+': (2, add),
    '-': (2, sub),
    '*': (2, mul),
    '/': (2, truediv),
    '^': (2, pow),
    'pi': (0, lambda:math.pi),
    'e': (0, lambda:math.exp(1)),
    'sqrt': (1, math.sqrt),
    'sin': (1, math.sin),
    'cos': (1, math.cos),
    'tan': (1, math.tan),
    'min': (2, min),
    'max': (2, max),
    'abs': (1, abs)
}


def compute_rpn(rpn: str, additional_functions: Optional[FunctionDictionary] = None) -> Number:
    """Compute the value of an expression in the Reverse Polish Notation format (see https://en.wikipedia.org/wiki/Reverse_Polish_notation for more details).
    The included function are the five base operations (+-*/^), sin, cos, tan, sqrt, abs, min, max and e and pi as constants.
    The additional_functions parameters enables more function to be used in the computation. See below for its format.


    >>> compute_rpn("1 2 3 * +")
    7

    >>> compute_rpn("1 2 * 3 +")
    5

    >>> compute_rpn("pi 2 / sin")
    1.0

    Args:
        rpn (str): RPN expression.
        additional_functions (FunctionDictionary): dictionary containing more functions. The keys should be string, and the values should be a tuple
        containing first the number of parameters of the function (>= 0), and then the function itself. For example {'inc': (1, lambda x:x+1)} will
        enable the computation to use the inc function. If the function exists by default, it will be overwritten.

    Raises:
        ValueError: raised if an unknown function is in the expression.

    Returns:
        Number: The result of the operation.
    """

    functions = FUNCTIONS
    if additional_functions is not None:
        functions = functions.update(additional_functions)

    stack: list[Number] = []

    for token in rpn.split():
        if token[0] in NUMBER_CHARS:
            # Convert to float or int according to the presence of a dot
            stack.append(float(token) if '.' in token else int(token))
        else:
            if not token in FUNCTIONS:
                raise ValueError(f'Unknown function : {token}')

            param_count, func = FUNCTIONS[token]

            # Seperate both cases because l[-0:] is all the list and not an empty one
            if param_count > 0:
                if len(stack) < param_count:
                    raise WrongExpressionError(f"Not enough parameters for function '{token}' : {len(stack)} found, {param_count} expected.")
                parameters = stack[-param_count:]
                stack = stack[:-param_count]
            else:
                parameters = []

            stack.append(func(*parameters))

    if len(stack) > 1:
        raise WrongExpressionError(f"Expression does not give only one result.")

    return stack[0]
