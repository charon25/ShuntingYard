from string import ascii_lowercase
import math
from enum import Enum

from shunting_yard.tokenize import tokenize
from shunting_yard.constants import BASE_OPERATORS, NUMBER_CHARS, FUNCTION_CHARS


class MismatchedBracketsError(Exception):
    pass


OPERATORS_PRECEDENCE: dict[str, int] = {
    '+': 10,
    '-': 10,
    '*': 20,
    '/': 20,
    '^': 30
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
}



# Reference : https://en.wikipedia.org/wiki/Shunting_yard_algorithm
def shunting_yard(expression: str) -> str:
    """Convert the given classical math expression into Reverse Polish Notation using the Shunting-yard algorithm (see https://en.wikipedia.org/wiki/Shunting_yard_algorithm for more details). All whitespace are ignored.


    >>> shuting_yard("1 + 2")
    '1 2 +'

    >>> shuting_yard("sin(max(2, 3) / 3 * pi)")
    '2 3 max 3 / pi * sin'
    

    Args:
        expression (str): string containing the mathematical expression to convert.

    Raises:
        MismatchedBracketsError: raised if the bracket are unbalanced.


    Returns:
        str: The RPN expression corresponding to the mathematical expression.
    """
    output: list[str] = []
    operator_stack: list[str] = []

    for token in tokenize(expression):
        first_char = token[0]

        if first_char in NUMBER_CHARS:
            output.append(token)

        elif first_char in FUNCTION_CHARS:
            operator_stack.append(token)

        elif first_char == '(':
            operator_stack.append(first_char)

        elif first_char == ')':
            if len(operator_stack) == 0:
                raise MismatchedBracketsError('More right than left brackets.')

            while operator_stack[-1] != '(':
                output.append(operator_stack.pop())
                if len(operator_stack) == 0:
                    raise MismatchedBracketsError('More right than left brackets.')

            operator_stack.pop() # Pop the '(' left over

            # If there is a function left, pop it to the output
            if len(operator_stack) > 0 and operator_stack[-1] in FUNCTION_CHARS:
                output.append(operator_stack.pop())

        elif first_char in BASE_OPERATORS:
            while (len(operator_stack) > 0 and
                  (operator := operator_stack[-1]) != '(' and 
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
