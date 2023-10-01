from __future__ import annotations

from dataclasses import dataclass

from sly import Parser

from .lang_lexer import LangLexer


@dataclass
class Id:
    id: str


@dataclass
class Value:
    value: str | int | bool | float | Dict

    def to_obj(self):
        if isinstance(self.value, Dict):
            return self.value.to_obj()
        return self.value


@dataclass
class Pair:
    id: Id
    value: Value | list[Value]

    def to_obj(self):
        return self.id, self.value.to_obj() if isinstance(self.value, Value) else [x.to_obj() for x in self.value]


@dataclass
class Dict:
    pairs: list[Pair]

    def to_obj(self):
        d = {}
        for pair in self.pairs:
            pair_obj = pair.to_obj()
            d[pair_obj[0]] = pair_obj[1]
        return d


class LangParser(Parser):
    tokens = LangLexer.tokens

    def __init__(self):
        pass

    @_("s_exp_list")
    def program(self, p):
        if len(p.s_exp_list) == 1:
            # return Dict(p.s_exp_list)
            if isinstance(p.s_exp_list[0], Pair):
                return Dict(p.s_exp_list)
            else:
                return p.s_exp_list[0].value
        else:
            raise RuntimeError()

    @_("data")
    def s_exp(self, p):
        return p.data

    @_("'(' s_exp_list ')'")
    def s_exp(self, p):
        if isinstance(p.s_exp_list[0], Id):
            if len(p.s_exp_list) == 2:
                return Pair(p.s_exp_list[0].id, p.s_exp_list[1])
            else:
                if all([isinstance(x, Pair) for x in p.s_exp_list[1:]]):
                    return Pair(p.s_exp_list[0].id, Value(Dict(p.s_exp_list[1:])))
                else:
                    return Pair(p.s_exp_list[0].id, p.s_exp_list[1:])
        elif all([isinstance(x, Pair) for x in p.s_exp_list]):
            return Value(Dict(p.s_exp_list))
        else:
            raise RuntimeError()

    @_("s_exp s_exp_list")
    def s_exp_list(self, p):
        if p.s_exp_list is None:
            return [p.s_exp]
        else:
            return [p.s_exp] + p.s_exp_list

    @_("")
    def s_exp_list(self, p):
        return []

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
        return Value(p.BOOL)

