from sly import Lexer


class MakeLexer(Lexer):
    tokens = {IDENTIFIER, ASSIGN, STRING, INT, FLOAT, BOOL, COMMENT, COMMAND}
    literals = {"\n"}
    ignore = " "

    IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ASSIGN = r":="

    @_(r"\".*?\"")
    def STRING(self, t):
        t.value = t.value.removeprefix('"').removesuffix('"')
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

    @_("\# .+")
    def COMMENT(self, t):
        return t

    @_(r"[ \t]*?.+")
    def COMMAND(self, t):
        return t
