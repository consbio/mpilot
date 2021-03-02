import numpy
import six
from numpy.ma import is_masked

if six.PY3:
    from typing import Sequence, Any

from mpilot.exceptions import ProgramError
from mpilot.parser.parser import CommandNode


EEMS_COMMANDS = {
    "READ": "EEMSRead",
    "CVTTOFUZZY": "CvtToFuzzy",
    "CVTTOFUZZYCURVE": "CvtToFuzzyCurve",
    "CVTTOFUZZYCAT": "CvtToFuzzyCat",
    "MEANTOMID": "MeanToMid",
    "COPYFIELD": "Copy",
    "NOT": "FuzzyNot",
    "OR": "FuzzyOr",
    "AND": "FuzzyAnd",
    "ORNEG": "FuzzyAnd",
    "XOR": "FuzzyXOr",
    "SUM": "Sum",
    "MULT": "Multiply",
    "DIVIDE": "ADividedByB",
    "MIN": "Minimum",
    "MAX": "Maximum",
    "MEAN": "Mean",
    "UNION": "FuzzyUnion",
    "DIF": "AMinusB",
    "SELECTEDUNION": "FuzzySelectedUnion",
    "WTDUNION": "FuzzyWeightedUnion",
    "WTDMEAN": "WeightedMean",
    "WTDSUM": "WeightedSum",
    "SCORERANGEBENEFIT": "ScoreRangeBenefit",
    "SCORERANGECOST": "ScoreRangeCost",
}


def flatten(li):
    # type: (Sequence[Any]) -> Sequence[Any]
    """ Flattens a list of lists of any depth to a 1D list and returns a generator """

    for item in li:
        if isinstance(item, (list, tuple)):
            for list_item in flatten(item):
                yield list_item
        else:
            yield item


def insure_fuzzy(arr, fuzzy_min, fuzzy_max):
    # type: (numpy.ma.masked_array, float, float) -> numpy.ma.masked_array
    """ Limits all array values in-place to fuzzy_min and fuzzy_max and returns the array """

    arr[arr > fuzzy_max] = fuzzy_max
    arr[arr < fuzzy_min] = fuzzy_min

    if is_masked(arr):
        arr.data[arr.mask] = arr.fill_value

    return arr


def convert_eems2_commands(command_nodes):
    # type: (Sequence[CommandNode]) -> Sequence[CommandNode]
    """ Converts command nodes returned by the parser to their MPilot equivalents """

    def find_argument(node, name):
        for argument in node.arguments:
            if argument.name == name:
                return argument.value.value

    converted = []

    for node in command_nodes:
        try:
            converted.append(
                CommandNode(
                    node.result_name
                    or find_argument(node, "NewFieldName")
                    or find_argument(node, "InFieldName"),
                    EEMS_COMMANDS.get(node.command, node.command),
                    [
                        arg
                        for arg in node.arguments
                        if arg.name not in ("NewFieldName", "OutFileName")
                    ],
                    node.lineno,
                )
            )
        except StopIteration:
            raise ProgramError(
                lineno=node.lineno,
                message="Cannot convert from EEMS 2.0: No InFieldName argument for command without a result name.",
            )

    return converted
