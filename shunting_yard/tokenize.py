import re
from typing import Iterator

from shunting_yard.constants import BASE_OPERATORS, FUNCTION_CHARS, FUNCTION_FIRST_CHARS, NUMBER_CHARS, SEPARATORS, UNARY_OPERATORS
from shunting_yard.constants import IMPLICIT_MULTIPLICATION_BRACKET_REGEX, IMPLICIT_MULTIPLICATION_NUMBER_REGEX, SCIENTIFIC_NOTATION_AFTER_DOT_REGEX, SCIENTIFIC_NOTATION_BEFORE_DOT_REGEX



def _remove_implicit_multiplication(expression: str) -> str:
    """Add '*' to every implicit multiplication. These can be :
        - between a number and a variable or function: 2x 3sin(x)
        - between brackets: (x+1)(x-1), sin(x)(1+2)
        - between a closing bracket and a number/variable/function: sin(x)2, (1+2)x, (1+2)sin(x)
    However, a lot of cases do not require implicit multiplication, such as:
        - 0.5
        - min(1,2)
        - min((1+2),2)
        ...
    """
    
    # Insert '*' between a number and anything other than a digit, an operation, a closing bracket, a decimal dot, a function parameters separator
    expression = re.sub(IMPLICIT_MULTIPLICATION_NUMBER_REGEX, r'\1*\2', expression)
    # Insert '*' between a closing bracket and anything other than an operation, another closing bracket, a function parameters separator
    expression = re.sub(IMPLICIT_MULTIPLICATION_BRACKET_REGEX, r'\1*\2', expression)
    return expression


def _convert_scientific_notation(expression: str) -> str:
    """"""

    # Replace everything of the form "xey" by "x*10^y" where y is an integer and x is a float not ending with just a dot
    expression = re.sub(SCIENTIFIC_NOTATION_AFTER_DOT_REGEX, r'\1*10^(\2)', expression)

    # Replace everything of the form "xey" by "x*10^y" where y is an integer and x is a float not starting with just a dot
    expression = re.sub(SCIENTIFIC_NOTATION_BEFORE_DOT_REGEX, r'\1*10^(\2)', expression)

    return expression


def tokenize(string: str, convert_scientific_notation: bool = True) -> Iterator[str]:
    if string == '':
        return

    # Remove all whitespaces are they do not change anything
    string = ''.join(string.split())

    if convert_scientific_notation:
        string = _convert_scientific_notation(string)

    string = _remove_implicit_multiplication(string)

    cursor = 0
    is_infix = False

    while cursor < len(string):
        char = string[cursor]

        if not is_infix and char in UNARY_OPERATORS:
            if char == '-':
                yield from '(0-1)*'
            cursor += 1

        elif char in BASE_OPERATORS or char in SEPARATORS:
            yield char
            cursor += 1
            is_infix = (char == ')')

        elif char in NUMBER_CHARS:
            # Go through until not a number anymore
            cursor_end = cursor + 1
            while cursor_end < len(string) and string[cursor_end] in NUMBER_CHARS:
                cursor_end += 1

            yield string[cursor:cursor_end]
            cursor += (cursor_end - cursor)
            is_infix = True

        elif char in FUNCTION_FIRST_CHARS:
            # Go through until not a function anymore
            cursor_end = cursor + 1
            while  cursor_end < len(string) and string[cursor_end] in FUNCTION_CHARS:
                cursor_end += 1

            yield string[cursor:cursor_end]
            cursor += (cursor_end - cursor)
            is_infix = True

        else:
            # This mean we encountered another character acting as a separator
            is_infix = False
            cursor += 1
