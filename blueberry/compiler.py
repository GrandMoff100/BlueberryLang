from blueberry.parser import CompilerParser
import warnings


class Compiler(CompilerParser):
    def ignore_warnings(self):
        warnings.filterwarnings('ignore')
