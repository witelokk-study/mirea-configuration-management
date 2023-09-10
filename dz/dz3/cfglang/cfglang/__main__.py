from sly import Lexer, Parser


class LangLexer(Lexer):
    tokens = {NUMBER}

    @_(r"\d+")
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
