EEMS Basic
==========

The EEMS Basic library contains several commands for performing basic, non-fuzzy operations on data. These include
arithmetic commands (e.g., Sum, AMinusB), aggregation commands, and utility commands.

.. function:: Copy(InFieldName)

  Creates a copy of the input data.

  :param InFieldName: (:ref:`param-result`) The result to copy.

.. function:: AMinusB(A, B)

  Performs the operation ``A - B``.

  :param A: (:ref:`param-result`)
  :param B: (:ref:`param-result`)

.. function:: Sum(InFieldNames)

  Produces an array in which each value is the sum of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the results to sum.

.. function:: WeightedSum(InFieldNames, Weights)

  Produces an array in which each value is the sum of all input arrays at that index, weighted by the input weights.
  E.g., values ``8`` and ``10``, with weights of ``0.6`` and ``0.4`` respectively will produce a result of ``8.8``.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the results to sum.
  :param Weights: (:ref:`param-list` [:ref:`param-number`]) A list of weights; one for each input. The number of
    weights must match the number of results specified by ``InFieldNames``.

.. function:: Multiply(InFieldNames)

  Multiplies multiple results together.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the results to multiply.

.. function:: ADividedByB(A, B)

  Performs the operation ``A / B``.

  :param A: (:ref:`param-result`) The numerator.
  :param B: (:ref:`param-result`) The denominator.

.. function:: Minimum(InFieldNames)

  Produces an array in which each value is the minimum of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the results to derive minimum values from.

.. function:: Maximum(InFieldNames)

  Produces an array in which each value is the maximum of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the results to derive maximum values from.

.. function:: Mean(InFieldNames)

  Produces an array in which each value is the mean of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the results to derive mean values from.

.. function:: WeightedMean(InFieldNames, Weights)

  Produces an array in which each values is the mean of all inputs arrays at that index, weighted by the input weights.
  E.g., values ``8`` and ``10`` with weights of ``2`` and ``1`` respectively will produce a result of ``8.667``

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the results to derive mean values from.
  :param Weights: (:ref:`param-list` [:ref:`param-number`]) A list of weights; one for each input. The number of
    weights must match the number of results specified by ``InFieldNames``.

.. function:: Normalize(InFieldName, StartVal, EndVal)

  Normalize values to a specified range, where the minimum value will be mapped to ``StartVal``, the maximum value will
  be mapped to ``EndVal``, and values between will be processed by linear interpolation between ``StartVal`` and
  ``EndVal``.

  :param InFieldName: (:ref:`param-result`) The result to normalize.
  :param StartVal: (:ref:`param-number`) *Optional*. The lowest value of the normalized array. Defaults to ``0``.
  :param EndVal: (:ref:`param-number`) *Optional*. The highest value of the normalized array. Defaults to ``1``.

.. function:: NormalizeZScore(InFieldName, TrueThresholdZScore, FalseThresholdZScore, StartVal, EndVal)

    Converts input values into normalized values using linear interpolation based on Z Score.

    :param InFieldName: (:ref:`param-result`) The result to normalize
    :param TrueThresholdZScore: (:ref:`param-number`) *Optional*. The normalized "True" value. Defaults to ``1``.
    :param FalseThresholdZScore: (:ref:`param-number`) *Optional*. The normalized "False" value. Defaults to ``0``.
    :param StartVal: (:ref:`param-number`) *Optional*. The lowest value of the normalized array. Defaults to ``0``.
    :param EndVal: (:ref:`param-number`) *Optional*. The highest value of the normalized array. Defaults to ``1``.

.. function:: NormalizeCat(InFieldName, RawValues, NormalValues, DefaultNormalValue, StartVal, EndVal)

  Converts integer input values into normalized values based on user specification.

  :param InFieldName: (:ref:`param-result`) The result to convert to normalize.
  :param RawValues: (:ref:`param-list` [:ref:`param-number`]) A list of unique values from the input data.
  :param NormalValues: (:ref:`param-list` [:ref:`param-number`]) A list of normalized values that will be used to
    normalize values matching those in ``RawValues``. The ``RawValues`` and ``NormalValues`` lists must be the same
    size.
  :param DefaultNormalValue: (:ref:`param-number`) The default normal value used to convert any input value not
    specified in ``RawValues``.
  :param StartVal: (:ref:`param-number`) *Optional*. The lowest value of the normalized array. Defaults to ``0``.
  :param EndVal: (:ref:`param-number`) *Optional*. The highest value of the normalized array. Defaults to ``1``.

.. function:: NormalizeCurve(InFieldName, RawValues, NormalValues, StartVal, EndVal)

  Converts input values into normalized values based on user-defined curve

  :param InFieldName: (:ref:`param-result`) The result to normalize.
  :param RawValues: (:ref:`param-list` [:ref:`param-number`]) A list of unique values from the input data.
  :param NormalValues: (:ref:`param-list` [:ref:`param-number`]) A list of normalized values that will be used to map
    values matching those in ``RawValues`` to normalized ones. The ``RawValues`` and ``NormalValues`` lists must be the
    same size.
  :param StartVal: (:ref:`param-number`) *Optional*. The lowest value of the normalized array. Defaults to ``0``.
  :param EndVal: (:ref:`param-number`) *Optional*. The highest value of the normalized array. Defaults to ``1``.

.. function:: NormalizeMeanToMid(InFieldName, IgnoreZeros, NormalValues, StartVal, EndVal)

  Uses "NormalizeCurve" to create a non-linear transformation that is a good match for the input data.

  :param InFieldName: (:ref:`param-result`) The result to normalize.
  :param IgnoreZeros: (:ref:`param-boolean`) Ignore ``0`` values when determining the mean.
  :param NormalValues: (:ref:`param-list` [:ref:`param-number`]) A list of normalized values that will be used to map
    input values to normalized ones.
  :param StartVal: (:ref:`param-number`) *Optional*. The lowest value of the normalized array. Defaults to ``0``.
  :param EndVal: (:ref:`param-number`) *Optional*. The highest value of the normalized array. Defaults to ``1``.

.. function:: NormalizeCurveZScore(InFieldName, ZScoreValues, NormalValues, StartVal, EndVal)

  Converts input values into narmalized values based on user-defined curve

  :param InFieldName: (:ref:`param-result`) The result to normalize.
  :param ZScoreValues: (:ref:`param-list` [:ref:`param-number`]) A list of z scores that will be used to map input
    values to normalized ones.
  :param NormalValues: (:ref:`param-list` [:ref:`param-number`]) A list of normalized values that will be used to map
    values to normalized ones. The ``ZScoreValues`` and ``NormalValues`` lists must be the same size.

.. function:: PrintVars(InFieldNames, OutFileName)

  Print or write results for debugging purposes. If ``OutFileName`` is provided, the results will be written to that
  file, otherwise they will be printed to ``STDOUT``.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) The results to print.
  :param OutFileName: (:ref:`param-path`) *Optional*. The file to write results to. This file will be overwritten if it
    exists.
