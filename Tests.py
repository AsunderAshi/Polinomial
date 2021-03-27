import unittest
import polinomial
import rpn


class MyTestCase(unittest.TestCase):
    def test_get_numbers(self):
        polinomial = "-x123+0.123-(-8.6)+7*x-x2"
        self.assertListEqual(['-x123','0.123','-8.6','7','x','x2'], rpn.get_numbers(polinomial))

    def test_get_numbers_two(self):
        polinomial = "(x-1)(x1+1)-8.00001"
        self.assertListEqual(['x', '1', 'x1', '1', '8.00001'], rpn.get_numbers(polinomial))

    def test_get_numbers_three(self):
        polinomial = "x12345 +       (    2.01x345 - 8 + 7.5 + 9 )"
        self.assertListEqual(['x12345', '2.01', 'x345', '8', '7.5', '9'], rpn.get_numbers(polinomial))

    def test_unary_minus_handler(self):
        polinomial = "-(x-1)+(-(1+5))"
        self.assertEqual("(-1)*(x-1)+((-1)*(1+5))", rpn.unary_minus_handler(polinomial))

    def test_unary_minus_handler_two(self):
        polinomial = "-(-(x-1))"
        self.assertEqual("(-1)*((-1)*(x-1))", rpn.unary_minus_handler(polinomial))

    def test_add_multiplication(self):
        polinomial = "2x1+345x67 - (x-1)(x+5)"
        self.assertEqual("2*x1+345*x67 - (x-1)*(x+5)", rpn.add_multiplication(polinomial))

    def test_add_multiplication_two(self):
        polinomial = "2x1+345x67 - (x-1)(x+5) + 1.5(x+1)"
        self.assertEqual("2*x1+345*x67 - (x-1)*(x+5) + 1.5*(x+1)", rpn.add_multiplication(polinomial))

    def test_get_operators(self):
        polinomial = "-x123+0.123-(-8.6)+7*x-x2^3"
        self.assertListEqual(['+','-','(',')','+','*','-','^'], rpn.get_operators(polinomial))

    def test_polinomial_to_list(self):
        polinomial = "-x123+0.123-(-8.6)+7*x-x2^3"
        self.assertListEqual(['-x123','+','0.123','-','(','-8.6',')','+','7','*','x','-','x2','^','3'],
                             rpn.polinomial_to_list(polinomial))

    def test_operators_handler(self):
        stack = ['-','(','+','^']
        vs = ['1','2','3']
        operator = ')'
        rpn.operators_handler(operator, vs, stack)
        self.assertListEqual(['-'], stack)
        self.assertListEqual(['1','2','3','^','+'], vs)

    def test_extract_left_operators(self):
        stack = ['+','-','+']
        vs = []
        rpn.extract_left_operators(vs,stack,'+','-')
        self.assertListEqual(['+','-','+'], vs)

    def test_interpret(self):
        polinomial = "-(x-1)+x*x"
        self.assertListEqual(['-1','x','1','-','*','x','x','*','+'], rpn.interpret(polinomial))

    def test_interpret_two(self):
        polinomial = "2 - 2*1 + 3"
        self.assertListEqual(['2','2','1','*','-','3','+'], rpn.interpret(polinomial))

    def test_compute(self):
        expression = ['2','2','*']
        self.assertEqual(4.00, rpn.compute(expression))

    def test_replace(self):
        polinom = ['-x', '2', 'x1','+', 'x']
        symbol = 'x'
        symbol_to_replace = '2'
        self.assertListEqual(['-2', '2', 'x1', '+', '2'], polinomial.replace(polinom, symbol, symbol_to_replace))

    def test_compare(self):
        epsilon = 2
        polinom_one = "x^2 - 1 +     x"
        polinom_two = "- (1 -     x)+ x     * x"
        self.assertTrue(polinomial.compare(polinom_one, polinom_two, epsilon))

    def test_compare_two(self):
        epsilon = 0.1
        polinom_one = "x^1"
        polinom_two = "x"
        self.assertTrue(polinomial.compare(polinom_one, polinom_two, epsilon))

    def test_compare_three(self):
        epsilon = 0.2
        polinom_one = "-0.5x123^(2*(-(-1)))"
        polinom_two = "x123*x123/(-2)"
        self.assertTrue(polinomial.compare(polinom_one, polinom_two, epsilon))

    def test_compare_four(self):
        epsilon = 0.2
        polinom_one = "x1^3 + x2^3"
        polinom_two = "(x1 + x2)(x1^2 - x2*x1 + x2^2)"
        self.assertTrue(polinomial.compare(polinom_one, polinom_two, epsilon))

    def test_compare_five(self):
        epsilon = 2
        polinom_one = "1-x+2"
        polinom_two = "-x+3"
        self.assertTrue(polinomial.compare(polinom_one, polinom_two, epsilon))

    def test_compare_six(self):
        epsilon = 0.1
        polinom_one = "(x-1)^10"
        polinom_two = "(x-1)^9(x-1)"
        self.assertTrue(polinomial.compare(polinom_one, polinom_two, epsilon))


if __name__ == '__main__':
    unittest.main()
