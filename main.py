#!/usr/bin/env python3

import traceback
import readline
import sys

# readline.parse_and_bind('tab: complete')

from lisptypes import *
from parser import tokenize, parse
from eval import eval, create_env, run_file

global_env = create_env()

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


if __name__=='__main__':
    env = create_env()

    if len(sys.argv) > 1:
        file = sys.argv[1]
        print("(run test.lisp)")
        print("==> %s" % run_file(file, env))
    repl(env)
