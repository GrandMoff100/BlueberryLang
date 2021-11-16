from rply.token import BaseBox
import typing as t


class Box(BaseBox):
    def eval(self, locals: dict, globals: dict):
        return


class BuiltInDataType(Box):
    def __init__(self, value):
        self.value = value

    def eval(self, locals: dict, globals: dict):
        return self.value


class String(BuiltInDataType):
    pass


class Int(BuiltInDataType):
    pass


class Float(BuiltInDataType):
    pass


class Dict(BuiltInDataType):
    pass


class List(BuiltInDataType):
    pass


class Null(BuiltInDataType):
    def __init__(self):
        super().__init__(None)


class Bool(BuiltInDataType):
    pass


# Operators
class Operation(Box):
    def __init__(self, left: Box = None, right: Box = None):
        self.right = right
        self.left = left


class Mul(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) * self.right.eval(locals, globals)


class Divide(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) / self.right.eval(locals, globals)


class FloorDivide(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) // self.right.eval(locals, globals)


class Sub(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) - self.right.eval(locals, globals)


class Add(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) + self.right.eval(locals, globals)


class BinOr(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) | self.right.eval(locals, globals)


class BinAnd(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) & self.right.eval(locals, globals)


class And(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) and self.right.eval(locals, globals)


class Or(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) * self.right.eval(locals, globals)


class BinNot(Operation):
    def eval(self, locals: dict, globals: dict):
        return ~self.left.eval(locals, globals)


class Not(Operation):
    def eval(self, locals: dict, globals: dict):
        return not self.left.eval(locals, globals)


class RShift(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) >> self.right.eval(locals, globals)


class LShift(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) << self.right.eval(locals, globals)


class BinXOr(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) ^ self.right.eval(locals, globals)


class Mod(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) % self.right.eval(locals, globals)


class Exponent(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) ** self.right.eval(locals, globals)


class In(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) in self.right.eval(locals, globals)


class NotIn(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) not in self.right.eval(locals, globals)


# Comparisons
class GE(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) >= self.right.eval(locals, globals)


class LE(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) <= self.right.eval(locals, globals)


class GT(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) > self.right.eval(locals, globals)


class LT(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) < self.right.eval(locals, globals)


class NE(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) != self.right.eval(locals, globals)


class EQ(Operation):
    def eval(self, locals: dict, globals: dict):
        return self.left.eval(locals, globals) == self.right.eval(locals, globals)


class Namespace(Box):
    def __init__(self, name: str):
        self.name = name

    def eval(self, locals: dict, globals: dict):
        value = locals.get(self.name)
        if value is None:
            value = globals.get(self.name)
        if value is None:
            raise NameError(f"{self.name} is undefined")
        return value


class Parameters(Box):
    def __init__(self, name: str, default=None):
        self.args = []
        self.kwargs = {}
        if default:
            self.kwargs[name] = default.eval(locals, globals)
        else:
            self.args.append(name)

    def add(self, parameters):
        self.args += parameters.args
        self.kwargs.update(parameters.kwargs)
        return self


class Return(Box):
    def __init__(self, expression: Box):
        self.expression = expression

    def eval(self, locals: dict, globals: dict):
        return self.expression.eval(locals, globals)


class Statement(Box):
    pass


class Function(Statement):
    def __init__(self, name: str, parameters: Parameters, statements: t.Tuple[Statement]):
        self.name = name
        self.parameters = parameters
        self.statements = statements

    def eval(self, locals: dict, globals: dict):
        scope = locals.get('__scope__')
        for statement in self.statements:
            if isinstance(statement, Return):
                return statement.eval({'__scope__': scope + 1, '__scope_name__': self.name}, globals)
            else:
                statement.eval({'__scope__': scope + 1, '__scope_name__': self.name}, globals)


class If(Statement):
    def __init__(
        self,
        _if_expression: Box,
        _if_statements: t.Tuple[Statement],
        _elifs: t.Tuple[t.Tuple[t.Union[Box, Statement]]] = None,
        _else: Box = None,
        _else_statements: t.Tuple[Statement] = None
    ):
        self._if = self._if_expression
        self._if_statements = _if_statements
        self._else = _else
        self._else_statements = _else_statements
        self._elifs = _elifs

    def eval(self, locals: dict, globals: dict):
        if self._if.eval(locals, globals):
            for statement in self._if_statements:
                if isinstance(statement, Return):
                    return statement.eval(locals, globals)
                else:
                    statement.eval(locals, globals)
        elif self._elifs:
            for expression, statements in self._elifs:
                if expression.eval(locals, globals):
                    for statement in statements:
                        if isinstance(statement, Return):
                            return statement.eval(locals, globals)
                        else:
                            statement.eval(locals, globals)
        elif self._else_statements:
            for statement in self._else_statements:
                if isinstance(statement, Return):
                    return statement.eval(locals, globals)
                else:
                    statement.eval(locals, globals)


class ForLoop(Statement):
    def __init__(self, namespace: str, expression: Box, statements: t.Tuple[Statement]):
        self.namespace = namespace
        self.expression = self.expression
        self.statements = statements

    def eval(self, locals: dict, globals: dict):
        pass


class Pass(Statement):
    pass


class WhileLoop(Statement):
    def __init__(self, expression: Box, statements: t.Tuple[Statement]):
        self.expression = expression
        self.statements = statements

    def eval(self, locals: dict, globals: dict):
        pass


class VariableDeclaration(Statement):
    def __init__(self, name: str, expression: Box):
        self.name = name
        self.expression = expression

    def eval(self, locals: dict, globals: dict):
        value = {self.name: self.expression.eval(locals, globals)}
        scope = locals.get('__scope__')
        if scope == 0:
            globals.update(value)
        locals.update(value)
