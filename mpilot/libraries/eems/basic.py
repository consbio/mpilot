import copy

from mpilot.commands import Command
from mpilot import params


class Copy(Command):
    inputs = {
        "InFieldName": params.ResultParameter(),
    }
    output = params.Parameter()

    def execute(self, InFieldName):
        return copy.deepcopy(InFieldName.result)
