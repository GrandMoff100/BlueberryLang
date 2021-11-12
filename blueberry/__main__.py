import sys
from blueberry.compiler import Compiler
from blueberry.state import CompilerState


compiler = Compiler()
lexer = compiler.lg.build()
parser = compiler.pg.build()


file = sys.argv[1]
with open(file, "r") as f:
    code = f.read()

print(code)

ast = parser.parse(lexer.lex(code))

print(ast)
