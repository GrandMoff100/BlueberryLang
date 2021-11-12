from blueberry.lexer import CompilerLexer
from blueberry.tokens import Token


class CompilerParser(CompilerLexer):
    def __init__(self):
        super().__init__()
        