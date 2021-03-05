from __future__ import print_function

from collections import namedtuple

import six
from six import add_metaclass

if six.PY3:
    from typing import List, Any, Dict

from mpilot.exceptions import MissingParameters, NoSuchParameter
from mpilot.params import TupleParameter


Argument = namedtuple("Argument", ("name", "value", "lineno"))
CommandInfo = namedtuple("CommandInfo", ("module", "command"))


class CommandMeta(type):
    """ Command metaclass, used to automatically register commands, which can then be loaded by name. """

    _commands = set()

    def __new__(mcs, name, bases, attrs):
        attrs.update(
            {"inputs": attrs.get("inputs", {}), "output": attrs.get("output", None)}
        )

        # Add an optional "Metadata" input to all commands
        attrs["inputs"]["Metadata"] = TupleParameter(required=False)

        new_class = super(CommandMeta, mcs).__new__(mcs, name, bases, attrs)

        # Use an explicit command name if one is set, otherwise use the class name
        command_name = attrs.get("name", name)

        new_class.name = command_name
        new_class.display_name = attrs.get("display_name", command_name)
        new_class.required_inputs = {
            name: param for name, param in attrs["inputs"].items() if param.required
        }

        if not any(
            info.module == new_class.__module__
            and getattr(info.command, "name", info.command.__name__) == command_name
            for info in mcs._commands
        ):
            mcs._commands.add(CommandInfo(new_class.__module__, new_class))

        new_class._commands = mcs._commands

        return new_class


@add_metaclass(CommandMeta)
class Command(object):
    @classmethod
    def get_commands(cls):
        # type: () -> List[CommandInfo]

        return list(cls._commands)

    def __init__(self, result_name, arguments=[], program=None, lineno=None):
        # type: (str, List[Any], Any, int) -> None

        self.result_name = result_name
        self.arguments = arguments
        self.program = program
        self.lineno = lineno

        self.argument_lines = {arg.name: arg.lineno for arg in arguments}

        self.is_finished = False
        self._result = None

    @property
    def result(self):
        if not self.is_finished:
            self.run()

        return self._result

    @property
    def metadata(self):
        # type: () -> Dict[str, str]

        for arg in self.arguments:
            if arg.name == "Metadata":
                return self.inputs["Metadata"].clean(
                    arg.value, self.program, self.argument_lines.get(arg.name)
                )
        return {}

    def get_argument_value(self, name, default=None):
        # type: (str, Any) -> Any

        for arg in self.arguments:
            if arg.name == name:
                return arg.value
        return default

    def validate_params(self, params):
        # type: (Dict[str, Any]) -> Dict[str, Any]

        required_inputs = [key for key, value in self.inputs.items() if value.required]
        all_inputs = [key for key in self.inputs.keys()]

        missing_params = set(required_inputs).difference(params.keys())
        if missing_params:
            raise MissingParameters(self.result_name, missing_params, self.lineno)

        cleaned = {}
        for name, value in params.items():
            if name not in all_inputs:
                raise NoSuchParameter(
                    self.result_name, name, self.argument_lines.get(name)
                )

            cleaned[name] = self.inputs[name].clean(
                value, self.program, self.argument_lines.get(name)
            )

        return cleaned

    def run(self):
        if not self.is_finished:
            self.is_running = True
            self._result = self.execute(
                **self.validate_params({arg.name: arg.value for arg in self.arguments})
            )
            self.is_finished = True

    def execute(self, **kwargs):
        raise NotImplemented
