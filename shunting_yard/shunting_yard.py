from string import ascii_lowercase
import math
from enum import Enum
from typing import Optional

from shunting_yard.tokenize import tokenize
from shunting_yard.constants import BASE_OPERATORS, NUMBER_CHARS, FUNCTION_CHARS, SEPARATORS, SEPARATORS_NO_CLOSING_BRACKET, UNARY_OPERATORS_SYMBOLS


class MismatchedBracketsError(Exception):
    pass


OPERATORS_PRECEDENCE: dict[str, int] = {
    '+': 10,
    '-': 10,
    '*': 20,
    '/': 20,
    '^': 30,
    '-u': 40,
    '+u': 40,
}

# Returns the precendence if the operator is one of +-*/^, or infinity if it is a function
def get_precedence(operator: str):
    return OPERATORS_PRECEDENCE.get(operator, math.inf)

class Associativity(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

OPERATORS_ASSOCIATIVITY: dict[str, Associativity] = {
    '+': Associativity.LEFT,
    '-': Associativity.LEFT,
    '*': Associativity.LEFT,
    '/': Associativity.LEFT,
    '^': Associativity.RIGHT,
    '-u': Associativity.RIGHT,
    '+u': Associativity.LEFT,
}



# Reference : https://en.wikipedia.org/wiki/Shunting_yard_algorithm
def shunting_yard(expression: str, case_sensitive: bool = True, variable: Optional[str] = None) -> str:
    """Convert the given classical math expression into Reverse Polish Notation using the Shunting-yard algorithm (see https://en.wikipedia.org/wiki/Shunting_yard_algorithm for more details). All whitespace are ignored.


    >>> shuting_yard("1 + 2")
    '1 2 +'

    >>> shuting_yard("sin(max(2, 3) / 3 * pi)")
    '2 3 max 3 / pi * sin'


    Args:
        expression (str): string containing the mathematical expression to convert.
        case_sensitive (bool): indicates whether the expression should care about case.
        variable (str, optional): if defined, will treat every token matching the variable as a number.

    Raises:
        MismatchedBracketsError: raised if the bracket are unbalanced.


    Returns:
        str: The RPN expression corresponding to the mathematical expression.
    """
    output: list[str] = []
    operator_stack: list[str] = []

    if not case_sensitive:
        expression = expression.lower()

    for token in tokenize(expression):
        first_char = token[0]

        if first_char in NUMBER_CHARS or token == variable:
            output.append(token)
            if len(operator_stack) > 0 and operator_stack[-1] in UNARY_OPERATORS_SYMBOLS:
                output.append(operator_stack.pop())

        elif first_char in FUNCTION_CHARS:
            operator_stack.append(token)

        elif first_char == '(':
            operator_stack.append(first_char)

        elif first_char in SEPARATORS: # The ( has already been processed above, so it's only ),;
            if len(operator_stack) == 0:
                raise MismatchedBracketsError('More right than left brackets.')

            while not operator_stack[-1] in SEPARATORS_NO_CLOSING_BRACKET:
                output.append(operator_stack.pop())
                if len(operator_stack) == 0:
                    raise MismatchedBracketsError('More right than left brackets.')

            operator_stack.pop() # Pop the left over separator
            if first_char != ')': # If it's not the end of a bracket, replace by the current separator
                operator_stack.append(first_char)

            # If there is a function left, pop it to the output
            if len(operator_stack) > 0 and (operator_stack[-1] in FUNCTION_CHARS or operator_stack[-1] in UNARY_OPERATORS_SYMBOLS):
                output.append(operator_stack.pop())

        elif first_char in BASE_OPERATORS:
            while (len(operator_stack) > 0 and
                  (operator := operator_stack[-1]) not in SEPARATORS_NO_CLOSING_BRACKET and
                  (get_precedence(operator) > get_precedence(token) or
                        (get_precedence(operator) == get_precedence(token) and
                        OPERATORS_ASSOCIATIVITY[token] == Associativity.LEFT))):

                output.append(operator_stack.pop())

            operator_stack.append(token)

    # Empty the stack
    for token in reversed(operator_stack):
        if token == '(':
            raise MismatchedBracketsError('More left than right brackets.')
        output.append(token)

    return ' '.join(output)
