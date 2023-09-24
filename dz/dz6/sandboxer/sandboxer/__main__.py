from argparse import ArgumentParser
from .sandboxer import Sandboxer


def main():
    parser = ArgumentParser("sandboxer")
    parser.add_argument("program", help="Program's executable file")
    parser.add_argument("--with-gui", action="store_true",
                        help="Run with UI")
    parser.add_argument("--from-source", action="store_true",
                        help="Build from provided source directory with Makefile")

    args = parser.parse_args()

    sandboxer = Sandboxer(args.program, args.with_gui, args.from_source)
    sandboxer.run()


if __name__ == "__main__":
    main()
