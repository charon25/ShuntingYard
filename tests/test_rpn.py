import math
import unittest

from shunting_yard import compute_rpn


class TestReversePolishNotation(unittest.TestCase):

    def test_base_operators(self):
        self.assertEqual(compute_rpn('1 2 +'), 3)
        self.assertEqual(compute_rpn('1 2 -'), -1)
        self.assertEqual(compute_rpn('1 2 *'), 2)
        self.assertAlmostEqual(compute_rpn('1 2 /'), 0.5)
        self.assertEqual(compute_rpn('1 2 ^'), 1)

    def test_priority_brackets(self):
        self.assertEqual(compute_rpn('2 1 * 3 +'), 5)
        self.assertEqual(compute_rpn('2 1 3 + *'), 8)

    def test_function_no_argument(self):
        self.assertAlmostEqual(compute_rpn('2 pi *'), 2 * math.pi)

    def test_function_one_argument(self):
        self.assertAlmostEqual(compute_rpn('pi 2 / sin'), 1.0)

    def test_function_two_argument(self):
        self.assertEqual(compute_rpn('2 5 max'), 5)

if __name__ == '__main__':
    unittest.main()
