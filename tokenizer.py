import re


__author__ = 'mijicd'


REGEX = r'(?:\d*\.\d+)|(?:\d+)|(?:[()+\-\^/*])'


class ExpressionNotStringError(Exception):
    pass


class UnknownCharacterError(Exception):
    pass


def tokenize(expression):
    if not isinstance(expression, str):
        raise ExpressionNotStringError("Expression should be string!")

    tokens = re.findall(REGEX, expression)

    if expression.replace(" ", "") != "".join(tokens):
        raise UnknownCharacterError("Expression contains unsupported character(s).")

    return tokens
