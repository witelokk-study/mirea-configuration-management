from os import getcwd

from .gitviz import Gitviz


def main():
    gitviz = Gitviz(getcwd())
    print(gitviz.get_dot())


if __name__ == "__main__":
    main()
