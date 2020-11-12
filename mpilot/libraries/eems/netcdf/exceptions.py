from six import python_2_unicode_compatible

from mpilot.exceptions import MPilotError


class NoSuchVariable(MPilotError):
    def __init__(self, path, variable, lineno=None):
        super(NoSuchVariable, self).__init__(lineno)

        self.path = path
        self.variable = variable

    @python_2_unicode_compatible
    def __str__(self):
        return "\n".join(
            (
                "Problem: The dataset has no variable named '{}': {}".format(self.variable, self.path),
                "Solution: Double check the path and contents of the dataset.",
            )
        )


class InvalidPositiveData(MPilotError):
    def __init__(self, path, expected_type, lineno=None):
        super(InvalidPositiveData, self).__init__(lineno)

        self.path = path
        self.expected_type = expected_type

    @python_2_unicode_compatible
    def __str__(self):
        return "\n".join(
            (
                "Problem: The expected datatype is '{}', but the dataset has a negative value: {}".format(
                    self.expected_type, self.path
                ),
                "Solution: Double check the input data type and dataset.",
            )
        )


class InvalidFuzzyData(MPilotError):
    def __init__(self, path, lineno=None):
        super(InvalidPositiveData, self).__init__(lineno)

        self.path = path

    @python_2_unicode_compatible
    def __str__(self):
        return "\n".join(
            (
                "Problem: The expected datatype is 'Fuzzy', but the dataset has invalid values: {}".format(self.path),
                "Solution: Make sure the input dataset has values within the fuzzy range.",
            )
        )
