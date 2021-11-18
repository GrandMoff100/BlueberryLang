class Scope(dict):
    def __init__(
        self,
        name='__main__',
        layer=0,
        locals=None,
        globals=None,
        file=None
    ):
        self.layer = layer
        self.name = name
        self.file = file
        self.update(locals=Locals.default(self) if not locals else locals)
        self.update(globals=Globals.default(self) if not globals else globals)
        self.update(sub_scopes={})

    def new_scope(self, function):
        scope = Scope(
            layer=self.layer + 1,
            name=function.name,
            file=self.file,
            globals=self.globals
        )
        self['sub_scopes'][function.name] = scope
        scope.globals.update(self.locals)
        return scope

    @property
    def locals(self):
        return self['locals']

    @property
    def globals(self):
        return self['globals']

    def fetch_namespace(self, name: str):
        if name in self.locals:
            return self.locals.get(name)
        elif name in self.globals:
            return self.globals.get(name)
        elif name == '__name__':
            return self.name
        elif name == '__scope_layer__':
            return self.layer
        elif name == '__file__':
            pass 


class Locals(dict):
    @staticmethod
    def default(scope):
        return Locals({
            '__name__': scope.name,
            '__file__': scope.file,
            '__scope_layer__': scope.layer,
            })


class Globals(dict):
    @staticmethod
    def default(scope):
        return Globals({
            '__name__': scope.name,
            '__file__': scope.file,
            '__scope_layer__': scope.layer,
            })

