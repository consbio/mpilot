Working with Models
===================

This guide addresses working programmatically with models. This includes loading models from source, creating new
models, modifying and running models, and writing models back to source. The examples in this guide will mostly focus
on the :py:class:`mpilot.program.Program` class, which is the Python representation of the MPilot model.

Loading a model from source
---------------------------

The :py:meth:`~mpilot.program.Program.from_source` class method will parse a string containing an MPilot model and
return a new :py:class:`~mpilot.program.Program` representing the model. For example, the following will open a model
file, read the contents, and call ``from_source``, then run the model:

.. code-block:: python

  from mpilot.program import Program

  with open('model.mpt') as f:
    p = Program.from_source(f.read())
  p.run()

``from_source`` takes two optional arguments. The first is ``libraries``, which determines which commands are
available to the model. This defaults to :py:const:`~mpilot.program.EEMS_CSV_LIBRARIES`, which contains all commands
necessary to run EEMS models based on CSV data. If instead, you want to run an EEMS model which depends on NetCDF data,
you could use :py:const:`~mpilot.program.EEMS_NETCDF_LIBRAIRES` instead:

.. code-block:: python

  p = Program.from_source(f.read(), libraries=EEMS_NETCDF_LIBRARIES)

You can also use additional, custom libraries; in addition to or instead of the defaults provided by
``EEMS_CSV_LIBRARIES`` and ``EEMS_NETCDF_LIBRARIES``. Libraries are referenced by their Python module path, and must be
importable. As an example, let's say you create some custom commands, which can be imported from the
``myproject.commands.custom`` module. You could use this in addition to built-in EEMS commands:

.. code-block:: python

  p = Program.from_source(
    f.read(),
    libraries=EEMS_CSV_LIBRARIES + ('myproject.commands.custom',)
  )

The second optional argument, ``working_dir``, defines the directly used to resolve any relative paths in the model.
This argument can be omitted or set to ``None``, but this will result in an exception if any relative paths are
encountered. The CLI program sets ``working_dir`` to the directory of the model. For example:

.. code-block:: python

  model_path = '/path/to/model.mpt'
  working_dir = os.path.dirname(model_path)

  with open(model_path) as f:
    p = Program.from_source(f.read(), working_dir=working_dir)

Creating a new model
--------------------

Creating a new, empty model is as simple as creating a new instance of :py:class:`mpilot.program.Program`.

.. code-block:: python

  from mpilot.program import Program

  p = Program()

The ``Program`` constructor takes the same arguments (``libraries`` and ``working_dir``) as
:py:meth:`~mpilot.program.Program.from_source`, as described in the previous section.

Modifying the model
-------------------

Whether you have loaded a model from source, or created a new, blank model, you can modify it by adding or removing
commands.

Adding commands
^^^^^^^^^^^^^^^

Add commands with :py:meth:`~mpilot.program.Program.add_command`. At a minimum, you'll need to provide a command class,
a name for the command result, and arguments to run the command.

You can import the command class directly, or find it by name using
:py:meth:`~mpilot.program.Program.find_command_class`.

.. code-block:: python

  # Import command class
  from mpilot.libraries.eems.csv.io import EEMSRead

  # Look up by name
  p = Program()
  EEMSRead = p.find_command_class('EEMSRead')

The command arguments are passed to ``add_command`` as a dictionary.

.. code-block:: python

  p.add_command(
    EEMSRead,
    'Var_A',
    {
      'InFileName': 'input.csv',
      'InFieldName': 'Var_A'
    }
 )

This is equivalent to the following, in an MPilot command file:

.. code-block:: none

  Var_A = EEMSRead(
    InFileName = "input.csv",
    InFieldName = "Var_A"
  )

Removing commands
^^^^^^^^^^^^^^^^^

Remove commands from the model by deleting them from the :py:attr:`~mpilot.program.Program.commands` property.
``commands`` is a dictionary, where the key is the result name.

.. code-block:: python

  del p.commands['Var_A']

This will remove a command assigned to the result ``Var_A`` (e.g., ``Var_A = EEMSRead( ... )``).

Running the model
-----------------

Once the model has been created or loaded from source, and modified as needed, run it with
:py:meth:`~mpilot.program.Program.run`. This will build a dependency tree and then execute each command in the model.

Creating an MPilot command file
--------------------------------

Models can be serialized back to the MPilot Command File format using the :py:meth:`~mpilot.program.Program.to_string`
and py:meth:`~mpilot.program.Program.to_file`.

.. code-block:: python

  p = Program()
  EEMSRead = p.find_command_class('EEMSRead')
  p.add_command(EEMSRead, 'Var_A', {'InFileName': 'input.csv', 'InFieldName': 'Var_A'})

  # Returns the model as a string
  s = p.to_string()

  # Var_A = EEMSRead(
  #   InFileName = "model.mpt",
  #   InFieldName = "Var_A"
  # )

  # Writes the model to file
  p.to_file('model.mpt')

  # A file object works, too.
  with open('model.mpt') as f:
    p.to_file(f)
