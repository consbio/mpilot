from collections import namedtuple

from ply import yacc, lex
from ply.lex import TOKEN

CommandNode = namedtuple("CommandNode", ("result_name", "command", "arguments", "lineno"))
ArgumentNode = namedtuple("ArgumentNode", ("name", "value", "lineno"))
ExpressionNode = namedtuple("ExpressionNode", ("value", "lineno"))


class Lexer(object):
    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens = [
        "COLON",
        "COMMA",
        "EQUAL",
        "FALSE",
        "FLOAT",
        "ID",
        "INT",
        "LBRACK",
        "LPAREN",
        "MINUS",
        "PLAIN_STRING",
        "PLUS",
        "RBRACK",
        "RPAREN",
        "STRING",
        "TRUE",
    ]

    t_ignore = " \t"

    t_COLON = ":"
    t_COMMA = ","
    t_EQUAL = "="
    t_FALSE = "False"
    t_LBRACK = r"\["
    t_LPAREN = r"\("
    t_MINUS = "-"
    t_PLAIN_STRING = r"[^\:\,\=\-\+\(\)\[\]\"\r\n]+"
    t_PLUS = r"\+"
    t_RBRACK = r"\]"
    t_RPAREN = r"\)"
    t_TRUE = "True"

    @TOKEN(r"[a-zA-Z_][a-zA-Z_0-9]*")
    def t_ID(self, t):
        return t

    @TOKEN(r"((\d+\.\d*)|(\.\d+))([eE][\+\-]?\d+)?")
    def t_FLOAT(self, t):
        t.value = float(t.value)
        return t

    @TOKEN(r"\d+")
    def t_INT(self, t):
        t.value = int(t.value)
        return t

    @TOKEN(r'("(\\.|[^"\\])*")|(\'(\\.|[^"\\])*\')')
    def t_STRING(self, t):
        t.value = t.value.strip("\"'").encode().decode("unicode_escape")
        return t

    @TOKEN(r"\n+")
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise SyntaxError("Illegal character {0} at position {1}".format(t.value[0], t.lexpos))


class Parser(object):
    tokens = Lexer.tokens

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=False)
        self.lexer = Lexer().lexer

    def p_program(self, p):
        """
        program : commands
        """

        p[0] = p[1]

    def p_commands(self, p):
        """
        commands : command commands
        """

        p[0] = [p[1]] + p[2]

    def p_commands_command(self, p):
        """
        commands : command
        """

        p[0] = [p[1]]

    def p_command(self, p):
        """
        command : ID EQUAL ID arguments
        """

        p[0] = CommandNode(p[1], p[3], p[4], p.lineno(3))

    def p_arguments(self, p):
        """
        arguments : LPAREN argument_list RPAREN
        """

        p[0] = p[2]

    def p_argument_empty(self, p):
        """
        arguments : LPAREN RPAREN
        """

        p[0] = []

    def p_argument_list(self, p):
        """
        argument_list : argument COMMA argument_list
        """

        p[0] = [p[1]] + p[3]

    def p_argument_list_argument(self, p):
        """
        argument_list : argument COMMA
                      | argument
        """
        p[0] = [p[1]]

    def p_argument(self, p):
        """
        argument : ID EQUAL expression
        """

        p[0] = ArgumentNode(p[1], p[3], p.lineno(1))

    def p_expression(self, p):
        """
        expression : ID
                   | PLAIN_STRING
                   | STRING
                   | number
                   | list
                   | boolean
        """

        p[0] = ExpressionNode(p[1], p.lineno(1))

    def p_expression_identifier_expression(self, p):
        """
        expression : ID expression
        """

        p[0] = ExpressionNode("{} {}".format(p[1], str(p[2].value)), p.lineno(1))

    def p_number(self, p):
        """
        number : INT
               | FLOAT
        """

        p[0] = p[1]

    def p_number_unary(self, p):
        """
        number : PLUS number
               | MINUS number
        """

        if p[1] == "-":
            p[0] = p[2] * -1
        else:
            p[0] = p[2]

    def p_list(self, p):
        """
        list : LBRACK elements RBRACK
        """

        p[0] = p[2]

    def p_list_empty(self, p):
        """
        list : LBRACK RBRACK
        """

        p[0] = []

    def p_elements(self, p):
        """
        elements : element COMMA elements
        """

        p[0] = [p[1]] + p[3]

    def p_elements_element(self, p):
        """
        elements : element COMMA
                 | element
        """

        p[0] = [p[1]]

    def p_element_expression(self, p):
        """
        element : expression
        """

        p[0] = p[1]

    def p_boolean(self, p):
        """
        boolean : TRUE
                | FALSE
        """

        p[0] = p[1]

    def p_error(self, p):
        if p:
            raise SyntaxError("Syntax error '{0}' at position {1}".format(p.value, p.lexpos))
        else:
            raise SyntaxError("Invalid syntax at end of statement")

    def parse(self, source):
        """ Parses the source text and returns a list of `CommandNode` objects """

        return self.parser.parse(source, lexer=self.lexer, tracking=True)
