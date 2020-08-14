from __future__ import unicode_literals

import six


class MPilotError(Exception):
    pass


class ProgramError(MPilotError):
    def __init__(self, lineno=None):
        self.lineno = lineno


class CommandDoesNotExist(ProgramError):
    def __init__(self, name, lineno=None):
        super(CommandDoesNotExist, self).__init__(lineno)

        self.name = name

    def __unicode__(self):
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

    def __unicode__(self):
        return "\n".join(
            (
                'Problem: The result name "{}" is duplicated in the command file.'.format(self.result),
                "Solution: Make sure that the result name for each command doesn't exist elsewhere in the model.",
            )
        )


class ParameterNotValid(ProgramError):
    def __init__(self, value, required_type, lineno=None):
        super(ParameterNotValid, self).__init__(lineno)

        self.value = value
        self.required_type = required_type

    def __unicode__(self):
        return "\n".join(
            (
                "Problem: A value of type {} was expected, but value {} of type {} was provided.".format(
                    self.required_type, six.text_type(self.value), six.text_type(type(self.value))
                ),
                "Solution: Make sure command parameters are correct.",
            )
        )


class PathDoesNotExist(ProgramError):
    def __init__(self, path, lineno=None):
        super(PathDoesNotExist, self).__init__(lineno)

        self.path = path

    def __unicode__(self):
        return "\n".join(
            (
                "Problem: The following path does not exist: {}".format(self.path),
                "Solution: Double check the path and create it if necessary.",
            )
        )


class ResultDoesNotExist(ProgramError):
    def __init__(self, result, lineno=None):
        super(ResultDoesNotExist, self).__init__(lineno)

        self.result = result

    def __unicode__(self):
        return "\n".join(
            (
                'Problem: The result "{}" does not exist.'.format(self.result),
                "Solution: Double check that the result has been defined elsewhere in the command file.",
            )
        )


class ResultTypeNotValid(ProgramError):
    def __init__(self, result, lineno=None):
        super(ResultTypeNotValid, self).__init__(lineno)

        self.result = result

    def __unicode__(self):
        return "\n".join(
            (
                'Problem: The value returned by "{}" does not match the required parameter type for this parameter.'.format(
                    self.result
                ),
                "Solution: Double check that the correct command result is being used for this parameter.",
            )
        )
