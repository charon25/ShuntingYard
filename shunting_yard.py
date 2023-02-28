from enum import Enum
from string import ascii_lowercase
from typing import Iterator

BASE_OPERATORS = '+-*/^'
NUMBER_CHARS = '0123456789.'
LETTERS_CHARS = ascii_lowercase + '_'

class TokenType(Enum):
    BRACKET = 0
    INTEGER = 10
    FLOAT = 11
    OPERATOR = 20
    FUNCTION = 30

def tokenize(string: str) -> Iterator[tuple[TokenType, str]]:
    if string == '':
        return

    string = string.lower()
    cursor = 0
    while cursor < len(string):
        char = string[cursor]
        if char in BASE_OPERATORS:
            yield (TokenType.OPERATOR, char)
            cursor += 1
        elif char in '()':
            yield (TokenType.BRACKET, char)
            cursor += 1
        elif char in NUMBER_CHARS:
            # Go through until not a number anymore
            cursor_end = cursor + 1
            while cursor_end < len(string) and string[cursor_end] in NUMBER_CHARS:
                cursor_end += 1

            yield (TokenType.FLOAT if '.' in string[cursor:cursor_end] else TokenType.INTEGER, string[cursor:cursor_end])
            cursor += (cursor_end - cursor)
        elif char in LETTERS_CHARS:
            # Go through until not a number anymore
            cursor_end = cursor + 1
            while  cursor_end < len(string) and string[cursor_end] in LETTERS_CHARS:
                cursor_end += 1

            yield (TokenType.FUNCTION, string[cursor:cursor_end])
            cursor += (cursor_end - cursor)
        else:
            cursor += 1

