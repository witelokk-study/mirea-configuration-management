import os
import subprocess
import sys
from collections import defaultdict
from os import path, environ

from .dataclasses.makefile import Makefile
from .hashes_manager import HashesManager
from .makefile_lexer import MakefileLexer
from .make_file_parser import MakefileParser
from .graph import topological_sort


class Minimake:
    def __init__(self, file: str, target: str):
        self._makefile_path = file
        self._target = target
        self._makefile = self._parse_makefile()
        self._hashes_manager = HashesManager(path.dirname(file))

    def start(self):
        # set environment variables
        if not self._proceed_target_and_dependencies(self._target):
            print(f"'{self._target}' is up to date.")
        self._hashes_manager.write()

    def _proceed_target_and_dependencies(self, target) -> bool:
        """Executes target's commands if any dependency has been updated

        :returns: True if it was executed, otherwise False"""
        if target not in self._makefile.rules:
            raise RuntimeError(f"Target '{target}' does not exist")

        dependency_graph = self._create_dependency_graph(target)

        sorted_dependencies = topological_sort(dependency_graph, inverted=True)

        proceeded_dependencies = {}
        for dependency in sorted_dependencies[:-1]:
            if dependency in self._makefile.rules:
                dependency_dependencies =\
                    self._makefile.rules[dependency].dependencies
                requires_execution =\
                    any([proceeded_dependencies[x] for x in dependency_dependencies])

                if requires_execution:
                    self._proceed_target(dependency)

                proceeded_dependencies[dependency] = requires_execution
            elif os.path.exists(dependency):
                proceeded_dependencies[dependency] = \
                    self._hashes_manager.is_file_updated(dependency)
                self._hashes_manager.update_hash(dependency)
            else:
                raise RuntimeError(f"'{dependency}' is neither a file nor a rule")

        requires_execution = any(proceeded_dependencies.values())

        if requires_execution:
            self._proceed_target(target)

        return requires_execution

    def _proceed_target(self, target):
        """Simply executes target's rule's command without executing any
        dependencies"""

        rule = self._makefile.rules[target]

        for command in rule.commands:
            try:
                subprocess.run(command.split(" "))
            except:
                raise RuntimeError(f"Failed to run command: '{command}'")

    def _create_dependency_graph(self, target) -> dict[str, list[str]]:
        graph = defaultdict(list)

        graph[target] = []

        if target not in self._makefile.rules:
            return graph

        rule = self._makefile.rules[target]

        for dependency in rule.dependencies:
            graph[target].append(dependency)
            graph[dependency] += []

            for key, value in self._create_dependency_graph(dependency).items():
                graph[key] += value

        return graph

    def _parse_makefile(self) -> Makefile:
        try:
            with open(self._makefile_path) as f:
                text = f.read()
                tokens = MakefileLexer().tokenize(text)
                return MakefileParser().parse(tokens)
        except FileNotFoundError:
            print(f"Error: File '{self._makefile_path}' not found!")
            sys.exit(-1)
