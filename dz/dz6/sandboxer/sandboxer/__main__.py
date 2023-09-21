from argparse import ArgumentParser
from .sandboxer import Sandboxer


def main():
    parser = ArgumentParser("sandboxer")
    parser.add_argument("program", help="Program's executable file")
    parser.add_argument("-ui", action="store_true",
                        help="Run with UI")

    args = parser.parse_args()

    sandboxer = Sandboxer(args.program, args.ui)
    sandboxer.run()


if __name__ == "__main__":
    main()
