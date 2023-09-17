from argparse import ArgumentParser
from pprint import pprint
from os import environ

from .make_file_parser import MakefileParser
from .makefile_lexer import MakefileLexer


def parse_makefile(path: str):
    try:
        with open(path) as f:
            text = f.read()
    except FileNotFoundError:
        print("Invalid path")
        return -1

    lexer = MakefileLexer()
    parser = MakefileParser()

    tokens = lexer.tokenize(text)
    config = parser.parse(tokens)

    return config


def main():
    arg_parser = ArgumentParser("minimake")
    arg_parser.add_argument("target", default=None, nargs="?")
    arg_parser.add_argument("-f", "--file", default="Minimakefile")
    args = arg_parser.parse_args()

    makefile = parse_makefile(args.file)


if __name__ == "__main__":
    main()
