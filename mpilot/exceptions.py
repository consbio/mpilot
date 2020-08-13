class MPilotError(Exception):
    pass


class ProgramError(MPilotError):
    def __init__(self, lineno=None):
        self.lineno = lineno


class CommandDoesNotExist(ProgramError):
    def __init__(self, name, lineno=None):
        super(CommandDoesNotExist, self).__init__(lineno)

        self.name = name

    def __str__(self):
        return "\n".join(
            (
                'Problem: The command "{}" does not exist.'.format(self.name),
                "Solution: Make sure the command exists and is spelled correctly.",
            )
        )


class DuplicateResult(ProgramError):
    def __init__(self, result, lineno=None):
        super(DuplicateResult, self).__init__(lineno)

        self.result = result

    def __str__(self):
        return "\n".join(
            (
                'Problem: The result name "{}" is duplicated in the command file.'.format(self.result),
                "Solution: Make sure that the result name for each command doesn't exist elsewhere in the model.",
            )
        )
