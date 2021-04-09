from mpilot.commands import Command


def create_command_with_result(result_name, result, fuzzy=False):
    command = Command(result_name)
    if fuzzy:
        command.is_fuzzy = True

    command.is_finished = True
    command._result = result

    return command
