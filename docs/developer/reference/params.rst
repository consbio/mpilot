:mod:`mpilot.params`
====================

.. automodule:: mpilot.params

  .. autoclass:: Parameter

    :param bool required: If ``True``, this argument is required and will cause the model execution to fail if it's not
      present.

    .. automethod:: clean

  .. autoclass:: StringParameter
    :show-inheritance:

  .. autoclass:: NumberParameter
    :show-inheritance:

  .. autoclass:: BooleanParameter
    :show-inheritance:

  .. autoclass:: PathParameter
    :show-inheritance:

    :param bool must_exist: If ``True``, the path is required to already exist when the model is run.

  .. autoclass:: ResultParameter
    :show-inheritance:

    :param Parameter output_type: The output type of the result. For example:
    :param Optional[bool] is_fuzzy: If ``True``, the input is required be fuzzy, if ``False``, the input cannot be
      fuzzy. If ``None``, either fuzzy of non-fuzzy is accepted.

      .. code-block:: python

        ResultParameter(NumberParameter())

      ... denotes a result that is of a "Number" type. During validation, the ``output`` type of the result is checked
      against ``output_type``.

  .. autoclass:: ListParameter
    :show-inheritance:

    :param Parameter value_type: The list item type. All items in the list will be validated for this type. E.g., for
      a list of numbers:

      .. code-block:: python

        ListParameter(NumberParameter())

  .. autoclass:: TupleParameter
    :show-inheritance:

  .. autoclass:: DataParameter
    :show-inheritance:

  .. autoclass:: DataTypeParameter(valid_types={'Float': float, 'Integer': int}, **kwargs)
    :show-inheritance:

    :param Dict[str,Any] valid_types: A dictionary in which the keys are values that can be passed to this argument
      and the values are the type used to transform the data. For example, to accept either integer or floating point
      data types:

      .. code-block:: python

        DataTypeParameter(valid_types={"Integer": int, "Float": float})
