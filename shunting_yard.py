from string import ascii_lowercase

BASE_OPERATORS = '+-*/^'
NUMBER_CHARS = '0123456789.'
LETTERS_CHARS = ascii_lowercase + '_'

def tokenize(string: str):
    if string == '':
        return

    string = string.lower()
    cursor = 0
    while cursor < len(string):
        char = string[cursor]
        if char in BASE_OPERATORS or char in '()':
            yield char
            cursor += 1
        elif char in NUMBER_CHARS:
            # Go through until not a number anymore
            cursor_end = cursor + 1
            while cursor_end < len(string) and string[cursor_end] in NUMBER_CHARS:
                cursor_end += 1
            # Convert either to float or int
            number = string[cursor:cursor_end]
            yield float(number) if '.' in number else int(number)
            cursor += (cursor_end - cursor)
        elif char in LETTERS_CHARS:
            # Go through until not a number anymore
            cursor_end = cursor + 1
            while  cursor_end < len(string) and string[cursor_end] in LETTERS_CHARS:
                cursor_end += 1

            yield string[cursor:cursor_end]
            cursor += (cursor_end - cursor)
        else:
            cursor += 1


print(list(tokenize('1+3')))
