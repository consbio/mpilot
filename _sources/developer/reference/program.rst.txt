Program
=======

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

    .. automethod:: add_command

    .. automethod:: to_string

    .. automethod:: to_file

    .. automethod:: run

  .. data:: EEMS_CSV_LIBRARIES
    :annotation: = Libraries required for CSV-based EEMS models

  .. data:: EEMS_NETCDF_LIBRARIES
    :annotation: = Libraries required for NetCDF-based EEMS models


