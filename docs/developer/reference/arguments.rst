:mod:`mpilot.arguments`
=======================

.. automodule:: mpilot.arguments

  .. autoclass:: Argument

    .. py:attribute:: name
      :type: str

      The name of the argument, e.g., ``InFieldName``.

    .. py:attribute:: value
      :type: Any

      The argument value itself. This could be any valid parameter type.

    .. py:attribute:: lineno
      :type: int

      The line that the argument appears on in the source file.

  .. autoclass:: ListArgument

    .. py:attribute:: list_linenos
      :type: List[int]

      The line that each list item appear on in the source file. For example, if the source argument looks like this:

      .. code-block:: none
        :linenos:
        :lineno-start: 2

        InFieldNames=[
          Var_A,
          Var_B,
          Var_C
        ]

      The ``list_linenos`` might be:

      .. code-block:: python

        [3, 4, 5]

