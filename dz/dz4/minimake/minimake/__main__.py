from argparse import ArgumentParser

from minimake.minimake import Minimake


def main():
    arg_parser = ArgumentParser("minimake")
    arg_parser.add_argument("target", default=None, nargs="?")
    arg_parser.add_argument("-f", "--file", default="Minimakefile")
    args = arg_parser.parse_args()

    try:
        Minimake(args.file, args.target).start()
    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
