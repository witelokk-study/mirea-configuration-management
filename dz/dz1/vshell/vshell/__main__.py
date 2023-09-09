from argparse import ArgumentParser

from .vshell import VShell


def main():
    arg_parser = ArgumentParser("vshell")
    arg_parser.add_argument("filename", help="zip archive filename")
    arg_parser.add_argument("--script", help="путь до файла")

    parsed_args = arg_parser.parse_args()

    vshell = VShell(parsed_args.filename)

    if parsed_args.script:
        try:
            with open(parsed_args.script) as f:
                while line := f.readline():
                    vshell.execute_command(line.strip())
        except FileNotFoundError:
            print(f"Ошибка: файл {parsed_args.script} не существует")
    else:
        vshell.loop()


if __name__ == "__main__":
    main()
