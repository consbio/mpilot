import os
from numbers import Number

import six

from mpilot.commands import Command
from mpilot.exceptions import ParameterNotValid, PathDoesNotExist, ResultDoesNotExist, ResultTypeNotValid


class Parameter:
    def __init__(self, required=True):
        self.required = required

    def clean(self, value, program=None, lineno=None):
        """ Clean and validate a raw parameter value """

        return value


class StringParameter(Parameter):
    def __init__(self, **kwargs):
        super(StringParameter, self).__init__(**kwargs)

    def clean(self, value, program=None, lineno=None):
        return six.text_type(value)

    @staticmethod
    def accepts(parameter_cls):
        return issubclass(parameter_cls, (StringParameter, NumberParameter, PathParameter))


class NumberParameter(Parameter):
    def clean(self, value, program=None, lineno=None):
        if isinstance(value, Number):
            return value

        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                raise ParameterNotValid(value, "Number", lineno)

    @staticmethod
    def accepts(parameter_cls):
        return issubclass(parameter_cls, NumberParameter)


class BooleanParameter(Parameter):
    def clean(self, value, program=None, lineno=None):
        if isinstance(value, bool):
            return value

        if isinstance(value, int):
            return bool(value)

        if isinstance(value, six.string_types):
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False

            try:
                return bool(int(value))
            except ValueError:
                pass

        raise ParameterNotValid(value, "Boolean", lineno)


class PathParameter(StringParameter):
    def __init__(self, must_exist=True, **kwargs):
        super(PathParameter, self).__init__(**kwargs)
        self.must_exist = must_exist

    def clean(self, value, program=None, lineno=None):
        super().clean(value, program, lineno)

        if not os.path.isabs(value):
            value = os.path.join(program.working_dir, value)

        if self.must_exist and not os.path.exists(value):
            raise PathDoesNotExist(value, lineno)

        return value


class ResultParameter(Parameter):
    def __init__(self, output_type=None, **kwargs):
        super(ResultParameter, self).__init__(**kwargs)
        self.output_type = output_type

    def clean(self, value, program=None, lineno=None):
        if isinstance(value, Command):
            result = value.result

            if self.output_type is not None:
                return self.output_type.clean(result, program, lineno)
            return result

        if not isinstance(value, six.string_types):
            raise ParameterNotValid(value, "Result", lineno)

        if isinstance(value, bytes):
            value = value.decode()

        try:
            command = program.commands[value][0]
        except KeyError:
            raise ResultDoesNotExist(value, lineno)

        if command.output is None:
            raise ResultTypeNotValid(value, lineno)

        if self.output_type is None:
            return value

        if hasattr(self.output_type, "accepts"):
            is_valid = self.output_type.accepts(command.output.__class__)
        else:
            is_valid = issubclass(command.output.__class__, self.__class__)

        if not is_valid:
            raise ResultTypeNotValid(value, lineno)

        return value


class ListParameter(Parameter):
    def __init__(self, value_type=Parameter(), **kwargs):
        super(ListParameter, self).__init__(**kwargs)

        self.value_type = value_type

    def clean(self, value, program=None, lineno=None):
        if not isinstance(value, (list, tuple)):
            raise ParameterNotValid(value, "List", lineno)

        return [self.value_type.clean(item, program, lineno) for item in value]
