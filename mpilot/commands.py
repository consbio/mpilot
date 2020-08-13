from __future__ import print_function
from __future__ import unicode_literals

import pkgutil
from importlib import import_module
from importlib.util import module_from_spec

import six
from six import add_metaclass

from mpilot.exceptions import MPilotError


class CommandMeta(type):
    """ Command metaclass, used to automatically register commands, which can then be loaded by name. """

    _commands_by_name = {}

    def __new__(cls, name, bases, attrs):
        new_class = super(CommandMeta, cls).__new__(cls, name, bases, attrs)

        # Use the `name` attribute if this class defines one. Otherwise, use the class name itself.
        command_name = attrs.get("name", name)
        if command_name in cls._commands_by_name:
            raise MPilotError(
                "A command named '{}' has been declared more than once. Command names must be unique.".format(
                    command_name
                )
            )

        new_class.name = command_name
        cls._commands_by_name[command_name] = new_class

        new_class._command_by_name = cls._commands_by_name

        return new_class


@add_metaclass(CommandMeta)
class Command(object):
    @classmethod
    def load_commands(cls, module):
        if isinstance(module, six.string_types):
            if isinstance(module, bytes):
                module = module.decode()

            module = import_module(module)

        if hasattr(module, "__path__"):
            for info, name, _ in pkgutil.iter_modules(module.__path__):
                spec = info.find_spec(name)
                new_module = module_from_spec(spec)
                spec.loader.exec_module(new_module)
                cls.load_commands(new_module)

    @classmethod
    def find_by_name(cls, name):
        """ Finds and returns a command matching `name` """

        return cls._command_by_name.get(name)
