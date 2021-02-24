import six
from six import python_2_unicode_compatible

if six.PY3:
    from typing import Union, Sequence, Set, Any


class MPilotError(Exception):
    pass


@python_2_unicode_compatible
class ProgramError(MPilotError):
    def __init__(self, lineno=None, message=None):
        # type: (int, str) -> None

        self.lineno = lineno,
        self.message = message

    def __str__(self):
        return self.message or "ProgramError"


@python_2_unicode_compatible
class CommandDoesNotExist(ProgramError):
    def __init__(self, name, lineno=None):
        # type: (str, int) -> None

        super(CommandDoesNotExist, self).__init__(lineno)

        self.name = name

    def __str__(self):
        return "\n".join(
            (
                'Problem: The command "{}" does not exist.'.format(self.name),
                "Solution: Make sure the command exists and is spelled correctly.",
            )
        )


@python_2_unicode_compatible
class DuplicateResult(ProgramError):
    def __init__(self, result, lineno=None):
        # type: (str, int) -> None

        super(DuplicateResult, self).__init__(lineno)

        self.result = result

    def __str__(self):
        return "\n".join(
            (
                'Problem: The result name "{}" is duplicated in the command file.'.format(self.result),
                "Solution: Make sure that the result name for each command doesn't exist elsewhere in the model.",
            )
        )


@python_2_unicode_compatible
class MissingParameters(ProgramError):
    def __init__(self, command, parameters, lineno=None):
        # type: (Union[str, Any], Union[Sequence[str], Set[str]], int) -> None

        super(MissingParameters, self).__init__(lineno)

        self.command = command if isinstance(command, six.string_types) else command.name
        self.parameters = parameters

    def __str__(self):
        return "\n".join(
            (
                'Problem: The command "{}" is missing the following required parameters: {}'.format(
                    self.command, ", ".join(self.parameters)
                ),
                "Solution: Make sure all required parameters are provided for this command.",
            )
        )


@python_2_unicode_compatible
class NoSuchParameter(ProgramError):
    def __init__(self, command, parameter, lineno=None):
        # type: (Union[str, Any], str, int) -> None

        super(NoSuchParameter, self).__init__(lineno)

        self.command = command if isinstance(command, six.string_types) else command.name
        self.parameter = parameter

    def __str__(self):
        return "\n".join(
            (
                'Problem: The command "{}" has no parameter named "{}".'.format(self.command, self.parameter),
                "Solution: Make sure the parameters are correct for this command.",
            )
        )


@python_2_unicode_compatible
class ParameterNotValid(ProgramError):
    def __init__(self, value, required_type, lineno=None):
        # type: (Any, str, int) -> None

        super(ParameterNotValid, self).__init__(lineno)

        self.value = value
        self.required_type = required_type

    def __str__(self):
        return "\n".join(
            (
                "Problem: A value of type {} was expected, but value {} of type {} was provided.".format(
                    self.required_type, six.text_type(self.value), six.text_type(type(self.value))
                ),
                "Solution: Make sure command parameters are correct.",
            )
        )


@python_2_unicode_compatible
class PathDoesNotExist(ProgramError):
    def __init__(self, path, lineno=None):
        # type: (str, int) -> None

        super(PathDoesNotExist, self).__init__(lineno)

        self.path = path

    def __str__(self):
        return "\n".join(
            (
                "Problem: The following path does not exist: {}".format(self.path),
                "Solution: Double check the path and create it if necessary.",
            )
        )


@python_2_unicode_compatible
class ResultDoesNotExist(ProgramError):
    def __init__(self, result, lineno=None):
        # type: (str, int) -> None

        super(ResultDoesNotExist, self).__init__(lineno)

        self.result = result

    def __str__(self):
        return "\n".join(
            (
                'Problem: The result "{}" does not exist.'.format(self.result),
                "Solution: Double check that the result has been defined elsewhere in the command file.",
            )
        )


@python_2_unicode_compatible
class ResultTypeNotValid(ProgramError):
    def __init__(self, result, lineno=None):
        # type: (str, int) -> None

        super(ResultTypeNotValid, self).__init__(lineno)

        self.result = result

    def __str__(self):
        return "\n".join(
            (
                'Problem: The value returned by "{}" does not match the required parameter type for this parameter.'.format(
                    self.result
                ),
                "Solution: Double check that the correct command result is being used for this parameter.",
            )
        )


@python_2_unicode_compatible
class RecursiveModelStructure(ProgramError):
    def __str__(self):
        return "\n".join(
            ("Problem: The model is recursive.", "Solution: Double check that command references don't create a loop")
        )
