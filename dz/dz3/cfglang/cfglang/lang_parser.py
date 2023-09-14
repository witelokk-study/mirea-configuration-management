from sly import Parser
from itertools import chain

from .lang_lexer import LangLexer

class LangParser(Parser):
    tokens = LangLexer.tokens

    def __init__(self):
        pass

    @_("s_exp_list")
    def program(self, p):
        return p.s_exp_list

    @_("data")
    def s_exp(self, p):
        return p.data

    @_("'(' s_exp_list ')'")
    def s_exp(self, p):
        # if isinstance(p.s_exp_list, str):
        #     return [p.s_exp_list]
        #
        # if isinstance(p.s_exp_list, list) and len(p.s_exp_list):
        #     return {p.s_exp_list[0]: p.s_exp_list[1]}

        if isinstance(p.s_exp_list, dict) and len(p.s_exp_list) == 1 or not isinstance(p.s_exp_list, dict):
            return p.s_exp_list

        return [p.s_exp_list]

    @_("s_exp s_exp_list")
    def s_exp_list(self, p):
        if isinstance(p.s_exp, (str, int, float)):
            return [p.s_exp, p.s_exp_list] if p.s_exp_list else p.s_exp
        elif isinstance(p.s_exp, list):
            if isinstance(p.s_exp_list, list):
                return p.s_exp + p.s_exp_list
            else:
                return p.s_exp
        else:
            if not p.s_exp_list:
                return p.s_exp
            return p.s_exp | p.s_exp_list

    @_("")
    def s_exp_list(self, p):
        pass

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
        return P.BOOL

    # @_("'.'")
    # def data(self, p):
    #     return None
