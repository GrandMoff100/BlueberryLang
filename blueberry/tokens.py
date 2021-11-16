class Token:
    name: str = None
    regex: str = None
    tokens: dict = {}

    def __init_subclass__(cls, **kwargs):
        if cls.regex is not None:
            Token.tokens.update({cls.__name__.upper(): cls.regex})
        super().__init_subclass__(**kwargs)


# Types
class Null(Token):
    regex = "None"


class Bool(Token):
    regex = "(?:True)|(?:False)"


class Int(Token):
    regex = r"\d+"


class Float(Token):
    regex = r"0+\.\d+"


class Double(Token):
    regex = r"\d*[1-9]\.\d+"


class String(Token):
    # Credit: https://stackoverflow.com/questions/49906179/regex-to-match-string-syntax-in-code
    regex = '([bruf]*)("""|\'\'\'|"|\')(?:(?!\\2)(?:\\\\.|[^\\\\]))*\\2'


# Comparison Operators
class EQ(Token):
    regex = "=="


class NE(Token):
    regex = "!="


class GE(Token):
    regex = ">="


class LE(Token):
    regex = "<="


class LT(Token):
    regex = "<"


class GT(Token):
    regex = ">"


# Bianry Operators
class Minus(Token):
    regex = "-"


class Plus(Token):
    regex = r"\+"


class Times(Token):
    regex = r"\*"


class Divide(Token):
    regex = "/"


class Mod(Token):
    regex = "%"


class Exponent(Token):
    regex = r"\*\*"


class FloorDivide(Token):
    regex = "//"


class BinOr(Token):
    regex = r"\|"


class BinAnd(Token):
    regex = "&"


class BinXOr(Token):
    regex = r"\^"


class BinNot(Token):
    regex = "~"


class LShift(Token):
    regex = "<<"


class RShift(Token):
    regex = ">>"


# Characters
class LBrace(Token):
    regex = r"\{"


class RBrace(Token):
    regex = r"\}"


class LBracket(Token):
    regex = r"\["


class RBracket(Token):
    regex = r"\]"


class Comma(Token):
    regex = ","


class Period(Token):
    regex = r"\."


class Colon(Token):
    regex = ":"


class LParen(Token):
    regex = r"\("


class RParen(Token):
    regex = r"\)"


class Equals(Token):
    regex = "="


# Namespaces
class While(Token):
    regex = "while"


class If(Token):
    regex = "if"


class Elif(Token):
    regex = "elif"


class Else(Token):
    regex = "else"


class For(Token):
    regex = "for"


class In(Token):
    regex = "in"


class NotIn(Token):
    regex = "not in"


class Pass(Token):
    regex = "pass"


class Or(Token):
    regex = r"or"


class And(Token):
    regex = r"and"


class Not(Token):
    regex = r"not"


class Return(Token):
    regex = "return"


class Function(Token):
    regex = "def"


class Namespace(Token):
    regex = r"[a-zA-Z_]\w*"
