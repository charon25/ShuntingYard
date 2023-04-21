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


IMPLICIT_MULTIPLICATION_NUMBER_REGEX = r'\b(\d+)([^)\d.,;+*\/^-])'
IMPLICIT_MULTIPLICATION_BRACKET_REGEX = r'(\))([^),;+*\/^-])'


SCIENTIFIC_NOTATION_AFTER_DOT_REGEX = r'([+-]?\d*\.?\d+)e([+-]?\d+)'
SCIENTIFIC_NOTATION_BEFORE_DOT_REGEX = r'([+-]?\d+\.?\d*)e([+-]?\d+)'
