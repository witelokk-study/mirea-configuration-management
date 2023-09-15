from argparse import ArgumentParser

from .make_parser import MakeLexer, MakeParser


def main():
    arg_parser = ArgumentParser("minimake")
    arg_parser.add_argument("input")
    args = arg_parser.parse_args()

    try:
        with open(args.input) as f:
            text = f.read()
    except FileNotFoundError:
        print("Invalid path")
        return -1

    print(list(MakeLexer().tokenize(text)))
    print(MakeParser().parse(MakeLexer().tokenize(text)))


if __name__ == "__main__":
    main()
