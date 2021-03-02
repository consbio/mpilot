from __future__ import absolute_import

import six

if six.PY3:
    from typing import Dict, Any, Union, TextIO

from .arguments import Argument, ListArgument
from .commands import Command
from .exceptions import (
    CommandDoesNotExist,
    DuplicateResult,
    MissingParameters,
    NoSuchParameter,
)
from .params import ResultParameter, ListParameter
from .parser.parser import Parser, ProgramNode
from .utils import flatten, EEMS_COMMANDS, convert_eems2_commands


class Program(object):
    """ A program consists of connected MPilot commands, and the arguments that will be used to run them """

    def __init__(self, working_dir=None):
        # Commands lookup, in the form of {result_name: command, ...}
        self.commands = {}

        self.working_dir = working_dir

    @classmethod
    def from_source(cls, source, working_dir=None):
        # type: (str, str) -> Program
        """ Creates a program from MPilot source code """

        def resolve_list(name, expression_node):
            """ Recursively resolves parsed list expressions into ListArgument values """

            return ListArgument(
                name,
                [
                    resolve_list(name, n) if isinstance(n.value, list) else n.value
                    for n in expression_node.value
                ],
                lineno=expression_node.lineno,
                list_linenos=[n.lineno for n in expression_node.value],
            )

        program = cls(working_dir)
        program_node = Parser().parse(source)

        if program_node.version == 2 or any(
            node.command in EEMS_COMMANDS for node in program_node.commands
        ):
            program_node = ProgramNode(convert_eems2_commands(program_node.commands), 3)

        for node in program_node.commands:
            command_cls = Command.find_by_name(node.command)
            if not command_cls:
                raise CommandDoesNotExist(node.command, node.lineno)

            arguments = {}
            for argument_node in node.arguments:
                if isinstance(argument_node.value.value, list):
                    arguments[argument_node.name] = resolve_list(
                        argument_node.name, argument_node.value
                    )
                else:
                    arguments[argument_node.name] = Argument(
                        argument_node.name,
                        argument_node.value.value,
                        argument_node.lineno,
                    )

            program.add_command(command_cls, node.result_name, arguments, node.lineno)

        return program

    def add_command(self, command_cls, result_name, arguments, lineno=None):
        # type: (type(Command), str, Dict[str, Any], int) -> None
        """ Adds a command to the program """

        if result_name in self.commands:
            raise DuplicateResult(result_name, lineno=lineno)

        missing_params = set(command_cls.required_inputs.keys()).difference(
            arguments.keys()
        )
        if missing_params:
            raise MissingParameters(command_cls, missing_params, lineno=lineno)

        command_args = []
        for (name, value) in sorted(arguments.items()):
            if name not in command_cls.inputs:
                raise NoSuchParameter(
                    command_cls,
                    name,
                    lineno=value.lineno if isinstance(value, Argument) else None,
                )

            if isinstance(value, Argument):
                command_args.append(value)
            else:
                command_args.append(Argument(name, value))

        self.commands[result_name] = command_cls(
            result_name, command_args, program=self, lineno=lineno
        )

    def to_string(self):
        # type: () -> str
        """ Returns a string with commands formatted in the MPilot command file syntax """

        def serialize_value(value, argument, command):
            # type: (Any, Argument, Command) -> str

            param = command.inputs[argument.name]

            if isinstance(param, ResultParameter) or (
                isinstance(param, ListParameter)
                and isinstance(param.value_type, ResultParameter)
            ):
                return str(value)
            if isinstance(value, six.string_types):
                return '"{}"'.format(value)
            else:
                return str(value)

        def serialize_argument(argument, command):
            # type: (Argument, Command) -> str

            if isinstance(argument, ListArgument):
                return "[{}]".format(
                    ", ".join(
                        serialize_value(x, argument, command) for x in argument.value
                    )
                )
            elif isinstance(argument.value, dict):
                return "[{}]".format(
                    ", ".join(
                        '"{}": "{}"'.format(key, value)
                        for key, value in argument.value.values()
                    )
                )
            return serialize_value(argument.value, argument, command)

        def serialize_command(command):
            # type: (Command) -> str

            return "{} = {}({})".format(
                command.result_name,
                command.name,
                "\n    {}\n".format(
                    ",\n    ".join(
                        "{} = {}".format(a.name, serialize_argument(a, command))
                        for a in command.arguments
                    )
                ),
            )

        return "\n".join(
            serialize_command(command) for command in self.commands.values()
        )

    def to_file(self, file_or_path):
        # type: (Union[TextIO, str]) -> None
        if hasattr(file_or_path, 'write'):
            f = file_or_path
        else:
            f = open(file_or_path, 'w')

        f.write(self.to_string())

    def run(self):
        # Build dependency lookup
        dependents = {}  # {result_name, [dependent_name, ...], ...}

        for command in self.commands.values():
            references = []
            for argument in command.arguments:
                value = command.inputs[argument.name].clean(
                    argument.value, self, lineno=argument.lineno
                )

                if isinstance(command.inputs[argument.name], ResultParameter):
                    references.append(
                        value.result_name if isinstance(value, Command) else value
                    )
                if isinstance(value, (list, tuple)):
                    references += [x for x in flatten(value) if isinstance(x, Command)]

            for reference in references:
                dependents[reference] = dependents.get(reference, set())
                dependents[reference].add(command.result_name)

        # Find and run leaf nodes (commands without any dependents)
        for command in (
            command
            for command in self.commands.values()
            if not dependents.get(command.result_name)
        ):
            command.run()
