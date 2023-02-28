import math
from operator import add, sub, mul, truediv
from typing import Union

from shunting_yard.constants import NUMBER_CHARS


Number = Union[int, float]

FUNCTIONS: dict[str, tuple[int, callable]] = {
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
    'abs': (2, abs)
}


def compute_rpn(rpn: str) -> Number:
    """Compute the value of an expression in the Reverse Polish Notation format (see https://en.wikipedia.org/wiki/Reverse_Polish_notation for more details).
    The included function are the five base operations (+-*/^), sin, cos, tan, sqrt, abs, min, max and e and pi as constants.

    >>> compute_rpn("1 2 3 * +")
    7

    >>> compute_rpn("1 2 * 3 +")
    5

    >>> compute_rpn("pi 2 / sin")
    1.0

    Args:
        rpn (str): RPN expression.

    Raises:
        ValueError: raised if an unknown function is in the expression.

    Returns:
        Number: The result of the operation.
    """

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
                parameters = stack[-param_count:]
                stack = stack[:-param_count]
            else:
                parameters = []

            stack.append(func(*parameters))

    return stack[0]
