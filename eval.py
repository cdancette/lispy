from lisptypes import *
import operator as op

from parser import parse

class Env(dict):
    def __init__(self, params, args, dict=None, outer=None):
        super().__init__()
        self.update(zip(params, args))
        if dict is not None:
            self.update(dict)
        self.outer = outer

    def find(self, variable):
        if variable in self:
            return self[variable]
        else:
            if self.outer is not None:
                return self.outer.find(variable)
            else:
                raise SyntaxError("'%s' not found in environment" % variable)

    def set(self, variable, value):
        if variable in self:
            self[variable] = value
        else:
            if self.outer is not None:
                self.outer.set(variable, value)
            else:
                raise SyntaxError("'%s' not find in environment" % variable)

def create_env():
    env = {
        '+': lambda *a: sum(a),
        '*': op.mul,
        '-': op.sub,
        'begin': lambda *x: x[-1],
        '/': op.truediv,
        '//': op.floordiv,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'list': lambda *a: list(a),
        'apply': lambda func, args: func(*args)
        }
    return Env([], [], dict=env)



def run_file(file, env):
    with open(file) as f:
        text = f.read()
        return eval(parse(text), env=env)

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


def eval(exp: Expression, env):
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