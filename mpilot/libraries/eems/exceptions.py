import six
from six import python_2_unicode_compatible

from mpilot.exceptions import ProgramError

if six.PY3:
    from typing import Tuple


@python_2_unicode_compatible
class EmptyDataFile(ProgramError):
    def __init__(self, path, lineno=None):
        # type: (str, int) -> None

        super(EmptyDataFile, self).__init__(lineno)

        self.path = path

    def __str__(self):
        return "\n".join(
            (
                "Problem: The input file is empty: {}".format(self.path),
                "Solution: Double check the path and the contents of the data file.",
            )
        )


@python_2_unicode_compatible
class InvalidDataFile(ProgramError):
    def __init__(self, problem, lineno=None):
        # type: (str, int) -> None

        super(InvalidDataFile, self).__init__(lineno)

        self.problem = problem

    def __str__(self):
        return "\n".join(
            ("Problem" + self.problem, "Solution: Double check the data file.")
        )


@python_2_unicode_compatible
class MixedArrayShapes(ProgramError):
    def __init__(self, shape_a, shape_b, lineno=None):
        # type: (Tuple[int, ...], Tuple[int, ...], int) -> None

        super(MixedArrayShapes, self).__init__(lineno)

        self.shape_a = shape_a
        self.shape_b = shape_b

    def __str__(self):
        return "\n".join(
            (
                "Problem: The shapes of at least two arrays do no match. The shapes are ({}, {}) and ({}, {}).".format(
                    *(self.shape_a + self.shape_b)
                ),
                "Solution: All arrays must have the same shape. Double check the shapes of your input data.",
            )
        )


@python_2_unicode_compatible
class InvalidDirection(ProgramError):
    def __init__(self, value, lineno=None):
        # type: (str, int) -> NOne

        super(InvalidDirection, self).__init__(lineno)

        self.value = value

    def __str__(self):
        return "\n".join(
            (
                "Problem: {} is an invalid direction value.".format(self.value),
                "Solution: Use a value of LowToHigh or HighToLow for direction.",
            )
        )


@python_2_unicode_compatible
class InvalidThresholds(ProgramError):
    def __str__(self):
        return "\n".join(
            (
                "Problem: True and False thresholds must not be equal.",
                "Solution: Make sure that the TrueThreshold and FalseThreshold parameters are distinct.",
            )
        )


@python_2_unicode_compatible
class MixedArrayLengths(ProgramError):
    def __init__(self, len_a, len_b, lineno=None):
        # type: (int, int, int) -> None

        super(MixedArrayLengths, self).__init__(lineno)

        self.len_a = len_a
        self.len_b = len_b

    def __str__(self):
        return "\n".join(
            (
                "Problem: Array lengths don't match: {} and {}".format(
                    self.len_a, self.len_b
                ),
                "Solution: Make sure that the array lengths are equal.",
            )
        )


@python_2_unicode_compatible
class DuplicateRawValues(ProgramError):
    def __str__(self):
        return "\n".join(
            (
                "Problem: Raw values are not unique.",
                "Solution: Double check that the raw values are unique.",
            )
        )


@python_2_unicode_compatible
class IsNotFuzzy(ProgramError):
    def __str__(self):
        return "\n".join(
            (
                "Problem: One or more inputs are not fuzzy.",
                "Solution: Make sure the inputs to this function are fuzzy.",
            )
        )


@python_2_unicode_compatible
class InvalidNumberToConsider(ProgramError):
    def __str__(self):
        return "\n".join(
            (
                "Problem: The number of InFieldNames must be greater than or equal to NumberToConsider.",
                "Solution: Double check that the number of inputs is at least as much as NumberToConsider.",
            )
        )


@python_2_unicode_compatible
class InvalidTruestOrFalsest(ProgramError):
    def __init__(self, value, lineno=None):
        # type: (str, int) -> None

        super(InvalidTruestOrFalsest, self).__init__(lineno)

        self.value = value

    def __str__(self):
        return "\n".join(
            (
                "Problem: The value '{}' is invalid.".format(self.value),
                "Solution: Make sure that the value is either Truest or Falsest.",
            )
        )
