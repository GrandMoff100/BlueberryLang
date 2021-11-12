from rply import LexerGenerator
from blueberry.tokens import Token


class CompilerLexer:
    def __init__(self):
        self.lg = LexerGenerator()
        for name, regex in Token.tokens.items():
            self.lg.add(name, regex)
        self.lg.ignore(r"\s+")
        self.lg.ignore(r"#.*")

