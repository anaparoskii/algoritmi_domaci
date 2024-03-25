"""Modul omogućava parsiranje aritmetičkih izraza."""
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


if __name__ == '__main__':
    #
    # key: izraz, value: očekivana lista tokena
    #
    test_cases = {
        # test floats
        "3.14   ^2": ['3.14', '^', '2'],
        "(2.08-.03) ^  2": ['(', '2.08', '-', '.03', ')', '^', '2'],

        # test integers
        "2+(3*4)": ['2', '+', '(', '3', '*', '4', ')'],
        "22     56": ['22', '56'],

        # test invalid
        "ab cd": [],
        "10,22": ['10', '22']
    }

    for expression, expected in test_cases.items():
        assert expected == tokenize(expression)
