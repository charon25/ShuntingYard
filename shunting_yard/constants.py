from string import ascii_lowercase, ascii_uppercase, digits


UNARY_OPERATORS = '+-'
UNARY_OPERATORS_SYMBOLS = ('-u', '+u')
BASE_OPERATORS = '+-*/^'
NUMBER_CHARS = digits + '.'
# functions cannot start with a number
FUNCTION_FIRST_CHARS = ascii_lowercase + ascii_uppercase + '_'
FUNCTION_CHARS = FUNCTION_FIRST_CHARS + NUMBER_CHARS

SEPARATORS_NO_CLOSING_BRACKET = '(,;'
SEPARATORS = SEPARATORS_NO_CLOSING_BRACKET + ')'
