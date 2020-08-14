from __future__ import absolute_import

import os

from .commands import Command
from .exceptions import CommandDoesNotExist, DuplicateResult
from .parser.parser import Parser


class Program(object):
    """ A program consists of connected MPilot commands, and the arguments that will be used to run them """

    def __init__(self, working_dir=None):
        # Commands lookup, in the form of {result: (command, arguments_list), ...}
        self.commands = {}

        # A mapping of commands to their dependents, in the form of {result: dependents_list, ...}
        self.dependents = {}

        self.working_dir = working_dir

    @classmethod
    def from_source(cls, source, working_dir=None):
        """ Creates a program from MPilot source code """

        program = cls(working_dir)
        commands = Parser().parse(source)

        results = {c.result for c in commands}

        for command_node in commands:
            command = Command.find_by_name(command_node.command)

            if command is None:
                raise CommandDoesNotExist(command_node.command, command_node.lineno)

            arguments = None  # Todo: validate arguments

            program.add_command(command_node.result, command, arguments, command_node.lineno)

    @classmethod
    def from_file(cls, path):
        """ Creates a program from an MPilot command file """

        with open(path) as f:
            return cls.from_source(f.read(), working_dir=os.path.dirname(path))

    def add_command(self, result, command, arguments, lineno=None):
        """
        Adds a command to the program. Result names must be unique. A duplicate result name will raise a
        `DuplicateReulst` exception.

        :param result: The command result name
        :param command: A command class
        :param arguments: A dictionary of arguments to be passed to the command when it's executed
        :param lineno: An optional line number representing the line this command appears in the original source
        """

        if result in self.commands:
            raise DuplicateResult(result, lineno)

        self.commands[result] = (command, arguments)

    def remove_command(self, result):
        pass  # Todo

    def execute(self):
        """ Runs the program. """
