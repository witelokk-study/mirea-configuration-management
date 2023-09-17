from typing import Any
from dataclasses import dataclass, field

from minimake.dataclasses.rule import Rule
from minimake.dataclasses.variable import Variable


@dataclass
class Makefile:
    vars: dict[str, str] = field(default_factory=dict)
    rules: dict[str, Rule] = field(default_factory=dict)
