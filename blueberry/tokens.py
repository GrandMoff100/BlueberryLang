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
    regex = "^"


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
    regex = "\."


class Colon(Token):
    regex = ":"


class LParen(Token):
    regex = r"\("


class RParen(Token):
    regex = r"\)"
