from rply import LexerGenerator
from blueberry.tokens import Token


class CompilerLexer:
    lg = LexerGenerator()

    def __init__(self):
        for name, regex in Token.tokens.items():
            self.lg.add(name, regex)
        self.lg.ignore(r"\s+")
        self.lg.ignore(r"#.*")
