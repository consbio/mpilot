from __future__ import absolute_import
from __future__ import unicode_literals

from .commands import Command, Argument
from .exceptions import CommandDoesNotExist, DuplicateResult, MissingParameters, NoSuchParameter, ResultDoesNotExist
from .params import ResultParameter, ListParameter
from .parser.parser import Parser
from .utils import flatten


class Program(object):
    """ A program consists of connected MPilot commands, and the arguments that will be used to run them """

    def __init__(self, working_dir=None):
        # Commands lookup, in the form of {result_name: command, ...}
        self.commands = {}

        self.working_dir = working_dir

    @classmethod
    def from_source(cls, source, working_dir=None):
        """ Creates a program from MPilot source code """

        program = cls(working_dir)
        command_nodes = Parser().parse(source)

        # Check for duplicate result names
        result_names = set()
        for node in command_nodes:
            if node.result_name in result_names:
                raise DuplicateResult(node.result_name, node.lineno)
            result_names.add(node.result_name)

        # Resolve parsed results into `Command` instances
        program.resolve_commands(command_nodes)

        return program

    def resolve_commands(self, command_nodes):
        """ Creates `Command `instances from a parsed source file """

        nodes_by_name = {node.result_name: node for node in command_nodes}
        commands_by_name = {}

        def resolve_list(param_type, li, lineno):
            if isinstance(param_type, ListParameter):
                return [resolve_list(param_type.value_type, x.value, lineno) for x in li]
            elif isinstance(param_type, ResultParameter):
                return [resolve_result(x.value, lineno) for x in li]
            else:
                return li

        def resolve_result(result_name, lineno):
            result_command = commands_by_name.get(result_name)
            if result_command is not None:
                return result_command

            try:
                return resolve_command(nodes_by_name[result_name])
            except KeyError:
                raise ResultDoesNotExist(result_name, lineno)

        def resolve_command(node):
            if node.result_name in commands_by_name:
                return commands_by_name[node.result_name]

            command_cls = Command.find_by_name(node.command)

            if command_cls is None:
                raise CommandDoesNotExist(node.command, node.lineno)

            params = {arg.name: (arg.value.value, arg.lineno) for arg in node.arguments}
            missing_params = set(name for name in command_cls.required_inputs.keys()).difference(
                name for name in params.keys()
            )

            if missing_params:
                raise MissingParameters(command_cls, missing_params, node.lineno)

            arguments = []
            for name, (value, lineno) in params.items():
                if name not in command_cls.inputs.keys():
                    raise NoSuchParameter(command_cls, name, lineno)

                param_inst = command_cls.inputs[name]

                # Resolve references to other results
                if isinstance(param_inst, ResultParameter):
                    result_command = resolve_result(value, lineno)
                    value = result_command

                # Resolve lists
                elif isinstance(param_inst, ListParameter):
                    value = resolve_list(param_inst.value_type, value, lineno)

                arguments.append(Argument(name, param_inst.clean(value, self, lineno), lineno))

            command = command_cls(node.result_name, arguments, self, lineno)
            commands_by_name[node.result_name] = command
            return command

        self.commands = [resolve_command(node) for node in command_nodes]

    def run(self):
        # Build dependency lookup
        dependents = {}  # {result_name, [dependent_name, ...], ...}

        for command in self.commands:
            references = []
            for argument in command.arguments:
                if isinstance(argument.value, Command):
                    references.append(argument.value.result_name)
                if isinstance(argument.value, (list, tuple)):
                    references += [x for x in flatten(argument.value) if isinstance(x, Command)]

            for reference in references:
                dependents[reference] = dependents.get(reference, set())
                dependents[reference].add(command.result_name)

        # Find and run leaf nodes (commands without any dependents)
        for command in (command for command in self.commands if not dependents.get(command.result_name)):
            command.run()
