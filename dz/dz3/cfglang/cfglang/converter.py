import json
import sys

from .lang_lexer import LangLexer
from .lang_parser import LangParser


class Converter:
    def __init__(self):
        self._lexer = LangLexer()
        self._parser = LangParser()

    def convert(self, text: str, indent: int = None):
        tokens = self._lexer.tokenize(text)
        result = self._parser.parse(tokens)
        try:
            return json.dumps(result.to_obj(), indent=indent, ensure_ascii=False)
        except:
            print("Syntax error!")
            sys.exit(-1)
