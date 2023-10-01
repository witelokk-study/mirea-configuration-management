from sly import Lexer


class LangLexer(Lexer):
    literals = {"(", ")"}
    tokens = {ID, STRING, INT, FLOAT, BOOL}

    # String containing ignored characters between tokens
    ignore = ' \t\n'
    ignore_comments = "#.+"

    ID = r"[a-zA-Z][a-zA-Z0-9]*"

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

    @_(r"true|false")
    def BOOL(self, t):
        t.value = True if t.value == "true" else False
        return t
