import blueberry.ast as ast

from rply import ParserGenerator
from blueberry.lexer import CompilerLexer
from blueberry.tokens import Token


class CompilerParser(CompilerLexer):
    precedence = (
        ('left', ['STATEMENTS']),
        ('left', ['STATEMENT']),
        ('left', ['IN']),
        ('left', ['OR']),
        ('left', ['AND']),
        ('left', ['BINOR']),
        ('left', ['BINXOR']),
        ('left', ['BINAND']),
        ('left', ['NE', 'EQ']),
        ('nonassoc', ['GT', 'LT', 'GE', 'LE']),
        ('left', ['LSHIFT', 'RSHIFT']),
        ('left', ['PLUS', 'MINUS']),  
        ('left', ['TIMES', 'DIVIDE', 'FLOORDIVIDE', 'MOD']),  # 4 * 6 / 3
        ('right', ['UMINUS']),  # -5
        ('right', ['EXPONENT']),  # 2 ** 3
        ('nonassoc', ['PAREN'])
    )

    pg = ParserGenerator(
        Token.tokens,
        precedence=precedence
    )

    @pg.production("statements : statements statement", precedence="STATEMENTS")
    @pg.production("statements : statements expression", precedence="STATEMENTS")
    def statements(p):
        return p[0] + (p[1],)

    @pg.production("statements : statement", precedence="STATEMENTS")
    @pg.production("statements : expression", precedence="STATEMENTS")
    def statements_base(p):
        return (p[0],)

    @pg.production("expression : NAMESPACE")
    def object_NAMESPACE(p):
        return ast.Namespace(p[0].value)

    @pg.production("expression : INT")
    def object_INT(p):
        return ast.Int(int(p[0].value))

    @pg.production("expression : STRING")
    def object_STRING(p):
        return ast.String(p[0].value)

    @pg.production("expression : FLOAT")
    @pg.production("expression : DOUBLE")
    def object_FLOAT(p):
        return ast.Float(float(p[0].value))

    @pg.production("expression : NULL")
    def object_NULL(p):
        return ast.Null()

    @pg.production("expression : BOOL")
    def object_BOOL(p):
        value_map = {
            "False": False,
            "True": True
        }
        return ast.Bool(value_map.get(p[0].value))

    @pg.production("list_items : list_items COMMA expression")
    def list_item(p):
        return p[0] + (p[2],)

    @pg.production("list_items : expression COMMA expression")
    def list_items(p):
        return (p[0],) + (p[2],)

    @pg.production("expression : LBRACKET list_items RBRACKET")
    def list(p):
        return ast.List(p[1])

    @pg.production("expression : LBRACKET expression RBRACKET")
    def list_expression(p):
        return ast.List((p[1],))

    @pg.production("dict_items : expression COLON expression")
    def dict_item(p):
        return ((p[0], p[2]),)

    @pg.production("dict_items : dict_items COMMA expression COLON expression")
    def dict_items(p):
        return p[0] + ((p[2], p[4]),)

    @pg.production("expression : LBRACE dict_items RBRACE")
    def dict_dict_items(p):
        return ast.Dict(dict(p[1]))

    @pg.production("expression : expression TIMES expression", precedence="TIMES")
    @pg.production("expression : expression DIVIDE expression", precedence="DIVIDE")
    @pg.production("expression : expression PLUS expression", precedence="PLUS")
    @pg.production("expression : expression MINUS expression", precedence="MINUS")
    @pg.production("expression : expression BINOR expression", precedence="BINOR")
    @pg.production("expression : expression BINAND expression", precedence="BINAND")
    @pg.production("expression : expression OR expression", precedence="OR")
    @pg.production("expression : expression AND expression", precedence="AND")
    @pg.production("expression : expression MOD expression", precedence="MOD")
    @pg.production("expression : expression FLOORDIVIDE expression", precedence="FLOORDIVIDE")
    @pg.production("expression : expression EXPONENT expression", precedence="EXPONENT")
    @pg.production("expression : expression BINXOR expression", precedence="BINXOR")
    @pg.production("expression : expression LSHIFT expression", precedence="LSHIFT")
    @pg.production("expression : expression RSHIFT expression", precedence="RSHIFT")
    @pg.production("expression : expression GE expression", precedence="GE")
    @pg.production("expression : expression LE expression", precedence="LE")
    @pg.production("expression : expression GT expression", precedence="GT")
    @pg.production("expression : expression LT expression", precedence="LT")
    @pg.production("expression : expression NE expression", precedence="NE")
    @pg.production("expression : expression EQ expression", precedence="EQ")
    @pg.production("expression : expression IN expression", precedence="IN")
    @pg.production("expression : expression NOTIN expression", precedence="IN")
    def double_param_expression(p):
        value_map = {
            'TIMES': ast.Mul,
            'DIVIDE': ast.Divide,
            'FLOORDIVIDE': ast.FloorDivide,
            'PLUS': ast.Add,
            'MINUS': ast.Sub,
            'BINOR': ast.BinOr,
            'BINAND': ast.BinAnd,
            'OR': ast.Or,
            'AND': ast.And,
            'MOD': ast.Mod,
            'EXPONENT': ast.Exponent,
            'BINXOR': ast.BinXOr,
            'LSHIFT': ast.LShift,
            'RSHIFT': ast.RShift,
            'GE': ast.GE,
            'LE': ast.LE,
            'GT': ast.GT,
            'LT': ast.LT,
            'NE': ast.NE,
            'EQ': ast.EQ,
            'IN': ast.In,
            'NOTIN': ast.NotIn
        }
        return value_map.get(p[1].name)(p[0], p[2])

    @pg.production("expression : NOT expression", precedence="UMINUS")
    @pg.production("expression : BINNOT expression", precedence="UMINUS")
    @pg.production("expression : MINUS expression", precedence="UMINUS")
    def single_param_expression(p):
        if p[0].name == 'NOT':
            return ast.Not(p[1])
        elif p[0].name == 'BINNOT':
            return ast.BinNot(p[1])
        elif p[0].name == 'MINUS':
            return ast.Neg(p[1])
        raise AssertionError("This is not supposed to happen!")

    @pg.production("expression : LPAREN expression RPAREN", precedence="PAREN")
    def paren_expression(p):
        return p[1]

    @pg.production("expression : expression PERIOD NAMESPACE")
    def get_attribute(p):
        pass

    @pg.production("expression : expression LPAREN list_items RPAREN")
    @pg.production("expression : expression LPAREN expression RPAREN")
    def function_call(p):
        pass

    @pg.production("statement : NAMESPACE EQUALS expression", precedence="STATEMENT")
    def statement_variable_declaration(p):
        return ast.VariableDeclaration(p[0].value, p[2])

    @pg.production("statement : WHILE expression LBRACE statements RBRACE", precedence="STATEMENT")
    def while_statement(p):
        return ast.WhileLoop()

    @pg.production("statement : RETURN expression")
    def return_statement(p):
        return ast.Return(p[1])

    @pg.production("parameters : NAMESPACE")
    @pg.production("parameters : NAMESPACE EQUALS expression")
    def function_parameters_base(p):
        if len(p) == 1:
            return ast.Parameters(p[0].value)
        elif len(p) == 3:
            return ast.Parameters(p[0].value, default=p[2])
        raise AssertionError("This should be impossible!")

    @pg.production("parameters : parameters COMMA NAMESPACE")
    @pg.production("parameters : parameters COMMA NAMESPACE EQUALS expression")
    def function_parameters(p):
        if len(p) == 3:
            return p[0].add(ast.Parameters(p[2].value))
        elif len(p) == 5:
            return p[0].add(ast.Parameters(p[2].value), default=p[4])
        raise AssertionError("This should be impossible!")

    @pg.production("statement : FUNCTION NAMESPACE LPAREN parameters RPAREN LBRACE statements RBRACE")
    def function_statement(p):
        return ast.Function(
            p[1].value,
            p[3],
            p[6]
        )

    @pg.production("statement : FOR NAMESPACE IN expression LBRACE statements RBRACE", precedence="STATEMENT")
    def for_statement(p):
        return ast.ForLoop(
            p[1].value,
            p[3],
            p[5]
        )

    @pg.production("statement : PASS")
    def pass_statement(p):
        return ast.Pass()

    @pg.production("if : IF expression LBRACE statements RBRACE")
    def if_statement(p):
        return p[1], p[3]

    @pg.production("elif : ELIF expression LBRACE statements RBRACE")
    def elif_statement(p):
        return p[1], p[3]

    @pg.production("elifs : elif")
    def elifs(p):
        return p[0]

    @pg.production("elifs : elifs elif")
    def elifs_elif(p):
        return p[0] + (p[1],)

    @pg.production("else : ELSE LBRACE statements RBRACE")
    def else_statement(p):
        return p[2]

    @pg.production("statement : if")
    def statement_if(p):
        return ast.If(
            *p[0]
        )

    @pg.production("statement : if elifs")
    def statement_if_elifs(p):
        return ast.If(
            *p[0],
            _elifs=p[1]
        )

    @pg.production("statement : if elifs else")
    def statement_if_elifs_else(p):
        return ast.If(
            *p[0],
            _elifs=p[1],
            _else=p[2]
        )

    @pg.production("statement : if else")
    def statement_if_else(p):
        return ast.If(
            *p[0],
            _else=p[1]
        )

    @pg.error
    def error(token):
        exit(print("Unexpected", token.gettokentype(), repr(token.value), "at", token.getsourcepos()))
