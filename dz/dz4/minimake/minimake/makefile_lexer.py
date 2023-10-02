from sly import Lexer


class MakefileLexer(Lexer):
    tokens = {
        ID,
        STRING,
        COL,
        COMMAND,
        NEW_LINE,
    }
    literals = {"=", }

    # Tokens
    @_(r"\n(\t|\s{4}).+")
    def COMMAND(self, t):
        t.value = t.value.strip()
        return t

    NEW_LINE = r"\n"
    ID = r'\w+'
    STRING = r'\".*?\"'
    COL = r":"

    # Ignore whitespace and tabs
    ignore = ' \t'
    ignore_comment = r'\#.*'

    @_(r"\$\(.*?\)")
    def VARIABLE(self, t):
        t.value = t.value.removeprefix("$(").removesuffix(")")
        return t
