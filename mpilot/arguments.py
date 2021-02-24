import six

if six.PY3:
    from typing import Any, List


class Argument(object):
    def __init__(self, name, value, lineno=None):
        # type: (str, Any, int) -> None

        self.name = name
        self.value = value
        self.lineno = lineno


class ListArgument(Argument):
    def __init__(self, name, value, lineno=None, list_linenos=None):
        # type: (str, List[Any], int, List[int]) -> None

        super(ListArgument, self).__init__(name, value, lineno=lineno)

        self.list_linenos = list_linenos
