from os import getcwd

from .gitviz import Gitviz


def main():
    try:
        gitviz = Gitviz(getcwd())
        print(gitviz.get_dot())
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()
