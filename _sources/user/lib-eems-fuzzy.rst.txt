EEMS Fuzzy
==========

The EEMS Fuzzy library consists of commands related to converting data to and from fuzzy space, and performing
operations in fuzzy space, such as ``FuzzyOr`` and ``FuzzyAnd``.

.. function:: CvtToFuzzy(InFieldName, TrueThreshold, FalseThreshold, Direction)

  Converts input values into fuzzy values using linear interpolation.

  :param InFieldName: (:ref:`param-result`) The result to convert to fuzzy space.
  :param TrueThreshold: (:ref:`param-number`) *Optional*. The "true" value in fuzzy space. The default is ``1``.
  :param FalseThreshold: (:ref:`param-number`) *Optional*. The "false" value in fuzzy space. The default is ``-1``.
  :param Direction: (:ref:`param-string`) *Optional*. If ``LowToHigh``, the minimum input value is mapped to
    ``FalseThreshold`` and the maximum input value mapped to ``TrueThreshold``. For ``HighToLow``, this is reversed
    with the minimum input value mapped to ``TrueThreshold`` and the maximum input value mapped to ``FalseThreshold``.
    The default is ``LowToHigh``.

.. function:: CvtToFuzzyZScore(InFieldName, TrueThreshold, FalseThreshold)

  Converts input values into fuzzy values using linear interpolation based on Z Score.

  :param InFieldName: (:ref:`param-result`) The result to convert to fuzzy space.
  :param TrueThreshold: (:ref:`param-number`) *Optional*. The "true" value in fuzzy space. The default is ``1``.
  :param FalseThreshold: (:ref:`param-number`) *Optional*. The "false" value in fuzzy space. The default is ``-1``.

.. function:: CvtToFuzzyCat(InFieldName, RawValues, FuzzyValues, DefaultFuzzyValue)

  Converts integer input values into fuzzy based on user specification.

  :param InFieldName: (:ref:`param-result`) The result to convert to fuzzy space.
  :param RawValues: (:ref:`param-list` [:ref:`param-number`]) A list of unique values from the input data.
  :param FuzzyValues: (:ref:`param-list` [:ref:`param-number`]) A list of fuzzy values that will be used to map values
    matching those in ``RawValues`` to fuzzy space. The ``RawValues`` and ``FuzzyValues`` lists must be the same size.
  :param DefaultFuzzyValue: (:ref:`param-number`) The default fuzzy value used to convert any input value not specified in
    ``RawValues``.

.. function:: CvtToFuzzyCurve(InFieldName, RawValues, FuzzyValues)

  Converts input values into fuzzy based on user-defined curve

  :param InFieldName: (:ref:`param-result`) The result to convert to fuzzy space.
  :param RawValues: (:ref:`param-list` [:ref:`param-number`]) A list of unique values from the input data.
  :param FuzzyValues: (:ref:`param-list` [:ref:`param-number`]) A list of fuzzy values that will be used to map values
    matching those in ``RawValues`` to fuzzy space. The ``RawValues`` and ``FuzzyValues`` lists must be the same size.

.. function:: CvtToFuzzyMeanToMid(InFieldName, IgnoreZeros, FuzzyValues)

  Uses "CvtToFuzzyCurve" to create a non-linear transformation that is a good match for the input data.

  :param InFieldName: (:ref:`param-result`) The result to convert to fuzzy space.
  :param IgnoreZeros: (:ref:`param-boolean`) Ignore ``0`` values when determining the mean.
  :param FuzzyValues: (:ref:`param-list` [:ref:`param-number`]) A list of fuzzy values that will be used to map input
    values to fuzzy space.

.. function:: CvtToFuzzyCurveZScore(InFieldName, ZScoreValues, FuzzyValues)

  Converts input values into fuzzy based on user-defined curve.

  :param InFieldName: (:ref:`param-result`) The result to convert to fuzzy space.
  :param ZScoreValues: (:ref:`param-list` [:ref:`param-number`]) A list of z scores that will be used to map input
    values to fuzzy space.
  :param FuzzyValues: (:ref:`param-list` [:ref:`param-number`]) A list of fuzzy values that will be used to map values
    to fuzzy space. The ``ZScoreValues`` and ``FuzzyValues`` lists must be the same size.

.. function:: CvtToBinary(InFieldName, Threshold, Direction)

  Converts input values into binary 0 or 1 based on threshold.

  :param InFieldName: (:ref:`param-result`) The result to convert to fuzzy space.
  :param Threshold: (:ref:`param-number`) This threshold value used to bisect the input values into 0 and 1.
  :param Direction: (:ref:`param-string`) If ``LowToHigh``, values less than ``Threshold`` will be converted to ``0``.
    If ``HighToLow``, values less than ``Threshold`` will be converted to ``1``.

.. function:: FuzzyUnion(InFieldNames)

  Produces an array in which each value is the fuzzy union (mean) of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the fuzzy results to union.

.. function:: FuzzyWeightedUnion(InFieldNames, Weights)

  Produces an array in which each value is the weighted fuzzy union (mean) weighted of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the fuzzy results to union.
  :param Weights: (:ref:`param-list` [:ref:`param-number`]) A list of weights; one for each input. The number of
    weights must match the number of results specified by ``InFieldNames``.

.. function:: FuzzySelectedUnion(InFieldNames, TruestOrFalsest, NumberToConsider)

  Produces an array in which each value is the the fuzzy union (mean) of N Truest or Falsest of each input at that
  index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the fuzzy results to union.
  :param TruestOrFalsest: (:ref:`param-string`) Either ``Truest`` or ``Falsest``.
  :param NumberToConsider: (:ref:`param-number`)

.. function:: FuzzyOr(InFieldNames)

  Produces an array in which each value is the fuzzy ``OR`` of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the fuzzy results to perform the ``OR``
    operation on.

.. function:: FuzzyAnd(InFieldNames)

  Produces an array in which each value is the fuzzy ``AND`` of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the fuzzy results to perform the ``AND``
    operation on.

.. function:: FuzzyXOr(InFieldNames)

  Produces an array in which each value is the fuzzy ``XOR`` of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the fuzzy results to perform the ``XOR``
    operation on.

.. function:: FuzzyNot(InFieldNames)

  Produces an array in which each value is the fuzzy ``NOT`` of all input arrays at that index.

  :param InFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of the fuzzy results to perform the ``NOT``
    operation on.

.. function:: CvtFromFuzzy(InFieldName, TrueThreshold, FalseThreshold)

  Converts input fuzzy values into non-fuzzy values using linear interpolation. This is essentially the reverse
  operation of :py:func:`CvtToFuzzy`.

  :param InFieldName: (:ref:`param-result`) The fuzzy result to convert to normal space.
  :param TrueThreshold: (:ref:`param-number`) The "true" value in normal space. ``1`` in fuzzy space will be mapped to
    this value.
  :param FalseThreshold: (:ref:`param-number`) The "false" value in normal space. ``-1`` in fuzzy space will be mapped
    to this value.
