from rply import LexerGenerator
from blueberry.tokens import Token


class CompilerLexer:
    def __init__(self):
        self.generator = LexerGenerator()
        for name, regex in Token.tokens.items():
            self.generator.add(name, regex)

