from __future__ import division

from functools import reduce

import numpy

from mpilot import params
from mpilot.commands import Command
from mpilot.libraries.eems.mixins import SameArrayShapeMixin


class Copy(Command):
    """ Copies the data from another field """

    display_name = "Copy"
    inputs = {"InFieldName": params.ResultParameter(params.DataParameter())}
    output = params.DataParameter()

    def execute(self, **kwargs):
        return numpy.copy(kwargs["InFieldName"].result)


class AMinusB(SameArrayShapeMixin, Command):
    """ Performs A - B """

    display_name = "A Minus B"
    inputs = {"A": params.DataParameter(), "B": params.DataParameter()}
    output = params.DataParameter()

    def execute(self, **kwargs):
        a = kwargs["A"].result
        b = kwargs["B"].result
        self.validate_array_shapes([a, b], lineno=self.lineno)

        return a - b


class Sum(SameArrayShapeMixin, Command):
    """ Sums input variables """

    display_name = "Sum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        result = numpy.copy(arrays[0])
        for arr in arrays[1:]:
            result += arr

        return result


class WeightedSum(SameArrayShapeMixin, Command):
    """ Takes the weighted sum of input variables """

    display_name = "Weighted Sum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        ),
        "Weights": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        weights = kwargs["Weights"]
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        result = arrays[0] * weights[0]
        for weight, arr in zip(weights[1:], arrays[1:]):
            result += arr * weight

        return result


class Multiply(SameArrayShapeMixin, Command):
    """ Multiplies input variables """

    display_name = "Multiply"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        result = numpy.copy(arrays[0])
        for arr in arrays[1:]:
            result *= arr

        return result


class ADividedByB(SameArrayShapeMixin, Command):
    """ Performs A / B """

    display_name = "A Divided By B"
    inputs = {
        "A": params.ResultParameter(params.DataParameter()),
        "B": params.ResultParameter(params.DataParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        a = kwargs["A"].result
        b = kwargs["B"].result
        self.validate_array_shapes([a, b], lineno=self.lineno)

        return a / b


class Minimum(SameArrayShapeMixin, Command):
    """ Takes the minimum input variables """

    display_name = "Minimum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        return reduce(lambda x, y: numpy.ma.minimum(x, y), arrays)


class Maximum(SameArrayShapeMixin, Command):
    """ Takes the maximum input variables """

    display_name = "Maximum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        return reduce(lambda x, y: numpy.ma.maximum(x, y), arrays)


class Mean(SameArrayShapeMixin, Command):
    """ Mean of input variables """

    display_name = "Mean"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        return sum(arrays) / len(arrays)


class WeightedMean(SameArrayShapeMixin, Command):
    """ Takes the weighted mean of input variables """

    display_name = "Weighted Mean"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        ),
        "Weights": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        weights = kwargs["Weights"]
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        result = arrays[0] * weights[0]
        for weight, arr in zip(weights[1:], arrays[1:]):
            result += arr * weight

        return result / sum(weights)


class Normalize(Command):
    """ Normalizes the data from another field to range (default 0:1) """

    display_name = "Normalize"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "StartVal": params.NumberParameter(required=False),
        "EndVal": params.NumberParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        start = kwargs.get("StartVal", 0)
        end = kwargs.get("EndVal", 1)

        arr_min = arr.min()
        arr_max = arr.max()

        return (arr - arr_min) * (start - end) / (arr_min - arr_max) + start


class PrintVars(Command):
    """ Prints each variable in a list of variable names. """

    display_name = "Print variable(s) to screen or file"
    inputs = {
        "InFieldNames": params.ListParameter(params.ResultParameter()),
        "OutFileName": params.PathParameter(required=False),
    }
    output = params.BooleanParameter()

    def execute(self, **kwargs):
        commands = kwargs["InFieldNames"]
        out_path = kwargs.get("OutFileName")

        if out_path:
            with open(out_path, "w") as f_out:
                f_out.write(
                    "\n".join(
                        "{}: {}".format(c.result_name, c.result) for c in commands
                    )
                )
        else:
            for command in kwargs["InFieldNames"]:
                print("{}: {}".format(command.result_name, command.result))

        return True
