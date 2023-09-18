import sys
from os import path, environ
import subprocess

from .dataclasses.makefile import Makefile
from .hashes_manager import HashesManager
from .makefile_lexer import MakefileLexer
from .make_file_parser import MakefileParser


class Minimake:
    def __init__(self, file: str, target: str):
        self._makefile_path = file
        self._target = target
        self._makefile = self._parse_makefile()
        self._hashes_manager = HashesManager(path.dirname(file))

    def start(self):
        # set environment variables
        for name, value in self._makefile.vars:
            environ[name] = value

        if not self._proceed_target(self._target):
            print(f"'{self._target}' is up to date.")
        self._hashes_manager.write()

    def _proceed_target(self, target) -> bool:
        """Executes target's commands if any dependency has been updated

        :returns: True if it was executed, otherwise False"""
        if target not in self._makefile.rules:
            raise RuntimeError("Target does not exist")

        rule = self._makefile.rules[target]

        requires_execution = not rule.dependencies
        for dependency in rule.dependencies:
            if dependency in self._makefile.rules:
                requires_execution = requires_execution or\
                                     self._proceed_target(dependency)
                continue

            # otherwise it is a file
            requires_execution = requires_execution or\
                self._hashes_manager.is_file_updated(dependency)
            self._hashes_manager.update_hash(dependency)

        if requires_execution:
            for command in rule.commands:
                subprocess.run(command.split(" "))

        return requires_execution

    def _parse_makefile(self) -> Makefile:
        try:
            with open(self._makefile_path) as f:
                text = f.read()
                tokens = MakefileLexer().tokenize(text)
                return MakefileParser().parse(tokens)
        except FileNotFoundError:
            print(f"Error: File {self._makefile_path} not found!")
            sys.exit(-1)