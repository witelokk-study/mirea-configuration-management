from argparse import ArgumentParser
import json

from .lang_lexer import LangLexer
from .lang_parser import LangParser


if __name__ == "__main__":
    arg_parser = ArgumentParser("conflang")
    arg_parser.add_argument("input")
    args = arg_parser.parse_args()

    try:
        with open(args.input) as f:
            text = f.read()
    except FileNotFoundError:
        print("Invalid path")
        exit(-1)

    lexer = LangLexer()
    parser = LangParser()
    # for tok in lexer.tokenize(text):
    #     print('type=%r, value=%r' % (tok.type, tok.value))

    res = parser.parse(lexer.tokenize(text))

    print(json.dumps((res), indent=4))