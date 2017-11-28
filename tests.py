from unittest import TestCase
from parser import tokenize, parse, read_from_tokens
from eval import eval, create_env

class Test(TestCase):

    def setUp(self):
        self.test_string =  "(+ 1 2)"

    def test_tokenize(self):

        string = "(+ 1 2)"
        answer = ["(", "+", "1", "2", ")"]
        self.assertEqual(tokenize(string), answer)

        string = " ( + 1 2 ) "

        self.assertEqual(tokenize(string), answer)

    def test_read_tokens(self):

        tokens = tokenize(self.test_string)

        result = read_from_tokens(tokens)
        self.assertEqual(result, ['+', 1, 2])

        self.assertEqual(parse("(+ 1 (- 2 3))"), ['+',
                                                  1,
                                                  ['-', 2, 3]])
        # test single
        self.assertEqual(parse("3"), 3)


    def lots_of_tests(self):

        def test_expr(expr, expected_val):
            env = create_env()
            self.assertEqual(eval(parse(expr), env), expected_val)


        # test keywords


        test_expr("(defun (f x) (+ x 2))", None)
        test_expr("(begin (defun (f x) (+ x 2)) (f 3))", 5)

    def test_eval(self):
        env = create_env()
        self.assertEqual(eval(parse(self.test_string), env), 3)

