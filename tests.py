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


        # test basic operations

        test_expr("3", 3)
        test_expr("3.14", 3.14)
        test_expr("#f", False)
        test_expr("#t", True)

        test_expr("(+ 1 2)", 3)
        test_expr("(- 2.5 1.5)", 1.0)
        test_expr("(/ 3 2)", 1.5)
        test_expr("(// 3 2)", 1)


        test_expr("(if #t 3 2)", 3)
        test_expr("(if #f 3 2)", 2)
        test_expr("(if (> 3 2) 3 2)", 3)

        test_expr("(begin 2 3 5)", 5)

        test_expr("(quote (define x 2))", ["define",  "x", 2])

        test_expr("(list 1 2 3)", [1, 2, 3])
        test_expr("(list #f 2 3.14)", [False, 2, 3.14])
        test_expr("(head (list 1 2))", 1)
        test_expr("(tail (list 1 2 3))", [2, 3])
        test_expr("(tail (list 1))", [])
        test_expr("(empty? (list))", True)
        test_expr("(empty? (list 1))", False)

        test_expr("(quote (list 1))", ['list', 1])

        test_expr("(begin (define x 3) x)", 3)
        test_expr("(begin (define x 3) (set! x 5) x)", 5)

        test_expr("(defun (f x) (+ x 2))", None)
        test_expr("(begin (defun (f x) (+ x 2)) (f 3))", 5)

        # test recursive factorial
        test_expr("(begin (defun (fact n) (if (<= n 1) 1 (* n (fact (- n 1))))) (fact 10))", 3628800)

        # test closure
        test_expr("(begin "
                  "(define add "
                  "     (lambda (x) (lambda (y) (+ x y))))"
                  "(define add10 (add 10)) (add10 5)"
                  ")", 15)

    def test_eval(self):
        env = create_env()
        self.assertEqual(eval(parse(self.test_string), env), 3)

