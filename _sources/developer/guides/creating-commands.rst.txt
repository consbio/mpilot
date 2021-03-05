Creating Commands
=================

It's a fairly simple task to create new MPilot commands for use in models. Let's start with an example:

.. code-block:: python

  from mpilot.commands import Command
  from mpilot import params

  class AddNumbers(Command):
    inputs = {
      'A': params.NumberParameter()
      'B': params.NumberParameter()
    }
    output = params.NumberParameter()

    def execute(self, **kwargs):
      A = kwargs['A']
      B = kwargs['B']

      return A + B

This command, named ``Add``, takes two numbers, ``A`` and ``B`` and returns their sum. It might be used in a model like
this:

.. code-block:: none

  Result = AddNumbers(
    A = 5
    B = 2
  )

Command Name
------------

By default, the class name will be used as the command name. In the above example, the class is named ``AddNumbers``,
and so it's referenced as ``AddNumbers`` in the model file. Set the :py:attr:`~mpilot.commands.Command.name` property
to use a different name.

.. code-block:: python

  class AddNumbers(Command):
    name = 'Add'
    ...

Now this command must be referenced as ``Add`` in the model.

.. code-block:: none

  Result = Add( ... )

Parameters
----------

The ``inputs`` and ``output`` attributes define the arguments the command will accept, and the type of output the
command is expected to produce. See the :py:mod:`mpilot.params` module for a full list of valid parameters, or
:doc:`create your own <creating-parameters>`. Two of particular note that we'll discuss here are
:py:class:`~mpilot.params.ListParameter` and :py:class:`~mpilot.params.ResultParameter`.

Lists
^^^^^

List parameters are useful any time your command needs to accept a list for an argument. Let's change the example
command at the top of the page to return the sum of many numbers.

.. code-block:: python

  class SumNumbers(Command):
    inputs = {
      'Numbers': params.ListParameter(params.NumberParameter())
    }
    output = params.NumberParameter()

    def execute(self, **kwargs):
      numbers = kwargs['Numbers']
      return sum(numbers)

``ListParameter`` accepts a parameter as its first argument, indicating which type of value is expected by this list.
In the above example, the list values are expected to be numbers and will cause an exception if they are not numbers
and can't be converted.

Results
^^^^^^^

Result parameters accept the output of a previous command. As with lists, ``ResultParameter`` accepts a parameter as
its first argument, indicating the expected output type of the command connected to it.

.. code-block:: python

  class Reverse(Command):
    inputs = {
      'InFieldName': params.ResultParameter(params.ListParameter(params.NumberParameter()))
    }
    output = params.ListParameter(params.NumberParameter())

    def execute(self, **kwargs):
      li = kwargs['InFieldName]
      return reversed(li)

Here we see a fairly deep nesting of parameters. Breaking it down, this that ``InFieldName`` is expected to be a
result from another command, and that that result should be a list of numbers. The command returns a list in which the
input list has been reversed.

In this case, we have a result that is a list, but the reverse works too: a list of results:

.. code-block:: python

  params.ListParameter(params.ResultParameter(params.DataParameter()))

This would be accept a list of results from commands that return numpy arrays
(:py:class:`~mpilot.params.DataParameter`).

Optional Parameters
^^^^^^^^^^^^^^^^^^^

Any parameter can be marked as optional by passing ``required=False``

.. code-block:: python

  params.ListParameter(params.NumberParameter(), required=False)

Be sure to account for missing optional parameters in the ``execute`` method.

.. code-block:: python

  def execute(self, **kwargs):
    # Defaults to an empty list if not provided
    numbers = kwargs.get('Numbers', [])
