class Argument(object):
    def __init__(self, name, value, lineno=None):
        self.name = name
        self.value = value
        self.lineno = lineno


class ListArgument(Argument):
    def __init__(self, name, value, lineno=None, list_linenos=None):
        super(ListArgument, self).__init__(name, value, lineno=lineno)

        self.list_linenos = list_linenos
