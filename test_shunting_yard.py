import unittest

from shunting_yard import tokenize, TokenType as TT

class TestTokenizer(unittest.TestCase):

    def test_base_operations(self):
        self.assertListEqual(list(tokenize('1+2')), [(TT.INTEGER, '1'), (TT.OPERATOR, '+'), (TT.INTEGER, '2')])
        self.assertListEqual(list(tokenize('1-2')), [(TT.INTEGER, '1'), (TT.OPERATOR, '-'), (TT.INTEGER, '2')])
        self.assertListEqual(list(tokenize('1*2')), [(TT.INTEGER, '1'), (TT.OPERATOR, '*'), (TT.INTEGER, '2')])
        self.assertListEqual(list(tokenize('1/2')), [(TT.INTEGER, '1'), (TT.OPERATOR, '/'), (TT.INTEGER, '2')])
        self.assertListEqual(list(tokenize('1^2')), [(TT.INTEGER, '1'), (TT.OPERATOR, '^'), (TT.INTEGER, '2')])

    def test_spaces(self):
        self.assertListEqual(list(tokenize('1    + 2             - 3')), [(TT.INTEGER, '1'), (TT.OPERATOR, '+'), (TT.INTEGER, '2'), (TT.OPERATOR, '-'), (TT.INTEGER, '3')])

    def test_incorrect(self):
        self.assertListEqual(list(tokenize('1+')), [(TT.INTEGER, '1'), (TT.OPERATOR, '+')])

    def test_empty(self):
        self.assertListEqual(list(tokenize('')), [])

    def test_brackets(self):
        self.assertListEqual(list(tokenize('1+(2 * 3) - 4 * (2 / 3)')), [(TT.INTEGER, '1'), (TT.OPERATOR, '+'), (TT.BRACKET, '('), (TT.INTEGER, '2'), (TT.OPERATOR, '*'), (TT.INTEGER, '3'), (TT.BRACKET, ')'), (TT.OPERATOR, '-'), (TT.INTEGER, '4'), (TT.OPERATOR, '*'), (TT.BRACKET, '('), (TT.INTEGER, '2'), (TT.OPERATOR, '/'), (TT.INTEGER, '3'), (TT.BRACKET, ')')])

    def test_multiple_digits_numbers(self):
        self.assertListEqual(list(tokenize('123456 + 321654 * 3141515 - 2')), [(TT.INTEGER, '123456'), (TT.OPERATOR, '+'), (TT.INTEGER, '321654'), (TT.OPERATOR, '*'), (TT.INTEGER, '3141515'), (TT.OPERATOR, '-'), (TT.INTEGER, '2')])

    def test_decimal_numbers(self):
        self.assertListEqual(list(tokenize('1.23 * 2.354')), [(TT.FLOAT, '1.23'), (TT.OPERATOR, '*'), (TT.FLOAT, '2.354')])

    def test_decimal_numbers_no_leading(self):
        self.assertListEqual(list(tokenize('.1 + .2')), [(TT.FLOAT, '.1'), (TT.OPERATOR, '+'), (TT.FLOAT, '.2')])

    def test_function_one_argument(self):
        self.assertListEqual(list(tokenize('sin(1 + 4)')), [(TT.FUNCTION, 'sin'), (TT.BRACKET, '('), (TT.INTEGER, '1'), (TT.OPERATOR, '+'), (TT.INTEGER, '4'), (TT.BRACKET, ')')])

    def test_function_no_argument(self):
        self.assertListEqual(list(tokenize('-3/2*pi')), [(TT.OPERATOR, '-'), (TT.INTEGER, '3'), (TT.OPERATOR, '/'), (TT.INTEGER, '2'), (TT.OPERATOR, '*'), (TT.FUNCTION, 'pi')])

    def test_function_2_arguments(self):
        self.assertListEqual(list(tokenize('max(1, 4)')), [(TT.FUNCTION, 'max'), (TT.BRACKET, '('), (TT.INTEGER, '1'), (TT.INTEGER, '4'), (TT.BRACKET, ')')])

    def test_function_upper_case(self):
        self.assertListEqual(list(tokenize('MIN(1;4)')), [(TT.FUNCTION, 'min'), (TT.BRACKET, '('), (TT.INTEGER, '1'), (TT.INTEGER, '4'), (TT.BRACKET, ')')])

    def test_function_underscore(self):
        self.assertListEqual(list(tokenize('arc_cos(0)')), [(TT.FUNCTION, 'arc_cos'), (TT.BRACKET, '('), (TT.INTEGER, '0'), (TT.BRACKET, ')')])

if __name__ == '__main__':
    unittest.main()
