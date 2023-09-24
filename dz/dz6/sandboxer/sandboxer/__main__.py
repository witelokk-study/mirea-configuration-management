from argparse import ArgumentParser
from .sandboxer import Sandboxer


def main():
    parser = ArgumentParser("sandboxer")
    parser.add_argument("program", help="Program's executable file")
    parser.add_argument("--with-gui", action="store_true",
                        help="Run with UI")
    parser.add_argument("--from-source", action="store_true",
                        help="Build from provided source directory with "
                             "Makefile")
    parser.add_argument("--headless-output",
                        help="Run headlessly and save output to a file")

    args = parser.parse_args()

    if args.with_gui and args.headless_output:
        print("--with-gui and --headless-output are incompatible")
        return -1

    sandboxer = Sandboxer(args.program, args.with_gui, args.from_source,
                          args.headless_output)
    sandboxer.run()


if __name__ == "__main__":
    main()
