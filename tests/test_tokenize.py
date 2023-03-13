import unittest

from shunting_yard import tokenize


class TestTokenizer(unittest.TestCase):

    def test_base_operations(self):
        self.assertListEqual(list(tokenize('1+2')), ['1', '+', '2'])
        self.assertListEqual(list(tokenize('1-2')), ['1', '-', '2'])
        self.assertListEqual(list(tokenize('1*2')), ['1', '*', '2'])
        self.assertListEqual(list(tokenize('1/2')), ['1', '/', '2'])
        self.assertListEqual(list(tokenize('1^2')), ['1', '^', '2'])

    def test_spaces(self):
        self.assertListEqual(list(tokenize('1    + 2             - 3')), ['1', '+', '2', '-', '3'])

    def test_incorrect(self):
        self.assertListEqual(list(tokenize('1+')), ['1', '+'])

    def test_empty(self):
        self.assertListEqual(list(tokenize('')), [])

    def test_brackets(self):
        self.assertListEqual(list(tokenize('1+(2 * 3) - 4 * (2 / 3)')), ['1', '+', '(', '2', '*', '3', ')', '-', '4', '*', '(', '2', '/', '3', ')'])

    def test_multiple_digits_numbers(self):
        self.assertListEqual(list(tokenize('123456 + 321654 * 3141515 - 2')), ['123456', '+', '321654', '*', '3141515', '-', '2'])

    def test_decimal_numbers(self):
        self.assertListEqual(list(tokenize('1.23 * 2.354')), ['1.23', '*', '2.354'])

    def test_decimal_numbers_no_leading(self):
        self.assertListEqual(list(tokenize('.1 + .2')), ['.1', '+', '.2'])

    def test_function_one_argument(self):
        self.assertListEqual(list(tokenize('sin(1 + 4)')), ['sin', '(', '1', '+', '4', ')'])

    def test_function_no_argument(self):
        self.assertListEqual(list(tokenize('-3/2*pi')), ['-u', '3', '/', '2', '*', 'pi'])

    def test_function_2_arguments(self):
        self.assertListEqual(list(tokenize('max(1, 4)')), ['max', '(', '1', ',', '4', ')'])
        self.assertListEqual(list(tokenize('max(1; 4)')), ['max', '(', '1', ';', '4', ')'])

    def test_function_3_arguments(self):
        self.assertListEqual(list(tokenize('max(1, 2, 3)')), ['max', '(', '1', ',', '2', ',', '3', ')'])
        self.assertListEqual(list(tokenize('max(1, 2; 3)')), ['max', '(', '1', ',', '2', ';', '3', ')'])
        self.assertListEqual(list(tokenize('max(1; 2, 3)')), ['max', '(', '1', ';', '2', ',', '3', ')'])
        self.assertListEqual(list(tokenize('max(1; 2; 3)')), ['max', '(', '1', ';', '2', ';', '3', ')'])

    def test_function_underscore(self):
        self.assertListEqual(list(tokenize('arc_cos(0)')), ['arc_cos', '(', '0', ')'])

    def test_function_unary_minus(self):
        self.assertListEqual(list(tokenize('-1')), ['-u', '1'])
        self.assertListEqual(list(tokenize('-(1+2)')), ['-u', '(', '1', '+', '2', ')'])
        self.assertListEqual(list(tokenize('2*-1')), ['2', '*', '-u', '1'])
        self.assertListEqual(list(tokenize('-(-1)')), ['-u', '(', '-u', '1', ')'])

    def test_function_unary_plus(self):
        self.assertListEqual(list(tokenize('+1')), ['+u', '1'])
        self.assertListEqual(list(tokenize('+(1+2)')), ['+u', '(', '1', '+', '2', ')'])
        self.assertListEqual(list(tokenize('2*+1')), ['2', '*', '+u', '1'])
        self.assertListEqual(list(tokenize('+(+1)')), ['+u', '(', '+u', '1', ')'])

    def test_function_unary_in_function(self):
        self.assertListEqual(list(tokenize('min(-1, 2)')), ['min', '(', '-u', '1', ',', '2', ')'])
        self.assertListEqual(list(tokenize('min(1, -2)')), ['min', '(', '1', ',', '-u', '2', ')'])
        self.assertListEqual(list(tokenize('min(1, -(2+sin(3)))')), ['min', '(', '1', ',', '-u', '(', '2', '+', 'sin', '(', '3', ')', ')', ')'])

    def test_digits_in_function_name(self):
        self.assertListEqual(list(tokenize('min3(1, 2)')), ['min3', '(', '1', ',', '2', ')'])



if __name__ == '__main__':
    unittest.main()
