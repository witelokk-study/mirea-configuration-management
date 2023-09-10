from argparse import ArgumentParser

from .dependency_visualizer import NpmDependencyVisualizer


def main():
    arg_parser = ArgumentParser("dependency_visualizer")
    arg_parser.add_argument("package_name")

    parsed_args = arg_parser.parse_args()
    dv = NpmDependencyVisualizer(parsed_args.package_name)
    print(dv.get_graph())


if __name__ == "__main__":
    main()
