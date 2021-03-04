EEMS CSV I/O
============

The EEMS CSV I/O library contains ``EEMSRead`` and ``EEMSWrite`` used for reading variables from CSV files and writing
variables to CSV files respectively.

.. function:: EEMSRead(InFileName, InFieldName, MissingVal, DataType)

  The ``EEMSRead`` command reads a single variable from a CSV file. Multiple ``EEMSRead`` commands can read different
  variables from the same CSV file.

  :param InFileName: (:ref:`param-path`) The CSV file to read from.
  :param InFieldName: (:ref:`param-string`) The name of the column to read from.
  :param MissingVal: (:ref:`param-number`) *Optional*. A mask value, which indicates missing data. Any occurrences of
    this value will be masked in the loaded array.
  :param DataType: (:ref:`param-data-type`) *Optional*. Either ``Float`` or ``Integer``, converts incoming data to this
    type. The default is ``Float``.

.. function:: EEMSWrite(OutFileName, OutFieldNames)

  The ``EEMSWrite`` command writes one or more variables to a CSV file. If the file already exists, it will be
  overwritten.

  :param OutFileName: (:ref:`param-path`) The CSV file to create.
  :param OutFieldNames: (:ref:`param-list` [:ref:`param-result`]) A list of results to write to the CSV.
