from rply.token import BaseBox


class DataType(BaseBox):
    def __init__(self, raw: str, type: str):
        self.raw = raw
        self.type = type

    def eval(self):
        return self.raw




