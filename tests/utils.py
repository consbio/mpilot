from mpilot.commands import Command
from mpilot.libraries.eems.fuzzy import FuzzyCommand


class FuzzyTestCommand(FuzzyCommand):
    is_fuzzy = True


def create_command_with_result(result_name, result, fuzzy=False):
    command = (FuzzyTestCommand if fuzzy else Command)(result_name)
    command.is_finished = True
    command._result = result

    return command
