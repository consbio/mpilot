from __future__ import division

import numpy

from mpilot.libraries.eems.fuzzy import (
    CvtToFuzzy,
    CvtToFuzzyZScore,
    CvtToFuzzyCat,
    CvtToFuzzyCurve,
    CvtToFuzzyCurveZScore,
    CvtToBinary,
    FuzzyUnion,
    FuzzyWeightedUnion,
    FuzzySelectedUnion,
    FuzzyOr,
    FuzzyAnd,
    FuzzyXOr,
    FuzzyNot,
    CvtFromFuzzy,
    MeanToMid,
)
from ..utils import create_command_with_result


def test_convert_to_fuzzy():
    arr = numpy.ma.arange(10)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [-1.00, -0.78, -0.56, -0.33, -0.11, 0.11, 0.33, 0.56, 0.78, 1.00]
    )
    result = CvtToFuzzy("ConvertResult").execute(InFieldName=command)

    assert (result.round(2) == answer).all()

    answer = numpy.ma.array([-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    result = CvtToFuzzy("ConvertResult").execute(
        InFieldName=command, TrueThreshold=2, FalseThreshold=0
    )

    assert (result == answer).all()


def test_convert_to_fuzzy_z_score():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [-1.0, -1.0, -0.87, -0.52, -0.17, 0.17, 0.52, 0.87, 1.0, 1.0]
    )
    result = CvtToFuzzyZScore("ConvertResult").execute(
        InFieldName=command, TrueThresholdZScore=1, FalseThresholdZScore=-1
    )

    assert (result.round(2) == answer).all()


def test_convert_to_fuzzy_cat():
    arr = numpy.ma.array([1, 1, 5, 4, 4, 8, 8, 9], dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array([-1.0, -1.0, 0.1, 0, 0, 0.9, 0.9, 1.0], dtype=float)
    result = CvtToFuzzyCat("ConvertResult").execute(
        InFieldName=command,
        RawValues=[1, 4, 5, 8, 9],
        FuzzyValues=[-1.0, 0.0, 0.1, 0.9, 1.0],
        DefaultFuzzyValue=0,
    )

    assert (result == answer).all()

    result = CvtToFuzzyCat("ConvertResult").execute(
        InFieldName=command,
        RawValues=[1, 4, 8, 9],
        FuzzyValues=[-1.0, 0.0, 0.9, 1.0],
        DefaultFuzzyValue=0.1,
    )

    assert (result == answer).all()


def test_convert_to_fuzzy_curve():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [-1.0, -1.0, -0.5, 0.0, 0.17, 0.33, 0.5, 0.67, 0.83, 1.0], dtype=float
    )
    result = CvtToFuzzyCurve("ConvertResult").execute(
        InFieldName=command, RawValues=[1.0, 3.0, 9.0], FuzzyValues=[-1.0, 0.0, 1.0]
    )

    assert (result.round(2) == answer).all()


def test_mean_to_mid():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [-1.0, -0.6, -0.2, -0.12, -0.04, 0.08, 0.24, 0.4, 0.7, 1.0], dtype=float
    )
    result = MeanToMid("ConvertResult").execute(
        InFieldName=command, IgnoreZeros=False, FuzzyValues=[-1.0, -0.2, 0.0, 0.4, 1.0]
    )

    assert (result.round(2) == answer).all()


def test_convert_to_fuzzy_z_score():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array(
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=float
    )
    result = CvtToFuzzyCurveZScore("ConvertResult").execute(
        InFieldName=command, ZScoreValues=[-0.1, 0.0, 0.1], FuzzyValues=[1.0, 5.0, 9.0]
    )

    assert (result == answer).all()


def test_convert_to_binary():
    arr = numpy.ma.arange(10, dtype=float)
    command = create_command_with_result("Result", arr)
    answer = numpy.ma.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    result = CvtToBinary("ConvertResult").execute(
        InFieldName=command, Threshold=5, Direction="LowToHigh"
    )

    assert (result == answer).all()

    answer = numpy.ma.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
    result = CvtToBinary("ConvertResult").execute(
        InFieldName=command, Threshold=5, Direction="HighToLow"
    )

    assert (result == answer).all()


def test_fuzzy_union():
    arr_1 = numpy.ma.array([-1, -0.5, 1, 0.5, 0.25])
    arr_2 = numpy.ma.array([1, 0.75, 0.5, 1, 0.5])
    command_1 = create_command_with_result("Result", arr_1, fuzzy=True)
    command_2 = create_command_with_result("Result", arr_2, fuzzy=True)
    answer = numpy.ma.array([0, 0.125, 0.75, 0.75, 0.375])
    result = FuzzyUnion("UnionResult").execute(InFieldNames=[command_1, command_2])

    assert (result == answer).all()


def test_fuzzy_weighted_union():
    arr_1 = numpy.ma.array([-1, -0.5, 1, 0.5, 0.25])
    arr_2 = numpy.ma.array([1, 0.75, 0.5, 1, 0.5])
    command_1 = create_command_with_result("Result", arr_1, fuzzy=True)
    command_2 = create_command_with_result("Result", arr_2, fuzzy=True)
    answer = numpy.ma.array([-0.33, -0.08, 0.83, 0.67, 0.33])
    result = FuzzyWeightedUnion("UnionResult").execute(
        InFieldNames=[command_1, command_2], Weights=[1, 0.5]
    )

    assert (result.round(2) == answer).all()


def test_fuzzy_selected_union():
    arr_1 = numpy.ma.array([-1, -0.5, 1, 0.5, 0.25])
    arr_2 = numpy.ma.array([1, 0.75, 0.5, 1, 0.5])
    command_1 = create_command_with_result("Result", arr_1, fuzzy=True)
    command_2 = create_command_with_result("Result", arr_2, fuzzy=True)
    answer = numpy.ma.array([1.0, 0.75, 1.0, 1.0, 0.5])
    result = FuzzySelectedUnion("UnionResult").execute(
        InFieldNames=[command_1, command_2],
        TruestOrFalsest="Truest",
        NumberToConsider=1,
    )

    assert (result == answer).all()

    answer = numpy.ma.array([-1.0, -0.5, 0.5, 0.5, 0.25])
    result = FuzzySelectedUnion("UnionResult").execute(
        InFieldNames=[command_1, command_2],
        TruestOrFalsest="Falsest",
        NumberToConsider=1,
    )

    assert (result == answer).all()

    answer = numpy.ma.array([0.0, 0.125, 0.75, 0.75, 0.375])
    result = FuzzySelectedUnion("UnionResult").execute(
        InFieldNames=[command_1, command_2],
        TruestOrFalsest="Truest",
        NumberToConsider=2,
    )

    assert (result == answer).all()


def test_fuzzy_or():
    arr_1 = numpy.ma.array([-1, -0.5, 1, 0.5, 0.25])
    arr_2 = numpy.ma.array([1, 0.75, 0.5, 1, 0.5])
    command_1 = create_command_with_result("Result", arr_1, fuzzy=True)
    command_2 = create_command_with_result("Result", arr_2, fuzzy=True)
    answer = numpy.ma.array([1, 0.75, 1, 1, 0.5])
    result = FuzzyOr("OrResult").execute(InFieldNames=[command_1, command_2])

    assert (result == answer).all()


def test_fuzzy_and():
    arr_1 = numpy.ma.array([-1, -0.5, 1, 0.5, 0.25])
    arr_2 = numpy.ma.array([1, 0.75, 0.5, 1, 0.5])
    command_1 = create_command_with_result("Result", arr_1, fuzzy=True)
    command_2 = create_command_with_result("Result", arr_2, fuzzy=True)
    answer = numpy.ma.array([-1, -0.5, 0.5, 0.5, 0.25])
    result = FuzzyAnd("AndResult").execute(InFieldNames=[command_1, command_2])

    assert (result == answer).all()


def test_fuzzy_xor():
    arr_1 = numpy.ma.array([-1, -0.5, 1, 0.5, 0.25])
    arr_2 = numpy.ma.array([1, 0.75, 0.5, 1, 0.5])
    command_1 = create_command_with_result("Result", arr_1, fuzzy=True)
    command_2 = create_command_with_result("Result", arr_2, fuzzy=True)
    answer = numpy.ma.array([1.0, 0.393, 0.625, 0.625, 0.292])
    result = FuzzyXOr("XOrResult").execute(InFieldNames=[command_1, command_2])

    assert (result.round(3) == answer).all()


def test_fuzzy_not():
    arr = numpy.ma.array([-1, -0.5, 1, 0.5, 0.25])
    command = create_command_with_result("Result", arr, fuzzy=True)
    answer = numpy.ma.array([1, 0.5, -1, -0.5, -0.25])
    result = FuzzyNot("NotResult").execute(InFieldName=command)

    assert (result == answer).all()


def test_convert_from_fuzzy():
    arr = numpy.ma.array(
        [-1.00, -0.78, -0.56, -0.33, -0.11, 0.11, 0.33, 0.56, 0.78, 1.00]
    )
    command = create_command_with_result("Result", arr, fuzzy=True)
    answer = numpy.ma.arange(10, dtype=float)
    result = CvtFromFuzzy("ConvertResult").execute(
        InFieldName=command, TrueThreshold=9.0, FalseThreshold=0.0
    )

    assert (result.round() == answer).all()
