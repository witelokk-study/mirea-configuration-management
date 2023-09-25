from sly import Lexer


class MakefileLexer(Lexer):
    tokens = {
        ID,
        STRING,
        COL,
        NEW_LINE,
        VARIABLE,
    }
    literals = {"=", " ", "\t"}

    # Ignore whitespace and tabs
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Tokens
    ID = r'[^ \n:="]+'
    STRING = r'\".*?\"'
    COL = ":"
    NEW_LINE = "\n"

    # Error handling
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

    @_(r'^[ \t]+.+')  # Matches lines starting with spaces or tabs
    def COMMAND(self, t):
        # t.value = t.value.lstrip()  # Remove leading whitespace
        return t

    @_(r"\$\(.*?\)")
    def VARIABLE(self, t):
        t.value = t.value.removeprefix("$(").removesuffix(")")
        return t
