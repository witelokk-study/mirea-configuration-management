from dataclasses import dataclass

from sly import Parser
from itertools import chain

from .lang_lexer import LangLexer



@dataclass
class Id:
    id: str


@dataclass
class Value:
    value: str | int | bool | float


@dataclass
class Pair:
    id: str
    value: str | int | bool | float | list[str | int | bool | float]


class LangParser(Parser):
    tokens = LangLexer.tokens

    def __init__(self):
        pass

    @_("s_exp_list")
    def program(self, p):
        return p.s_exp_list[0]

    @_("data")
    def s_exp(self, p):
        return p.data

    @_("'(' s_exp_list ')'")
    def s_exp(self, p):
        if isinstance(p.s_exp_list[0], Id):
            if len(p.s_exp_list) == 2:
                return Pair(p.s_exp_list[0].id, p.s_exp_list[1].value if isinstance(p.s_exp_list[1], Value) else p.s_exp_list[1])
            else:
                return Pair(p.s_exp_list[0].id,
                            [x.value if isinstance(x, Value) else x for x in
                             p.s_exp_list[1:]])
        elif isinstance(p.s_exp_list[0], Pair):
            return {pair.id: pair.value for pair in p.s_exp_list}
        else:
            pass


    @_("s_exp s_exp_list")
    def s_exp_list(self, p):
        if p.s_exp_list is None:
            return [p.s_exp]
        else:
            return [p.s_exp] + p.s_exp_list

    @_("")
    def s_exp_list(self, p):
        pass

    @_("ID")
    def data(self, p):
        return Id(p.ID)

    @_("STRING")
    def data(self, p):
        return Value(p.STRING)

    @_("INT")
    def data(self, p):
        return Value(p.INT)

    @_("FLOAT")
    def data(self, p):
        return Value(p.FLOAT)

    @_("BOOL")
    def data(self, p):
        return Value(P.BOOL)

