from argparse import ArgumentParser

from .vshell import VShell


def main():
    arg_parser = ArgumentParser("vshell")
    arg_parser.add_argument("filename", help="zip archive filename")

    parsed_args = arg_parser.parse_args()

    vshell = VShell(parsed_args.filename)
    vshell.loop()


if __name__ == "__main__":
    main()
