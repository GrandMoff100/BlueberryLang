from rply.token import BaseBox
from blueberry.scope import Scope

import typing as t
import operator


class Box(BaseBox):
    def eval(self, scope: Scope):
        return

    def __repr__(self):
        return f'<{type(self).__name__}>'

    def tree(self, level=0):
        print('  ' * level, self)
        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if isinstance(value, Box):
                    value.tree(level + 1) 
                for            


class BuiltInDataType(Box):
    def __init__(self, value):
        self.value = value

    def eval(self, scope: Scope):
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
    def eval(self, scope: Scope):
        return operator.mul(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class Divide(Operation):
    def eval(self, scope: Scope):
        return operator.div(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class FloorDivide(Operation):
    def eval(self, scope: Scope):
        return operator.floordiv(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class Sub(Operation):
    def eval(self, scope: Scope):
        return operator.sub(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class Add(Operation):
    def eval(self, scope: Scope):
        return operator.add(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class And(Operation):
    def eval(self, scope: Scope):
        return operator.and_(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class Or(Operation):
    def eval(self, scope: Scope):
        return operator.or_(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class BinOr(Or):
    pass


class BinAnd(And):
    pass


class BinNot(Operation):
    def eval(self, scope: Scope):
        return operator.invert(self.left.eval(scope))


class Not(Operation):
    def eval(self, scope: Scope):
        return operator.not_(self.left.eval(scope))

class Neg(Operation):
    def eval(self, scope: Scope):
        return operator.neg(self.left)

class RShift(Operation):
    def eval(self, scope: Scope):
        return operator.rshift(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class LShift(Operation):
    def eval(self, scope: Scope):
        return operator.lshift(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class BinXOr(Operation):
    def eval(self, scope: Scope):
        return operator.xor(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class Mod(Operation):
    def eval(self, scope: Scope):
        return operator.mod(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class Exponent(Operation):
    def eval(self, scope: Scope):
        return operator.pow(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class In(Operation):
    def eval(self, scope: Scope):
        return operator.contains(
            self.right.eval(scope),
            self.left.eval(scope)
        )


class NotIn(Operation):
    def eval(self, scope: Scope):
        return not operator.contains(
            self.right.eval(scope),
            self.left.eval(scope)
        )


# Comparisons
class GE(Operation):
    def eval(self, scope: Scope):
        return operator.ge(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class LE(Operation):
    def eval(self, scope: Scope):
        return operator.le(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class GT(Operation):
    def eval(self, scope: Scope):
        return operator.gt(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class LT(Operation):
    def eval(self, scope: Scope):
        return operator.lt(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class NE(Operation):
    def eval(self, scope: Scope):
        return operator.ne(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class EQ(Operation):
    def eval(self, scope: Scope):
        return operator.eq(
            self.left.eval(scope),
            self.right.eval(scope)
        )


class Parameters(Box):
    def __init__(self, name: str, default=None):
        self.args = []
        self.kwargs = {}
        if default:
            self.kwargs[name] = default
        else:
            self.args.append(name)

    def add(self, parameters):
        self.args += parameters.args
        self.kwargs.update(parameters.kwargs)
        return self

    def eval(self, scope: Scope):
        for name, expression in self.kwargs.items():
            self.kwargs[name] = expression.eval(scope)


class Statement(Box):
    pass


class Return(Statement):
    def __init__(self, expression: Box):
        self.expression = expression

    def eval(self, scope: Scope):
        return self.expression.eval(scope)


class Function(Statement):
    def __init__(self, name: str, parameters: Parameters, statements: t.Tuple[Statement]):
        self.name = name
        self.parameters = parameters
        self.statements = statements

    def eval(self, scope: Scope):
        self.parameters.eval(scope)
        value = {self.name: self}
        if scope.name == '__main__':
            scope.globals.update(value)
        scope.locals.update(value)

    def call(self, scope: Scope):
        for statement in self.statements:
            if isinstance(statement, Return):
                return statement.eval(scope.new_scope(self))
            else:
                statement.eval(scope.new_scope(self))

class If(Statement):
    def __init__(
        self,
        _if_expression: Box,
        _if_statements: t.Tuple[Statement],
        _elifs: t.Tuple[t.Tuple[t.Union[Box, Statement]]] = None,
        _else: Box = None,
        _else_statements: t.Tuple[Statement] = None
    ):
        self._if = _if_expression
        self._if_statements = _if_statements
        self._else = _else
        self._else_statements = _else_statements
        self._elifs = _elifs

    def eval(self, scope: Scope):
        if self._if.eval(scope):
            for statement in self._if_statements:
                if isinstance(statement, Return):
                    return statement.eval(scope)
                else:
                    statement.eval(scope)
        elif self._elifs:
            for expression, statements in self._elifs:
                if expression.eval(scope):
                    for statement in statements:
                        if isinstance(statement, Return):
                            return statement.eval(scope)
                        else:
                            statement.eval(scope)
        elif self._else_statements:
            for statement in self._else_statements:
                if isinstance(statement, Return):
                    return statement.eval(scope)
                else:
                    statement.eval(scope)


class ForLoop(Statement):
    def __init__(self, namespace: str, expression: Box, statements: t.Tuple[Statement]):
        self.namespace = namespace
        self.expression = expression
        self.statements = statements

    def eval(self, scope: Scope):
        pass


class Pass(Statement):
    pass


class WhileLoop(Statement):
    def __init__(self, expression: Box, statements: t.Tuple[Statement]):
        self.expression = expression
        self.statements = statements

    def eval(self, scope: Scope):
        pass


class VariableDeclaration(Statement):
    def __init__(self, name: str, expression: Box):
        self.name = name
        self.expression = expression

    def eval(self, scope: Scope):
        value = {self.name: self.expression.eval(scope)}
        if scope.name == '__main__':
            scope.globals.update(value)
        scope.locals.update(value)


class Namespace(Box):
    def __init__(self, name: str):
        self.name = name

    def eval(self, scope: Scope):
        value = scope.locals.get(self.name)
        if value is None:
            value = scope.globals.get(self.name)
        if value is None:
            raise NameError(f"{self.name} is undefined")
        return value


class File(Box):
    def __init__(self, statements: t.Tuple[Statement]):
        self.statements = statements

    def eval(self):
        main_scope = Scope()
        for statement in self.statements:
            statement.eval(main_scope)
