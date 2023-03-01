from typing import Optional

from shunting_yard.rpn import compute_rpn, FunctionDictionary, Number, WrongExpressionError
from shunting_yard.shunting_yard import MismatchedBracketsError, shunting_yard
from shunting_yard.tokenize import tokenize


def compute(expression: str, additional_functions: Optional[FunctionDictionary] = None) -> Number:
    """Compute the value of a mathematical expression. Equivalent to compute_rpn(shunting_yard(expression), additional_functions).
    Check the docstring of these functions for more details.

    Args:
        string (str): string containing the mathematical expression to compute.

    Returns:
        Number: Result.
    """
    return compute_rpn(shunting_yard(expression), additional_functions)
