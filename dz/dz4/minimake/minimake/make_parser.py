from sly import Parser

from .dataclasses.config import Config
from .make_lexer import MakeLexer
from .dataclasses.variable import Variable
from .dataclasses.rule import Rule


class MakeParser(Parser):
    tokens = MakeLexer.tokens

    @_("expression_list")
    def program(self, p):
        config = Config()
        for expression in p.expression_list:
            if isinstance(expression, Variable):
                config.vars.append(expression)
            if isinstance(expression, Rule):
                config.rules.append(expression)
        return config

    @_("comment")
    def expression(self, p):
        return p.comment

    @_("variable_assign")
    def expression(self, p):
        return p.variable_assign

    @_("rule")
    def expression(self, p):
        return p.rule

    @_("expression expression_list")
    def expression_list(self, p):
        lst = []
        if p.expression:
            lst += [p.expression]
        if p.expression_list:
            lst += p.expression_list
        return lst

    @_("")
    def expression_list(self, p):
        pass

    @_("COMMENT")
    def comment(self, p):
        pass  # ignore

    @_("IDENTIFIER ASSIGN data")
    def variable_assign(self, p):
        return Variable(p.IDENTIFIER, p.data)

    @_("IDENTIFIER ':' identifier_list command_list")
    def rule(self, p):
        return Rule(p.IDENTIFIER, p.identifier_list, [])

    @_("IDENTIFIER identifier_list")
    def identifier_list(self, p):
        lst = []
        if p.IDENTIFIER:
            lst += [p.IDENTIFIER]
        if p.identifier_list:
            lst += p.identifier_list
        return lst

    @_(r"'\n'")
    def identifier_list(self, p):
        return []

    @_("COMMAND; command_list")
    def command_list(self, p):
        lst = []
        if p.COMMAND:
            lst += [p.COMMAND]
        if p.command_list:
            lst += p.command_list
        return lst


    @_("STRING")
    def data(self, p):
        return p.STRING

    @_("INT")
    def data(self, p):
        return p.INT

    @_("FLOAT")
    def data(self, p):
        return p.FLOAT

    @_("BOOL")
    def data(self, p):
        return p.BOOL
