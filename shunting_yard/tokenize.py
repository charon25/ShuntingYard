from typing import Iterator

from shunting_yard.constants import BASE_OPERATORS, FUNCTION_CHARS, NUMBER_CHARS, UNARY_OPERATORS


def tokenize(string: str) -> Iterator[str]:
    if string == '':
        return

    cursor = 0
    is_infix = False

    while cursor < len(string):
        char = string[cursor]

        if not is_infix and char in UNARY_OPERATORS:
            yield f'{char}u'
            cursor += 1

        elif char in BASE_OPERATORS or char in '()':
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

        elif char in FUNCTION_CHARS:
            # Go through until not a number anymore
            cursor_end = cursor + 1
            while  cursor_end < len(string) and string[cursor_end] in FUNCTION_CHARS:
                cursor_end += 1

            yield string[cursor:cursor_end]
            cursor += (cursor_end - cursor)
            is_infix = True

        else:
            cursor += 1
