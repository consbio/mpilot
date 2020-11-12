from mpilot.commands import Command


def create_command_with_result(result_name, result):
    command = Command(result_name)
    command.is_finished = True
    command._result = result

    return command
