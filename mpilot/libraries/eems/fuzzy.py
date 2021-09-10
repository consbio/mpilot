from __future__ import division

import copy
from functools import reduce

import numpy
from packaging import version

from mpilot import params
from mpilot.commands import Command
from mpilot.libraries.eems.basic import (
    NormalizeZScore,
    NormalizeCat,
    NormalizeCurve,
    NormalizeMeanToMid,
    NormalizeCurveZScore,
)
from mpilot.libraries.eems.exceptions import (
    InvalidDirection,
    InvalidThresholds,
    MixedArrayLengths,
    DuplicateRawValues,
    InvalidNumberToConsider,
    InvalidTruestOrFalsest,
    MismatchedWeights,
)
from mpilot.libraries.eems.mixins import SameArrayShapeMixin
from mpilot.utils import insure_fuzzy, make_masked

FUZZY_MIN = -1
FUZZY_MAX = 1


class CvtToFuzzy(Command):
    """Converts input values into fuzzy values using linear interpolation"""

    is_fuzzy = True

    display_name = "Convert to Fuzzy"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
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


class CvtToFuzzyZScore(NormalizeZScore):
    """Converts input values into fuzzy values using linear interpolation based on Z Score"""

    is_fuzzy = True

    display_name = "Convert to Fuzzy by Z Score"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "TrueThresholdZScore": params.NumberParameter(required=False),
        "FalseThresholdZScore": params.NumberParameter(required=False),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        return insure_fuzzy(
            super(CvtToFuzzyZScore, self).execute(
                **{
                    "TrueThresholdZScore": FUZZY_MAX,
                    "FalseThresholdZScore": FUZZY_MIN,
                    **kwargs,
                },
                StartVal=FUZZY_MIN,
                EndVal=FUZZY_MAX,
            ),
            FUZZY_MIN,
            FUZZY_MAX,
        )


class CvtToFuzzyCat(NormalizeCat):
    """Converts integer input values into fuzzy based on user specification"""

    is_fuzzy = True

    display_name = "Convert to Fuzzy by Category"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "RawValues": params.ListParameter(params.NumberParameter()),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
        "DefaultFuzzyValue": params.NumberParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        kwargs = copy.copy(kwargs)
        kwargs["NormalValues"] = kwargs["FuzzyValues"]
        kwargs["DefaultNormalValue"] = kwargs["DefaultFuzzyValue"]
        del kwargs["FuzzyValues"]
        del kwargs["DefaultFuzzyValue"]

        return insure_fuzzy(
            super(CvtToFuzzyCat, self).execute(
                **kwargs, StartVal=FUZZY_MIN, EndVal=FUZZY_MAX
            ),
            FUZZY_MIN,
            FUZZY_MAX,
        )


class CvtToFuzzyCurve(NormalizeCurve):
    """Converts input values into fuzzy based on user-defined curve"""

    is_fuzzy = True

    display_name = "Convert to Fuzzy Curve"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "RawValues": params.ListParameter(params.NumberParameter()),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        kwargs = copy.copy(kwargs)
        kwargs["NormalValues"] = kwargs["FuzzyValues"]
        del kwargs["FuzzyValues"]

        return insure_fuzzy(
            super(CvtToFuzzyCurve, self).execute(
                **kwargs, StartVal=FUZZY_MIN, EndVal=FUZZY_MAX
            ),
            FUZZY_MIN,
            FUZZY_MAX,
        )


class CvtToFuzzyMeanToMid(NormalizeMeanToMid):
    """Uses "CvtToFuzzyCurve" to create a non-linear transformation that is a good match for the input data"""

    is_fuzzy = True

    display_name = "Mean to Mid"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "IgnoreZeros": params.BooleanParameter(),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        kwargs = copy.copy(kwargs)
        kwargs["NormalValues"] = kwargs["FuzzyValues"]
        del kwargs["FuzzyValues"]

        return insure_fuzzy(
            super(CvtToFuzzyMeanToMid, self).execute(
                **kwargs, StartVal=FUZZY_MIN, EndVal=FUZZY_MAX
            ),
            FUZZY_MIN,
            FUZZY_MAX,
        )


class CvtToFuzzyCurveZScore(NormalizeCurveZScore):
    """Converts input values into fuzzy based on user-defined curve"""

    is_fuzzy = True

    display_name = "Convert to Fuzzy Curve by Z Score"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
        "ZScoreValues": params.ListParameter(params.NumberParameter()),
        "FuzzyValues": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        kwargs = copy.copy(kwargs)
        kwargs["NormalValues"] = kwargs["FuzzyValues"]
        del kwargs["FuzzyValues"]

        return insure_fuzzy(
            super(CvtToFuzzyCurveZScore, self).execute(
                **kwargs, StartVal=FUZZY_MIN, EndVal=FUZZY_MAX
            ),
            FUZZY_MIN,
            FUZZY_MAX,
        )


class CvtToBinary(Command):
    """
    Converts input values into binary 0 or 1 based on threshold.
    Direction = LowToHigh for values below threshold to be false and above to be true.
    Direction = HighToLow for values below threshold to be true and above to be false.
    """

    is_fuzzy = True

    display_name = "Convert to Fuzzy Binary"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=False),
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


class FuzzyUnion(SameArrayShapeMixin, Command):
    """Takes the fuzzy Union (mean) of fuzzy input variables"""

    is_fuzzy = True

    display_name = "Fuzzy Union"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=True)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]

        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = sum(arrays)
        result /= float(len(arrays))

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyWeightedUnion(SameArrayShapeMixin, Command):
    """Takes the weighted fuzzy Union (mean) of fuzzy input variables"""

    is_fuzzy = True

    display_name = "Fuzzy Weighted Union"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=True)
        ),
        "Weights": params.ListParameter(params.NumberParameter()),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        weights = kwargs["Weights"]

        if len(arrays) != len(weights):
            raise MismatchedWeights(len(weights), len(arrays))

        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = arrays[0] * weights[0]
        for weight, arr in zip(weights[1:], arrays[1:]):
            result += arr * weight

        result /= sum(weights)

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzySelectedUnion(SameArrayShapeMixin, Command):
    """Takes the fuzzy Union (mean) of N Truest or Falsest fuzzy input variables"""

    is_fuzzy = True

    display_name = "Fuzzy Selected Union"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=True)
        ),
        "TruestOrFalsest": params.StringParameter(),
        "NumberToConsider": params.NumberParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [make_masked(c.result) for c in kwargs["InFieldNames"]]
        truest_or_falsest = kwargs["TruestOrFalsest"]
        number_to_consider = kwargs["NumberToConsider"]

        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
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

        if version.parse(numpy.__version__) >= version.parse("1.10"):
            stacked_mask = numpy.broadcast_to(
                mask, [len(arrays)] + list(arrays[0].shape)
            )
        else:
            it = numpy.nditer(
                mask,
                flags=["multi_index", "refs_ok", "zerosize_ok"],
                itershape=[len(arrays)] + list(arrays[0].shape),
                order="C",
            )
            stacked_mask = it.itviews[0]

        stacked_arr = numpy.ma.array(
            numpy.vstack([arr.data for arr in arrays]),
            mask=stacked_mask.copy(),  # The array is un-writable (`.sort` will fail) without `.copy()`
        )

        stacked_arr.sort(axis=0, kind="heapsort")

        if truest_or_falsest == "Truest":
            result = numpy.ma.mean(stacked_arr[-number_to_consider:], axis=0)
        else:
            result = numpy.ma.mean(stacked_arr[:number_to_consider], axis=0)

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyOr(SameArrayShapeMixin, Command):
    """Takes the fuzzy Or (maximum) of fuzzy input variables"""

    is_fuzzy = True

    display_name = "Fuzzy Or"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=True)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = reduce(lambda x, y: numpy.ma.maximum(x, y), arrays[1:], arrays[0])

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyAnd(SameArrayShapeMixin, Command):
    """Takes the fuzzy And (minimum) of fuzzy input variables"""

    is_fuzzy = True

    display_name = "Fuzzy And"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=True)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [c.result for c in kwargs["InFieldNames"]]
        self.validate_array_shapes(
            arrays, lineno=self.argument_lines.get("InFieldNames")
        )

        result = reduce(lambda x, y: numpy.ma.minimum(x, y), arrays[1:], arrays[0])

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class FuzzyXOr(SameArrayShapeMixin, Command):
    """Computes Fuzzy XOr: Truest - (Truest - 2nd Truest) * (2nd Truest - full False)/(Truest - full False)"""

    is_fuzzy = True

    display_name = "Fuzzy XOr"
    inputs = {
        "InFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter(), is_fuzzy=True)
        )
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arrays = [make_masked(c.result) for c in kwargs["InFieldNames"]]
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

        if version.parse(numpy.__version__) >= version.parse("1.10"):
            stacked_mask = numpy.broadcast_to(
                mask, [len(arrays)] + list(arrays[0].shape)
            )
        else:
            it = numpy.nditer(
                mask,
                flags=["multi_index", "refs_ok", "zerosize_ok"],
                itershape=[len(arrays)] + list(arrays[0].shape),
                order="C",
            )
            stacked_mask = it.itviews[0]

        stacked_arr = numpy.ma.array(
            numpy.vstack([arr.data for arr in arrays]),
            mask=stacked_mask.copy(),
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


class FuzzyNot(Command):
    """Reverses the sign of the input fuzzy values from positive to negative or negative to positive"""

    is_fuzzy = True

    display_name = "Fuzzy Not"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=True)
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        arr = kwargs["InFieldName"].result

        result = -arr

        return insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)


class CvtFromFuzzy(Command):
    """Converts input fuzzy values into non-fuzzy values using linear interpolation"""

    is_fuzzy = False

    display_name = "Convert from Fuzzy"
    inputs = {
        "InFieldName": params.ResultParameter(params.DataParameter(), is_fuzzy=True),
        "TrueThreshold": params.NumberParameter(),
        "FalseThreshold": params.NumberParameter(),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
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
