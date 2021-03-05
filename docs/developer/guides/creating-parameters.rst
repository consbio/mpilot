Creating Parameters
===================

If the :py:mod:`built in parameters <mpilot.params>` don't suite your needs, you can create your own, custom
parameters. Creating a parameter involves subclassing :py:class:`~mpilot.params.Parameter` or another parameter class,
and overriding the :py:meth:`~mpilot.params.Parameter.clean` method to validate and (if necessary) transform the values
passed to an argument of that type. If the incoming value is invalid, the ``clean`` method should raise an exception
(see :py:mod:`mpilot.exceptions`).

.. code-block:: python

  from mpilot.params import StringParameter

  class FooBarParameter(StringParameter):
    def clean(self, value, program=None, lineno=None):
      if value.lower() not in ('foo', 'bar'):
        raise ParameterNotValid(value, "FooBar", lineno=lineno)
      return value

This parameter extends :py:class:`~mpilot.params.StringParameter`, restricts it to accept only "foo" or "bar" as
a valid value, and returns valid, incoming values unmodified.

Parameter Options
-----------------

You can add extra configuration options to your parameter by implementing ``__init__``. Let's modify the above example
to accept a list of valid values, rather than the hard-coded "foo" and "bar".

.. code-block:: python

  class FooBarParameter(StringParameter):
    def __init__(self, valid=('foo', 'bar'), **kwargs):
      super(StringParameter, self).__init__(**kwargs)

      self.valid = valid

    def clean(self, value, program=None, lineno=None):
      if value.lower() not in self.valid:
        raise ParameterNotValid(value, "FooBar", lineno=lineno)
      return value

When using this parameter in a command, now we could now provide different valid values.

.. code-block:: python

  class MyCommand(Command):
    inputs = {
      Speed = FooBarParameter(valid=('fast', 'slow'))
    }
