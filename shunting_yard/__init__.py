from shunting_yard.rpn import compute_rpn, Number
from shunting_yard.shunting_yard import shunting_yard
from shunting_yard.tokenize import tokenize

def compute(expression: str) -> Number:
    """Compute the value of a mathematical expression. Equivalent to compute_rpn(shunting_yard(expression)).
    Check the docstring of these functions for more details.

    Args:
        string (str): string containing the mathematical expression to compute.

    Returns:
        Number: Result.
    """
    return compute_rpn(shunting_yard(expression))
