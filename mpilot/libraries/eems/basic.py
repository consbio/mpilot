from __future__ import division

import copy
from functools import reduce

import numpy

from mpilot import params
from mpilot.commands import Command
from mpilot.libraries.eems.exceptions import (
    MismatchedWeights,
    MixedArrayLengths,
    DuplicateRawValues,
)
from mpilot.libraries.eems.mixins import SameArrayShapeMixin
from mpilot.utils import insure_fuzzy


class Copy(Command):
    """Copies the data from another field"""

    display_name = "Copy"
    inputs = {"InFieldName": params.ResultParameter(params.DataParameter())}
    output = params.DataParameter()

    def execute(self, **kwargs):
        return numpy.copy(kwargs["InFieldName"].result)


class AMinusB(SameArrayShapeMixin, Command):
    """Performs A - B"""

    display_name = "A Minus B"
    inputs = {
        "A": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "B": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        a = kwargs["A"].result
        b = kwargs["B"].result
        self.validate_array_shapes([a, b], lineno=self.lineno)

        return a - b


class Sum(SameArrayShapeMixin, Command):
    """Sums input variables"""

    display_name = "Sum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=False)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        result = numpy.copy(arrays[0], subok=True)
        for arr in arrays[1:]:
            result += arr

        return result


class WeightedSum(SameArrayShapeMixin, Command):
    """Takes the weighted sum of input variables"""

    display_name = "Weighted Sum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=False)
        ),
        "Weights": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        weights = kwargs["Weights"]
        arrays = [c.result for c in kwargs["InFieldNames"]]

        if len(weights) != len(arrays):
            raise MismatchedWeights(len(weights), len(arrays))

        self.validate_array_shapes(arrays, lineno=self.lineno)

        result = arrays[0] * weights[0]
        for weight, arr in zip(weights[1:], arrays[1:]):
            result += arr * weight

        return result


class Multiply(SameArrayShapeMixin, Command):
    """Multiplies input variables"""

    display_name = "Multiply"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=False)
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
    """Performs A / B"""

    display_name = "A Divided By B"
    inputs = {
        "A": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "B": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        a = kwargs["A"].result
        b = kwargs["B"].result
        self.validate_array_shapes([a, b], lineno=self.lineno)

        return a / b


class Minimum(SameArrayShapeMixin, Command):
    """Takes the minimum input variables"""

    display_name = "Minimum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=False)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        return reduce(lambda x, y: numpy.ma.minimum(x, y), arrays)


class Maximum(SameArrayShapeMixin, Command):
    """Takes the maximum input variables"""

    display_name = "Maximum"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=False)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        return reduce(lambda x, y: numpy.ma.maximum(x, y), arrays)


class Mean(SameArrayShapeMixin, Command):
    """Mean of input variables"""

    display_name = "Mean"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=False)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(arrays, lineno=self.lineno)

        return sum(arrays) / len(arrays)


class WeightedMean(SameArrayShapeMixin, Command):
    """Takes the weighted mean of input variables"""

    display_name = "Weighted Mean"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=False)
        ),
        "Weights": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        weights = kwargs["Weights"]
        arrays = [c.result for c in kwargs["InFieldNames"]]

        if len(weights) != len(arrays):
            raise MismatchedWeights(len(weights), len(arrays))

        self.validate_array_shapes(arrays, lineno=self.lineno)

        result = arrays[0] * weights[0]
        for weight, arr in zip(weights[1:], arrays[1:]):
            result += arr * weight

        return result / sum(weights)


class Normalize(Command):
    """Normalizes the data from another field to range (default 0:1)"""

    display_name = "Normalize"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
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


class NormalizeZScore(Command):
    """Converts input values into normalized values using linear interpolation based on Z Score"""

    display_name = "Normalize by Z Score"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "TrueThresholdZScore": params.NumberParameter(required=False),
        "FalseThresholdZScore": params.NumberParameter(required=False),
        "StartVal": params.NumberParameter(required=False),
        "EndVal": params.NumberParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        true_threshold = float(kwargs.get("TrueThresholdZScore", 0))
        false_threshold = float(kwargs.get("FalseThresholdZScore", 1))
        start = kwargs.get("StartVal", 0)
        end = kwargs.get("EndVal", 1)

        raw_mean = numpy.ma.mean(arr)
        raw_std = numpy.ma.std(arr)

        x1 = raw_mean + raw_std * true_threshold
        x2 = raw_mean + raw_std * false_threshold
        y1 = end
        y2 = start

        result = arr.copy()
        result -= x1
        result *= y2 - y1
        result /= x2 - x1
        result += y1

        # despite the name, `insure_fuzzy` works to constrain values to any range
        return insure_fuzzy(result, start, end)


class NormalizeCat(Command):
    """Converts integer input values into narmalized values based on user specification"""

    display_name = "Normalize by Category"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "RawValues": params.ListParameter(params.NumberParameter()),
        "NormalValues": params.ListParameter(params.NumberParameter()),
        "DefaultNormalValue": params.NumberParameter(),
        "StartVal": params.NumberParameter(required=False),
        "EndVal": params.NumberParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        raw_values = kwargs["RawValues"]
        normal_values = kwargs["NormalValues"]
        default_normal_value = kwargs["DefaultNormalValue"]
        start = kwargs.get("StartVal", 0)
        end = kwargs.get("EndVal", 1)

        if len(raw_values) != len(normal_values):
            raise MixedArrayLengths(
                len(raw_values), len(normal_values), lineno=self.lineno
            )

        if len(raw_values) != len(set(raw_values)):
            raise DuplicateRawValues(lineno=self.argument_lines.get("RawValues"))

        result = numpy.ma.array(
            numpy.full(arr.shape, default_normal_value, dtype=float)
        )

        for raw, normal in zip(raw_values, normal_values):
            result[arr.data == raw] = normal

        # despite the name, `insure_fuzzy` works to constrain values to any range
        return insure_fuzzy(result, start, end)


class NormalizeCurve(Command):
    """Converts input values into normalized values based on user-defined curve"""

    display_name = "Normalize Curve"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "RawValues": params.ListParameter(params.NumberParameter()),
        "NormalValues": params.ListParameter(params.NumberParameter()),
        "StartVal": params.NumberParameter(required=False),
        "EndVal": params.NumberParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        raw_values = kwargs["RawValues"]
        normal_values = kwargs["NormalValues"]
        start = kwargs.get("StartVal", 0)
        end = kwargs.get("EndVal", 1)

        if len(raw_values) != len(normal_values):
            raise MixedArrayLengths(
                len(raw_values), len(normal_values), lineno=self.lineno
            )

        if len(raw_values) != len(set(raw_values)):
            raise DuplicateRawValues(lineno=self.argument_lines.get("RawValues"))

        result = numpy.ma.empty(arr.shape, dtype=float)
        value_pairs = sorted(zip(raw_values, normal_values))

        # For raw values less than the lowest raw value, set them to the corresponding normal value
        result[arr <= value_pairs[0][0]] = value_pairs[0][1]

        # Assign normal values for each of the line segments that approximate the curve
        for i, (raw, normal) in list(enumerate(value_pairs))[1:]:
            prev_raw = value_pairs[i - 1][0]
            prev_normal = value_pairs[i - 1][1]

            m = (normal - prev_normal) / (raw - prev_raw)
            b = prev_normal - m * prev_raw

            where_idx = numpy.where(
                numpy.logical_and(arr.data > prev_raw, arr.data <= raw)
            )

            result[where_idx] = arr.data[where_idx]
            result[where_idx] *= m
            result[where_idx] += b

        # For raw values greater than the highest raw value, set them to the corresponding normal value
        result[arr > value_pairs[-1][0]] = value_pairs[-1][1]
        result.mask = arr.mask.copy()

        # despite the name, `insure_fuzzy` works to constrain values to any range
        return insure_fuzzy(result, start, end)


class NormalizeMeanToMid(NormalizeCurve):
    """Uses "NormalizeCurve" to create a non-linear transformation that is a good match for the input data"""

    display_name = "Mean to Mid"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "IgnoreZeros": params.BooleanParameter(),
        "NormalValues": params.ListParameter(params.NumberParameter()),
        "StartVal": params.NumberParameter(required=False),
        "EndVal": params.NumberParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        ignore_zeros = kwargs["IgnoreZeros"]

        low_value = arr.min()
        high_value = arr.max()

        if ignore_zeros:
            arr = arr[arr != 0]

        mean_value = arr.mean()
        below_mean = arr[arr <= mean_value]
        above_mean = arr[arr > mean_value]

        high_mean = above_mean.compressed().mean()
        low_mean = below_mean.compressed().mean()

        raw_values = [low_value, low_mean, mean_value, high_mean, high_value]
        normal_values = kwargs["NormalValues"][:]

        if raw_values[-1] == raw_values[-2]:
            del raw_values[-2]
            del normal_values[-2]
        if raw_values[0] == raw_values[1]:
            del raw_values[1]
            del normal_values[1]

        kwargs = copy.copy(kwargs)
        kwargs["RawValues"] = raw_values
        kwargs["NormalValues"] = normal_values

        return super(NormalizeMeanToMid, self).execute(**kwargs)


class NormalizeCurveZScore(Command):
    """Converts input values into narmalized values based on user-defined curve"""

    display_name = "Normalize Curve by Z Score"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "ZScoreValues": params.ListParameter(params.NumberParameter()),
        "NormalValues": params.ListParameter(params.NumberParameter()),
        "StartVal": params.NumberParameter(required=False),
        "EndVal": params.NumberParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        z_score_values = kwargs["ZScoreValues"]
        normal_values = kwargs["NormalValues"]
        start = kwargs.get("StartVal", 0)
        end = kwargs.get("EndVal", 1)

        if len(z_score_values) != len(normal_values):
            raise MixedArrayLengths(
                len(z_score_values), len(normal_values), lineno=self.lineno
            )

        raw_mean = numpy.ma.mean(arr)
        raw_std = numpy.ma.std(arr)

        raw_values = [raw_mean + value * raw_std for value in z_score_values]

        result = numpy.ma.empty(arr.shape, dtype=float)
        value_pairs = sorted(zip(raw_values, normal_values))

        # For raw values less than the lowest raw value, set them to the corresponding normal value
        result[arr <= value_pairs[0][0]] = value_pairs[0][1]

        # Assign normal values for each of the line segments that approximate the curve
        for i, (raw, normal) in list(enumerate(value_pairs))[1:]:
            prev_raw = value_pairs[i - 1][0]
            prev_normal = value_pairs[i - 1][1]

            m = (normal - prev_normal) / (raw - prev_raw)
            b = prev_normal - m * prev_raw

            where_idx = numpy.where(
                numpy.logical_and(arr.data > prev_raw, arr.data <= raw)
            )
            result[where_idx] = arr.data[where_idx]
            result[where_idx] *= m
            result[where_idx] += b

        # For raw values greater than the highest raw value, set them to the corresponding normal value
        result[arr > value_pairs[-1][0]] = value_pairs[-1][1]
        result.mask = arr.mask.copy()

        return insure_fuzzy(result, start, end)


class PrintVars(Command):
    """Prints each variable in a list of variable names."""

    display_name = "Print variable(s) to screen or file"
    inputs = {
        "InFieldNames": params.ListParameter(params.ResultParameter()),
        "OutFileName": params.PathParameter(must_exist=False, required=False),
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
