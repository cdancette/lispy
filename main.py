#!/usr/bin/env python3

import operator
import traceback
import readline
import re
import sys

# readline.parse_and_bind('tab: complete')

Symbol = str
Number = (int, float)
Boolean = bool
String = str
Atom = (Symbol, Number, Boolean, String)
List = list
Expression = (list, Atom)

comment_regex = re.compile("\(\*.*?\*\)")

class Env(dict):
    def __init__(self, params, args, dict=None, outer=None):
        super().__init__()
        self.update(zip(params, args))
        if dict is not None:
            self.update(dict)
        self.outer = outer

    def find(self, value):
        if value in self:
            return self[value]
        else:
            return self.outer.find(value)

    def set(self, variable, value):
        if variable in self:
            self[variable] = value
        else:
            self.outer.set(variable, value)

def create_env():
    env = {
        '+': lambda *a: sum(a),
        '*': operator.mul,
        '-': operator.sub,
        'begin': lambda *x: x[-1],
        '/': operator.truediv,
        '//': operator.floordiv,
        '>':operator.gt, '<':operator.lt, '>=':operator.ge, '<=':operator.le, '=':operator.eq,
        'list': lambda *a: list(a),
        'apply': lambda func, args: func(*args)
        }
    return Env([], [], dict=env)

global_env = create_env()


class Lambda:
    """
    (lambda (r1 r2) ( + r1 r2))
    :param parameters: list of symbols
    """
    def __init__(self, parameters: list, expression: Expression, env):

        self.parameters = parameters
        self.expression = expression
        self.env=env

    def __call__(self, *values):
        return eval(self.expression, env=Env(params=self.parameters, args=values, outer=self.env))


def tokenize(string: str) -> list:
    string = re.sub(comment_regex, "", string)  # remove comments
    return " ".join(string.replace("\n", " ").replace("(", " ( ").replace(")", " ) ").strip().split()).split()

def read_from_tokens(tokens: list) -> Expression:
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF")
    token = tokens.pop(0)
    if token == '(':
        result = []
        while tokens[0] != ')':
            result.append(read_from_tokens(tokens))
        tokens.pop(0)
        return result
    elif token == ')':
        raise SyntaxError("Unexpected ')'")
    elif token == '(*': # comment
        while tokens[0] != '*)':
            tokens.pop(0)
        tokens.pop(0)
    else:
        return atom(token)

def atom(token: str) -> Atom:
    try:
        return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            if token == "#f":
                return Boolean(False)
            elif token == "#t":
                return Boolean(True)
            else:
                return Symbol(token)

def parse(string) -> Expression:
    return read_from_tokens(tokenize(string))

def eval(exp: Expression, env=global_env):
    if isinstance(exp, Number):
        return exp
    elif isinstance(exp, Boolean):
        return exp
    elif isinstance(exp, Symbol):
        return env.find(exp)
    elif exp[0] == "define":
        symbol = exp[1]
        value = eval(exp[2], env=env)
        env[symbol] = value
        return None
    elif exp[0] == 'quote':
        return exp[1]
    elif exp[0] == 'if':
        cond = eval(exp[1], env=env)
        if cond:
            return eval(exp[2], env=env)
        else:
            return eval(exp[3], env=env)
    elif exp[0] == "set!":
        variable = exp[1]
        value = eval(exp[2], env)
        env.set(variable, value)
    elif exp[0] == "lambda":
        parameters = exp[1]
        value = exp[2]
        return Lambda(parameters, value, env=env)
    elif exp[0] == "run":
        file = exp[1]
        return run_file(file, env)
    else:
        function = eval(exp[0], env=env)
        arguments = [eval(sub_exp, env=env) for sub_exp in exp[1:]]
        return function(*arguments)

def repl(env=global_env):
    while True:
        expr = input("lispy> ")
        if expr == "quit":
            return
        try:
            result = eval(parse(expr), env=env)
            print("=> %s" % print_expression(result))
        except Exception as e:
            traceback.print_exc()

def print_expression(expr: Expression):

    if isinstance(expr, List):
        return '(' + ' '.join(((print_expression(e) for e in expr))) + ')'
    elif isinstance(expr, Boolean):
        return {True: "#t", False: "#f"}[expr]
    else:
        return str(expr)


def run_file(file, env):
    with open(file) as f:
        text = f.read()
        return eval(parse(text), env=env)

if __name__=='__main__':
    env = create_env()

    if len(sys.argv) > 1:
        file = sys.argv[1]
        print("(run test.lisp)")
        print("==> %s" % run_file(file, env))
    repl(env)
