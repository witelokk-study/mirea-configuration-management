from argparse import ArgumentParser

from cfglang.converter import Converter

if __name__ == "__main__":
    arg_parser = ArgumentParser("conflang")
    arg_parser.add_argument("input")
    args = arg_parser.parse_args()

    try:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("Invalid path")
        exit(-1)

    converter = Converter()
    print(converter.convert(text, indent=4))
