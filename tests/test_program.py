import os
import shutil
from tempfile import mkdtemp

import pytest

from mpilot import params
from mpilot.commands import Command
from mpilot.exceptions import (
    MissingParameters,
    NoSuchParameter,
    ParameterNotValid,
    ResultDoesNotExist,
    ResultTypeNotValid,
    CommandDoesNotExist, MPilotError,
)
from mpilot.program import Program, EEMS_NETCDF_LIBRARIES, EEMS_CSV_LIBRARIES


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
    program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    program.run()
    assert program.commands["Result"].result == ["Test", 3, [1, 2, 3]]


def test_optional_argument():
    source = "Result = SimpleCommand(A=Test, B=3, C=[1,2,3], D=Optional)"
    program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    program.run()
    assert program.commands["Result"].result == ["Test", 3, [1, 2, 3], "Optional"]


def test_no_command():
    source = "Result = InvalidCommand()"
    with pytest.raises(CommandDoesNotExist) as exc:
        Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    assert exc.value.name == "InvalidCommand"


def test_missing_argument():
    source = "Result = SimpleCommand(A=Test)"
    with pytest.raises(MissingParameters) as exc:
        Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    assert exc.value.parameters == {"B", "C"}


def test_extra_argument():
    source = "Result = SimpleCommand(A=Test, B=3, C=[1,2,3], E=Invalid)"
    with pytest.raises(NoSuchParameter) as exc:
        Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    assert exc.value.parameter == "E"


def test_invalid_argument():
    source = "Result = SimpleCommand(A=Test, B=3, C=WrongType)"
    with pytest.raises(ParameterNotValid) as exc:
        program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
        program.run()
    assert exc.value.value == "WrongType"
    assert exc.value.required_type == "List"


def test_result_parameter():
    source = """
        Result_A = SimpleCommand(A=Test, B=3, C=[1,2,3])
        Result_B = DependentCommand(A=Result_A)
    """

    program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    program.run()
    assert program.commands["Result_B"].result == ["Test", 3, [1, 2, 3]]


def test_missing_result():
    source = "Result = DependentCommand(A=Result_A)"
    with pytest.raises(ResultDoesNotExist) as exc:
        program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
        program.run()
    assert exc.value.result == "Result_A"


def test_invalid_result_type():
    source = """
        Result_A = InvalidDependencyCommand()
        Result_B = DependentCommand(A=Result_A)    
    """

    with pytest.raises(ResultTypeNotValid) as exc:
        program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
        program.run()
    assert exc.value.result == "Result_A"


def test_convert_from_eems():
    source = r"READ(InFileName = C:\path\to\file.gdb, InFieldName = Foo)"

    program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    assert "EEMSRead" in str(type(program.commands["Foo"]))
    assert program.commands["Foo"].result_name == "Foo"


def test_serialization():
    """ Tests that the program can generate a valid MPilot command file """

    source = """
        Simple = SimpleCommand(A=Foo, B=5.4, C=[1,2,.3])
        Result = DependentCommand(A=Simple, Metadata=[A:B])
    """

    answer = """
Simple = SimpleCommand(
    A = "Foo",
    B = 5.4,
    C = [1, 2, 0.3]
)
Result = DependentCommand(
    A = Simple,
    Metadata = ["A": "B"]
)
    """.strip()

    program = Program.from_source(source, libraries=EEMS_CSV_LIBRARIES + ('tests',))
    s = program.to_string()

    assert s == answer

    tmp_dir = mkdtemp()
    try:
        path = os.path.join(tmp_dir, 'test_path.mpt')
        program.to_file(path)
        with open(path) as f:
            assert f.read() == answer

        with open(os.path.join(tmp_dir, 'test_file.mpt'), 'w+') as f:
            program.to_file(f)
            f.seek(0)
            assert f.read() == answer
    finally:
        try:
            shutil.rmtree(tmp_dir)
        except OSError:
            pass


def test_duplicate_commands_error():
    """ Tests that loading libraries with duplicate commands causes an exception """

    with pytest.raises(MPilotError) as exc:
        Program(libraries=EEMS_CSV_LIBRARIES + EEMS_NETCDF_LIBRARIES)
    assert "duplicated" in str(exc)
