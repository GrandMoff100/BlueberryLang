import sys
from blueberry.compiler import Compiler


compiler = Compiler()
# compiler.ignore_warnings()
lexer = compiler.lg.build()
parser = compiler.pg.build()

file = sys.argv[1]
with open(file, "r") as f:
    code = f.read()

ast = parser.parse(lexer.lex(code))

print(ast)
