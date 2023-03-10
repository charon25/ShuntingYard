from typing import Iterator

from shunting_yard.constants import BASE_OPERATORS, FUNCTION_CHARS, FUNCTION_FIRST_CHARS, NUMBER_CHARS, SEPARATORS, UNARY_OPERATORS


def tokenize(string: str) -> Iterator[str]:
    if string == '':
        return

    # Remove all whitespaces are they do not change anything
    string = ''.join(string.split())

    cursor = 0
    is_infix = False

    while cursor < len(string):
        char = string[cursor]

        if not is_infix and char in UNARY_OPERATORS:
            yield f'{char}u'
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
