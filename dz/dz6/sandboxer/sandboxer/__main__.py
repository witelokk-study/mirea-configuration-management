from argparse import ArgumentParser
from .sandboxer import Sandboxer


def main():
    parser = ArgumentParser("sandboxer")
    parser.add_argument("program", help="Program's executable file")

    args = parser.parse_args()

    sandboxer = Sandboxer(args.program)
    sandboxer.run()


if __name__ == "__main__":
    main()
