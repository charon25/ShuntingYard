import unittest

from shunting_yard import tokenize
from shunting_yard.tokenize import _convert_scientific_notation, _remove_implicit_multiplication


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
        self.assertListEqual(list(tokenize('-3/2*pi')), ['(', '0', '-', '1', ')', '*', '3', '/', '2', '*', 'pi'])

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
        self.assertListEqual(list(tokenize('-1')), ['(', '0', '-', '1', ')', '*', '1'])
        self.assertListEqual(list(tokenize('-(1+2)')), ['(', '0', '-', '1', ')', '*',  '(', '1', '+', '2', ')'])
        self.assertListEqual(list(tokenize('2*-1')), ['2', '*', '(', '0', '-', '1', ')', '*',  '1'])
        self.assertListEqual(list(tokenize('-(-1)')), ['(', '0', '-', '1', ')', '*',  '(', '(', '0', '-', '1', ')', '*',  '1', ')'])

    def test_function_unary_plus(self):
        self.assertListEqual(list(tokenize('+1')), ['1'])
        self.assertListEqual(list(tokenize('+(1+2)')), ['(', '1', '+', '2', ')'])
        self.assertListEqual(list(tokenize('2*+1')), ['2', '*', '1'])
        self.assertListEqual(list(tokenize('+(+1)')), ['(', '1', ')'])

    def test_function_unary_in_function(self):
        self.assertListEqual(list(tokenize('min(-1, 2)')), ['min', '(', '(', '0', '-', '1', ')', '*',  '1', ',', '2', ')'])
        self.assertListEqual(list(tokenize('min(1, -2)')), ['min', '(', '1', ',', '(', '0', '-', '1', ')', '*',  '2', ')'])
        self.assertListEqual(list(tokenize('min(1, -(2+sin(3)))')), ['min', '(', '1', ',', '(', '0', '-', '1', ')', '*',  '(', '2', '+', 'sin', '(', '3', ')', ')', ')'])

    def test_digits_in_function_name(self):
        self.assertListEqual(list(tokenize('min3(1, 2)')), ['min3', '(', '1', ',', '2', ')'])

    def test_upper_case_functions(self):
        self.assertListEqual(list(tokenize('Sin(x)')), ['Sin', '(', 'x', ')'])
        self.assertListEqual(list(tokenize('sIN(x)')), ['sIN', '(', 'x', ')'])
        self.assertListEqual(list(tokenize('SIN(x)')), ['SIN', '(', 'x', ')'])


class TestRemoveImplicitMultiplication(unittest.TestCase):

    def test_no_implicit_mult(self):
        self.assertEqual(_remove_implicit_multiplication('1+1'), '1+1')
        self.assertEqual(_remove_implicit_multiplication('1-1'), '1-1')
        self.assertEqual(_remove_implicit_multiplication('1*1'), '1*1')
        self.assertEqual(_remove_implicit_multiplication('1/1'), '1/1')
        self.assertEqual(_remove_implicit_multiplication('1^1'), '1^1')
        self.assertEqual(_remove_implicit_multiplication('(1)+1'), '(1)+1')
        self.assertEqual(_remove_implicit_multiplication('(1)-1'), '(1)-1')
        self.assertEqual(_remove_implicit_multiplication('(1)*1'), '(1)*1')
        self.assertEqual(_remove_implicit_multiplication('(1)/1'), '(1)/1')
        self.assertEqual(_remove_implicit_multiplication('(1)^1'), '(1)^1')
        self.assertEqual(_remove_implicit_multiplication('((1))'), '((1))')

    def test_no_implicit_mult2(self):
        self.assertEqual(_remove_implicit_multiplication('0.5'), '0.5')
        self.assertEqual(_remove_implicit_multiplication('max(1,2)'), 'max(1,2)')
        self.assertEqual(_remove_implicit_multiplication('max(1;2)'), 'max(1;2)')
        self.assertEqual(_remove_implicit_multiplication('max((1+2),2)'), 'max((1+2),2)')
        self.assertEqual(_remove_implicit_multiplication('max((1+2);2)'), 'max((1+2);2)')

    def test_digit_other(self):
        self.assertEqual(_remove_implicit_multiplication('2x'), '2*x')
        self.assertEqual(_remove_implicit_multiplication('3cos(5)'), '3*cos(5)')
        self.assertEqual(_remove_implicit_multiplication('3_func(0)'), '3*_func(0)')
        self.assertEqual(_remove_implicit_multiplication('1(2+3)'), '1*(2+3)')
        self.assertEqual(_remove_implicit_multiplication('1(2(3(4(5(6(7(8(9(10+0)))))))))'), '1*(2*(3*(4*(5*(6*(7*(8*(9*(10+0)))))))))')

    def test_implicit_mult_double_brackets(self):
        self.assertEqual(_remove_implicit_multiplication('(1+2)(3+4)'), '(1+2)*(3+4)')
        self.assertEqual(_remove_implicit_multiplication('(1+(2))((3+5)+4)((6+7)(8+9))'), '(1+(2))*((3+5)+4)*((6+7)*(8+9))')
        self.assertEqual(_remove_implicit_multiplication('sin(pi)(1+2)'), 'sin(pi)*(1+2)')

    def test_implicit_mult_bracket_other(self):
        self.assertEqual(_remove_implicit_multiplication('sin(1)2'), 'sin(1)*2')
        self.assertEqual(_remove_implicit_multiplication('sin(1).5'), 'sin(1)*.5')
        self.assertEqual(_remove_implicit_multiplication('(1+2)3'), '(1+2)*3')
        self.assertEqual(_remove_implicit_multiplication('(1+2)x'), '(1+2)*x')
        self.assertEqual(_remove_implicit_multiplication('(1+2)sin(1)'), '(1+2)*sin(1)')

    def test_with_longer_numbers(self):
        self.assertEqual(_remove_implicit_multiplication('200x'), '200*x')
        self.assertEqual(_remove_implicit_multiplication('301cos(5)'), '301*cos(5)')
        self.assertEqual(_remove_implicit_multiplication('345_func(0)'), '345*_func(0)')
        self.assertEqual(_remove_implicit_multiplication('156(2+3)'), '156*(2+3)')
        self.assertEqual(_remove_implicit_multiplication('1+200x'), '1+200*x')


class TestScientificNotation(unittest.TestCase):

    def test_not_present(self):
        self.assertEqual(_convert_scientific_notation('abc'), 'abc')
        self.assertEqual(_convert_scientific_notation('123.4'), '123.4')
        self.assertEqual(_convert_scientific_notation('123exp(4)'), '123exp(4)')
        self.assertEqual(_convert_scientific_notation('123e +1'), '123e +1')

    def test_present(self):
        self.assertEqual(_convert_scientific_notation('12e3'), '12*10^(3)')
        self.assertEqual(_convert_scientific_notation('+12e3'), '+12*10^(3)')
        self.assertEqual(_convert_scientific_notation('-12e3'), '-12*10^(3)')
        self.assertEqual(_convert_scientific_notation('1.2e3'), '1.2*10^(3)')
        self.assertEqual(_convert_scientific_notation('1.e3'), '1.*10^(3)')
        self.assertEqual(_convert_scientific_notation('.2e3'), '.2*10^(3)')
        self.assertEqual(_convert_scientific_notation('12e-3'), '12*10^(-3)')
        self.assertEqual(_convert_scientific_notation('12e+3'), '12*10^(+3)')
        self.assertEqual(_convert_scientific_notation('12e34'), '12*10^(34)')
        self.assertEqual(_convert_scientific_notation('12e-34'), '12*10^(-34)')
        self.assertEqual(_convert_scientific_notation('12e+34'), '12*10^(+34)')

    def test_double(self):
        self.assertEqual(_convert_scientific_notation('12e3+45e-6'), '12*10^(3)+45*10^(-6)')


if __name__ == '__main__':
    unittest.main()
