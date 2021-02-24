from __future__ import division

from functools import reduce

import numpy
import six

if six.PY3:
    from typing import Union, Sequence

from mpilot import params
from mpilot.commands import Command
from mpilot.libraries.eems.exceptions import (
    InvalidDirection,
    InvalidThresholds,
    MixedArrayLengths,
    DuplicateRawValues,
    IsNotFuzzy,
    InvalidNumberToConsider,
    InvalidTruestOrFalsest,
)
from mpilot.libraries.eems.mixins import SameArrayShapeMixin
from mpilot.utils import insure_fuzzy

FUZZY_MIN = -1
FUZZY_MAX = 1


class FuzzyCommand(Command):
    is_fuzzy = False

    def validate_fuzzy_inputs(self, values, lineno=None):
        # type: (Union[Sequence[Command], Command], int) -> None

        if not isinstance(values, (list, tuple)):
            values = [values]

        for cmd in values:
            if not isinstance(cmd, FuzzyCommand) or not cmd.is_fuzzy:
                raise IsNotFuzzy(lineno=lineno)


class CvtToFuzzy(FuzzyCommand):
    """ Converts input values into fuzzy values using linear interpolation """

    is_fuzzy = True

    display_name = "Convert to Fuzzy"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "TrueThreshold": params.NumberParameter(required=False),
        "FalseThreshold": params.NumberParameter(required=False),
        "Direction": params.StringParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        direction = kwargs.get("Direction")

        if direction and direction not in ("LowToHigh", "HighToLow"):
            raise InvalidDirection(
                direction, lineno=self.argument_lines.get("Direction")
            )

        false_threshold = kwargs.get(
            "FalseThreshold", arr.max() if direction == "HighToLow" else arr.min()
        )
        true_threshold = kwargs.get(
            "TrueThreshold", arr.min() if direction == "HighToLow" else arr.max()
        )

        if true_threshold == false_threshold:
            raise InvalidThresholds(self.lineno)

        x1 = float(true_threshold)
        x2 = float(false_threshold)
        y1 = FUZZY_MAX
        y2 = FUZZY_MIN

        result = arr - x1
        result *= y2 - y1
        result /= x2 - x1
        result += y1

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class CvtToFuzzyZScore(FuzzyCommand):
    """ Converts input values into fuzzy values using linear interpolation based on Z Score """

    is_fuzzy = True

    display_name = "Convert to Fuzzy by Z Score"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "TrueThresholdZScore": params.NumberParameter(),
        "FalseThresholdZScore": params.NumberParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        true_threshold = float(kwargs["TrueThresholdZScore"])
        false_threshold = float(kwargs["FalseThresholdZScore"])

        raw_mean = numpy.ma.mean(arr)
        raw_std = numpy.ma.std(arr)

        x1 = raw_mean + raw_std * true_threshold
        x2 = raw_mean + raw_std * false_threshold
        y1 = FUZZY_MAX
        y2 = FUZZY_MIN

        result = arr.copy()
        result -= x1
        result *= y2 - y1
        result /= x2 - x1
        result += y1

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class CvtToFuzzyCat(FuzzyCommand):
    """ Converts integer input values into fuzzy based on user specification """

    is_fuzzy = True

    display_name = "Convert to Fuzzy by Category"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "RawValues": params.ListParameter(params.NumberParameter()),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
        "DefaultFuzzyValue": params.NumberParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        raw_values = kwargs["RawValues"]
        fuzzy_values = kwargs["FuzzyValues"]
        default_fuzzy_value = kwargs["DefaultFuzzyValue"]

        if len(raw_values) != len(fuzzy_values):
            raise MixedArrayLengths(
                len(raw_values), len(fuzzy_values), lineno=self.lineno
            )

        if len(raw_values) != len(set(raw_values)):
            raise DuplicateRawValues(lineno=self.argument_lines.get("RawValues"))

        result = numpy.ma.array(numpy.full(arr.shape, default_fuzzy_value, dtype=float))

        for raw, fuzzy in zip(raw_values, fuzzy_values):
            result[arr.data == raw] = fuzzy

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class CvtToFuzzyCurve(FuzzyCommand):
    """ Converts input values into fuzzy based on user-defined curve """

    is_fuzzy = True

    display_name = "Convert to Fuzzy Curve"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "RawValues": params.ListParameter(params.NumberParameter()),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        raw_values = kwargs["RawValues"]
        fuzzy_values = kwargs["FuzzyValues"]

        if len(raw_values) != len(fuzzy_values):
            raise MixedArrayLengths(
                len(raw_values), len(fuzzy_values), lineno=self.lineno
            )

        if len(raw_values) != len(set(raw_values)):
            raise DuplicateRawValues(lineno=self.argument_lines.get("RawValues"))

        result = numpy.ma.empty(arr.shape, dtype=float)
        value_pairs = sorted(zip(raw_values, fuzzy_values))

        # For raw values less than the lowest raw value, set them to the corresponding fuzzy value
        result[arr <= value_pairs[0][0]] = value_pairs[0][1]

        # Assign fuzzy values for each of the line segments that approximate the curve
        for i, (raw, fuzzy) in list(enumerate(value_pairs))[1:]:
            prev_raw = value_pairs[i - 1][0]
            prev_fuzzy = value_pairs[i - 1][1]

            m = (fuzzy - prev_fuzzy) / (raw - prev_raw)
            b = prev_fuzzy - m * prev_raw

            where_idx = numpy.where(
                numpy.logical_and(arr.data > prev_raw, arr.data <= raw)
            )

            result[where_idx] = arr.data[where_idx]
            result[where_idx] *= m
            result[where_idx] += b

        # For raw values greater than the highest raw value, set them to the corresponding fuzzy value
        result[arr > value_pairs[-1][0]] = value_pairs[-1][1]
        result.mask = arr.mask.copy()

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class MeanToMid(CvtToFuzzyCurve):
    """ Uses "CvtToFuzzyCurve" to create a non-linear transformation that is a good match for the input data """

    is_fuzzy = True

    display_name = "Mean to Mid"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "IgnoreZeros": params.BooleanParameter(),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
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

        high_mean = above_mean.mean()
        low_mean = below_mean.mean()

        return super(MeanToMid, self).execute(
            InFieldName=kwargs["InFieldName"],
            RawValues=[low_value, low_mean, mean_value, high_mean, high_value],
            FuzzyValues=kwargs["FuzzyValues"],
        )


class CvtToFuzzyCurveZScore(FuzzyCommand):
    """ Converts input values into fuzzy based on user-defined curve """

    is_fuzzy = True

    display_name = "Convert to Fuzzy Curve by Z Score"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "ZScoreValues": params.ListParameter(params.NumberParameter()),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        z_score_values = kwargs["ZScoreValues"]
        fuzzy_values = kwargs["FuzzyValues"]

        if len(z_score_values) != len(fuzzy_values):
            raise MixedArrayLengths(
                len(z_score_values), len(fuzzy_values), lineno=self.lineno
            )

        raw_mean = numpy.ma.mean(arr)
        raw_std = numpy.ma.std(arr)

        raw_values = [raw_mean + value * raw_std for value in z_score_values]

        result = numpy.ma.empty(arr.shape, dtype=float)
        value_pairs = sorted(zip(raw_values, fuzzy_values))

        # For raw values less than the lowest raw value, set them to the corresponding fuzzy value
        result[arr <= value_pairs[0][0]] = value_pairs[0][1]

        # Assign fuzzy values for each of the line segments that approximate the curve
        for i, (raw, fuzzy) in list(enumerate(value_pairs))[1:]:
            prev_raw = value_pairs[i - 1][0]
            prev_fuzzy = value_pairs[i - 1][1]

            m = (fuzzy - prev_fuzzy) / (raw - prev_raw)
            b = prev_fuzzy - m * prev_raw

            where_idx = numpy.where(
                numpy.logical_and(arr.data > prev_raw, arr.data <= raw)
            )
            result[where_idx] = arr.data[where_idx]
            result[where_idx] *= m
            result[where_idx] += b

        # For raw values greater than the highest raw value, set them to the corresponding fuzzy value
        result[arr > value_pairs[-1][0]] = value_pairs[-1][1]
        result.mask = arr.mask.copy()

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class CvtToBinary(FuzzyCommand):
    """
    Converts input values into binary 0 or 1 based on threshold.
    Direction = LowToHigh for values below threshold to be false and above to be true.
    Direction = HighToLow for values below threshold to be true and above to be false.
    """

    is_fuzzy = True

    display_name = "Convert to Fuzzy Binary"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "Threshold": params.NumberParameter(),
        "Direction": params.StringParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result
        threshold = kwargs["Threshold"]
        direction = kwargs["Direction"]

        if direction not in ("LowToHigh", "HighToLow"):
            raise InvalidDirection(
                direction, lineno=self.argument_lines.get("Direction")
            )

        low_value = 0.0 if direction == "LowToHigh" else 1.0
        high_value = 1.0 if direction == "LowToHigh" else 0.0

        result = numpy.ma.where(arr < threshold, low_value, high_value)

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyUnion(SameArrayShapeMixin, FuzzyCommand):
    """ Takes the fuzzy Union (mean) of fuzzy input variables """

    is_fuzzy = True

    display_name = "Fuzzy Union"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]

        self.validate_fuzzy_inputs(
            kwargs["InFieldNames"], lineno=self.argument_lines.get("InFieldNames")
        )
        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = sum(arrays)
        result /= float(len(arrays))

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyWeightedUnion(SameArrayShapeMixin, FuzzyCommand):
    """ Takes the weighted fuzzy Union (mean) of fuzzy input variables """

    is_fuzzy = True

    display_name = "Fuzzy Weighted Union"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        ),
        "Weights": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        weights = kwargs["Weights"]

        self.validate_fuzzy_inputs(
            kwargs["InFieldNames"], lineno=self.argument_lines.get("InFieldNames")
        )
        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = arrays[0] * weights[0]
        for weight, arr in zip(weights[1:], arrays[1:]):
            result += arr * weight

        result /= sum(weights)

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzySelectedUnion(SameArrayShapeMixin, FuzzyCommand):
    """ Takes the fuzzy Union (mean) of N Truest or Falsest fuzzy input variables """

    is_fuzzy = True

    display_name = "Fuzzy Selected Union"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        ),
        "TruestOrFalsest": params.StringParameter(),
        "NumberToConsider": params.NumberParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        for cmd in kwargs["InFieldNames"]:
            if not isinstance(cmd, FuzzyCommand):
                raise IsNotFuzzy(lineno=self.argument_lines.get("InFieldNames"))

        arrays = [c.result for c in kwargs["InFieldNames"]]
        truest_or_falsest = kwargs["TruestOrFalsest"]
        number_to_consider = kwargs["NumberToConsider"]

        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )
        self.validate_fuzzy_inputs(
            kwargs["InFieldNames"], lineno=self.argument_lines.get("InFieldNames")
        )
        if len(arrays) < number_to_consider:
            raise InvalidNumberToConsider(
                lineno=self.argument_lines.get("NumberToConsider")
            )

        if truest_or_falsest not in ("Truest", "Falsest"):
            raise InvalidTruestOrFalsest(
                truest_or_falsest, lineno=self.argument_lines.get("TruestOrFalsest")
            )

        # Create a stacked array with layers from input arrays, sort, and use to calculate fuzzy xor. Since there is no
        # numpy.ma.stacked, the masks are handled separately from the data. Note: we are building the maximal mask from
        # all the inputs before broadcasting it to the size of the stacked array.

        mask = reduce(
            lambda x, y: numpy.logical_or(x, y),
            (arr.mask for arr in arrays[1:]),
            arrays[0].mask,
        )
        stacked_arr = numpy.ma.array(
            numpy.stack([arr.data for arr in arrays]),
            mask=numpy.broadcast_to(
                mask, [len(arrays)] + list(arrays[0].shape)
            ).copy(),  # The array is un-writable (`.sort` will fail) without `.copy()`
        )

        stacked_arr.sort(axis=0, kind="heapsort")

        if truest_or_falsest == "Truest":
            result = numpy.ma.mean(stacked_arr[-number_to_consider:], axis=0)
        else:
            result = numpy.ma.mean(stacked_arr[:number_to_consider], axis=0)

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyOr(SameArrayShapeMixin, FuzzyCommand):
    """ Takes the fuzzy Or (maximum) of fuzzy input variables """

    is_fuzzy = True

    display_name = "Fuzzy Or"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        self.validate_fuzzy_inputs(
            kwargs["InFieldNames"], lineno=self.argument_lines.get("InFieldNames")
        )
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = reduce(lambda x, y: numpy.ma.maximum(x, y), arrays[1:], arrays[0])

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyAnd(SameArrayShapeMixin, FuzzyCommand):
    """ Takes the fuzzy And (minimum) of fuzzy input variables """

    is_fuzzy = True

    display_name = "Fuzzy And"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        self.validate_fuzzy_inputs(
            kwargs["InFieldNames"], lineno=self.argument_lines.get("InFieldNames")
        )
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = reduce(lambda x, y: numpy.ma.minimum(x, y), arrays[1:], arrays[0])

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyXOr(SameArrayShapeMixin, FuzzyCommand):
    """ Computes Fuzzy XOr: Truest - (Truest - 2nd Truest) * (2nd Truest - full False)/(Truest - full False) """

    is_fuzzy = True

    display_name = "Fuzzy XOr"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        self.validate_fuzzy_inputs(
            kwargs["InFieldNames"], lineno=self.argument_lines.get("InFieldNames")
        )
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        # Create a stacked array with layers from input arrays, sort, and use to calculate fuzzy xor. Since there is no
        # numpy.ma.stacked, the masks are handled separately from the data. Note: we are building the maximal mask from
        # all the inputs before broadcasting it to the size of the stacked array.

        mask = reduce(
            lambda x, y: numpy.logical_or(x, y),
            (arr.mask for arr in arrays[1:]),
            arrays[0].mask,
        )
        stacked_arr = numpy.ma.array(
            numpy.stack([arr.data for arr in arrays]),
            mask=numpy.broadcast_to(mask, [len(arrays)] + list(arrays[0].shape)).copy(),
        )

        stacked_arr.sort(axis=0, kind="heapsort")

        result = numpy.ma.where(
            stacked_arr[-1] <= FUZZY_MIN,
            FUZZY_MIN,
            stacked_arr[-1]
            - (stacked_arr[-1] - stacked_arr[-2])
            * (stacked_arr[-2] - FUZZY_MIN)
            / (stacked_arr[-1] - FUZZY_MIN),
        )

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyNot(FuzzyCommand):
    """ Takes the fuzzy And (minimum) of fuzzy input variables """

    is_fuzzy = True

    display_name = "Fuzzy Not"
    inputs = {"InFieldName": params.ResultParameter(params.DataParameter())}
    output = params.DataParameter()

    def execute(self, **kwargs):
        self.validate_fuzzy_inputs(
            kwargs["InFieldName"], lineno=self.argument_lines.get("InFieldNames")
        )
        arr = kwargs["InFieldName"].result

        result = -arr

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class CvtFromFuzzy(FuzzyCommand):
    """ Converts input fuzzy values into non-fuzzy values using linear interpolation """

    is_fuzzy = False

    display_name = "Convert from Fuzzy"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter()),
        "TrueThreshold": params.NumberParameter(),
        "FalseThreshold": params.NumberParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        self.validate_fuzzy_inputs(
            kwargs["InFieldName"], lineno=self.argument_lines.get("InFieldName")
        )
        arr = kwargs["InFieldName"].result
        true_threshold = kwargs["TrueThreshold"]
        false_threshold = kwargs["FalseThreshold"]

        if true_threshold == false_threshold:
            raise InvalidThresholds(self.lineno)

        y1 = float(true_threshold)
        y2 = float(false_threshold)
        x1 = FUZZY_MAX
        x2 = FUZZY_MIN

        result = arr - x1
        result *= y2 - y1
        result /= x2 - x1
        result += y1

        return result
