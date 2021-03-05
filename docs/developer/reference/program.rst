:mod:`mpilot.program`
=====================

.. automodule:: mpilot.program

  .. class:: Program(libraries: Sequence[str]=EEMS_CSV_LIBRARIES, working_dir: str=None)

    The ``Program`` class contains the command instances that comprise the model, and is responsible for running the
    model by building a dependency tree and running any "leaf" nodes (those which no other nodes depend on). Before the
    leaf nodes are run, they resolve their dependencies, which in turn resolve *their* dependencies, and so on in a
    recursive nature until the root nodes are run.

    :param Sequence[str] libraries: A list of command libraries to use in this program. The specified libraries will be
      used to look up commands. Command names must be unique across libraries; importing two libraries that have the
      same command names will raise an exception.
    :param str working_dir: The working directory is used to resolve relative paths used in the model. If ``None``,
      relative paths are invalid and will raise an exception. Defaults to ``None``.

    .. py:attribute:: commands
      :type: Dict[str, Command]

      A lookup of commands in the program by result name, in the form of ``{result_name: command, ...}``.

    .. py:attribute:: command_library
      :type: Dict[str, Type[Command]]

      A lookup of command classes by name.

    .. py:attribute:: working_dir
      :type: str

      The program's working directory, if set.

    .. automethod:: load_commands

    .. automethod:: from_source(libraries: Sequence[str]=EEMS_CSV_LIBRARIES, working_dir: str=None)

    .. automethod:: find_command_class

    .. py:method:: add_command(command_cls: Type[Command], result_name: str, arguments: Dict[str, Any], lineno: int=None) -> None

      Adds a command to the program and the arguments required to run it. This is the primary method used when
      constructing a model programmatically. The command class can be obtained by importing it from the appropriate
      module, or by using :py:meth:`find_command_class` to search for a command by name.

      .. code-block:: python

        p = Program()
        read_cls = p.find_command_class('EEMSRead')
        p.add_command(read_cls, 'Var_A', {'InFileName': 'input.csv', 'InFieldName': 'Var_A'})

      :param Type[Command] command_cls: The class of the command to add. This can be obtained by calling
        :py:meth:`find_command_class` with the name of the command.
      :param str result_name: The name of the result. This is equivalent to the left side of the ``=`` in an MPilot
        command file: ``<result> = <command>(<arguments>)``
      :param Dict[str, Any] arguments: A dictionary of arguments to be sent to the command. E.g.,
        ``{'InFileName': 'input.csv'}``
      :param int lineno: *Optional*. The line number the command appears on. This should be the first line in which the
        command occurs in the command file. This is used in error reporting by the command-line program, and may be
        set to ``None`` when being used from Python.

    .. automethod:: to_string

    .. automethod:: to_file

    .. automethod:: run

  .. data:: EEMS_CSV_LIBRARIES
    :annotation: = Libraries required for CSV-based EEMS models

  .. data:: EEMS_NETCDF_LIBRARIES
    :annotation: = Libraries required for NetCDF-based EEMS models


