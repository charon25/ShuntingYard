from shunting_yard.rpn import compute_rpn, Number
from shunting_yard.shunting_yard import shunting_yard
from shunting_yard.tokenize import tokenize

def compute(string: str) -> Number:
    return compute_rpn(shunting_yard(string))
