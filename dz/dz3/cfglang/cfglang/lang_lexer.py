from sly import Lexer

class LangLexer(Lexer):
    literals = {"(", ")"}
    tokens = {STRING, INT, FLOAT, BOOL}

    # String containing ignored characters between tokens
    ignore = ' \t\n'

    @_(r"\".*?\"")
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r"\d+")
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r"\d+.\d+")
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    BOOL = r"true|false"
