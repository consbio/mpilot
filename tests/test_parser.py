import six

from mpilot.parser.parser import Parser, CommandNode, ArgumentNode, ExpressionNode


def test_parse():
    """Tests that basic parsing works correctly"""

    source = """
    Result_A = Command1(
        Param_A = Foo
    )
    Result_B = Command2(
        Param_A = Bar,
        Param_B = "Hi."
    )
    """

    program = Parser().parse(source.strip())

    assert program.version == 3
    assert program.commands == [
        CommandNode(
            "Result_A",
            "Command1",
            [ArgumentNode("Param_A", ExpressionNode("Foo", 2), 2)],
            1,
        ),
        CommandNode(
            "Result_B",
            "Command2",
            [
                ArgumentNode("Param_A", ExpressionNode("Bar", 5), 5),
                ArgumentNode("Param_B", ExpressionNode("Hi.", 6), 6),
            ],
            4,
        ),
    ]


def test_parse_numbers():
    """Tests that numbers parse correctly"""

    commands = Parser().parse("A = Command(P = 1)").commands
    assert isinstance(commands[0].arguments[0].value.value, int)
    assert commands[0].arguments[0].value.value == 1

    commands = Parser().parse("A = Command(P = 1.)").commands
    assert isinstance(commands[0].arguments[0].value.value, float)
    assert commands[0].arguments[0].value.value == 1.0

    commands = Parser().parse("A = Command(P = .13E10)").commands
    assert isinstance(commands[0].arguments[0].value.value, float)
    assert commands[0].arguments[0].value.value == 1300000000.0

    commands = Parser().parse("A = Command(P = -1)").commands
    assert isinstance(commands[0].arguments[0].value.value, int)
    assert commands[0].arguments[0].value.value == -1

    commands = Parser().parse("A = Command(P = +1)").commands
    assert isinstance(commands[0].arguments[0].value.value, int)
    assert commands[0].arguments[0].value.value == 1


def test_parse_plain_string():
    """Tests that plain strings parse correctly"""

    commands = Parser().parse("A = Command(P = /Path/To/123.txt)").commands
    assert isinstance(commands[0].arguments[0].value.value, str)
    assert commands[0].arguments[0].value.value == "/Path/To/123.txt"

    # An identifier token in the context of an argument value should be treated as a plain string
    commands = Parser().parse("A = Command(P = Foo)").commands
    assert isinstance(commands[0].arguments[0].value.value, str)
    assert commands[0].arguments[0].value.value == "Foo"

    # Make sure plain strings can contain colons
    commands = Parser().parse(r"A = Command(P = C:\path\to\thing)").commands
    assert isinstance(commands[0].arguments[0].value.value, str)
    assert commands[0].arguments[0].value.value == r"C:\path\to\thing"

    # Make sure plain strings can contain + and -
    commands = Parser().parse(r"A = Command(P = A+/-B)").commands
    assert isinstance(commands[0].arguments[0].value.value, str)
    assert commands[0].arguments[0].value.value == "A+/-B"


def test_parse_quoted_string():
    """Tests that strings delineated with quotes parse correctly"""

    commands = Parser().parse('A = Command(P = "/Path/To/123.txt")').commands
    assert isinstance(commands[0].arguments[0].value.value, six.string_types)
    assert commands[0].arguments[0].value.value == "/Path/To/123.txt"

    commands = Parser().parse("A = Command(P = '/Path/To/123.txt')").commands
    assert isinstance(commands[0].arguments[0].value.value, six.string_types)
    assert commands[0].arguments[0].value.value == "/Path/To/123.txt"

    # Ensure escapes and symbols not allowed in plain strings work correctly in quoted strings
    commands = Parser().parse("A = Command(P = 'A+, \\n')").commands
    assert commands[0].arguments[0].value.value == "A+, \n"


def test_parse_list():
    """Tests that lists parse correctly"""

    commands = Parser().parse("A = Command(P = [1, 2, 3])").commands
    assert isinstance(commands[0].arguments[0].value.value, list)
    assert commands[0].arguments[0].value.value == [
        ExpressionNode(1, 1),
        ExpressionNode(2, 1),
        ExpressionNode(3, 1),
    ]

    commands = Parser().parse("A = Command(P = [1])").commands
    assert isinstance(commands[0].arguments[0].value.value, list)
    assert commands[0].arguments[0].value.value == [ExpressionNode(1, 1)]

    commands = Parser().parse("A = Command(P = [])").commands
    assert isinstance(commands[0].arguments[0].value.value, list)
    assert commands[0].arguments[0].value.value == []


def test_parse_tuple():
    """Tests that tuples parse correctly"""

    commands = Parser().parse('A = Command(P = ["A": "abc"])').commands
    assert isinstance(commands[0].arguments[0].value.value, dict)
    assert commands[0].arguments[0].value.value == {"A": ExpressionNode("abc", 1)}

    commands = Parser().parse("A = Command(P = [A: abc, B: b])").commands
    assert isinstance(commands[0].arguments[0].value.value, dict)
    assert commands[0].arguments[0].value.value == {
        "A": ExpressionNode("abc", 1),
        "B": ExpressionNode("b", 1),
    }

    commands = Parser().parse("A = Command(P = [A: 5abc, B: b])").commands
    assert isinstance(commands[0].arguments[0].value.value, dict)
    assert commands[0].arguments[0].value.value == {
        "A": ExpressionNode("5abc", 1),
        "B": ExpressionNode("b", 1),
    }

    commands = Parser().parse("A = Command(P = [A: %abc, B: b])").commands
    assert isinstance(commands[0].arguments[0].value.value, dict)
    assert commands[0].arguments[0].value.value == {
        "A": ExpressionNode("%abc", 1),
        "B": ExpressionNode("b", 1),
    }

    commands = Parser().parse("A = Command(P = [A: https://databasin.org, B: Link. https://consbio.org])").commands
    assert isinstance(commands[0].arguments[0].value.value, dict)
    assert commands[0].arguments[0].value.value == {
        "A": ExpressionNode("https://databasin.org", 1),
        "B": ExpressionNode("Link. https://consbio.org", 1),
    }


def test_v2_source():
    """Tests that a EEMS 2.0 read command parses and is identified as version 2"""

    program = Parser().parse("READ(InFileName = foo.gdb, InFieldName = Test)")
    assert program.version == 2
    assert program.commands[0].command == "READ"


def test_parse_comments():
    """Tests that comments parse correctly (don't cause an exception, aren't interpreted)"""

    source = """
    # This is a comment
    Result_A = Command1(
        Param_A = Foo
    )
    """

    program = Parser().parse(source.strip())
    assert program.commands == [
        CommandNode(
            "Result_A",
            "Command1",
            [ArgumentNode("Param_A", ExpressionNode("Foo", 3), 3)],
            2,
        )
    ]

    source = """
    # Result_B = Command1(Param_A = Bar)
    Result_A = Command1(
        Param_A = Foo
    )
    """

    program = Parser().parse(source.strip())
    assert program.commands == [
        CommandNode(
            "Result_A",
            "Command1",
            [ArgumentNode("Param_A", ExpressionNode("Foo", 3), 3)],
            2,
        )
    ]
