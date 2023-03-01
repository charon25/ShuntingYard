import math
import unittest

from shunting_yard import compute_rpn, WrongExpressionError


class TestReversePolishNotation(unittest.TestCase):

    def test_base_operators(self):
        self.assertEqual(compute_rpn('1 2 +'), 3)
        self.assertEqual(compute_rpn('1 2 -'), -1)
        self.assertEqual(compute_rpn('1 2 *'), 2)
        self.assertAlmostEqual(compute_rpn('1 2 /'), 0.5)
        self.assertEqual(compute_rpn('1 2 ^'), 1)

    def test_unary_minus(self):
        self.assertEqual(compute_rpn('1 -u'), -1)
        self.assertEqual(compute_rpn('1 2 + -u'), -3)
        self.assertEqual(compute_rpn('1 -u 2 *'), -2)

    def test_unary_plus(self):
        self.assertEqual(compute_rpn('1 +u'), 1)
        self.assertEqual(compute_rpn('1 2 + +u'), 3)
        self.assertEqual(compute_rpn('1 +u 2 *'), 2)

    def test_priority_brackets(self):
        self.assertEqual(compute_rpn('2 1 * 3 +'), 5)
        self.assertEqual(compute_rpn('2 1 3 + *'), 8)

    def test_function_no_argument(self):
        self.assertAlmostEqual(compute_rpn('2 pi *'), 2 * math.pi)

    def test_function_one_argument(self):
        self.assertAlmostEqual(compute_rpn('pi 2 / sin'), 1.0)

    def test_function_two_argument(self):
        self.assertEqual(compute_rpn('2 5 max'), 5)

    def test_function_additional_function(self):
        self.assertEqual(compute_rpn('3 inc', {'inc': (1, lambda x:x + 1)}), 4)

    def test_function_overwriting_function(self):
        self.assertEqual(compute_rpn('3 2 add', {'add': (2, lambda x, y:x + 2 * y)}), 7)

    def test_errors(self):
        with self.assertRaises(WrongExpressionError):
            compute_rpn('1 +')
            compute_rpn('abs')
        with self.assertRaises(WrongExpressionError):
            compute_rpn('1 1 1 +')


if __name__ == '__main__':
    unittest.main()
