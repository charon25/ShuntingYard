from string import ascii_lowercase, digits


UNARY_OPERATORS = '+-'
UNARY_OPERATORS_SYMBOLS = ('-u', '+u')
BASE_OPERATORS = '+-*/^'
NUMBER_CHARS = digits + '.'
# functions cannot start with a number
FUNCTION_FIRST_CHARS = ascii_lowercase + '_'
FUNCTION_CHARS = FUNCTION_FIRST_CHARS + NUMBER_CHARS
