from io import StringIO
from sly import Parser

from .dataclasses.makefile import Makefile
from .makefile_lexer import MakefileLexer
from .dataclasses.variable import Variable
from .dataclasses.rule import Rule


class MakefileParser(Parser):
    # debugfile = 'parser.out'
    tokens = MakefileLexer.tokens

    @_("expr_list")
    def makefile(self, p):
        config = Makefile()

        for expr in p.expr_list:
            if isinstance(expr, Variable):
                config.vars[expr.name] = expr.value
            elif isinstance(expr, Rule):
                config.rules[expr.target] = expr

        return config

    @_("expr")
    def expr_list(self, p):
        return [p.expr]

    @_("expr expr_list")
    def expr_list(self, p):
        return [p.expr] + p.expr_list

    @_("rule")
    def expr(self, p):
        return p.rule

    @_("var_assign")
    def expr(self, p):
        return p.var_assign

    @_("NEW_LINE")
    def expr(self, p):
        pass

    @_("ID '=' STRING")
    def var_assign(self, p):
        return Variable(p.ID, p.STRING)

    @_("ID COL dependencies commands")
    def rule(self, p):
        return Rule(p.ID, p.dependencies, p.commands)

    @_("ID COL commands")
    def rule(self, p):
        return Rule(p.ID, [], p.commands)

    @_("ID COL dependencies")
    def rule(self, p):
        return Rule(p.ID, p.dependencies, [])

    @_("ID")
    def dependencies(self, p):
        return [p.ID]

    @_("dependencies ID")
    def dependencies(self, p):
        return p.dependencies + [p.ID]

    @_("COMMAND commands")
    def commands(self, p):
        return [p.COMMAND] + p.commands

    @_("COMMAND")
    def commands(self, p):
        return [p.COMMAND]
