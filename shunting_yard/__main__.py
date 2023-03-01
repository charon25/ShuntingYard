import sys

from .rpn import compute_rpn, WrongExpressionError
from .shunting_yard import shunting_yard, MismatchedBracketsError


if len(sys.argv) <= 1:
    print('Expression to evaluate ?')
    expression = input('>>>')
else:
    expression = sys.argv[1]

try:
    result = compute_rpn(shunting_yard(expression))
    print(f"\n{expression} = {result}")
except MismatchedBracketsError:
    print('error: mismatched brackets')
except WrongExpressionError:
    print('error: incorrect expression')
