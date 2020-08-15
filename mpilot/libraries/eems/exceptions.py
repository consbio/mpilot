from six import python_2_unicode_compatible

from mpilot.exceptions import MPilotError


class EmptyDataFile(MPilotError):
    def __init__(self, path, lineno=None):
        super(EmptyDataFile, self).__init__(lineno)

        self.path = path

    @python_2_unicode_compatible
    def __str__(self):
        return "\n".join(
            (
                "Problem: The input file is empty: {}".format(self.path),
                "Solution: Double check the path and the contents of the data file.",
            )
        )


class InvalidDataFile(MPilotError):
    def __init__(self, problem, lineno=None):
        super(InvalidDataFile, self).__init__(lineno)

        self.problem = problem

    @python_2_unicode_compatible
    def __str__(self):
        return "\n".join(("Problem" + self.problem, "Solution: Double check the data file."))


class MixedArrayShapes(MPilotError):
    def __init__(self, shape_a, shape_b, lineno=None):
        super(MixedArrayShapes, self).__init__(lineno)

        self.shape_a = shape_a
        self.shape_b = shape_b

    @python_2_unicode_compatible
    def __str__(self):
        return "\n".join(
            (
                "Problem: The shapes of at least two arrays do no match. The shapes are ({}, {}) and ({}, {}).".format(
                    *self.shape_a, *self.shape_b
                ),
                "Solution: All arrays must have the same shape. Double check the shapes of your input data.",
            )
        )
