from unittest import TestCase
from main import tokenize, read_from_tokens, parse, eval

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

        #

    def test_eval(self):
        self.assertEqual(eval(parse(self.test_string)), 3)

