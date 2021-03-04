Parser
======

The MPilot parser is responsible for lexing and parsing the command file source according to the
`MPilot Spec <https://github.com/consbio/mpilot-spec>`_. It returns the command file structure expressed as a
:class:`CommandNode`. The parser validates syntax and grammar, but does not validate for things like proper command
names, and names and types. Validation of the latter is handled by ``mpilot.program.Program``.

.. automodule:: mpilot.parser.parser

  .. autoclass:: Parser
    :members: parse

  .. autoclass:: ProgramNode

    .. py:attribute:: commands
      :type: List[CommandNode]

      A list of command nodes, parsed from the source text.

    .. py:attribute:: version
      :type: int

      The determined EEMS version of this command file. Will be either ``2`` or ``3``. EEMS v1 files are not supported.

  .. autoclass:: CommandNode

    .. py:attribute:: result_name
      :type: str

      The name assigned to the command result. E.g., ``<result_name> = <command>(<arguments>)``

    .. py:attribute:: command
      :type: str

      The name of the command. This is used to resolve the correct command class to use by ``Program``.

    .. py:attribute:: arguments
      :type: List[ArgumentNode]

      A list of parsed arguments passed to this command.

    .. py:attribute:: lineno
      :type: int

      The line number where this command begins.

  .. autoclass:: ArgumentNode

    .. py:attribute:: name
      :type: str

      The name of the parameter.

    .. py:attribute:: value
      :type: ExpressionNode

      The parameter value

    .. py:attribute:: lineno
      :type: int

      The line number where this command begins.

  .. autoclass:: ExpressionNode

    .. py:attribute:: value

      The expression value

    .. py:attribute:: lineno
      :type: int

      The line number where this command begins.
