import json

from .lang_lexer import LangLexer
from .lang_parser import LangParser


class Converter:
    def __init__(self):
        self._lexer = LangLexer()
        self._parser = LangParser()

    def convert(self, text: str):
        tokens = self._lexer.tokenize(text)
        result = self._parser.parse(tokens)

        return json.dumps(result, indent=4, ensure_ascii=False)
