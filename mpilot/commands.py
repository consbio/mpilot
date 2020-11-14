from __future__ import print_function
from __future__ import unicode_literals

import pkgutil
from collections import namedtuple

import six
from six import add_metaclass

from mpilot.exceptions import MPilotError, MissingParameters, NoSuchParameter
from mpilot.params import TupleParameter

if six.PY3:
    from importlib import import_module
    from importlib.util import module_from_spec
else:
    import imp

Argument = namedtuple("Argument", ("name", "value", "lineno"))


class CommandMeta(type):
    """ Command metaclass, used to automatically register commands, which can then be loaded by name. """

    _commands_by_name = {}

    def __new__(mcs, name, bases, attrs):
        attrs.update({"inputs": attrs.get("inputs", {}), "output": attrs.get("output", None)})

        # Add an optional "Metadata" input to all commands
        attrs["inputs"]["Metadata"] = TupleParameter(required=False)

        new_class = super(CommandMeta, mcs).__new__(mcs, name, bases, attrs)

        # Use the `name` attribute if this class defines one. Otherwise, use the class name itself.
        command_name = attrs.get("name", name)
        if command_name in mcs._commands_by_name:
            raise MPilotError(
                "A command named '{}' has been declared more than once. Command names must be unique.".format(
                    command_name
                )
            )

        new_class.name = command_name
        mcs._commands_by_name[command_name] = new_class

        new_class._command_by_name = mcs._commands_by_name
        new_class.required_inputs = {name: param for name, param in attrs["inputs"].items() if param.required}

        return new_class


@add_metaclass(CommandMeta)
class Command(object):
    @classmethod
    def load_commands(cls, module):
        if isinstance(module, six.string_types):
            if isinstance(module, bytes):
                module = module.decode()

            if six.PY3:
                module = import_module(module)
            else:
                module = imp.load_module(module)

        if hasattr(module, "__path__"):
            if six.PY3:
                for info, name, _ in pkgutil.iter_modules(module.__path__):
                    spec = info.find_spec(name)
                    new_module = module_from_spec(spec)
                    spec.loader.exec_module(new_module)
                    cls.load_commands(new_module)
            else:
                for module_loader, name, _ in pkgutil.iter_modules(module.__path__):
                    new_module = module_loader.load_module(name)
                    cls.load_commands(new_module)

    @classmethod
    def find_by_name(cls, name):
        """ Finds and returns a command matching `name` """

        return cls._command_by_name.get(name)

    def __init__(self, result_name, arguments=(), program=None, lineno=None):
        self.result_name = result_name
        self.arguments = arguments
        self.program = program
        self.lineno = lineno

        self.argument_lines = {arg.name: arg.lineno for arg in arguments}

        self.is_running = False
        self.is_finished = False
        self._result = None

    @property
    def result(self):
        if not self.is_finished:
            self.run()

        return self._result

    @property
    def metadata(self):
        for arg in self.arguments:
            if arg.name == "Metadata":
                return self.inputs["Metadata"].clean(arg.value, self.program, self.argument_lines.get(arg.name))
        return {}

    def validate_params(self, params):
        required_inputs = [key for key, value in self.inputs.items() if value.required]
        all_inputs = [key for key in self.inputs.keys()]

        missing_params = set(required_inputs).difference(params.keys())
        if missing_params:
            raise MissingParameters(self.result_name, missing_params, self.lineno)

        cleaned = {}
        for name, value in params.items():
            if name not in all_inputs:
                raise NoSuchParameter(self.result_name, name, self.argument_lines.get(name))

            cleaned[name] = self.inputs[name].clean(value, self.program, self.argument_lines.get(name))

        return cleaned

    def run(self):
        if self.is_running:
            pass  # Raise recursive error

        if not self.is_finished:
            self.is_running = True
            self._result = self.execute(**self.validate_params({arg.name: arg.value for arg in self.arguments}))
            self.is_running = False
            self.is_finished = True

    def execute(self, **kwargs):
        raise NotImplemented
