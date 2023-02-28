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
    'sin': (1, math.sin),
    'cos': (1, math.cos),
    'tan': (1, math.tan),
    'min': (2, min),
    'max': (2, max),
    'abs': (2, abs)
}


def compute_rpn(rpn: str) -> Number:
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
