import unittest

from shunting_yard import compute_rpn, shunting_yard


class TestComputation(unittest.TestCase):

    def test_bug_minus_3_squared(self):
        self.assertEqual(compute_rpn(shunting_yard('-3^2')), -9)

    def test_unary_minus_operator(self):
        self.assertEqual(compute_rpn(shunting_yard('-1')), -1)
        self.assertEqual(compute_rpn(shunting_yard('--1')), 1)
        self.assertEqual(compute_rpn(shunting_yard('---1')), -1)

        self.assertAlmostEqual(compute_rpn(shunting_yard('-sin(-pi/2)')), 1)
        self.assertEqual(compute_rpn(shunting_yard('-(2*3)*(1+2)*(-5*2)')), 180)

    def test_unary_plus_operator(self):
        self.assertEqual(compute_rpn(shunting_yard('+1')), 1)
        self.assertEqual(compute_rpn(shunting_yard('++1')), 1)
        self.assertEqual(compute_rpn(shunting_yard('+++1')), 1)

        self.assertAlmostEqual(compute_rpn(shunting_yard('+sin(+pi/2)')), 1)
        self.assertEqual(compute_rpn(shunting_yard('+(2*3)*(1+2)*(+5*2)')), 180)



if __name__ == '__main__':
    unittest.main()
