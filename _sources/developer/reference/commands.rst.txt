:mod:`mpilot.commands`
======================

.. automodule:: mpilot.commands

  .. autoclass:: Command

    .. py:attribute:: inputs
      :type: Dict[str, Parameter]

      Individual command implementation are expected to set ``inputs`` to define their arguments. For example:

      .. code-block:: python

        class EEMSRead(Command):
          inputs = {
            'InFileName': params.PathParameter(must_exist=True),
            'InFieldName': params.StringParameter()
          }

    .. py:attribute:: output
      :type: Parameter

      The output parameter type for the command. Individual command implementations are expected to set this to the
      appropriate parameter for their expected output. For example:

      .. code-block:: python

        class EEMSRead(Command):
          inputs = { ... }
          output = params.DataParameter()

    .. py:attribute:: allow_extra_inputs
      :type: bool

      ``True`` indicates that this command accepts any inputs not explicitly defined in :py:attr:`inputs`. Any extra
      inputs from the model will be passed unmodified to :py:meth:`execute`. Defaults to ``False``.

    .. py:attribute:: result
      :type: Any

      The result from the command execution. Accessing this property will run the command if it hasn't already been run.
      Once the command is run, the result is memoized, and accessing this property will simply return the memoized
      value.

    .. py:attribute:: metadata
      :type: Dict[str, str]

      This property returns any metadata included with the command, as a dictionary. Metadata can be added to any
      command:

      .. code-block:: none

        Var_A = EEMSRead(
          InFileName = "input.csv",
          InFieldName = "Var_A",
          Metadata = [
            DisplayName: "Near Roads",
            Description: "Thresholds set using +/- 2 SD from the mean.",
            ColorMap: "PiYG"
          ]
        )

      The resulting ``.metadata`` property for this command will be:

      .. code-block:: python

        {
          'DisplayName': 'Near Roads',
          'Description': 'Thresholds set using +/- 2 SD from the mean.',
          'ColorMap': 'PiYG'
        }

    .. automethod:: get_argument_value

    .. automethod:: validate_params

    .. automethod:: run

    .. py:method:: execute(**kwargs) -> Any

      The implementation hook for commands. When the command is run, it's ``implementation`` method will be called and
      passed cleaned and validated arguments as keyword parameters. It should return the appropriate output for the
      command. This method should not be called directly.
