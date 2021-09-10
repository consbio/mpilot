from __future__ import division

import pytest
import six

from mpilot.libraries.eems.exceptions import MismatchedWeights

if six.PY3:
    from unittest.mock import mock_open, patch
else:
    from mock import mock_open, patch

import numpy

from mpilot.libraries.eems.basic import (
    Copy,
    AMinusB,
    Sum,
    WeightedSum,
    Multiply,
    ADividedByB,
    Minimum,
    Maximum,
    Mean,
    WeightedMean,
    Normalize,
    PrintVars,
    NormalizeZScore,
    NormalizeCat,
    NormalizeCurve,
    NormalizeMeanToMid,
    NormalizeCurveZScore,
)
from mpilot.parser.parser import ArgumentNode
from ..utils import create_command_with_result


def test_copy():
    arr = numpy.arange(10)
    command = create_command_with_result("Result", arr)

    result = Copy("CopyResult").execute(InFieldName=command)

    # Result should have the same values as the original but should not be the same object
    assert (result == arr).all()
    assert id(result) != id(arr)

    # Changing the copy shouldn't change the original
    result[0] = 10
    assert arr[0] == 0


def test_metadata():
    cmd = Copy("CopyResult", arguments=[ArgumentNode("Metadata", {"A": "a"}, 0)])

    assert cmd.metadata == {"A": "a"}


def test_a_minus_b():
    a = numpy.array([10, 10, 10])
    b = numpy.array([1, 2, 3])
    answer = numpy.array([9, 8, 7])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)

    result = AMinusB("MinusResult").execute(A=a_command, B=b_command)

    assert (result == answer).all()


def test_sum():
    a = numpy.array([1, 2, 3])
    b = numpy.array([4, 5, 6])
    c = numpy.array([9, 8, 7])
    answer = numpy.array([14, 15, 16])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    result = Sum("SumResult").execute(InFieldNames=[a_command, b_command, c_command])

    assert (result == answer).all()


def test_weighted_sum():
    a = numpy.array([1, 2, 3])
    b = numpy.array([4, 5, 6])
    c = numpy.array([9, 8, 7])
    weights = [0.1, 0.5, 0.4]
    answer = numpy.array([5.7, 5.9, 6.1])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    result = WeightedSum("SumResult").execute(
        InFieldNames=[a_command, b_command, c_command], Weights=weights
    )

    assert (result == answer).all()

    with pytest.raises(MismatchedWeights) as ex:
        WeightedSum("SumResult").execute(
            InFieldNames=[a_command, b_command, c_command], Weights=[0.1, 0.5]
        )
    assert ex.value.target_length == 3
    assert ex.value.length == 2

    with pytest.raises(MismatchedWeights) as ex:
        WeightedSum("SumResult").execute(
            InFieldNames=[a_command, b_command, c_command], Weights=[0.1, 0.5, 0.4, 0.1]
        )
    assert ex.value.target_length == 3
    assert ex.value.length == 4


def test_multiply():
    a = numpy.array([1, 2, 3])
    b = numpy.array([4, 5, 6])
    c = numpy.array([9, 8, 7])
    answer = numpy.array([36, 80, 126])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    result = Multiply("MultResult").execute(
        InFieldNames=[a_command, b_command, c_command]
    )

    assert (result == answer).all()


def test_a_divide_by_b():
    a = numpy.array([10, 5, 20])
    b = numpy.array([2, 1, 16])
    answer = numpy.array([5, 5, 1.25])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)

    result = ADividedByB("DivResult").execute(A=a_command, B=b_command)

    assert (result == answer).all()


def test_minimum():
    a = numpy.array([1, 5, 6])
    b = numpy.array([4, 2, 10])
    c = numpy.array([9, 8, 5])
    answer = numpy.array([1, 2, 5])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    result = Minimum("MinResult").execute(
        InFieldNames=[a_command, b_command, c_command]
    )

    assert (result == answer).all()


def test_maximum():
    a = numpy.array([1, 5, 6])
    b = numpy.array([4, 2, 10])
    c = numpy.array([9, 8, 5])
    answer = numpy.array([9, 8, 10])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    result = Maximum("MaxResult").execute(
        InFieldNames=[a_command, b_command, c_command]
    )

    assert (result == answer).all()


def test_mean():
    a = numpy.array([1, 2, 3])
    b = numpy.array([4, 5, 6])
    c = numpy.array([9, 8, 7])
    answer = numpy.array([14.0 / 3, 5, 16 / 3])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    result = Mean("MeanResult").execute(InFieldNames=[a_command, b_command, c_command])

    assert (result == answer).all()


def test_weighted_mean():
    a = numpy.array([1, 2, 3])
    b = numpy.array([4, 5, 6])
    c = numpy.array([9, 8, 7])
    weights = [0.7, 0.2, 0.1]
    answer = numpy.array(
        [
            1 * 0.7 + 4 * 0.2 + 9 * 0.1,
            2 * 0.7 + 5 * 0.2 + 8 * 0.1,
            3 * 0.7 + 6 * 0.2 + 7 * 0.1,
        ]
    )

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    result = WeightedMean("MeanResult").execute(
        InFieldNames=[a_command, b_command, c_command], Weights=weights
    )

    assert (result.round(2) == answer.round(2)).all()

    with pytest.raises(MismatchedWeights) as ex:
        WeightedMean("MeanResult").execute(
            InFieldNames=[a_command, b_command, c_command], Weights=[0.7, 0.2]
        )
    assert ex.value.target_length == 3
    assert ex.value.length == 2

    with pytest.raises(MismatchedWeights) as ex:
        WeightedMean("MeanResult").execute(
            InFieldNames=[a_command, b_command, c_command], Weights=[0.7, 0.2, 0.1, 0.7]
        )
    assert ex.value.target_length == 3
    assert ex.value.length == 4


def test_normalize():
    arr = numpy.array([1, 2, 3])
    answer = numpy.array([0, 0.5, 1])

    command = create_command_with_result("Result", arr)

    result = Normalize("NormResult").execute(InFieldName=command)

    assert (result == answer).all()


def test_normalize_z_score():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [-1.0, -1.0, -0.87, -0.52, -0.17, 0.17, 0.52, 0.87, 1.0, 1.0]
    )
    result = NormalizeZScore("NormalizeResult").execute(
        InFieldName=command,
        TrueThresholdZScore=1,
        FalseThresholdZScore=-1,
        StartVal=-1,
        EndVal=1,
    )

    assert (result.round(2) == answer).all()


def test_normalize_cat():
    arr = numpy.ma.array([1, 1, 5, 4, 4, 8, 8, 9], dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array([-1.0, -1.0, 0.1, 0, 0, 0.9, 0.9, 1.0], dtype=float)
    result = NormalizeCat("ConvertResult").execute(
        InFieldName=command,
        RawValues=[1, 4, 5, 8, 9],
        NormalValues=[-1.0, 0.0, 0.1, 0.9, 1.0],
        DefaultNormalValue=0,
        StartVal=-1,
        EndVal=1,
    )

    assert (result == answer).all()

    result = NormalizeCat("ConvertResult").execute(
        InFieldName=command,
        RawValues=[1, 4, 8, 9],
        NormalValues=[-1.0, 0.0, 0.9, 1.0],
        DefaultNormalValue=0.1,
        StartVal=-1,
        EndVal=1,
    )

    assert (result == answer).all()


def test_normalize_curve():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [-1.0, -1.0, -0.5, 0.0, 0.17, 0.33, 0.5, 0.67, 0.83, 1.0], dtype=float
    )
    result = NormalizeCurve("ConvertResult").execute(
        InFieldName=command,
        RawValues=[1.0, 3.0, 9.0],
        NormalValues=[-1.0, 0.0, 1.0],
        StartVal=-1,
        EndVal=1,
    )

    assert (result.round(2) == answer).all()


def test_normalize_mean_to_mid():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [-1.0, -0.6, -0.2, -0.12, -0.04, 0.08, 0.24, 0.4, 0.7, 1.0], dtype=float
    )
    result = NormalizeMeanToMid("ConvertResult").execute(
        InFieldName=command,
        IgnoreZeros=False,
        NormalValues=[-1.0, -0.2, 0.0, 0.4, 1.0],
        StartVal=-1,
        EndVal=1,
    )

    assert (result.round(2) == answer).all()


def test_normalize_mean_to_mid_with_uneven_distribution():
    """Tests that the NormalizeMeanToMid command works when the largest raw value is much larger than other values"""

    arr = numpy.ma.array([0, 25, 88, 999], dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array([-1.0, -0.47, -0.16, 1.0], dtype=float)
    result = NormalizeMeanToMid("ConvertResult").execute(
        InFieldName=command,
        IgnoreZeros=False,
        NormalValues=[-1.0, -0.2, 0.0, 0.4, 1.0],
        StartVal=-1,
        EndVal=1,
    )

    assert (result.round(2) == answer).all()


def test_normalize_curve_z_score():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=float
    )
    result = NormalizeCurveZScore("ConvertResult").execute(
        InFieldName=command,
        ZScoreValues=[-0.1, 0.0, 0.1],
        NormalValues=[1.0, 5.0, 9.0],
        StartVal=-1,
        EndVal=1,
    )

    assert (result == answer).all()


def test_print_vars():
    a = numpy.array([1, 2, 3])
    b = numpy.array([4, 5, 6])
    c = numpy.array([9, 8, 7])

    a_command = create_command_with_result("AResult", a)
    b_command = create_command_with_result("BResult", b)
    c_command = create_command_with_result("CResult", c)

    PrintVars("PrintResult").execute(InFieldNames=[a_command, b_command, c_command])

    mock = mock_open()
    with patch("mpilot.libraries.eems.basic.open", mock):
        PrintVars("PrintResult").execute(
            InFieldNames=[a_command, b_command, c_command], OutFileName="out.txt"
        )

    mock.assert_called_once_with("out.txt", "w")
    mock().write.assert_called_once_with(
        "\n".join(("AResult: [1 2 3]", "BResult: [4 5 6]", "CResult: [9 8 7]"))
    )
