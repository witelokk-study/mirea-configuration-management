from sly import Lexer


class MakefileLexer(Lexer):
    tokens = {
        ID,
        STRING,
        COL,
        COMMAND,
        NEW_LINE,
        # VARIABLE,
    }
    literals = {"=", " ", "\t"}

    # Tokens
    @_(r"\n(\t|\s\s\s\s).+")
    def COMMAND(self, t):
        t.value = t.value.strip()
        return t

    NEW_LINE = r"\n"
    ID = r'\w+'
    STRING = r'\".*?\"'
    COL = r":"

    # Ignore whitespace and tabs
    ignore = ' '
    ignore_comment = r'\#.*'


    # Error handling
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

    @_(r"\$\(.*?\)")
    def VARIABLE(self, t):
        t.value = t.value.removeprefix("$(").removesuffix(")")
        return t
