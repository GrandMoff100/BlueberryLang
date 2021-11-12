import sys
from blueberry.lexer import CompilerLexer


compiler = CompilerLexer()

lexer = compiler.lg.build()


file = sys.argv[1]


with open(file, "r") as f:
    code = f.read()


print(code)

for tok in lexer.lex(code):
    print(tok)


