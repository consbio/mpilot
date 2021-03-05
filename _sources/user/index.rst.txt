User Guide
==========

This documentation covers installing MPilot, the process of creating and running MPilot models, and the process of
using the ``mpilot`` command-line program. It also includes a reference of all built-in MPilot commands, including the
EEMS commands, used to created fuzzy logic models.

Installing MPilot
-----------------

MPilot requires the `Python <https://www.python.org/>`_ programming language. You will also need a program called
``Pip``, which comes installed with all newer versions of Python. If you have an old version of Python, you may need to
`install Pip <https://pip.pypa.io/en/stable/installing/>`_ separately.

Once you have Python and Pip, you can install MPilot by running the following command::

  pip install mpilot

If you plan to use NetCDF data in your MPilot models, you should install the NetCDF extra::

  pip install mpilot[netcdf]

.. note::

  Installing MPilot with NetCDF will require the NetCDF C library to already be installed on your computer. Installing
  the NetCDF C library is out of the scope of this document, but you can find more information about doing this in the
  `NetCDF documentation`_.

A Quick Example
---------------

This example will help you understand the basics of creating and MPilot command file and running it using the `mpilot`
command. In this example, we'll read two variables from a CSV file, apply a **Fuzzy Union**, and write the result to a
new CSV file. First, create a CSV file called ``input.csv`` with two columns, ``A`` and ``B``::

  A,B
  10,5
  8,2
  7,3
  5,10
  2,8

When this data is loaded by MPilot, each column will be treated as a list of number. In other words::

  A = [10, 8, 7, 5, 1]
  B = [5, 2, 3, 10, 8]

Now, create the command file, called ``model.mpt``::

  # Read A
  A = EEMSRead(
    InFileName = "input.csv",
    InFieldName = "A",
    DataType = "Integer"
  )

  # Read B
  B = EEMSRead(
    InFileName = "input.csv",
    InFieldName = "B",
    DataType = "Integer"
  )

  # Convert A and B to fuzzy
  A_Fz = CvtToFuzzy(
    InFieldName = A,
    TrueThreshold = 10,
    FalseThreshold = 2
  )
  B_Fz = CvtToFuzzy(
    InFieldName = B,
    TrueThreshold = 10,
    FalseThreshold = 2
  )

  # Combine A and B with fuzzy union
  Union = FuzzyUnion(
    InFieldNames = [A_Fz, B_Fz]
  )

  # Write A, B, and the union to a new CSV
  Out = EEMSWrite(
    OutFileName = "output.csv",
    OutFieldNames = [A, B, Union]
  )

This model loads ``A`` and ``B``, and converts each array to fuzzy space, i.e., normalized values to between ``-1``
to ``+1``. The ``TrueThreshold`` and ``FalseThreshold`` parameters determine how this conversion is done. In this case,
``10`` will become ``1`` and ``2`` will become ``-1``. Values between ``2`` and ``10`` will be interpolated to values
between ``-1`` and ``1``. The ``FuzzyUnion`` command produces the mean of the fuzzy values.

Now we can run this model with::

  mpilot eems-csv model.mpt

This should run quickly, and produce a new file, ``output.csv``, which will contain the two input columns, ``A`` and
``B``, as well as the result column, ``Union``.

The ``mpilot`` program
----------------------

``mpilot`` is the command-line program used to run models. It is run with the ``library`` to use, and the path to the
command file (model)::

  mpilot <library> <command file>

The ``library`` can be either ``eems-csv`` to use EEMS commands intended for use with CSV data, or ``eems-netcdf`` to
use EEMS commands intended for use with NetCDF data. Run ``mpilot --help`` for a full list of options.

Command File Syntax
-------------------

MPilot models are expressed using the `.mpt` command file syntax. These files are easy to write and to understand. They
consist of all the commands that make up the model.

Each command follows the same structure::

  <result> = <command name>(
    <parameters>
  )

Parameters are different for each command and may require a specific type of data (e.g., a number, or an output from a
previous command). Each parameter takes the form of ``<parameter> = <value>``, and multiple parameters are separated by
commas.

Parameter Types
---------------

These are the parameter types that may be used by MPilot commands.

.. _param-string:

String
^^^^^^

String parameters may be surrounded by quotes, or not. Strings not surrounded by quotes may not contain the following
characters: ``#:,=-+()[]``::

  # With quotes
  Param = "This is a string."

  # Without quotes
  Param = This is a string.

.. _param-number:

Number
^^^^^^

Numbers may be integer of decimal values::

  # Integer
  Param = 12

  # Decimal
  Param = 5.4

.. _param-boolean:

Boolean
^^^^^^^

A boolean parameter may be ``true`` or ``false``::

  Param = true
  Param = false

.. _param-path:

Path
^^^^

A path parameter is the same as a string, but must refer to a valid path. For some commands, the path must already exist
(e.g., a read command) while for others it will be created (e.g., a write command)::

  Param = "C:\path\to\file.csv"

.. _param-result:

Result
^^^^^^

A result parameter refers to the output of another command::

  A = CommandA()
  Out = Write(ResultParam = A)

.. _param-list:

List
^^^^

A list parameter contains any number of values of a specific type. For example, a list of strings, a list of numbers,
or a list of results::

  Param = [1, 2, 3, 4]

.. _param-tuple:

Tuple
^^^^^

A tuple parameter is similar to a list, but consists of any number of key/value pairs. Both the key and value are
strings, and are separated by a colon ``:``::

  Param = [Color:"Blue"]

.. _param-data-type:

Data Type
^^^^^^^^^

One of several possible data types, such as "Float" or "Integer", determined by the command::

  Param = Float


Built-In Command Libraries
--------------------------

MPilot includes built-in commands, currently limited to those used for creating EEMS models. A full reference of
built-in commands is at :doc:`libraries-ref`.

.. toctree::
   :hidden:
   :includehidden:

   libraries-ref

.. _NetCDF documentation: https://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html
