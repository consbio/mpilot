import pytest

from mpilot import params
from mpilot.commands import Command
from mpilot.exceptions import (
    MissingParameters,
    NoSuchParameter,
    ParameterNotValid,
    ResultDoesNotExist,
    ResultTypeNotValid,
    CommandDoesNotExist,
)
from mpilot.program import Program


class SimpleCommand(Command):
    inputs = {
        "A": params.StringParameter(),
        "B": params.NumberParameter(),
        "C": params.ListParameter(params.NumberParameter()),
        "D": params.StringParameter(required=False),
    }
    output = params.ListParameter()

    def execute(self, **kwargs):
        result = [kwargs["A"], kwargs["B"], kwargs["C"]]
        if kwargs.get("D"):
            result.append(kwargs["D"])
        return result


class DependentCommand(Command):
    inputs = {"A": params.ResultParameter(params.ListParameter())}
    output = params.ListParameter()

    def execute(self, **kwargs):
        return kwargs["A"].result


class InvalidDependencyCommand(Command):
    inputs = {}
    output = params.NumberParameter()

    def execute(self, **kwargs):
        return 5


def test_simple_command():
    source = "Result = SimpleCommand(A=Test, B=3, C=[1,2,3])"
    program = Program.from_source(source)
    program.run()
    assert program.commands["Result"].result == ["Test", 3, [1, 2, 3]]


def test_optional_argument():
    source = "Result = SimpleCommand(A=Test, B=3, C=[1,2,3], D=Optional)"
    program = Program.from_source(source)
    program.run()
    assert program.commands["Result"].result == ["Test", 3, [1, 2, 3], "Optional"]


def test_no_command():
    source = "Result = InvalidCommand()"
    with pytest.raises(CommandDoesNotExist) as exc:
        Program.from_source(source)
    assert exc.value.name == "InvalidCommand"


def test_missing_argument():
    source = "Result = SimpleCommand(A=Test)"
    with pytest.raises(MissingParameters) as exc:
        Program.from_source(source)
    assert exc.value.parameters == {"B", "C"}


def test_extra_argument():
    source = "Result = SimpleCommand(A=Test, B=3, C=[1,2,3], E=Invalid)"
    with pytest.raises(NoSuchParameter) as exc:
        Program.from_source(source)
    assert exc.value.parameter == "E"


def test_invalid_argument():
    source = "Result = SimpleCommand(A=Test, B=3, C=WrongType)"
    with pytest.raises(ParameterNotValid) as exc:
        program = Program.from_source(source)
        program.run()
    assert exc.value.value == "WrongType"
    assert exc.value.required_type == "List"


def test_result_parameter():
    source = """
        Result_A = SimpleCommand(A=Test, B=3, C=[1,2,3])
        Result_B = DependentCommand(A=Result_A)
    """

    program = Program.from_source(source)
    program.run()
    assert program.commands["Result_B"].result == ["Test", 3, [1, 2, 3]]


def test_missing_result():
    source = "Result = DependentCommand(A=Result_A)"
    with pytest.raises(ResultDoesNotExist) as exc:
        program = Program.from_source(source)
        program.run()
    assert exc.value.result == "Result_A"


def test_invalid_result_type():
    source = """
        Result_A = InvalidDependencyCommand()
        Result_B = DependentCommand(A=Result_A)    
    """

    with pytest.raises(ResultTypeNotValid) as exc:
        program = Program.from_source(source)
        program.run()
    assert exc.value.result == "Result_A"


def test_convert_from_eems():
    source = r"READ(InFileName = C:\path\to\file.gdb, InFieldName = Foo)"

    Command.load_commands('mpilot.libraries.eems.netcdf')
    program = Program.from_source(source)
    assert "EEMSRead" in str(type(program.commands["Foo"]))
    assert program.commands["Foo"].result_name == "Foo"


def test_loading_duplicate_library():
    """ Tests that loading the same library twice doesn't result in a duplicate command error """

    Command.load_commands('mpilot.libraries.eems.netcdf')
    Command.load_commands('mpilot.libraries.eems.netcdf')
