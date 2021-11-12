from rply import ParserGenerator
from blueberry.lexer import CompilerLexer
from blueberry.tokens import Token


class CompilerParser(CompilerLexer):
    precedence = (
        ('left', ['RETURN']),  # return expr
        ('left', ['LSHIFT', 'RSHIFT']),
        ('left', ['AND', 'OR', 'BINAND', 'BINOR', 'BINXOR']),  # (cond 1) AND (cond2)
        ('right', ['NOT', 'BINNOT']),
        ('left', ['GT', 'LT', 'GE', 'LE', 'NE', 'EQ']),
        ('left', ['PLUS', 'MINUS']),  # 3 - 2 + 4
        ('left', ['TIMES', 'DIVIDE', 'FLOORDIVIDE']),  # 4 * 6 / 3
        ('left', ['MOD']),  # 4 % 3
        ('left', ['EXPONENT']),  # 2 ** 3
        ('right', ['UMINUS']),  # -5
    )

    pg = ParserGenerator(
        Token.tokens,
        precedence=precedence
    )

    @pg.production("")
    def program():
        pass
        