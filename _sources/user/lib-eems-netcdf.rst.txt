EEMS NetCDF I/O
===============

The EEMS NetCDF I/O library contains ``EEMSRead`` and ``EEMSWrite`` used for reading variables from NetCDF datasets and
writing variables to NetCDF datasets respectively.

.. function:: EEMSRead(InFileName, InFieldName, MissingVal, DataType)

  The ``EEMSRead`` command reads a single variable from a NetCDF dataset. Multiple ``EEMSRead`` commands can read
  different variables from the same NetCDF dataset.

  :param InFileName: (:ref:`param-path`) The NetCDF dataset to read from.
  :param InFieldName: (:ref:`param-string`) The name of the NetCDF variable to read.
  :param MissingVal: (:ref:`param-number`) *Optional*. A mask value, which indicates missing data. Any occurrences of
    this value will be masked in the loaded array.
  :param DataType: (:ref:`param-data-type`) *Optional*. The type to convert incoming data to. Valid values are:
    ``Float``, ``Integer``, ``Positive Float``, ``Positive Integer``, ``Fuzzy``. The default is ``Float``.

.. function:: EEMSWrite(OutFileName, OutFieldNames, DimensionFileName, DimensionFieldName)

  The ``EEMSWrite`` command writes one or more variables to a NetCDF dataset. If the dataset already exists, it will be
  overwritten.

  :param OutFileName: (:ref:`param-path`) The NetCDF dataset to create.
  :param OutFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of results to write to the CSV.
  :param DimensionFileName: (:ref:`param-path`) An existing NetCDF data to use as a template for the new dataset.
  :param DimensionFieldName: (:ref:`param-string`) An existing variable in the ``DimensionFileName`` dataset to use as
    a template for the new variable(s).
