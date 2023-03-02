import unittest

from shunting_yard import MismatchedBracketsError, shunting_yard


class TestShuntingYard(unittest.TestCase):

    def test_base_operations(self):
        self.assertEqual(shunting_yard('1+2'), '1 2 +')
        self.assertEqual(shunting_yard('1-2'), '1 2 -')
        self.assertEqual(shunting_yard('1*2'), '1 2 *')
        self.assertEqual(shunting_yard('1/2'), '1 2 /')
        self.assertEqual(shunting_yard('1^2'), '1 2 ^')

    def test_priority(self):
        self.assertEqual(shunting_yard('2 * 1 + 3'), '2 1 * 3 +')

    def test_brackets(self):
        self.assertEqual(shunting_yard('2 * (1 + 3)'), '2 1 3 + *')

    def test_function_no_argument(self):
        self.assertEqual(shunting_yard('2 * pi - 1'), '2 pi * 1 -')

    def test_function_one_argument(self):
        self.assertEqual(shunting_yard('2 * sin(5/2)'), '2 5 2 / sin *')

    def test_function_two_argument(self):
        self.assertEqual(shunting_yard('5 * max(2; 6)'), '5 2 6 max *')

    def test_associativity(self):
        self.assertEqual(shunting_yard('5 ^ 4 ^ 3 ^ 2'), '5 4 3 2 ^ ^ ^')

    def test_complex_1(self):
        self.assertEqual(shunting_yard('3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3'), '3 4 2 * 1 5 - 2 3 ^ ^ / +')

    def test_complex_2(self):
        self.assertEqual(shunting_yard('sin ( max ( 2, 3 ) / 3 * pi )'), '2 3 max 3 / pi * sin')

    def test_mismatched_brackets(self):
        with self.assertRaises(MismatchedBracketsError):
            shunting_yard('sin(1')
        with self.assertRaises(MismatchedBracketsError):
            shunting_yard('1 + 2)')

    def test_case_sensitive(self):
        self.assertNotEqual(shunting_yard('min(1, 2)'), shunting_yard('MIN(1, 2)'))
        self.assertNotEqual(shunting_yard('min(1, 2)', case_sensitive=True), shunting_yard('MIN(1, 2)', case_sensitive=True))
        self.assertEqual(shunting_yard('min(1, 2)', case_sensitive=False), shunting_yard('MIN(1, 2)', case_sensitive=False))


if __name__ == '__main__':
    unittest.main()
