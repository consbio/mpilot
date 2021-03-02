from collections import namedtuple

from ply import yacc, lex
from ply.lex import TOKEN

ProgramNode = namedtuple("ProgramNode", ("commands", "version"))
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
    t_ignore_COMMENT = r'\#.*'

    t_COLON = ":"
    t_COMMA = ","
    t_EQUAL = "="
    t_FALSE = "False"
    t_LBRACK = r"\["
    t_LPAREN = r"\("
    t_MINUS = "-"
    t_PLAIN_STRING = r"[^\#\:\,\=\-\+\(\)\[\]\"\r\n]+"
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

    @TOKEN(r"[\r\n]+")
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise SyntaxError("Illegal character {0} at position {1}".format(t.value[0], t.lexpos))


class Parser(object):
    tokens = Lexer.tokens

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=False)
        self.lexer = Lexer().lexer
        self.eems_v2 = False

    def p_program(self, p):
        """
        program : commands
        """

        p[0] = ProgramNode(p[1], 2 if self.eems_v2 else 3)

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

    def p_eems2_command(self, p):
        """
        command : ID arguments
        """

        self.eems_v2 = True
        p[0] = CommandNode(None, p[1], p[2], p.lineno(1))

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
                   | plain_string
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

    def p_plain_string(self, p):
        """
        plain_string : PLAIN_STRING
                     | ID
        """

        p[0] = p[1]

    def p_plain_string_with_colon(self, p):
        """
        plain_string : plain_string COLON plain_string
        """

        p[0] = p[1] + ":" + p[3]

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

    def p_element_tuple_pairs(self, p):
        """
        elements : tuple_pairs
        """

        p[0] = p[1]

    def p_tuple_pairs(self, p):
        """
        tuple_pairs : tuple_pair COMMA tuple_pairs
        """

        p[0] = dict(list(p[3].items()) + [p[1]])

    def p_tuple_pairs_pair(self, p):
        """
        tuple_pairs : tuple_pair COMMA
                    | tuple_pair
        """

        p[0] = dict([p[1]])

    def p_tuple_pair(self, p):
        """
        tuple_pair : STRING COLON expression
                   | PLAIN_STRING COLON expression
                   | ID COLON expression
        """

        p[0] = (p[1], p[3])

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
        # type: (str) -> ProgramNode
        """ Parses the source text and returns a list of `CommandNode` objects """

        return self.parser.parse(source, lexer=self.lexer, tracking=True)
