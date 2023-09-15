from typing import Any
from dataclasses import dataclass, field

from minimake.dataclasses.rule import Rule
from minimake.dataclasses.variable import Variable


@dataclass
class Config:
    vars: list[Variable] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
