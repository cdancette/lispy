import re

comment_regex = re.compile("\(\*.*?\*\)")

from lisptypes import *

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
