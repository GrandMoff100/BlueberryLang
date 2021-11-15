from rply.token import BaseBox


class Box(BaseBox):
    def eval(self):
        return


class BuiltInDataType(Box):
    def __init__(self, value):
        self.value = value

    def eval(self):
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
    def __init__(self, left=None, right=None):
        self.right = right
        self.left = left


class Mul(Operation):
    def eval(self):
        return self.left.eval() * self.right.eval()


class Divide(Operation):
    def eval(self):
        return self.left.eval() / self.right.eval()


class FloorDivide(Operation):
    def eval(self):
        return self.left.eval() // self.right.eval()


class Sub(Operation):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Add(Operation):
    def eval(self):
        return self.left.eval() + self.right.eval()


class BinOr(Operation):
    def eval(self):
        return self.left.eval() | self.right.eval()


class BinAnd(Operation):
    def eval(self):
        return self.left.eval() & self.right.eval()


class And(Operation):
    def eval(self):
        return self.left.eval() and self.right.eval()


class Or(Operation):
    def eval(self):
        return self.left.eval() * self.right.eval()


class BinNot(Operation):
    def eval(self):
        return ~self.left.eval()


class Not(Operation):
    def eval(self):
        return not self.left.eval()


class RShift(Operation):
    def eval(self):
        return self.left.eval() >> self.right.eval()


class LShift(Operation):
    def eval(self):
        return self.left.eval() << self.right.eval()


class BinXOr(Operation):
    def eval(self):
        return self.left.eval() ^ self.right.eval()


class Mod(Operation):
    def eval(self):
        return self.left.eval() % self.right.eval()


class Exponent(Operation):
    def eval(self):
        return self.left.eval() ** self.right.eval()


class In(Operation):
    def eval(self):
        return self.left.eval() in self.right.eval()


class NotIn(Operation):
    def eval(self):
        return self.left.eval() not in self.right.eval()


# Comparisons
class GE(Operation):
    def eval(self):
        return self.left.eval() >= self.right.eval()


class LE(Operation):
    def eval(self):
        return self.left.eval() <= self.right.eval()


class GT(Operation):
    def eval(self):
        return self.left.eval() > self.right.eval()


class LT(Operation):
    def eval(self):
        return self.left.eval() < self.right.eval()


class NE(Operation):
    def eval(self):
        return self.left.eval() != self.right.eval()


class EQ(Operation):
    def eval(self):
        return self.left.eval() == self.right.eval()


class Namespace(Box):
    def __init__(self, name):
        self.name = name

    def eval(self):
        return f"global fetch {self.name}"